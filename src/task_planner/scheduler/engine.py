"""
Main scheduling engine using PyJobShop for a2rp schema.
"""

import base64
import io
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pyjobshop import solve
from pyjobshop.plot import plot_machine_gantt

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
        result = None
        try:
            if solve is not None:
                result = solve(
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

        # Extract best solution from result
        solution = result.best if result is not None else None

        # Check if solver found a solution
        if result is not None and solution is None:
            exceptions.append(
                {
                    "type": "NO_SOLUTION",
                    "severity": "error",
                    "message": f"Solver could not find a feasible solution. Status: {getattr(result, 'status', 'Unknown')}",
                }
            )

        # Parse solution
        solution_parser = SolutionParser(problem_builder, start_date)
        new_assignments, solution_metadata = solution_parser.parse_solution(solution, tasks)

        # Update metadata
        metadata.update(solution_metadata)
        metadata["solver_used"] = self.solver
        metadata["solve_time"] = solve_time

        # Add Result metadata if available
        if result is not None:
            metadata["result_status"] = str(getattr(result, "status", "Unknown"))
            metadata["lower_bound"] = float(getattr(result, "lower_bound", 0))

        # Generate Gantt chart if solution exists
        if solution is not None and problem_builder.model is not None:
            try:
                gantt_base64 = self._generate_gantt_chart(solution, problem_builder.model.data())
                metadata["gantt_chart"] = gantt_base64
            except Exception as e:
                print(f"Warning: Could not generate Gantt chart: {e}")
                import traceback

                traceback.print_exc()

        # Check for tasks that couldn't be scheduled
        scheduled_task_ids = {a.task_id for a in new_assignments}
        unscheduled_count = 0
        for task in tasks:
            if task.task_id not in scheduled_task_ids:
                unscheduled_count += 1
                exceptions.append(
                    {
                        "type": "CONSTRAINT_VIOLATION",
                        "severity": "warning",
                        "message": f"Task '{task.name}' (ID: {task.task_id}) could not be scheduled",
                        "task_id": task.task_id,
                    }
                )

        # Add summary if no assignments were created
        if len(new_assignments) == 0 and len(tasks) > 0:
            exceptions.append(
                {
                    "type": "NO_ASSIGNMENTS",
                    "severity": "error",
                    "message": f"No assignments generated. {len(tasks)} tasks and {len(resources)} resources available. Check if tasks have realistic constraints (dates, durations).",
                }
            )

        return new_assignments, metadata, exceptions

    def _generate_gantt_chart(self, solution: Any, problem_data: Any) -> Optional[str]:
        """
        Generate a Gantt chart from the solution.

        Args:
            solution: PyJobShop solution object
            problem_data: PyJobShop problem data

        Returns:
            Base64 encoded PNG image of the Gantt chart, or None if generation fails
        """
        try:
            import matplotlib

            matplotlib.use("Agg")  # Use non-interactive backend
            import matplotlib.pyplot as plt

            # Use PyJobShop's built-in Gantt chart plotting function
            # Calculate height based on number of machines/resources
            num_machines = len(problem_data.resources)
            fig_height = max(6, num_machines * 0.4)  # At least 6, scale with machines
            fig, ax = plt.subplots(figsize=(14, fig_height))
            plot_machine_gantt(solution, problem_data, ax=ax, plot_labels=True)

            # Reduce font size of task labels
            for text in ax.texts:
                text.set_fontsize(5)

            # Improve the appearance
            ax.set_xlabel("Time (minutes)", fontsize=10)
            ax.set_ylabel("Machines/Resources", fontsize=10)
            # ax.set_title("Schedule Gantt Chart", fontsize=12, fontweight="bold")

            # Fix overlapping y-axis labels
            plt.yticks(rotation=15)
            plt.setp(ax.get_yticklabels(), fontsize=8)

            plt.tight_layout(pad=1.5)

            # Save to bytes buffer
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
            buf.seek(0)
            plt.close(fig)

            # Encode as base64
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            print(f"Error generating Gantt chart: {e}")
            import traceback

            traceback.print_exc()
            return None

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
