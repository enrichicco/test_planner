"""
Report generation service for a2rp schema.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ...models.a2rp import Assignment, Project, Resource, Task


class ReportGenerator:
    """Generate various reports from a2rp schema data."""

    def __init__(self, db: Session) -> None:
        """
        Initialize report generator.

        Args:
            db: Database session
        """
        self.db = db

    def generate_project_summary(
        self, project_status_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a summary report of all projects.

        Args:
            project_status_id: Optional filter by project status

        Returns:
            Dictionary containing project summary statistics
        """
        query = self.db.query(Project)
        if project_status_id is not None:
            query = query.filter(Project.project_status_id == project_status_id)

        projects = query.all()

        # Count by status
        status_counts: Dict[int, int] = {}
        for project in projects:
            status_id = project.project_status_id
            status_counts[status_id] = status_counts.get(status_id, 0) + 1

        # Calculate date ranges
        active_projects = [p for p in projects if p.start_date and p.end_date]
        avg_duration_days = None
        if active_projects:
            durations = [
                (p.end_date - p.start_date).days  # type: ignore[union-attr]
                for p in active_projects
            ]
            avg_duration_days = sum(durations) / len(durations) if durations else None

        return {
            "total_projects": len(projects),
            "status_counts": status_counts,
            "average_duration_days": avg_duration_days,
            "generated_at": datetime.now().isoformat(),
        }

    def generate_task_summary(
        self,
        project_id: Optional[int] = None,
        task_status_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a summary report of tasks.

        Args:
            project_id: Optional filter by project
            task_status_id: Optional filter by task status

        Returns:
            Dictionary containing task summary statistics
        """
        query = self.db.query(Task)
        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        if task_status_id is not None:
            query = query.filter(Task.task_status_id == task_status_id)

        tasks = query.all()

        # Count by status
        status_counts: Dict[int, int] = {}
        for task in tasks:
            status_id = task.task_status_id
            status_counts[status_id] = status_counts.get(status_id, 0) + 1

        # Calculate work totals
        total_work = sum(task.work or 0.0 for task in tasks)

        # Count tasks with/without dates
        tasks_with_dates = sum(1 for t in tasks if t.start_date and t.end_date)
        tasks_overdue = sum(
            1
            for t in tasks
            if t.end_date and t.end_date < datetime.now() and t.task_status_id != 3
        )  # Assuming 3 is "completed"

        return {
            "total_tasks": len(tasks),
            "status_counts": status_counts,
            "total_work_hours": round(total_work, 2),
            "tasks_with_schedule": tasks_with_dates,
            "tasks_potentially_overdue": tasks_overdue,
            "generated_at": datetime.now().isoformat(),
        }

    def generate_resource_workload_report(
        self, resource_type_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate workload report for resources.

        Args:
            resource_type_id: Optional filter by resource type

        Returns:
            List of dictionaries with resource workload information
        """
        query = self.db.query(Resource)
        if resource_type_id is not None:
            query = query.filter(Resource.resource_type_id == resource_type_id)

        resources = query.all()

        report = []
        for resource in resources:
            # Get assignments for this resource
            assignments = (
                self.db.query(Assignment)
                .filter(Assignment.resource_id == resource.resource_id)
                .all()
            )

            total_assigned_work = sum(a.work or 0.0 for a in assignments)
            total_actual_work = sum(a.actual_work or 0.0 for a in assignments)
            active_assignments = len(assignments)

            # Calculate utilization (if actual work is recorded)
            utilization_percentage = None
            if total_assigned_work > 0 and total_actual_work > 0:
                utilization_percentage = (
                    total_actual_work / total_assigned_work
                ) * 100

            report.append(
                {
                    "resource_id": resource.resource_id,
                    "resource_name": resource.name,
                    "resource_type_id": resource.resource_type_id,
                    "active_assignments": active_assignments,
                    "total_assigned_work_hours": round(total_assigned_work, 2),
                    "total_actual_work_hours": round(total_actual_work, 2),
                    "utilization_percentage": (
                        round(utilization_percentage, 2)
                        if utilization_percentage
                        else None
                    ),
                }
            )

        # Sort by total assigned work descending
        report.sort(key=lambda x: x["total_assigned_work_hours"], reverse=True)

        return report

    def generate_assignment_report(
        self,
        project_id: Optional[int] = None,
        resource_id: Optional[int] = None,
        include_completed: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Generate detailed assignment report.

        Args:
            project_id: Optional filter by project
            resource_id: Optional filter by resource
            include_completed: Whether to include completed assignments

        Returns:
            List of dictionaries with assignment details
        """
        query = self.db.query(Assignment).join(Task).join(Resource)

        if project_id is not None:
            query = query.filter(Task.project_id == project_id)
        if resource_id is not None:
            query = query.filter(Assignment.resource_id == resource_id)

        assignments = query.all()

        report = []
        for assignment in assignments:
            task = (
                self.db.query(Task)
                .filter(Task.task_id == assignment.task_id)
                .first()
            )
            resource = (
                self.db.query(Resource)
                .filter(Resource.resource_id == assignment.resource_id)
                .first()
            )

            if not task or not resource:
                continue

            # Calculate variance
            variance_hours = None
            if assignment.work and assignment.actual_work:
                variance_hours = assignment.actual_work - assignment.work

            report.append(
                {
                    "assignment_id": assignment.assignment_id,
                    "task_id": task.task_id,
                    "task_name": task.name,
                    "resource_id": resource.resource_id,
                    "resource_name": resource.name,
                    "assigned_work_hours": assignment.work,
                    "actual_work_hours": assignment.actual_work,
                    "variance_hours": round(variance_hours, 2) if variance_hours else None,
                    "start_date": (
                        assignment.start_date.isoformat() if assignment.start_date else None
                    ),
                    "end_date": (
                        assignment.end_date.isoformat() if assignment.end_date else None
                    ),
                }
            )

        return report

    def generate_project_timeline_report(
        self, project_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate timeline report for projects.

        Args:
            project_id: Optional filter by specific project

        Returns:
            List of dictionaries with project timeline information
        """
        query = self.db.query(Project)
        if project_id is not None:
            query = query.filter(Project.project_id == project_id)

        projects = query.all()

        report = []
        for project in projects:
            # Get tasks for this project
            tasks = (
                self.db.query(Task)
                .filter(Task.project_id == project.project_id)
                .all()
            )

            total_tasks = len(tasks)
            total_work = sum(t.work or 0.0 for t in tasks)

            # Calculate completion percentage
            completed_tasks = sum(
                1 for t in tasks if t.task_status_id == 3
            )  # Assuming 3 is completed
            completion_percentage = (
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            )

            # Check if overdue
            is_overdue = False
            if project.end_date and datetime.now() > project.end_date:
                is_overdue = True

            report.append(
                {
                    "project_id": project.project_id,
                    "project_name": project.name,
                    "project_status_id": project.project_status_id,
                    "start_date": (
                        project.start_date.isoformat() if project.start_date else None
                    ),
                    "end_date": (
                        project.end_date.isoformat() if project.end_date else None
                    ),
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "completion_percentage": round(completion_percentage, 2),
                    "total_work_hours": round(total_work, 2),
                    "is_overdue": is_overdue,
                }
            )

        return report
