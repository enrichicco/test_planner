"""
Schedule report data structures and calculations.
"""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..models import Assignment, Person, Schedule, ScheduleException, Task


class ScheduleReport:
    """Generates comprehensive reports for schedules."""

    def __init__(
        self,
        schedule: Schedule,
        assignments: List[Assignment],
        tasks: List[Task],
        people: List[Person],
        exceptions: List[ScheduleException],
    ) -> None:
        """
        Initialize schedule report.

        Args:
            schedule: Schedule to report on
            assignments: List of assignments
            tasks: List of tasks
            people: List of people
            exceptions: List of exceptions
        """
        self.schedule = schedule
        self.assignments = assignments
        self.tasks = {t.id: t for t in tasks}
        self.people = {p.id: p for p in people}
        self.exceptions = exceptions

    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics."""
        total_tasks = len(self.tasks)
        scheduled_tasks = len(self.assignments)
        unscheduled_tasks = total_tasks - scheduled_tasks

        total_duration = sum(t.duration for t in self.tasks.values())
        scheduled_duration = sum(
            self.tasks[a.task_id].duration for a in self.assignments if a.task_id in self.tasks
        )

        # Calculate makespan
        makespan = None
        if self.assignments and self.assignments[0].scheduled_end:
            earliest_start = min(a.scheduled_start for a in self.assignments if a.scheduled_start)
            latest_end = max(a.scheduled_end for a in self.assignments if a.scheduled_end)
            makespan = (latest_end - earliest_start).total_seconds() / 3600  # hours

        return {
            "schedule_name": self.schedule.name,
            "status": self.schedule.status.value,
            "start_date": self.schedule.start_date.isoformat(),
            "end_date": self.schedule.end_date.isoformat(),
            "total_tasks": total_tasks,
            "scheduled_tasks": scheduled_tasks,
            "unscheduled_tasks": unscheduled_tasks,
            "total_duration_hours": round(total_duration, 2),
            "scheduled_duration_hours": round(scheduled_duration, 2),
            "makespan_hours": round(makespan, 2) if makespan else None,
            "objective_value": self.schedule.objective_value,
            "solver_used": self.schedule.solver_used,
            "solve_time_seconds": round(self.schedule.solve_time, 2)
            if self.schedule.solve_time
            else None,
            "total_exceptions": len(self.exceptions),
            "unresolved_exceptions": sum(1 for e in self.exceptions if not e.resolved),
        }

    def generate_person_utilization(self) -> List[Dict[str, Any]]:
        """Generate person utilization report."""
        person_stats: Dict[int, Dict[str, Any]] = defaultdict(
            lambda: {
                "person_id": None,
                "person_name": None,
                "total_tasks": 0,
                "total_hours": 0.0,
                "assignments": [],
            }
        )

        for assignment in self.assignments:
            if assignment.person_id:
                person_id = assignment.person_id
                task = self.tasks.get(assignment.task_id)

                if person_id not in self.people:
                    continue

                person = self.people[person_id]
                person_stats[person_id]["person_id"] = person_id
                person_stats[person_id]["person_name"] = person.name
                person_stats[person_id]["total_tasks"] += 1

                if task:
                    person_stats[person_id]["total_hours"] += task.duration

                person_stats[person_id]["assignments"].append(
                    {
                        "task_id": assignment.task_id,
                        "task_name": task.name if task else "Unknown",
                        "scheduled_start": assignment.scheduled_start.isoformat()
                        if assignment.scheduled_start
                        else None,
                        "scheduled_end": assignment.scheduled_end.isoformat()
                        if assignment.scheduled_end
                        else None,
                        "duration_hours": task.duration if task else 0,
                    }
                )

        result = list(person_stats.values())
        for item in result:
            item["total_hours"] = round(item["total_hours"], 2)
        return result

    def generate_task_timeline(self) -> List[Dict[str, Any]]:
        """Generate task timeline."""
        timeline: List[Dict[str, int | float | str | Optional[datetime]]] = []

        for assignment in self.assignments:
            task = self.tasks.get(assignment.task_id)
            person = self.people.get(assignment.person_id) if assignment.person_id else None

            timeline.append(
                {
                    "task_id": assignment.task_id,
                    "task_name": task.name if task else "Unknown",
                    "person_id": person.id if person else None,
                    "person_name": person.name if person else None,
                    "scheduled_start": assignment.scheduled_start.isoformat()
                    if assignment.scheduled_start
                    else None,
                    "scheduled_end": assignment.scheduled_end.isoformat()
                    if assignment.scheduled_end
                    else None,
                    "duration_hours": task.duration if task else 0,
                    "status": task.status.value if task else "unknown",
                    "priority": task.priority.value if task else 0,
                }
            )

        # Sort by scheduled start time
        timeline.sort(key=lambda x: x["scheduled_start"] if x["scheduled_start"] else "9999-12-31")
        return timeline

    def generate_exceptions_report(self) -> List[Dict[str, Any]]:
        """Generate exceptions report."""
        return [
            {
                "exception_id": exc.id,
                "type": exc.exception_type.value,
                "severity": exc.severity,
                "message": exc.message,
                "task_id": exc.task_id,
                "task_name": self.tasks[exc.task_id].name if exc.task_id in self.tasks else None,
                "resolved": exc.resolved,
                "resolved_at": exc.resolved_at.isoformat() if exc.resolved_at else None,
                "resolution_notes": exc.resolution_notes,
                "created_at": exc.created_at.isoformat(),
            }
            for exc in self.exceptions
        ]

    def generate_full_report(self) -> Dict[str, Any]:
        """Generate complete report with all sections."""
        return {
            "summary": self.generate_summary(),
            "person_utilization": self.generate_person_utilization(),
            "task_timeline": self.generate_task_timeline(),
            "exceptions": self.generate_exceptions_report(),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
