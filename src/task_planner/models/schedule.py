"""
Schedule model for representing generated schedules.
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .exception import ScheduleException
    from .task import Task


class ScheduleStatus(enum.Enum):
    """Status of a schedule."""

    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Schedule(Base, TimestampMixin):
    """Represents a generated schedule with optimization results."""

    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ScheduleStatus] = mapped_column(
        Enum(ScheduleStatus), default=ScheduleStatus.DRAFT
    )

    # Schedule time window
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Optimization results
    objective_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    solver_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    solve_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # in seconds
    optimization_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="schedule")
    exceptions: Mapped[List["ScheduleException"]] = relationship(
        "ScheduleException", back_populates="schedule", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Schedule(id={self.id}, name='{self.name}', status='{self.status.value}')>"
