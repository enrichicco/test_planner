"""
Base model for a2rp schema SQLAlchemy models.
"""
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional


class A2RPBase(DeclarativeBase):
    """Base class for all a2rp schema database models."""

    __table_args__ = {"schema": "a2rp"}


class TimestampMixin:
    """Mixin for adding created_date and modified_date timestamps."""

    created_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class RevisionMixin:
    """Mixin for adding revision counter fields."""

    created_revision_counter: Mapped[Optional[int]] = mapped_column(nullable=True)
    modified_revision_counter: Mapped[Optional[int]] = mapped_column(nullable=True)
