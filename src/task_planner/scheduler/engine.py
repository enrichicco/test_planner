"""
Main scheduling engine using PyJobShop.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    from pyjobshop import Model
    from pyjobshop.solvers import solve
except ImportError:
    # Fallback for when pyjobshop is not installed yet
    Model = Any
    solve = None

from ..models import Assignment, Person, Resource, Schedule, ScheduleStatus, Task
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
        people: List[Person],
        resources: List[Resource],
        start_date: datetime,
        end_date: datetime,
        schedule_name: str = "New Schedule",
    ) -> Tuple[Schedule, List[Assignment], List[Dict[str, Any]]]:
        """
        Create a schedule for the given tasks, people, and resources.

        Args:
            tasks: List of tasks to schedule
            people: List of available people
            resources: List of available resources
            start_date: Start date for the schedule
            end_date: End date for the schedule
            schedule_name: Name for the schedule

        Returns:
            Tuple of (Schedule, Assignments, Exceptions)
        """
        exceptions: List[Dict[str, Any]] = []

        # Validate inputs
        if not tasks:
            raise ValueError("No tasks provided for scheduling")
        if not people:
            raise ValueError("No people available for scheduling")

        # Build the problem
        problem_builder = ProblemBuilder()
        try:
            model = problem_builder.build_problem(tasks, people, resources, start_date)
        except Exception as e:
            exceptions.append(
                {
                    "type": "OTHER",
                    "severity": "error",
                    "message": f"Failed to build problem: {str(e)}",
                }
            )
            # Return empty schedule
            schedule = Schedule(
                name=schedule_name,
                start_date=start_date,
                end_date=end_date,
                status=ScheduleStatus.DRAFT,
            )
            return schedule, [], exceptions

        # Solve the problem
        solve_start = time.time()
        solution = None
        try:
            if solve is not None:
                solution = solve(
                    model,
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
        assignments, metadata = solution_parser.parse_solution(solution, tasks)

        # Check for tasks that couldn't be scheduled
        scheduled_task_ids = {a.task_id for a in assignments}
        for task in tasks:
            if task.id not in scheduled_task_ids:
                exceptions.append(
                    {
                        "type": "CONSTRAINT_VIOLATION",
                        "severity": "warning",
                        "message": f"Task '{task.name}' (ID: {task.id}) could not be scheduled",
                        "task_id": task.id,
                    }
                )

        # Check for deadline violations
        for assignment in assignments:
            task_obj: Optional[Task] = next((t for t in tasks if t.id == assignment.task_id), None)
            if task_obj and task_obj.deadline and assignment.scheduled_end:
                if assignment.scheduled_end > task_obj.deadline:
                    exceptions.append(
                        {
                            "type": "DEADLINE_MISS",
                            "severity": "error",
                            "message": f"Task '{task_obj.name}' scheduled to end after deadline",
                            "task_id": task_obj.id,
                        }
                    )

        # Create schedule object
        schedule = Schedule(
            name=schedule_name,
            start_date=start_date,
            end_date=end_date,
            status=ScheduleStatus.ACTIVE if assignments else ScheduleStatus.DRAFT,
            objective_value=metadata.get("objective_value"),
            solver_used=self.solver,
            solve_time=solve_time,
            optimization_metadata=metadata,
        )

        return schedule, assignments, exceptions

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

        # Check for person overallocation
        person_schedules: Dict[int, List[Assignment]] = {}
        for assignment in assignments:
            if assignment.person_id:
                if assignment.person_id not in person_schedules:
                    person_schedules[assignment.person_id] = []
                person_schedules[assignment.person_id].append(assignment)

        # Check for overlapping assignments per person
        for person_id, person_assignments in person_schedules.items():
            for i, a1 in enumerate(person_assignments):
                for a2 in person_assignments[i + 1 :]:
                    if a1.scheduled_start and a1.scheduled_end:
                        if a2.scheduled_start and a2.scheduled_end:
                            # Check for overlap
                            if not (
                                a1.scheduled_end <= a2.scheduled_start
                                or a2.scheduled_end <= a1.scheduled_start
                            ):
                                exceptions.append(
                                    {
                                        "type": "RESOURCE_CONFLICT",
                                        "severity": "error",
                                        "message": f"Person {person_id} has overlapping tasks",
                                        "person_id": person_id,
                                    }
                                )
                                break

        return exceptions
