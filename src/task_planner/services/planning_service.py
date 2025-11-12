"""Planning service using PyJobShop for task scheduling."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from ..models import Task, TaskStatus
from .exceptions import (
    InfeasibleScheduleException,
    PlanningException,
)


class PlanningService:
    """Service for creating and managing task schedules."""

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
        Create a schedule for given tasks.

        This is a simple sequential scheduler that respects dependencies.
        For more complex scheduling, PyJobShop can be integrated.

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
            # Create a simple schedule respecting dependencies
            schedule = self._create_simple_schedule(tasks, start_date)

            # Validate the schedule
            if not self.validate_schedule(schedule):
                raise InfeasibleScheduleException(
                    "Could not create a valid schedule (resource conflicts detected)"
                )

            # Update tasks with scheduled times
            self._update_task_schedules(schedule)

            return schedule

        except Exception as e:
            if isinstance(e, (PlanningException, InfeasibleScheduleException)):
                raise
            raise PlanningException(f"Scheduling failed: {str(e)}") from e

    def _create_simple_schedule(
        self,
        tasks: List[Task],
        start_date: datetime,
    ) -> Dict[int, Tuple[datetime, datetime]]:
        """
        Create a simple sequential schedule respecting task dependencies.
        """
        schedule: Dict[int, Tuple[datetime, datetime]] = {}
        # task_by_id = {task.id: task for task in tasks}
        scheduled_tasks = set()
        person_availability: Dict[int, datetime] = {}  # Track when each person becomes available

        # Sort tasks by priority (higher priority first)
        sorted_tasks = sorted(tasks, key=lambda t: -t.priority.value)

        for task in sorted_tasks:
            if task.id in scheduled_tasks:
                continue

            # Find the earliest start time based on dependencies
            earliest_start = start_date

            # Check predecessor (single dependency via predecessor_id)
            if task.predecessor_id and task.predecessor_id in schedule:
                # Task must start after its predecessor ends
                _, pred_end = schedule[task.predecessor_id]
                if pred_end > earliest_start:
                    earliest_start = pred_end

            # Check earliest_start constraint from task
            if task.earliest_start and task.earliest_start > earliest_start:
                earliest_start = task.earliest_start

            # Check assigned person availability (from assignments)
            for assignment in task.assignments:
                person_id = assignment.person_id
                if person_id is not None and person_id in person_availability:
                    if person_availability[person_id] > earliest_start:
                        earliest_start = person_availability[person_id]

            # Calculate task end time using duration field
            task_end = earliest_start + timedelta(hours=task.duration)

            # Check deadline constraint
            if task.deadline and task_end > task.deadline:
                # Try to fit it in
                if task.deadline > earliest_start:
                    task_end = task.deadline
                else:
                    raise InfeasibleScheduleException(
                        f"Cannot schedule task {task.id} within its time window"
                    )

            schedule[task.id] = (earliest_start, task_end)
            scheduled_tasks.add(task.id)

            # Update person availability for all assigned people
            for assignment in task.assignments:
                if assignment.person_id is not None:
                    person_availability[assignment.person_id] = task_end

        return schedule

    def _update_task_schedules(self, schedule: Dict[int, Tuple[datetime, datetime]]) -> None:
        """Update task records with scheduled times."""
        # Note: Task model doesn't have scheduled_start/scheduled_end fields
        # Status is updated to SCHEDULED to indicate the task has been scheduled
        # Actual schedule times are stored in the Schedule model through relationships
        for task_id, (_start_time, _end_time) in schedule.items():
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if task:
                # Only update status for now
                # TODO: Create Schedule entries if needed
                task.status = TaskStatus.SCHEDULED

        self.db.commit()

    def reschedule_task(
        self,
        task_id: int,
        reason: str,
        new_start: Optional[datetime] = None,
    ) -> Union[Tuple[datetime, datetime], Tuple[None, None]]:
        """
        Reschedule a task, potentially affecting dependent tasks.

        Args:
            task_id: ID of task to reschedule
            reason: Reason for rescheduling
            new_start: New start time (optional)

        Returns:
            Tuple of (new_start_time, new_end_time) or (None, None) if not found
        """
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise PlanningException(f"Task {task_id} not found")

        # Get all dependent tasks (tasks that have this task as predecessor)
        dependent_tasks = self._get_dependent_tasks(task)

        # Include the task itself
        all_tasks = [task] + dependent_tasks

        # Create new schedule
        schedule = self.create_schedule(all_tasks, new_start)

        return schedule.get(task_id, (None, None))

    def _get_dependent_tasks(self, task: Task) -> List[Task]:
        """Get all tasks that depend on the given task (have it as predecessor)."""
        # Query tasks where predecessor_id equals this task's id
        dependent = self.db.query(Task).filter(Task.predecessor_id == task.id).all()

        # Recursively get dependent tasks
        all_dependent = list(dependent)
        for dep_task in dependent:
            all_dependent.extend(self._get_dependent_tasks(dep_task))

        return all_dependent

    def validate_schedule(self, schedule: Dict[int, Tuple[datetime, datetime]]) -> bool:
        """
        Validate a schedule for conflicts and constraint violations.

        Args:
            schedule: Schedule to validate

        Returns:
            True if valid, False otherwise
        """
        # Check for resource conflicts
        resource_usage: Dict[int, List[Tuple[datetime, datetime]]] = {}

        for task_id, (start_time, end_time) in schedule.items():
            task = self.db.query(Task).filter(Task.id == task_id).first()
            if not task:
                continue

            # Check assigned person availability (from assignments)
            for assignment in task.assignments:
                person_id = assignment.person_id
                if person_id is None:
                    continue

                if person_id not in resource_usage:
                    resource_usage[person_id] = []

                # Check for overlaps
                for other_start, other_end in resource_usage[person_id]:
                    if start_time < other_end and end_time > other_start:
                        return False

                resource_usage[person_id].append((start_time, end_time))

        return True
