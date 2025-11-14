"""
Supporting table models for a2rp schema.
Includes processing orders, planning tables, and historical data.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import A2RPBase

if TYPE_CHECKING:
    from .core import Task
    from .lookups import ProcessingOrderStatus, ProcessingOrderType
    from .organizational import (
        TechnicalFeature,
        WorkBreakdownStructure,
    )


class ProcessingOrder(A2RPBase):
    """Work order or processing request."""

    __tablename__ = "processing_order"

    # Primary key
    processing_order_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    project_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phase: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    row_state_processing_order_shark: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    # Foreign keys
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.project.project_id"), nullable=True
    )
    task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.task.task_id"), nullable=True
    )
    processing_order_type_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.processing_order_type.processing_order_type_id"), nullable=True
    )
    processing_order_status_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.processing_order_status.processing_order_status_id"),
        nullable=True,
    )
    work_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.work_breakdown_structure.work_breakdown_structure_id"),
        nullable=True,
    )
    technical_feature_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.technical_feature.technical_feature_id"), nullable=True
    )
    program_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    project_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    value_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    release_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    modified_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    processing_order_type: Mapped[Optional["ProcessingOrderType"]] = relationship(
        "ProcessingOrderType", back_populates="processing_orders"
    )
    processing_order_status: Mapped[Optional["ProcessingOrderStatus"]] = relationship(
        "ProcessingOrderStatus", back_populates="processing_orders"
    )
    work_breakdown_structure: Mapped[Optional["WorkBreakdownStructure"]] = relationship(
        "WorkBreakdownStructure", back_populates="processing_orders"
    )
    technical_feature: Mapped[Optional["TechnicalFeature"]] = relationship(
        "TechnicalFeature", back_populates="processing_orders"
    )
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="processing_order", foreign_keys="Task.processing_order_id"
    )

    def __repr__(self) -> str:
        return f"<ProcessingOrder(id={self.processing_order_id}, name='{self.name}')>"


class HistoricalProjectSummary(A2RPBase):
    """Historical summary data for projects."""

    __tablename__ = "historical_project_summary"

    # Primary key
    historical_project_summary_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Fields
    month: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    object: Mapped[str] = mapped_column(String(255), nullable=False)
    object_type: Mapped[str] = mapped_column(String(20), nullable=False)
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    def __repr__(self) -> str:
        return f"<HistoricalProjectSummary(id={self.historical_project_summary_id}, object='{self.object}')>"


class HistoricalProjectSummaryResource(A2RPBase):
    """Historical resource allocation data."""

    __tablename__ = "historical_project_summary_resource"

    # Composite primary key
    historical_project_summary_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("a2rp.historical_project_summary.historical_project_summary_id"),
        primary_key=True,
    )
    resource_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), primary_key=True
    )
    cost_item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.cost_item.cost_item_id"), primary_key=True
    )

    # Fields
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    def __repr__(self) -> str:
        return f"<HistoricalProjectSummaryResource(summary_id={self.historical_project_summary_id}, resource_id={self.resource_id})>"


class ProjectToPlan(A2RPBase):
    """Projects in planning phase."""

    __tablename__ = "project_to_plan"

    # Primary key
    project_to_plan_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign keys
    imputation_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.imputation.imputation_id"), nullable=True
    )
    responsible: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Cost fields
    total: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    labour_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    third_party_supplies: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    expences: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    consultants: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    materials: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    labour_cost_2: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    project_costs: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Risk fields
    prob: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    impact: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    risk_value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    risk: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    risk_description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Opportunity fields
    prob_2: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    saving: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    opportunity_value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    opportunity_description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<ProjectToPlan(id={self.project_to_plan_id})>"


class ProjectToPlanOrganizationalUnit(A2RPBase):
    """Link between projects to plan and organizational units."""

    __tablename__ = "project_to_plan_organizational_unit"

    # Composite primary key
    project_to_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.project_to_plan.project_to_plan_id"), primary_key=True
    )
    organizational_unit_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), primary_key=True
    )

    # Fields
    hours: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    def __repr__(self) -> str:
        return f"<ProjectToPlanOrganizationalUnit(project_to_plan_id={self.project_to_plan_id}, org_unit_id={self.organizational_unit_id})>"


class TaskToPlan(A2RPBase):
    """Tasks in planning phase."""

    __tablename__ = "task_to_plan"

    # Primary key
    task_to_plan_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    wp_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    row_type: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    is_milestone: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    previous: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign keys
    project_to_plan_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.project_to_plan.project_to_plan_id"), nullable=True
    )
    responsible: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Cost fields
    total: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    labour_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    third_party_supplies: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    expences: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    consultants: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    materials: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    labour_cost_2: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    project_costs: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Risk fields
    prob: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    impact: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    risk_value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    risk: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    risk_description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Opportunity fields
    prob_2: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    saving: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    opportunity_value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    value: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    opportunity_description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<TaskToPlan(id={self.task_to_plan_id}, wp_id='{self.wp_id}')>"


class TaskToPlanOrganizationalUnit(A2RPBase):
    """Link between tasks to plan and organizational units."""

    __tablename__ = "task_to_plan_organizational_unit"

    # Composite primary key
    task_to_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.task_to_plan.task_to_plan_id"), primary_key=True
    )
    organizational_unit_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), primary_key=True
    )

    # Fields
    hours: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    project_to_plan_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.project_to_plan.project_to_plan_id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<TaskToPlanOrganizationalUnit(task_to_plan_id={self.task_to_plan_id}, org_unit_id={self.organizational_unit_id})>"
