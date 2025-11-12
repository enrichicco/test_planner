"""
Base model for SQLAlchemy models.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )
