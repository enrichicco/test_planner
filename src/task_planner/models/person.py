"""
Person model for representing team members.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_planner.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from .assignment import Assignment
    from .team import Team


class Person(Base, TimestampMixin):  # type: ignore[misc]
    """Represents a person who can be assigned to tasks."""

    __tablename__ = "people"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    skills: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    max_concurrent_tasks: Mapped[int] = mapped_column(Integer, default=5)

    # Foreign Keys
    team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)

    # Relationships
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="members")
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="person")

    def __repr__(self) -> str:
        return f"<Person(id={self.id}, name='{self.name}', email='{self.email}')>"
