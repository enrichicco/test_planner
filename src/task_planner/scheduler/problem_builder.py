"""
Problem builder for converting database models to PyJobShop problems.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pyjobshop import Model, Task as PyJobShopTask, Machine, Job, Resource as PyJobShopResource

from ..models import Task, Person, Resource, Team


class ProblemBuilder:
    """Builds PyJobShop problem instances from database models."""

    def __init__(self) -> None:
        self.model: Optional[Model] = None
        self.task_mapping: Dict[int, int] = {}  # DB task id -> PyJobShop task index
        self.person_mapping: Dict[int, int] = {}  # DB person id -> PyJobShop machine index
        self.resource_mapping: Dict[int, int] = {}  # DB resource id -> PyJobShop resource index

    def build_problem(
        self,
        tasks: List[Task],
        people: List[Person],
        resources: List[Resource],
        start_date: datetime,
    ) -> Model:
        """
        Build a PyJobShop model from database entities.

        Args:
            tasks: List of tasks to schedule
            people: List of available people
            resources: List of available resources
            start_date: Start date for the schedule

        Returns:
            PyJobShop Model instance
        """
        self.model = Model()

        # Create machines (people)
        for idx, person in enumerate(people):
            if person.is_available:
                machine = self.model.add_machine(
                    name=f"person_{person.id}",
                    optional=False,
                )
                self.person_mapping[person.id] = idx

        # Create resources
        for idx, resource in enumerate(resources):
            if resource.is_available:
                pj_resource = self.model.add_resource(
                    name=f"resource_{resource.id}",
                    capacity=int(resource.capacity),
                    renewable=resource.is_renewable,
                )
                self.resource_mapping[resource.id] = idx

        # Create jobs and tasks
        # Group tasks by team or create individual jobs
        job_groups: Dict[Optional[int], List[Task]] = {}
        for task in tasks:
            team_id = task.team_id
            if team_id not in job_groups:
                job_groups[team_id] = []
            job_groups[team_id].append(task)

        # Build jobs
        for team_id, team_tasks in job_groups.items():
            job_name = f"team_{team_id}" if team_id else "no_team"
            job = self.model.add_job(name=job_name)

            for task in team_tasks:
                # Convert duration from hours to time units (minutes)
                duration = int(task.duration * 60)

                # Determine which machines can perform this task
                # If task has required skills, filter people by skills
                # For simplicity, we'll allow any available person for now
                eligible_machines = list(self.person_mapping.values())

                if eligible_machines:
                    # Add task with one or more processing modes
                    pj_task = job.add_task(
                        name=f"task_{task.id}",
                        duration=duration,
                        machines=[eligible_machines[0]],  # Simplified: use first eligible machine
                    )

                    self.task_mapping[task.id] = len(self.model.tasks()) - 1

                    # Add release date if specified
                    if task.earliest_start:
                        release_minutes = int(
                            (task.earliest_start - start_date).total_seconds() / 60
                        )
                        if release_minutes > 0:
                            pj_task.add_release_date(release_minutes)

                    # Add deadline if specified
                    if task.deadline:
                        deadline_minutes = int(
                            (task.deadline - start_date).total_seconds() / 60
                        )
                        if deadline_minutes > 0:
                            pj_task.add_deadline(deadline_minutes)

                    # Add due date if specified
                    if task.due_date:
                        due_minutes = int((task.due_date - start_date).total_seconds() / 60)
                        if due_minutes > 0:
                            pj_task.add_due_date(due_minutes)

        # Add precedence constraints
        for task in tasks:
            if task.predecessor_id and task.id in self.task_mapping:
                if task.predecessor_id in self.task_mapping:
                    pred_idx = self.task_mapping[task.predecessor_id]
                    curr_idx = self.task_mapping[task.id]
                    # Add precedence constraint: predecessor must finish before current starts
                    self.model.add_precedence(pred_idx, curr_idx)

        return self.model

    def get_task_id(self, pyjobshop_idx: int) -> Optional[int]:
        """Get database task ID from PyJobShop task index."""
        for db_id, pj_idx in self.task_mapping.items():
            if pj_idx == pyjobshop_idx:
                return db_id
        return None

    def get_person_id(self, machine_idx: int) -> Optional[int]:
        """Get database person ID from PyJobShop machine index."""
        for db_id, pj_idx in self.person_mapping.items():
            if pj_idx == machine_idx:
                return db_id
        return None
