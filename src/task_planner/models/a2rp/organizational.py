"""
Organizational and structure models for a2rp schema.
Includes organizational units, cost centers, customers, and breakdown structures.
"""
from sqlalchemy import Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal

from .base import A2RPBase

if TYPE_CHECKING:
    from .core import Project, Task, Resource, Assignment, ProcessingOrder


class CostCenter(A2RPBase):
    """Cost center for financial tracking."""

    __tablename__ = "cost_center"

    cost_center_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource", foreign_keys="Resource.cost_center_id", back_populates="cost_center"
    )
    resource_cost_centers: Mapped[List["Resource"]] = relationship(
        "Resource",
        foreign_keys="Resource.resource_cost_center_id",
        back_populates="resource_cost_center",
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", foreign_keys="Task.cost_center_id", back_populates="cost_center"
    )
    executor_tasks: Mapped[List["Task"]] = relationship(
        "Task",
        foreign_keys="Task.executor_cost_center_id",
        back_populates="executor_cost_center",
    )

    def __repr__(self) -> str:
        return f"<CostCenter(id={self.cost_center_id}, name='{self.name}')>"


class CostItem(A2RPBase):
    """Cost line item for tracking project costs."""

    __tablename__ = "cost_item"

    cost_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<CostItem(id={self.cost_item_id}, name='{self.name}')>"


class Customer(A2RPBase):
    """Customer/client information."""

    __tablename__ = "customer"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="customer"
    )

    def __repr__(self) -> str:
        return f"<Customer(id={self.customer_id}, name='{self.name}')>"


class Imputation(A2RPBase):
    """Cost imputation/allocation."""

    __tablename__ = "imputation"

    imputation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="imputation"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", foreign_keys="Task.imputation_ce_id", back_populates="imputation_ce"
    )
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", back_populates="imputation"
    )

    def __repr__(self) -> str:
        return f"<Imputation(id={self.imputation_id}, name='{self.name}')>"


class OrganizationalUnit(A2RPBase):
    """Organizational unit in company hierarchy."""

    __tablename__ = "organizational_unit"

    organizational_unit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rate: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    monthly_hours_availability: Mapped[Optional[Decimal]] = mapped_column(
        Numeric, nullable=True
    )

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource",
        foreign_keys="Resource.organizational_unit_id",
        back_populates="organizational_unit",
    )
    resource_organizational_units: Mapped[List["Resource"]] = relationship(
        "Resource",
        foreign_keys="Resource.resource_organizational_unit_id",
        back_populates="resource_organizational_unit",
    )
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="project_manager_organizational_unit"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="organizational_unit_manager"
    )
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", back_populates="organizational_unit_manager"
    )

    def __repr__(self) -> str:
        return f"<OrganizationalUnit(id={self.organizational_unit_id}, name='{self.name}')>"


class TechnicalFeature(A2RPBase):
    """Technical feature definition."""

    __tablename__ = "technical_feature"

    technical_feature_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    processing_orders: Mapped[List["ProcessingOrder"]] = relationship(
        "ProcessingOrder", back_populates="technical_feature"
    )

    def __repr__(self) -> str:
        return f"<TechnicalFeature(id={self.technical_feature_id}, name='{self.name}')>"


class WorkBreakdownStructure(A2RPBase):
    """Work Breakdown Structure (WBS) definition."""

    __tablename__ = "work_breakdown_structure"

    work_breakdown_structure_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.project.project_id"), nullable=True
    )

    # Relationships
    project: Mapped[Optional["Project"]] = relationship(
        "Project", foreign_keys=[project_id], back_populates="wbs_elements"
    )
    projects_using: Mapped[List["Project"]] = relationship(
        "Project",
        foreign_keys="Project.work_breakdown_structure_id",
        back_populates="work_breakdown_structure",
    )
    processing_orders: Mapped[List["ProcessingOrder"]] = relationship(
        "ProcessingOrder", back_populates="work_breakdown_structure"
    )
    tasks_verify: Mapped[List["Task"]] = relationship(
        "Task",
        foreign_keys="Task.verify_work_breakdown_structure_id",
        back_populates="verify_work_breakdown_structure",
    )
    tasks_element: Mapped[List["Task"]] = relationship(
        "Task",
        foreign_keys="Task.element_work_breakdown_structure_id",
        back_populates="element_work_breakdown_structure",
    )

    def __repr__(self) -> str:
        return f"<WorkBreakdownStructure(id={self.work_breakdown_structure_id}, name='{self.name}')>"


class ResourceBreakdownStructure(A2RPBase):
    """Resource Breakdown Structure (RBS) definition."""

    __tablename__ = "resource_breakdown_structure"

    resource_breakdown_structure_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    resources: Mapped[List["Resource"]] = relationship(
        "Resource",
        foreign_keys="Resource.resource_breakdown_structure_id",
        back_populates="resource_breakdown_structure",
    )
    resources_1: Mapped[List["Resource"]] = relationship(
        "Resource",
        foreign_keys="Resource.resource_breakdown_structure_1_id",
        back_populates="resource_breakdown_structure_1",
    )
    resources_2: Mapped[List["Resource"]] = relationship(
        "Resource",
        foreign_keys="Resource.resource_breakdown_structure_2_id",
        back_populates="resource_breakdown_structure_2",
    )

    def __repr__(self) -> str:
        return f"<ResourceBreakdownStructure(id={self.resource_breakdown_structure_id}, name='{self.name}')>"
