"""
Service for managing tasks in the a2rp schema.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from ...models.a2rp import Project, Task, TaskStatus


class TaskService:
    """Service for task operations in a2rp schema."""

    def __init__(self, db: Session) -> None:
        """Initialize task service with database session."""
        self.db = db

    def create_task(
        self,
        name: str,
        project_id: int,
        task_status_id: int,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        work: Optional[float] = None,
        **kwargs: object,
    ) -> Task:
        """Create a new task."""
        # Validate project exists
        project = self.db.query(Project).filter(Project.project_id == project_id).first()
        if not project:
            raise LookupError(f"Project {project_id} not found")

        # Validate task status exists
        task_status = (
            self.db.query(TaskStatus).filter(TaskStatus.task_status_id == task_status_id).first()
        )
        if not task_status:
            raise LookupError(f"TaskStatus {task_status_id} not found")

        task = Task(
            name=name,
            description=description,
            project_id=project_id,
            task_status_id=task_status_id,
            start_date=start_date,
            end_date=end_date,
            work=work,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self.db.query(Task).filter(Task.task_id == task_id).first()

    def list_tasks(
        self,
        project_id: Optional[int] = None,
        task_status_id: Optional[int] = None,
        limit: int = 100,
    ) -> List[Task]:
        """List tasks, optionally filtered by project and status."""
        query = self.db.query(Task)

        if project_id is not None:
            query = query.filter(Task.project_id == project_id)

        if task_status_id is not None:
            query = query.filter(Task.task_status_id == task_status_id)

        return query.limit(limit).all()

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        task_status_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        work: Optional[float] = None,
    ) -> Optional[Task]:
        """Update a task."""
        task = self.get_task(task_id)
        if not task:
            return None

        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        if task_status_id is not None:
            task.task_status_id = task_status_id
        if start_date is not None:
            task.start_date = start_date
        if end_date is not None:
            task.end_date = end_date
        if work is not None:
            task.work = Decimal(work)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        task = self.get_task(task_id)
        if not task:
            return False

        self.db.delete(task)
        self.db.commit()
        return True
