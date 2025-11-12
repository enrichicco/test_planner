"""
Team model for organizing people into groups.
"""

from typing import List, Optional

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Person, Task
from .base import Base, TimestampMixin


class Team(Base, TimestampMixin):
    """Represents a team of people working together."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    members: Mapped[List["Person"]] = relationship(
        "Person", back_populates="team", cascade="all, delete-orphan"
    )
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="team")

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name='{self.name}')>"
