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
        self.machine_objects: list = []  # Store machine objects for mode assignment

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

        # Diagnostic counters
        tasks_without_dates = 0
        tasks_with_past_dates = 0

        # Create machines (resources that can perform work)
        # In a2rp, resources are generic - they can be people, equipment, etc.
        for idx, resource in enumerate(resources):
            machine = self.model.add_machine(
                name=f"resource_{resource.resource_id}",
            )
            self.resource_mapping[resource.resource_id] = idx
            self.machine_objects.append(machine)

        print(f"\n=== Scheduler Diagnostics ===")
        print(f"Schedule window: {start_date}")
        print(f"Total resources: {len(resources)}")
        print(f"Total tasks: {len(tasks)}")
        print(f"Mode: Ignoring individual task dates - all tasks schedulable within window")

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

            # Jobs can start immediately (release_date=0) and have no deadline
            # This allows the scheduler to freely place tasks within the schedule window
            job = self.model.add_job(
                name=job_name,
                release_date=0,
                deadline=MAX_VALUE,
                due_date=None,
            )

            for task in project_tasks:
                # Duration in minutes (work is in hours)
                duration = int((task.work or 8.0) * 60)

                # Track diagnostics
                if task.start_date is None and task.end_date is None:
                    tasks_without_dates += 1
                if task.start_date and task.start_date < start_date:
                    tasks_with_past_dates += 1

                # IGNORE individual task dates - schedule all tasks within the window
                # Tasks can start immediately (earliest_start=0)
                # Tasks can end anytime (latest_end=MAX_VALUE)
                earliest_start = 0
                latest_end = MAX_VALUE

                # Debug first few tasks
                if len(self.task_mapping) < 3:
                    print(f"\nTask {task.task_id} ({task.name}):")
                    print(f"  work: {task.work}h -> duration: {duration}min")
                    print(f"  DB start_date: {task.start_date} (IGNORED)")
                    print(f"  DB end_date: {task.end_date} (IGNORED)")
                    print(f"  earliest_start: {earliest_start}min (can start immediately)")
                    print(f"  latest_end: {latest_end} (no deadline)")

                pj_task = self.model.add_task(
                    job=job,
                    earliest_start=earliest_start,
                    latest_end=latest_end,
                    name=f"task_{task.task_id}",
                )

                self.task_mapping[task.task_id] = pj_task

                # Add modes: allow any resource to perform this task
                # Each mode represents a (machine, duration) pair
                for resource_id, machine_idx in self.resource_mapping.items():
                    machine = self.machine_objects[machine_idx]
                    self.model.add_mode(pj_task, machine, duration)

        print(f"\n=== Constraint Summary ===")
        print(f"Tasks without dates (start/end both None): {tasks_without_dates}")
        print(f"Tasks with start dates before schedule start: {tasks_with_past_dates}")
        print(f"Total PyJobShop tasks created: {len(self.task_mapping)}")
        print(f"Total modes (task-resource pairs): {len(self.task_mapping) * len(self.machine_objects)}")
        print(f"===========================\n")

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
