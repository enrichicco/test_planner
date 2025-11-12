"""
Exception model for tracking scheduling conflicts and issues.
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .schedule import Schedule
    from .task import Task


class ExceptionType(enum.Enum):
    """Types of scheduling exceptions."""

    RESOURCE_CONFLICT = "resource_conflict"
    DEADLINE_MISS = "deadline_miss"
    CONSTRAINT_VIOLATION = "constraint_violation"
    PERSON_UNAVAILABLE = "person_unavailable"
    RESOURCE_UNAVAILABLE = "resource_unavailable"
    DEPENDENCY_CONFLICT = "dependency_conflict"
    CAPACITY_EXCEEDED = "capacity_exceeded"
    OTHER = "other"


class ScheduleException(Base, TimestampMixin):
    """Represents an exception or issue that occurred during scheduling."""

    __tablename__ = "schedule_exceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exception_type: Mapped[ExceptionType] = mapped_column(Enum(ExceptionType), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="warning")  # warning, error, critical
    message: Mapped[str] = mapped_column(Text, nullable=False)
    resolved: Mapped[bool] = mapped_column(default=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign Keys
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedules.id"), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=True)

    # Relationships
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="exceptions")
    task: Mapped[Optional["Task"]] = relationship("Task")

    def __repr__(self) -> str:
        return f"<ScheduleException(id={self.id}, type='{self.exception_type.value}', severity='{self.severity}')>"
