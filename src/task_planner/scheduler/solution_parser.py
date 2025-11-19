"""
Solution parser for converting PyJobShop solutions back to a2rp database models.
"""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from ..models.a2rp import Assignment, Task

if TYPE_CHECKING:
    from .problem_builder import ProblemBuilder


class SolutionParser:
    """Parses PyJobShop solutions into database assignments."""

    def __init__(
        self,
        problem_builder: "ProblemBuilder",
        start_date: datetime,
    ) -> None:
        """
        Initialize solution parser.

        Args:
            problem_builder: The problem builder with mappings
            start_date: Start date of the schedule
        """
        self.problem_builder = problem_builder
        self.start_date = start_date

    def parse_solution(
        self,
        solution: Any,
        tasks: List[Task],
    ) -> Tuple[List[Assignment], Dict[str, Any]]:
        """
        Parse PyJobShop solution into assignments.

        Args:
            solution: PyJobShop solution object
            tasks: Original list of tasks

        Returns:
            Tuple of (assignments, metadata)
        """
        assignments: List[Assignment] = []
        metadata: Dict[str, Any] = {
            "objective_value": None,
            "makespan": None,
            "total_flow_time": None,
        }

        if solution is None:
            return assignments, metadata

        # Extract solution metadata
        metadata["objective_value"] = float(getattr(solution, "objective", 0))
        metadata["makespan"] = getattr(solution, "makespan", None)
        metadata["total_flow_time"] = None  # Calculate if needed

        # Parse task assignments
        task_dict = {task.task_id: task for task in tasks}

        if self.problem_builder.model is None or not hasattr(solution, "tasks"):
            return assignments, metadata

        # Calculate makespan from tasks if not directly available
        if metadata["makespan"] is None and len(solution.tasks) > 0:
            metadata["makespan"] = max(task_data.end for task_data in solution.tasks)

        # Iterate through solution tasks
        try:
            for pj_task_idx, task_data in enumerate(solution.tasks):
                task_id = self.problem_builder.get_task_id(pj_task_idx)
                if task_id and task_id in task_dict:
                    task = task_dict[task_id]

                    # Get scheduled start and end times from task_data
                    start_time = task_data.start
                    end_time = task_data.end
                    machine = task_data.machine

                    # Convert from minutes to datetime
                    scheduled_start = self.start_date + timedelta(minutes=start_time)
                    scheduled_end = self.start_date + timedelta(minutes=end_time)

                    # Get resource ID from machine
                    # machine is a Machine object, find its index
                    machine_idx = None
                    for idx, m in enumerate(self.problem_builder.machine_objects):
                        if m == machine:
                            machine_idx = idx
                            break

                    resource_id = (
                        self.problem_builder.get_resource_id(machine_idx)
                        if machine_idx is not None
                        else None
                    )

                    # Calculate work hours from time difference
                    work_hours = (scheduled_end - scheduled_start).total_seconds() / 3600

                    # Create assignment
                    assignment = Assignment(
                        task_id=task.task_id,
                        resource_id=resource_id,
                        work=work_hours,
                        start_date=scheduled_start,
                        end_date=scheduled_end,
                        wp_status_id="scheduled",
                    )
                    assignments.append(assignment)

        except Exception as e:
            # Handle parsing errors gracefully
            print(f"Warning: Error parsing solution: {e}")
            import traceback

            traceback.print_exc()

        return assignments, metadata
