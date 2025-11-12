"""
Core entity models for a2rp schema.
Includes Project, Task, Resource, and Assignment models.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import A2RPBase, RevisionMixin, TimestampMixin
from .lookups import (
    Job,
    NtAccount,
    ProjectStatus,
    ProjectType,
    Property,
    ResourceStatus,
    ResourceType,
    TaskStatus,
)
from .organizational import (
    CostCenter,
    Customer,
    Imputation,
    OrganizationalUnit,
    ResourceBreakdownStructure,
    WorkBreakdownStructure,
)

if TYPE_CHECKING:
    from .supporting import ProcessingOrder


class Project(A2RPBase, TimestampMixin, RevisionMixin):
    """Main project entity with extensive earned value management fields."""

    __tablename__ = "project"

    # Primary key
    project_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    unique_id: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign keys - people
    author_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    owner_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    program_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    project_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )

    # Foreign keys - organizational
    project_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.project_type.project_type_id"), nullable=False
    )
    project_status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.project_status.project_status_id"), nullable=False
    )
    customer_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.customer.customer_id"), nullable=True
    )
    imputation_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.imputation.imputation_id"), nullable=True
    )
    work_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.work_breakdown_structure.work_breakdown_structure_id"),
        nullable=True,
    )
    project_manager_organizational_unit_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), nullable=True
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.project.project_id"), nullable=True
    )

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    contract_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    early_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    early_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    late_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    late_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Cost fields
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    total_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    prev_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    finalized_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    residual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cost_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cv: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cvp: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Work fields
    work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    work_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Duration fields
    duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    calendar_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    duration_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    start_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    end_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # EVM metrics
    acwp: Mapped[Optional[Decimal]] = mapped_column(
        Numeric, nullable=True
    )  # Actual Cost of Work Performed
    bcws: Mapped[Optional[Decimal]] = mapped_column(
        Numeric, nullable=True
    )  # Budgeted Cost of Work Scheduled
    spi: Mapped[Optional[Decimal]] = mapped_column(
        Numeric, nullable=True
    )  # Schedule Performance Index
    tcpi: Mapped[Optional[Decimal]] = mapped_column(
        Numeric, nullable=True
    )  # To Complete Performance Index
    vac: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)  # Variance At Completion
    eac: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)  # Estimate At Completion
    cpi: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)  # Cost Performance Index
    sv: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)  # Schedule Variance
    svp: Mapped[Optional[Decimal]] = mapped_column(
        Numeric, nullable=True
    )  # Schedule Variance Percentage

    # Completion percentages
    percent_completed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    percent_work_completed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Baseline fields - Baseline 0
    baseline0_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    baseline0_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    baseline0_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    baseline0_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    baseline0_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Baseline fields - Baseline 1
    baseline1_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    baseline1_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    baseline1_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    baseline1_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    baseline1_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Baseline fields - Baseline 6
    baseline6_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    baseline6_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    baseline6_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    baseline6_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    baseline6_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Baseline fields - Baseline 10
    baseline10_fixed_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Budget fields
    budget_current_year: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    budget: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Other fields
    workspace_internal_h_ref: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    calculations_are_stale: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    fes_offer: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    accounting_sector: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    project_type: Mapped["ProjectType"] = relationship("ProjectType", back_populates="projects")
    project_status: Mapped["ProjectStatus"] = relationship(
        "ProjectStatus", back_populates="projects"
    )
    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="projects")
    imputation: Mapped[Optional["Imputation"]] = relationship(
        "Imputation", back_populates="projects"
    )
    work_breakdown_structure: Mapped[Optional["WorkBreakdownStructure"]] = relationship(
        "WorkBreakdownStructure",
        foreign_keys=[work_breakdown_structure_id],
        back_populates="projects_using",
    )
    wbs_elements: Mapped[List["WorkBreakdownStructure"]] = relationship(
        "WorkBreakdownStructure",
        foreign_keys="WorkBreakdownStructure.project_id",
        back_populates="project",
    )
    project_manager_organizational_unit: Mapped[Optional["OrganizationalUnit"]] = relationship(
        "OrganizationalUnit", back_populates="projects"
    )

    # Resource relationships (author, owner, managers)
    author: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[author_id], back_populates="authored_projects"
    )
    owner: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[owner_id], back_populates="owned_projects"
    )
    program_manager: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[program_manager_id], back_populates="program_managed_projects"
    )
    project_manager: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[project_manager_id], back_populates="project_managed_projects"
    )

    # Hierarchy
    parent: Mapped[Optional["Project"]] = relationship(
        "Project", remote_side=[project_id], foreign_keys=[parent_id], backref="children"
    )

    # Tasks
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project")

    def __repr__(self) -> str:
        return f"<Project(id={self.project_id}, name='{self.name}', status_id={self.project_status_id})>"


class Task(A2RPBase, TimestampMixin, RevisionMixin):
    """Work breakdown structure task with extensive scheduling and tracking fields."""

    __tablename__ = "task"

    # Primary key
    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    unique_id: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign keys
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.task.task_id"), nullable=True
    )
    task_status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.task_status.task_status_id"), nullable=False
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.project.project_id"), nullable=True
    )
    processing_order_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.processing_order.processing_order_id"), nullable=True
    )
    imputation_ce_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.imputation.imputation_id"), nullable=True
    )
    imputation_ce_old_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    verify_work_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.work_breakdown_structure.work_breakdown_structure_id"),
        nullable=True,
    )
    element_work_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.work_breakdown_structure.work_breakdown_structure_id"),
        nullable=True,
    )
    organizational_unit_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), nullable=True
    )
    manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    executor_cost_center_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.cost_center.cost_center_id"), nullable=True
    )
    cost_center_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.cost_center.cost_center_id"), nullable=True
    )
    project_status_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Task attributes
    fixed_cost_assignment_uid: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    task_priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    task_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    outline_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    outline_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    wbs_tree: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    client_unique_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Boolean flags
    is_overallocated: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_project_summary: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_milestone: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_critical: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_summary: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    duration_is_estimated: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_effort_driven: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_external: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_recurring: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    ignores_resource_calendar: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_marked: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    activity_with_processing_order: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deliverable_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deliverable_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    early_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    early_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    late_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    late_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    milestone_estimated_end_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    validity_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Cost fields
    fixed_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_fixed_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_overtime_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_overtime_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cost_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cv: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cvp: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    available_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    processing_order_actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Work fields
    work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    overtime_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_overtime_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_overtime_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    work_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Duration fields
    duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_duration: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    duration_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    start_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    end_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Slack
    total_slack: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    free_slack: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # EVM metrics
    acwp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bcwp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bcws: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    spi: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tcpi: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vac: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    eac: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cpi: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    sv: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    svp: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Completion percentages
    percent_completed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    percent_work_completed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    physical_percent_completed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Additional fields
    contractual_milestone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    engagement: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    milestone_project: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    activity_group: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    wp_status_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    output_task: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phase: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    task_status: Mapped["TaskStatus"] = relationship("TaskStatus", back_populates="tasks")
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="tasks")
    processing_order: Mapped[Optional["ProcessingOrder"]] = relationship(
        "ProcessingOrder", back_populates="tasks"
    )
    imputation_ce: Mapped[Optional["Imputation"]] = relationship(
        "Imputation", back_populates="tasks"
    )
    verify_work_breakdown_structure: Mapped[Optional["WorkBreakdownStructure"]] = relationship(
        "WorkBreakdownStructure",
        foreign_keys=[verify_work_breakdown_structure_id],
        back_populates="tasks_verify",
    )
    element_work_breakdown_structure: Mapped[Optional["WorkBreakdownStructure"]] = relationship(
        "WorkBreakdownStructure",
        foreign_keys=[element_work_breakdown_structure_id],
        back_populates="tasks_element",
    )
    organizational_unit_manager: Mapped[Optional["OrganizationalUnit"]] = relationship(
        "OrganizationalUnit", back_populates="tasks"
    )
    manager: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[manager_id], back_populates="managed_tasks"
    )
    executor_cost_center: Mapped[Optional["CostCenter"]] = relationship(
        "CostCenter", foreign_keys=[executor_cost_center_id], back_populates="executor_tasks"
    )
    cost_center: Mapped[Optional["CostCenter"]] = relationship(
        "CostCenter", foreign_keys=[cost_center_id], back_populates="tasks"
    )

    # Hierarchy
    parent: Mapped[Optional["Task"]] = relationship(
        "Task", remote_side=[task_id], foreign_keys=[parent_id], backref="subtasks"
    )

    # Assignments
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="task")

    def __repr__(self) -> str:
        return f"<Task(id={self.task_id}, name='{self.name}', status_id={self.task_status_id})>"


class Resource(A2RPBase, TimestampMixin, RevisionMixin):
    """Resource (person or equipment) that can be assigned to tasks."""

    __tablename__ = "resource"

    # Primary key
    resource_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    unique_id: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    mail_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    initials: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    alias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tda: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Foreign keys
    resource_status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.resource_status.resource_status_id"), nullable=False
    )
    resource_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.resource_type.resource_type_id"), nullable=False
    )
    timesheet_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    nt_account_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.nt_account.nt_account_id"), nullable=True
    )
    resource_cost_center_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.cost_center.cost_center_id"), nullable=True
    )
    organizational_unit_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), nullable=True
    )
    resource_organizational_unit_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), nullable=True
    )
    resource_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.resource_breakdown_structure.resource_breakdown_structure_id"),
        nullable=True,
    )
    resource_breakdown_structure_1_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.resource_breakdown_structure.resource_breakdown_structure_id"),
        nullable=True,
    )
    resource_breakdown_structure_2_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.resource_breakdown_structure.resource_breakdown_structure_id"),
        nullable=True,
    )
    property_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.property.property_id"), nullable=True
    )
    cost_center_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.cost_center.cost_center_id"), nullable=True
    )
    job_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.job.job_id"), nullable=True
    )

    # Resource attributes
    standard_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    max_units: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    booking_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    client_unique_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Dates
    earliest_available_from: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    latest_available_to: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Boolean flags
    can_level: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_generic: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_team: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    internal_work: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Calendar
    base_calendar: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    resource_status: Mapped["ResourceStatus"] = relationship(
        "ResourceStatus", back_populates="resources"
    )
    resource_type: Mapped["ResourceType"] = relationship("ResourceType", back_populates="resources")
    timesheet_manager: Mapped[Optional["Resource"]] = relationship(
        "Resource",
        remote_side=[resource_id],
        foreign_keys=[timesheet_manager_id],
        backref="timesheet_reports",
    )
    nt_account: Mapped[Optional["NtAccount"]] = relationship(
        "NtAccount", back_populates="resources"
    )
    resource_cost_center: Mapped[Optional["CostCenter"]] = relationship(
        "CostCenter", foreign_keys=[resource_cost_center_id], back_populates="resource_cost_centers"
    )
    cost_center: Mapped[Optional["CostCenter"]] = relationship(
        "CostCenter", foreign_keys=[cost_center_id], back_populates="resources"
    )
    organizational_unit: Mapped[Optional["OrganizationalUnit"]] = relationship(
        "OrganizationalUnit",
        foreign_keys=[organizational_unit_id],
        back_populates="resources",
    )
    resource_organizational_unit: Mapped[Optional["OrganizationalUnit"]] = relationship(
        "OrganizationalUnit",
        foreign_keys=[resource_organizational_unit_id],
        back_populates="resource_organizational_units",
    )
    resource_breakdown_structure: Mapped[Optional["ResourceBreakdownStructure"]] = relationship(
        "ResourceBreakdownStructure",
        foreign_keys=[resource_breakdown_structure_id],
        back_populates="resources",
    )
    resource_breakdown_structure_1: Mapped[Optional["ResourceBreakdownStructure"]] = relationship(
        "ResourceBreakdownStructure",
        foreign_keys=[resource_breakdown_structure_1_id],
        back_populates="resources_1",
    )
    resource_breakdown_structure_2: Mapped[Optional["ResourceBreakdownStructure"]] = relationship(
        "ResourceBreakdownStructure",
        foreign_keys=[resource_breakdown_structure_2_id],
        back_populates="resources_2",
    )
    property: Mapped[Optional["Property"]] = relationship("Property", back_populates="resources")
    job: Mapped[Optional["Job"]] = relationship("Job", back_populates="resources")

    # Project relationships (various roles)
    authored_projects: Mapped[List["Project"]] = relationship(
        "Project", foreign_keys="Project.author_id", back_populates="author"
    )
    owned_projects: Mapped[List["Project"]] = relationship(
        "Project", foreign_keys="Project.owner_id", back_populates="owner"
    )
    program_managed_projects: Mapped[List["Project"]] = relationship(
        "Project", foreign_keys="Project.program_manager_id", back_populates="program_manager"
    )
    project_managed_projects: Mapped[List["Project"]] = relationship(
        "Project", foreign_keys="Project.project_manager_id", back_populates="project_manager"
    )

    # Task relationships
    managed_tasks: Mapped[List["Task"]] = relationship(
        "Task", foreign_keys="Task.manager_id", back_populates="manager"
    )

    # Assignments
    assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", foreign_keys="Assignment.resource_id", back_populates="resource"
    )
    owned_assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", foreign_keys="Assignment.owner_id", back_populates="owner"
    )
    managed_assignments: Mapped[List["Assignment"]] = relationship(
        "Assignment", foreign_keys="Assignment.manager_id", back_populates="manager"
    )

    def __repr__(self) -> str:
        return f"<Resource(id={self.resource_id}, name='{self.name}', type_id={self.resource_type_id})>"


class Assignment(A2RPBase, TimestampMixin, RevisionMixin):
    """Assignment of a resource to a task."""

    __tablename__ = "assignment"

    # Primary key
    assignment_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic fields
    unique_id: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Foreign keys
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("a2rp.task.task_id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=False
    )
    owner_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource.resource_id"), nullable=True
    )
    resource_type_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.resource_type.resource_type_id"), nullable=True
    )
    imputation_ce_a_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.imputation.imputation_id"), nullable=True
    )
    verify_work_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.work_breakdown_structure.work_breakdown_structure_id"),
        nullable=True,
    )
    element_work_breakdown_structure_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("a2rp.work_breakdown_structure.work_breakdown_structure_id"),
        nullable=True,
    )
    organizational_unit_manager_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.organizational_unit.organizational_unit_id"), nullable=True
    )
    executor_cost_center_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("a2rp.cost_center.cost_center_id"), nullable=True
    )

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Cost fields
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    cost_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Work fields
    work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    material_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    material_actual_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    work_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    percent_work_completed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Other fields
    delay: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    start_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    end_variance: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    acwp: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    bcwp: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    bcws: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cv: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    sv: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    vac: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    is_over_allocated: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    peak_units: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    activity_with_processing_order: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    internal_work: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    wp_status_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="assignments")
    resource: Mapped["Resource"] = relationship(
        "Resource", foreign_keys=[resource_id], back_populates="assignments"
    )
    owner: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[owner_id], back_populates="owned_assignments"
    )
    manager: Mapped[Optional["Resource"]] = relationship(
        "Resource", foreign_keys=[manager_id], back_populates="managed_assignments"
    )
    imputation: Mapped[Optional["Imputation"]] = relationship(
        "Imputation", back_populates="assignments"
    )
    organizational_unit_manager: Mapped[Optional["OrganizationalUnit"]] = relationship(
        "OrganizationalUnit", back_populates="assignments"
    )

    def __repr__(self) -> str:
        return f"<Assignment(id={self.assignment_id}, task_id={self.task_id}, resource_id={self.resource_id})>"


class AssignmentByMonth(A2RPBase):
    """Monthly aggregation of assignment data."""

    __tablename__ = "assignment_by_month"

    # Primary key
    assignment_by_month_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign keys
    month: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    assignment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.assignment.assignment_id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("a2rp.project.project_id"), nullable=False
    )
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("a2rp.task.task_id"), nullable=False)

    # Cost fields
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    overtime_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_overtime_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_overtime_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    budget_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    # Work fields
    work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    overtime_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_overtime_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    material_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    material_actual_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_overtime_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    actual_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    remaining_regular_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    budget_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    budget_material_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    resource_plan_work: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)

    def __repr__(self) -> str:
        return f"<AssignmentByMonth(id={self.assignment_by_month_id}, month={self.month})>"
