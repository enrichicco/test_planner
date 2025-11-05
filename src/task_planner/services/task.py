"""Service for managing tasks."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from task_planner.models import (
    Task,
    TaskStatus,
    TaskResource,
    TaskDependency,
    TaskException,
)
from task_planner.services.exceptions import ValidationException


class TaskService:
    """Service for managing tasks."""

    def __init__(self, db: Session):
        """Initialize task service with database session."""
        self.db = db

    def create_task(
        self,
        name: str,
        estimated_hours: float,
        description: Optional[str] = None,
        priority: int = 5,
        team_id: Optional[int] = None,
        assigned_person_id: Optional[int] = None,
        earliest_start: Optional[datetime] = None,
        latest_end: Optional[datetime] = None,
        parent_task_id: Optional[int] = None,
    ) -> Task:
        """Create a new task."""
        task = Task(
            name=name,
            description=description,
            estimated_hours=estimated_hours,
            priority=priority,
            team_id=team_id,
            assigned_person_id=assigned_person_id,
            earliest_start=earliest_start,
            latest_end=latest_end,
            parent_task_id=parent_task_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_tasks(
        self,
        status: Optional[TaskStatus] = None,
        team_id: Optional[int] = None,
    ) -> List[Task]:
        """Get all tasks, optionally filtered by status and team."""
        query = self.db.query(Task)

        if status is not None:
            query = query.filter(Task.status == status)

        if team_id is not None:
            query = query.filter(Task.team_id == team_id)

        return query.all()

    def add_resource_requirement(
        self,
        task_id: int,
        resource_id: int,
        quantity: float = 1.0,
    ):
        """Add a resource requirement to a task."""
        task = self.get_task(task_id)
        if not task:
            raise ValidationException(f"Task {task_id} not found")

        task_resource = TaskResource(
            task_id=task_id,
            resource_id=resource_id,
            quantity_required=quantity,
        )
        self.db.add(task_resource)
        self.db.commit()

    def add_dependency(
        self,
        task_id: int,
        depends_on_task_id: int,
        dependency_type: str = "finish_to_start",
    ):
        """Add a dependency between tasks."""
        task = self.get_task(task_id)
        if not task:
            raise ValidationException(f"Task {task_id} not found")

        depends_on = self.get_task(depends_on_task_id)
        if not depends_on:
            raise ValidationException(f"Task {depends_on_task_id} not found")

        # Check for circular dependencies
        if self._would_create_cycle(task_id, depends_on_task_id):
            raise ValidationException("Adding this dependency would create a cycle")

        dependency = TaskDependency(
            task_id=task_id,
            depends_on_task_id=depends_on_task_id,
            dependency_type=dependency_type,
        )
        self.db.add(dependency)
        self.db.commit()

    def _would_create_cycle(self, task_id: int, depends_on_task_id: int) -> bool:
        """Check if adding a dependency would create a cycle."""
        visited = set()

        def has_path(from_id: int, to_id: int) -> bool:
            if from_id == to_id:
                return True
            if from_id in visited:
                return False

            visited.add(from_id)

            # Get all tasks that from_id depends on
            dependencies = (
                self.db.query(TaskDependency).filter(TaskDependency.task_id == from_id).all()
            )

            for dep in dependencies:
                if has_path(dep.depends_on_task_id, to_id):
                    return True

            return False

        return has_path(depends_on_task_id, task_id)

    def record_exception(
        self,
        task_id: int,
        exception_type: str,
        description: str,
    ) -> TaskException:
        """Record an exception for a task."""
        task = self.get_task(task_id)
        if not task:
            raise ValidationException(f"Task {task_id} not found")

        exception = TaskException(
            task_id=task_id,
            exception_type=exception_type,
            description=description,
        )
        self.db.add(exception)
        self.db.commit()
        self.db.refresh(exception)
        return exception

    def resolve_exception(
        self,
        exception_id: int,
        resolution_notes: str,
    ):
        """Resolve a task exception."""
        exception = self.db.query(TaskException).filter(TaskException.id == exception_id).first()
        if not exception:
            raise ValidationException(f"Exception {exception_id} not found")

        exception.resolved = True
        exception.resolved_at = datetime.utcnow()
        exception.resolution_notes = resolution_notes
        self.db.commit()

    def update_task_status(self, task_id: int, status: TaskStatus) -> Task:
        """Update task status."""
        task = self.get_task(task_id)
        if not task:
            raise ValidationException(f"Task {task_id} not found")

        task.status = status

        # Update actual times based on status
        if status == TaskStatus.IN_PROGRESS and not task.actual_start:
            task.actual_start = datetime.utcnow()
        elif status == TaskStatus.COMPLETED and not task.actual_end:
            task.actual_end = datetime.utcnow()

        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        priority: Optional[int] = None,
        assigned_person_id: Optional[int] = None,
    ) -> Task:
        """Update task information."""
        task = self.get_task(task_id)
        if not task:
            raise ValidationException(f"Task {task_id} not found")

        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        if estimated_hours is not None:
            task.estimated_hours = estimated_hours
        if priority is not None:
            task.priority = priority
        if assigned_person_id is not None:
            task.assigned_person_id = assigned_person_id

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int):
        """Delete a task."""
        task = self.get_task(task_id)
        if not task:
            raise ValidationException(f"Task {task_id} not found")

        self.db.delete(task)
        self.db.commit()
