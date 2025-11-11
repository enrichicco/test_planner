"""
Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


# Enums
class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TaskPriorityEnum(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ScheduleStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Team schemas
class TeamCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TeamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Person schemas
class PersonCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: Optional[str] = None
    team_id: Optional[int] = None
    skills: Optional[Dict[str, Any]] = None
    max_concurrent_tasks: int = Field(default=5, ge=1)


class PersonUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    team_id: Optional[int] = None
    skills: Optional[Dict[str, Any]] = None
    is_available: Optional[bool] = None
    max_concurrent_tasks: Optional[int] = Field(None, ge=1)


class PersonResponse(BaseModel):
    id: int
    name: str
    email: str
    role: Optional[str]
    team_id: Optional[int]
    skills: Optional[Dict[str, Any]]
    is_available: bool
    max_concurrent_tasks: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Resource schemas
class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    resource_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    capacity: float = Field(default=1.0, gt=0)
    is_renewable: bool = True
    properties: Optional[Dict[str, Any]] = None


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    resource_type: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    capacity: Optional[float] = Field(None, gt=0)
    is_renewable: Optional[bool] = None
    is_available: Optional[bool] = None
    properties: Optional[Dict[str, Any]] = None


class ResourceResponse(BaseModel):
    id: int
    name: str
    resource_type: str
    description: Optional[str]
    capacity: float
    is_renewable: bool
    is_available: bool
    properties: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Task schemas
class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    duration: float = Field(..., gt=0)
    description: Optional[str] = None
    team_id: Optional[int] = None
    priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    earliest_start: Optional[datetime] = None
    deadline: Optional[datetime] = None
    due_date: Optional[datetime] = None
    required_skills: Optional[Dict[str, Any]] = None
    required_resources: Optional[Dict[str, Any]] = None
    predecessor_id: Optional[int] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    duration: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    status: Optional[TaskStatusEnum] = None
    priority: Optional[TaskPriorityEnum] = None
    earliest_start: Optional[datetime] = None
    deadline: Optional[datetime] = None
    due_date: Optional[datetime] = None
    required_skills: Optional[Dict[str, Any]] = None
    required_resources: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    duration: float
    status: str
    priority: int
    earliest_start: Optional[datetime]
    deadline: Optional[datetime]
    due_date: Optional[datetime]
    team_id: Optional[int]
    schedule_id: Optional[int]
    predecessor_id: Optional[int]
    required_skills: Optional[Dict[str, Any]]
    required_resources: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Schedule schemas
class ScheduleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    start_date: datetime
    end_date: datetime
    task_ids: Optional[List[int]] = None
    team_id: Optional[int] = None


class ScheduleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    start_date: datetime
    end_date: datetime
    objective_value: Optional[float]
    solver_used: Optional[str]
    solve_time: Optional[float]
    optimization_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Assignment schemas
class AssignmentResponse(BaseModel):
    id: int
    task_id: int
    person_id: Optional[int]
    resource_id: Optional[int]
    scheduled_start: Optional[datetime]
    scheduled_end: Optional[datetime]
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    allocated_capacity: float
    created_at: datetime

    class Config:
        from_attributes = True


# Exception schemas
class ExceptionResponse(BaseModel):
    id: int
    exception_type: str
    severity: str
    message: str
    resolved: bool
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    schedule_id: int
    task_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ExceptionResolve(BaseModel):
    resolution_notes: str
    reschedule: bool = True
