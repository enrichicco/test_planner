"""
Pydantic schemas for a2rp models API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Project Schemas
class ProjectBase(BaseModel):
    """Base schema for Project."""

    name: str
    description: Optional[str] = None
    project_type_id: int
    project_status_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = None
    description: Optional[str] = None
    project_status_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""

    project_id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Task Schemas
class TaskBase(BaseModel):
    """Base schema for Task."""

    name: str
    description: Optional[str] = None
    project_id: int
    task_status_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    work: Optional[float] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    name: Optional[str] = None
    description: Optional[str] = None
    task_status_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    work: Optional[float] = None


class TaskResponse(TaskBase):
    """Schema for task response."""

    task_id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Resource Schemas
class ResourceBase(BaseModel):
    """Base schema for Resource."""

    name: str
    email: Optional[str] = None
    resource_type_id: int
    resource_status_id: int


class ResourceCreate(ResourceBase):
    """Schema for creating a resource."""

    pass


class ResourceUpdate(BaseModel):
    """Schema for updating a resource."""

    name: Optional[str] = None
    email: Optional[str] = None
    resource_status_id: Optional[int] = None


class ResourceResponse(ResourceBase):
    """Schema for resource response."""

    resource_id: int
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Assignment Schemas
class AssignmentBase(BaseModel):
    """Base schema for Assignment."""

    task_id: int
    resource_id: int
    work: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AssignmentCreate(AssignmentBase):
    """Schema for creating an assignment."""

    pass


class AssignmentUpdate(BaseModel):
    """Schema for updating an assignment."""

    work: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    actual_work: Optional[float] = None


class AssignmentResponse(AssignmentBase):
    """Schema for assignment response."""

    assignment_id: int
    actual_work: Optional[float] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
