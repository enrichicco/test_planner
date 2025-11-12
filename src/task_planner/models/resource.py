"""
Resource model for representing equipment, tools, and other resources.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .assignment import Assignment


class Resource(Base, TimestampMixin):
    """Represents a resource that can be allocated to tasks."""

    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    capacity: Mapped[float] = mapped_column(Float, default=1.0)
    is_renewable: Mapped[bool] = mapped_column(Boolean, default=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="resource")

    def __repr__(self) -> str:
        return f"<Resource(id={self.id}, name='{self.name}', type='{self.resource_type}')>"
