"""
Problem builder for converting a2rp database models to PyJobShop problems.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pyjobshop import MAX_VALUE, Model
from pyjobshop import Task as PJTask

from ..models.a2rp import Assignment, Resource, Task


class ProblemBuilder:
    """Builds PyJobShop problem instances from a2rp database models."""

    def __init__(self) -> None:
        self.model: Optional[Model] = None
        self.task_mapping: Dict[int, PJTask] = {}  # DB task id -> PyJobShop task
        self.resource_mapping: Dict[
            int, int
        ] = {}  # DB resource id -> PyJobShop machine/resource index

    def build_problem(
        self,
        tasks: List[Task],
        resources: List[Resource],
        assignments: List[Assignment],
        start_date: datetime,
    ) -> Model:
        """
        Build a PyJobShop model from a2rp database entities.

        Args:
            tasks: List of tasks to schedule
            resources: List of available resources (people, machines, etc.)
            assignments: List of assignments linking resources to tasks
            start_date: Start date for the schedule

        Returns:
            PyJobShop Model instance
        """
        self.model = Model()

        # Create machines (resources that can perform work)
        # In a2rp, resources are generic - they can be people, equipment, etc.
        for idx, resource in enumerate(resources):
            self.model.add_machine(
                name=f"resource_{resource.resource_id}",
            )
            self.resource_mapping[resource.resource_id] = idx

        # Create jobs and tasks
        # Group tasks by project
        job_groups: Dict[Optional[int], List[Task]] = {}
        for task in tasks:
            project_id = task.project_id
            if project_id not in job_groups:
                job_groups[project_id] = []
            job_groups[project_id].append(task)

        # Build jobs
        for project_id, project_tasks in job_groups.items():
            job_name = f"project_{project_id}" if project_id else "no_project"

            # Aggregate dates
            job_release = None
            job_deadline = MAX_VALUE
            job_due = None

            for task in project_tasks:
                if task.start_date:
                    release_minutes = max(0, int((task.start_date - start_date).total_seconds() / 60))
                    job_release = release_minutes if job_release is None else min(job_release, release_minutes)

                if task.end_date:
                    deadline_minutes = int((task.end_date - start_date).total_seconds() / 60)
                    job_deadline = max(
                        job_deadline if job_deadline != MAX_VALUE else deadline_minutes,
                        deadline_minutes,
                    )

            job = self.model.add_job(
                name=job_name,
                release_date=job_release if job_release is not None else 0,
                deadline=job_deadline,
                due_date=job_due,
            )

            for task in project_tasks:
                # Duration in minutes (work is in hours)
                duration = int((task.work or 8.0) * 60)

                earliest_start = (
                    max(0, int((task.start_date - start_date).total_seconds() / 60))
                    if task.start_date
                    else 0
                )
                latest_end = (
                    int((task.end_date - start_date).total_seconds() / 60)
                    if task.end_date
                    else MAX_VALUE
                )

                pj_task = self.model.add_task(
                    job=job,
                    earliest_start=earliest_start,
                    latest_end=(
                        earliest_start + duration if latest_end == MAX_VALUE else latest_end
                    ),
                    name=f"task_{task.task_id}",
                )

                self.task_mapping[task.task_id] = pj_task

        return self.model

    def get_task_id(self, pyjobshop_idx: int) -> Optional[int]:
        """Get database task ID from PyJobShop task index."""
        for db_id, pj_idx in self.task_mapping.items():
            if pj_idx == pyjobshop_idx:
                return db_id
        return None

    def get_resource_id(self, machine_idx: int) -> Optional[int]:
        """Get database resource ID from PyJobShop machine index."""
        for db_id, pj_idx in self.resource_mapping.items():
            if pj_idx == machine_idx:
                return db_id
        return None
