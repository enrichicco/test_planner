"""
Service for managing tasks.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Task, TaskStatus, TaskPriority


class TaskService:
    """Service for task operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_task(
        self,
        name: str,
        duration: float,
        description: Optional[str] = None,
        team_id: Optional[int] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        earliest_start: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        due_date: Optional[datetime] = None,
        required_skills: Optional[Dict[str, Any]] = None,
        required_resources: Optional[Dict[str, Any]] = None,
        predecessor_id: Optional[int] = None,
    ) -> Task:
        """Create a new task."""
        task = Task(
            name=name,
            duration=duration,
            description=description,
            team_id=team_id,
            priority=priority,
            earliest_start=earliest_start,
            deadline=deadline,
            due_date=due_date,
            required_skills=required_skills or {},
            required_resources=required_resources or {},
            predecessor_id=predecessor_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list_tasks(
        self,
        team_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        limit: int = 100,
    ) -> List[Task]:
        """List tasks."""
        query = self.db.query(Task).order_by(Task.created_at.desc())
        if team_id:
            query = query.filter(Task.team_id == team_id)
        if status:
            query = query.filter(Task.status == status)
        return query.limit(limit).all()

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        duration: Optional[float] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        earliest_start: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        due_date: Optional[datetime] = None,
        required_skills: Optional[Dict[str, Any]] = None,
        required_resources: Optional[Dict[str, Any]] = None,
    ) -> Optional[Task]:
        """Update a task."""
        task = self.get_task(task_id)
        if not task:
            return None

        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        if duration is not None:
            task.duration = duration
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if earliest_start is not None:
            task.earliest_start = earliest_start
        if deadline is not None:
            task.deadline = deadline
        if due_date is not None:
            task.due_date = due_date
        if required_skills is not None:
            task.required_skills = required_skills
        if required_resources is not None:
            task.required_resources = required_resources

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
