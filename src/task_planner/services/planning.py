"""Planning service using PyJobShop for task scheduling."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session

from pyjobshop import solve
from pyjobshop.Model import Model
from pyjobshop.ProblemData import ProblemData

from task_planner.models import Task, Person, Resource, TaskStatus, Team
from task_planner.services.exceptions import (
    PlanningException,
    ResourceConflictException,
    InfeasibleScheduleException,
)


class PlanningService:
    """Service for creating and managing task schedules using PyJobShop."""
    
    def __init__(self, db: Session):
        """Initialize planning service with database session."""
        self.db = db
    
    def create_schedule(
        self,
        tasks: List[Task],
        start_date: Optional[datetime] = None,
        max_horizon_days: int = 90,
    ) -> Dict[int, Tuple[datetime, datetime]]:
        """
        Create a schedule for given tasks using PyJobShop.
        
        Args:
            tasks: List of tasks to schedule
            start_date: Start date for scheduling (default: now)
            max_horizon_days: Maximum planning horizon in days
            
        Returns:
            Dictionary mapping task IDs to (start_time, end_time) tuples
            
        Raises:
            PlanningException: If scheduling fails
        """
        if not tasks:
            return {}
        
        if start_date is None:
            start_date = datetime.now()
        
        try:
            # Build problem data for PyJobShop
            problem_data = self._build_problem_data(tasks, start_date, max_horizon_days)
            
            # Create model and solve
            model = Model(problem_data)
            result = solve(model)
            
            if not result.is_optimal() and not result.is_feasible():
                raise InfeasibleScheduleException(
                    "Could not find a feasible schedule for the given tasks"
                )
            
            # Extract schedule from solution
            schedule = self._extract_schedule(result, tasks, start_date)
            
            # Update tasks with scheduled times
            self._update_task_schedules(schedule)
            
            return schedule
            
        except Exception as e:
            raise PlanningException(f"Scheduling failed: {str(e)}") from e
    
    def _build_problem_data(
        self,
        tasks: List[Task],
        start_date: datetime,
        max_horizon_days: int,
    ) -> ProblemData:
        """Build PyJobShop problem data from tasks."""
        # Create jobs from tasks
        jobs = []
        machines = []
        processing_times = []
        
        # Get unique resources (machines in PyJobShop terms)
        resources = self._get_task_resources(tasks)
        machine_map = {res.id: idx for idx, res in enumerate(resources)}
        machines = list(range(len(resources)))
        
        # Get people who can work on tasks (also treated as machines)
        people = self._get_task_people(tasks)
        person_map = {person.id: idx + len(resources) for idx, person in enumerate(people)}
        machines.extend(range(len(resources), len(resources) + len(people)))
        
        # Build jobs (each task is a job with operations)
        for task_idx, task in enumerate(tasks):
            job_operations = []
            
            # Each task needs a resource and/or person
            if task.assigned_person_id and task.assigned_person_id in person_map:
                machine_idx = person_map[task.assigned_person_id]
                processing_time = int(task.estimated_hours * 60)  # Convert to minutes
                job_operations.append((machine_idx, processing_time))
            else:
                # Assign to first available person if not assigned
                if people:
                    machine_idx = person_map[people[0].id]
                    processing_time = int(task.estimated_hours * 60)
                    job_operations.append((machine_idx, processing_time))
            
            if job_operations:
                jobs.append(job_operations)
        
        # Create problem data
        data = ProblemData(
            jobs=jobs,
            processing_times=[[op[1] for op in job] for job in jobs],
            machines=[[op[0] for op in job] for job in jobs],
        )
        
        return data
    
    def _get_task_resources(self, tasks: List[Task]) -> List[Resource]:
        """Get unique resources required by tasks."""
        resource_ids = set()
        for task in tasks:
            for req in task.resource_requirements:
                resource_ids.add(req.resource_id)
        
        if not resource_ids:
            return []
        
        return (
            self.db.query(Resource)
            .filter(Resource.id.in_(resource_ids))
            .all()
        )
    
    def _get_task_people(self, tasks: List[Task]) -> List[Person]:
        """Get unique people assigned to tasks or available for assignment."""
        person_ids = set()
        for task in tasks:
            if task.assigned_person_id:
                person_ids.add(task.assigned_person_id)
            elif task.team_id:
                # Get team members
                team = self.db.query(Team).filter(Team.id == task.team_id).first()
                if team:
                    person_ids.update([m.id for m in team.members if m.is_active])
        
        # If no people found, get all active people
        if not person_ids:
            return self.db.query(Person).filter(Person.is_active == True).all()
        
        return (
            self.db.query(Person)
            .filter(Person.id.in_(person_ids))
            .all()
        )
    
    def _extract_schedule(
        self,
        result,
        tasks: List[Task],
        start_date: datetime,
    ) -> Dict[int, Tuple[datetime, datetime]]:
        """Extract schedule from PyJobShop solution."""
        schedule = {}
        
        # PyJobShop returns a solution with job start times
        # We need to map these back to our tasks
        for idx, task in enumerate(tasks):
            if idx < len(result.schedule):
                job_schedule = result.schedule[idx]
                # Get start time in minutes from start_date
                start_minutes = job_schedule.start if hasattr(job_schedule, 'start') else 0
                end_minutes = job_schedule.end if hasattr(job_schedule, 'end') else start_minutes + int(task.estimated_hours * 60)
                
                task_start = start_date + timedelta(minutes=start_minutes)
                task_end = start_date + timedelta(minutes=end_minutes)
                
                schedule[task.id] = (task_start, task_end)
            else:
                # Fallback: schedule sequentially
                task_start = start_date + timedelta(hours=idx * task.estimated_hours)
                task_end = task_start + timedelta(hours=task.estimated_hours)
                schedule[task.id] = (task_start, task_end)
        
        return schedule
    
    def _update_task_schedules(self, schedule: Dict[int, Tuple[datetime, datetime]]):
        """Update task records with scheduled times."""
        for task_id, (start_time, end_time) in schedule.items():
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.scheduled_start = start_time
                task.scheduled_end = end_time
                task.status = TaskStatus.SCHEDULED
        
        self.db.commit()
    
    def reschedule_task(
        self,
        task_id: int,
        reason: str,
        new_start: Optional[datetime] = None,
    ) -> Tuple[datetime, datetime]:
        """
        Reschedule a task, potentially affecting dependent tasks.
        
        Args:
            task_id: ID of task to reschedule
            reason: Reason for rescheduling
            new_start: New start time (optional)
            
        Returns:
            Tuple of (new_start_time, new_end_time)
        """
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise PlanningException(f"Task {task_id} not found")
        
        # Get all dependent tasks
        dependent_tasks = self._get_dependent_tasks(task)
        
        # Include the task itself
        all_tasks = [task] + dependent_tasks
        
        # Create new schedule
        schedule = self.create_schedule(all_tasks, new_start)
        
        return schedule.get(task_id, (task.scheduled_start, task.scheduled_end))
    
    def _get_dependent_tasks(self, task: Task) -> List[Task]:
        """Get all tasks that depend on the given task."""
        dependent = []
        for dep in task.dependent_on:
            dependent_task = dep.task
            dependent.append(dependent_task)
            # Recursively get dependencies
            dependent.extend(self._get_dependent_tasks(dependent_task))
        
        return dependent
    
    def validate_schedule(self, schedule: Dict[int, Tuple[datetime, datetime]]) -> bool:
        """
        Validate a schedule for conflicts and constraint violations.
        
        Args:
            schedule: Schedule to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check for resource conflicts
        resource_usage = {}
        
        for task_id, (start_time, end_time) in schedule.items():
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task:
                continue
            
            # Check assigned person availability
            if task.assigned_person_id:
                person_id = task.assigned_person_id
                if person_id not in resource_usage:
                    resource_usage[person_id] = []
                
                # Check for overlaps
                for other_start, other_end in resource_usage[person_id]:
                    if (start_time < other_end and end_time > other_start):
                        return False
                
                resource_usage[person_id].append((start_time, end_time))
        
        return True
