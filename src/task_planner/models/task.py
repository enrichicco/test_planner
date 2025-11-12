"""
Task model for representing work items to be scheduled.
"""

import enum
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Assignment, Schedule, Team
from .base import Base, TimestampMixin


class TaskStatus(enum.Enum):
    """Status of a task."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TaskPriority(enum.Enum):
    """Priority levels for tasks."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Task(Base, TimestampMixin):
    """Represents a task to be scheduled and executed."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration: Mapped[float] = mapped_column(Float, nullable=False)  # in hours
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), default=TaskPriority.MEDIUM)

    # Scheduling constraints
    earliest_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Resource requirements
    required_skills: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    required_resources: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Foreign Keys
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    schedule_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("schedules.id"), nullable=True
    )
    predecessor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=True
    )

    # Relationships
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="tasks")
    schedule: Mapped[Optional["Schedule"]] = relationship("Schedule", back_populates="tasks")
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", back_populates="task", cascade="all, delete-orphan"
    )
    predecessor: Mapped[Optional["Task"]] = relationship(
        "Task", remote_side=[id], backref="successors"
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status.value}')>"
