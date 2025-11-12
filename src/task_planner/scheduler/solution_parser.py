"""
Solution parser for converting PyJobShop solutions back to database models.
"""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from ..models import Assignment, Task

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
        try:
            if hasattr(solution, "objective"):
                metadata["objective_value"] = float(solution.objective())
            if hasattr(solution, "makespan"):
                metadata["makespan"] = solution.makespan()
        except Exception:
            pass

        # Parse task assignments
        task_dict = {task.id: task for task in tasks}

        if self.problem_builder.model is None:
            return assignments, metadata

        # Iterate through solution to extract assignments
        # The exact API depends on PyJobShop version
        try:
            # Attempt to get task assignments from solution
            for pj_task_idx in range(len(self.problem_builder.model.tasks)):
                task_id = self.problem_builder.get_task_id(pj_task_idx)
                if task_id and task_id in task_dict:
                    task = task_dict[task_id]

                    # Get scheduled start and end times
                    try:
                        # These methods may vary based on PyJobShop version
                        start_time = solution.task_start(pj_task_idx)
                        end_time = solution.task_end(pj_task_idx)
                        machine_idx = solution.task_machine(pj_task_idx)

                        # Convert from minutes to datetime
                        scheduled_start = self.start_date + timedelta(minutes=start_time)
                        scheduled_end = self.start_date + timedelta(minutes=end_time)

                        # Get person ID from machine index
                        person_id = self.problem_builder.get_person_id(machine_idx)

                        # Create assignment
                        assignment = Assignment(
                            task_id=task.id,
                            person_id=person_id,
                            scheduled_start=scheduled_start,
                            scheduled_end=scheduled_end,
                            allocated_capacity=1.0,
                        )
                        assignments.append(assignment)

                    except (AttributeError, IndexError, KeyError):
                        # Solution doesn't have this information or task not scheduled
                        continue

        except Exception as e:
            # Handle parsing errors gracefully
            print(f"Warning: Error parsing solution: {e}")

        return assignments, metadata
