"""
Main scheduling engine using PyJobShop for a2rp schema.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pyjobshop import solve

from ..models.a2rp import Assignment, Resource, Task
from .problem_builder import ProblemBuilder
from .solution_parser import SolutionParser


class SchedulerEngine:
    """
    Main scheduling engine that uses PyJobShop to solve scheduling problems.
    """

    def __init__(
        self,
        solver: str = "ortools",
        time_limit: int = 60,
    ) -> None:
        """
        Initialize the scheduler engine.

        Args:
            solver: Solver to use ('ortools' or 'cpoptimizer')
            time_limit: Time limit in seconds for solving
        """
        self.solver = solver
        self.time_limit = time_limit

    def create_schedule(
        self,
        tasks: List[Task],
        resources: List[Resource],
        assignments: List[Assignment],
        start_date: datetime,
        end_date: datetime,
    ) -> Tuple[List[Assignment], Dict[str, Any], List[Dict[str, Any]]]:
        """
        Create a schedule for the given tasks and resources.

        Args:
            tasks: List of tasks to schedule
            resources: List of available resources (people, machines, etc.)
            assignments: Existing assignments for resources to tasks
            start_date: Start date for the schedule
            end_date: End date for the schedule

        Returns:
            Tuple of (Assignments, Metadata, Exceptions)
        """
        exceptions: List[Dict[str, Any]] = []
        metadata: Dict[str, Any] = {}

        # Validate inputs
        if not tasks:
            raise ValueError("No tasks provided for scheduling")
        if not resources:
            raise ValueError("No resources available for scheduling")

        # Build the problem
        problem_builder = ProblemBuilder()
        try:
            model = problem_builder.build_problem(tasks, resources, assignments, start_date)
        except Exception as e:
            exceptions.append(
                {
                    "type": "OTHER",
                    "severity": "error",
                    "message": f"Failed to build problem: {str(e)}",
                }
            )
            return [], metadata, exceptions

        # Solve the problem
        solve_start = time.time()
        solution = None
        try:
            if solve is not None:
                solution = solve(
                    model.data(),
                    solver=self.solver,
                    time_limit=self.time_limit,
                    display=False,
                )
        except Exception as e:
            exceptions.append(
                {
                    "type": "OTHER",
                    "severity": "error",
                    "message": f"Solver failed: {str(e)}",
                }
            )

        solve_time = time.time() - solve_start

        # Parse solution
        solution_parser = SolutionParser(problem_builder, start_date)
        new_assignments, solution_metadata = solution_parser.parse_solution(solution, tasks)

        # Update metadata
        metadata.update(solution_metadata)
        metadata["solver_used"] = self.solver
        metadata["solve_time"] = solve_time

        # Check for tasks that couldn't be scheduled
        scheduled_task_ids = {a.task_id for a in new_assignments}
        for task in tasks:
            if task.task_id not in scheduled_task_ids:
                exceptions.append(
                    {
                        "type": "CONSTRAINT_VIOLATION",
                        "severity": "warning",
                        "message": f"Task '{task.name}' (ID: {task.task_id}) could not be scheduled",
                        "task_id": task.task_id,
                    }
                )

        # Check for deadline violations (if task has end_date)
        for assignment in new_assignments:
            task_obj: Optional[Task] = next(
                (t for t in tasks if t.task_id == assignment.task_id), None
            )
            if task_obj and task_obj.end_date and assignment.end_date:
                if assignment.end_date > task_obj.end_date:
                    exceptions.append(
                        {
                            "type": "DEADLINE_MISS",
                            "severity": "error",
                            "message": f"Task '{task_obj.name}' scheduled to end after deadline",
                            "task_id": task_obj.task_id,
                        }
                    )

        return new_assignments, metadata, exceptions

    def validate_schedule(
        self,
        tasks: List[Task],
        assignments: List[Assignment],
    ) -> List[Dict[str, Any]]:
        """
        Validate a schedule for conflicts and violations.

        Args:
            tasks: List of tasks
            assignments: List of assignments

        Returns:
            List of validation exceptions
        """
        exceptions: List[Dict[str, Any]] = []

        # Check for resource overallocation
        resource_schedules: Dict[int, List[Assignment]] = {}
        for assignment in assignments:
            if assignment.resource_id:
                if assignment.resource_id not in resource_schedules:
                    resource_schedules[assignment.resource_id] = []
                resource_schedules[assignment.resource_id].append(assignment)

        # Check for overlapping assignments per resource
        for resource_id, resource_assignments in resource_schedules.items():
            for i, a1 in enumerate(resource_assignments):
                for a2 in resource_assignments[i + 1 :]:
                    if a1.start_date and a1.end_date:
                        if a2.start_date and a2.end_date:
                            # Check for overlap
                            if not (a1.end_date <= a2.start_date or a2.end_date <= a1.start_date):
                                exceptions.append(
                                    {
                                        "type": "RESOURCE_CONFLICT",
                                        "severity": "error",
                                        "message": f"Resource {resource_id} has overlapping tasks",
                                        "resource_id": resource_id,
                                    }
                                )
                                break

        return exceptions
