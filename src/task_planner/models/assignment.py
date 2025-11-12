"""
Assignment model for linking tasks to people and resources.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Person, Resource, Task
from .base import Base, TimestampMixin


class Assignment(Base, TimestampMixin):
    """Represents the assignment of a task to a person and/or resource."""

    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Keys
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"), nullable=False)
    person_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("people.id"), nullable=True
    )
    resource_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("resources.id"), nullable=True
    )

    # Scheduling information
    scheduled_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    scheduled_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    allocated_capacity: Mapped[float] = mapped_column(Float, default=1.0)

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="assignments")
    person: Mapped[Optional["Person"]] = relationship("Person", back_populates="assignments")
    resource: Mapped[Optional["Resource"]] = relationship("Resource", back_populates="assignments")

    def __repr__(self) -> str:
        return f"<Assignment(id={self.id}, task_id={self.task_id}, person_id={self.person_id})>"
