"""
A2RP Schema Models Package.
Exports all models for the customer's a2rp database schema.
"""

# Base classes
from .base import A2RPBase, TimestampMixin, RevisionMixin

# Lookup/Reference tables
from .lookups import (
    ProjectStatus,
    ProjectType,
    TaskStatus,
    ResourceStatus,
    ResourceType,
    ProcessingOrderStatus,
    ProcessingOrderType,
    CostType,
    Job,
    NtAccount,
    Property,
)

# Organizational and structure tables
from .organizational import (
    CostCenter,
    CostItem,
    Customer,
    Imputation,
    OrganizationalUnit,
    TechnicalFeature,
    WorkBreakdownStructure,
    ResourceBreakdownStructure,
)

# Core entities
from .core import (
    Project,
    Task,
    Resource,
    Assignment,
    AssignmentByMonth,
)

# Supporting tables
from .supporting import (
    ProcessingOrder,
    HistoricalProjectSummary,
    HistoricalProjectSummaryResource,
    ProjectToPlan,
    ProjectToPlanOrganizationalUnit,
    TaskToPlan,
    TaskToPlanOrganizationalUnit,
)

__all__ = [
    # Base
    "A2RPBase",
    "TimestampMixin",
    "RevisionMixin",
    # Lookups
    "ProjectStatus",
    "ProjectType",
    "TaskStatus",
    "ResourceStatus",
    "ResourceType",
    "ProcessingOrderStatus",
    "ProcessingOrderType",
    "CostType",
    "Job",
    "NtAccount",
    "Property",
    # Organizational
    "CostCenter",
    "CostItem",
    "Customer",
    "Imputation",
    "OrganizationalUnit",
    "TechnicalFeature",
    "WorkBreakdownStructure",
    "ResourceBreakdownStructure",
    # Core
    "Project",
    "Task",
    "Resource",
    "Assignment",
    "AssignmentByMonth",
    # Supporting
    "ProcessingOrder",
    "HistoricalProjectSummary",
    "HistoricalProjectSummaryResource",
    "ProjectToPlan",
    "ProjectToPlanOrganizationalUnit",
    "TaskToPlan",
    "TaskToPlanOrganizationalUnit",
]
