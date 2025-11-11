"""
Lookup and reference table models for a2rp schema.
These tables store status values, types, and other reference data.
"""
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from .base import A2RPBase

if TYPE_CHECKING:
    from .core import Project, Task, Resource, ProcessingOrder


class ProjectStatus(A2RPBase):
    """Project status lookup table."""

    __tablename__ = "project_status"

    project_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="project_status"
    )

    def __repr__(self) -> str:
        return f"<ProjectStatus(id={self.project_status_id}, name='{self.name}')>"


class ProjectType(A2RPBase):
    """Project type lookup table."""

    __tablename__ = "project_type"

    project_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="project_type"
    )

    def __repr__(self) -> str:
        return f"<ProjectType(id={self.project_type_id}, name='{self.name}')>"


class TaskStatus(A2RPBase):
    """Task status lookup table."""

    __tablename__ = "task_status"

    task_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="task_status")

    def __repr__(self) -> str:
        return f"<TaskStatus(id={self.task_status_id}, name='{self.name}')>"


class ResourceStatus(A2RPBase):
    """Resource status lookup table."""

    __tablename__ = "resource_status"

    resource_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource", back_populates="resource_status"
    )

    def __repr__(self) -> str:
        return f"<ResourceStatus(id={self.resource_status_id}, name='{self.name}')>"


class ResourceType(A2RPBase):
    """Resource type lookup table."""

    __tablename__ = "resource_type"

    resource_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource", back_populates="resource_type"
    )

    def __repr__(self) -> str:
        return f"<ResourceType(id={self.resource_type_id}, name='{self.name}')>"


class ProcessingOrderStatus(A2RPBase):
    """Processing order status lookup table."""

    __tablename__ = "processing_order_status"

    processing_order_status_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    processing_orders: Mapped[List["ProcessingOrder"]] = relationship(
        "ProcessingOrder", back_populates="processing_order_status"
    )

    def __repr__(self) -> str:
        return f"<ProcessingOrderStatus(id={self.processing_order_status_id}, name='{self.name}')>"


class ProcessingOrderType(A2RPBase):
    """Processing order type lookup table."""

    __tablename__ = "processing_order_type"

    processing_order_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    processing_orders: Mapped[List["ProcessingOrder"]] = relationship(
        "ProcessingOrder", back_populates="processing_order_type"
    )

    def __repr__(self) -> str:
        return f"<ProcessingOrderType(id={self.processing_order_type_id}, name='{self.name}')>"


class CostType(A2RPBase):
    """Cost type lookup table."""

    __tablename__ = "cost_type"

    cost_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<CostType(id={self.cost_type_id}, name='{self.name}')>"


class Job(A2RPBase):
    """Job definition lookup table."""

    __tablename__ = "job"

    job_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship("Resource", back_populates="job")

    def __repr__(self) -> str:
        return f"<Job(id={self.job_id}, name='{self.name}')>"


class NtAccount(A2RPBase):
    """Windows NT account integration table."""

    __tablename__ = "nt_account"

    nt_account_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource", back_populates="nt_account"
    )

    def __repr__(self) -> str:
        return f"<NtAccount(id={self.nt_account_id}, name='{self.name}')>"


class Property(A2RPBase):
    """Generic property lookup table."""

    __tablename__ = "property"

    property_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource", back_populates="property"
    )

    def __repr__(self) -> str:
        return f"<Property(id={self.property_id}, name='{self.name}')>"
