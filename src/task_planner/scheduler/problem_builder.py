"""
Problem builder for converting database models to PyJobShop problems.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pyjobshop import MAX_VALUE, Model
from pyjobshop import Task as PJTask

from ..models import Person, Resource, Task


class ProblemBuilder:
    """Builds PyJobShop problem instances from database models."""

    def __init__(self) -> None:
        self.model: Optional[Model] = None
        self.task_mapping: Dict[int, PJTask] = {}  # DB task id -> PyJobShop task
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
                self.model.add_machine(
                    name=f"person_{person.id}",
                )
                self.person_mapping[person.id] = idx

        # Create resources
        for idx, resource in enumerate(resources):
            if resource.is_available:
                if resource.is_renewable:
                    self.model.add_renewable(capacity=int(resource.capacity))
                else:
                    self.model.add_non_renewable(capacity=int(resource.capacity))
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

            # Aggregate dates
            job_release = 0
            job_deadline = MAX_VALUE
            job_due = None

            for task in team_tasks:
                if task.earliest_start:
                    release_minutes = int((task.earliest_start - start_date).total_seconds() / 60)
                    job_release = min(job_release or release_minutes, release_minutes)

                if task.deadline:
                    deadline_minutes = int((task.deadline - start_date).total_seconds() / 60)
                    job_deadline = max(job_deadline or deadline_minutes, deadline_minutes)

                if task.due_date:
                    due_minutes = int((task.due_date - start_date).total_seconds() / 60)
                    job_due = max(job_due or due_minutes, due_minutes)

            job = self.model.add_job(
                name=job_name,
                release_date=job_release,
                deadline=job_deadline,
                due_date=job_due,
            )

            for task in team_tasks:
                duration = int(task.duration * 60)

                earliest_start = (
                    int((task.earliest_start - start_date).total_seconds() / 60)
                    if task.earliest_start
                    else 0
                )
                latest_end = (
                    int((task.deadline - start_date).total_seconds() / 60)
                    if task.deadline
                    else MAX_VALUE
                )

                pj_task = self.model.add_task(
                    job=job,
                    earliest_start=earliest_start,
                    latest_end=earliest_start + duration if latest_end == MAX_VALUE else latest_end,
                    name=f"task_{task.id}",
                )

                self.task_mapping[task.id] = pj_task

        # Add precedence constraints
        for task in tasks:
            if task.predecessor_id and task.id in self.task_mapping:
                if task.predecessor_id in self.task_mapping:
                    pred_task = self.task_mapping[task.predecessor_id]
                    curr_task = self.task_mapping[task.id]
                    # Add precedence constraint: predecessor must finish before current starts
                    self.model.add_consecutive(pred_task, curr_task)

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
