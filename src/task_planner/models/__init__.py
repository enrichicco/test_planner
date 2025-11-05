"""Database models for task planner service."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


# Association tables
team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
    Column("person_id", Integer, ForeignKey("people.id"), primary_key=True),
)

person_skills = Table(
    "person_skills",
    Base.metadata,
    Column("person_id", Integer, ForeignKey("people.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id"), primary_key=True),
)


class TaskStatus(enum.Enum):
    """Task status enumeration."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ResourceType(enum.Enum):
    """Resource type enumeration."""

    EQUIPMENT = "equipment"
    MATERIAL = "material"
    SKILL = "skill"
    FACILITY = "facility"


class Team(Base):
    """Team model representing a group of people."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    members: Mapped[List["Person"]] = relationship(secondary=team_members, back_populates="teams")
    tasks: Mapped[List["Task"]] = relationship(back_populates="team")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"


class Person(Base):
    """Person model representing an individual."""

    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(50))
    availability_hours_per_day: Mapped[float] = mapped_column(Float, default=8.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    teams: Mapped[List["Team"]] = relationship(secondary=team_members, back_populates="members")
    skills: Mapped[List["Resource"]] = relationship(
        secondary=person_skills, back_populates="skilled_people"
    )
    assigned_tasks: Mapped[List["Task"]] = relationship(back_populates="assigned_person")

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', email='{self.email}')>"


class Resource(Base):
    """Resource model representing equipment, materials, skills, etc."""

    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[ResourceType] = mapped_column(Enum(ResourceType), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    capacity: Mapped[float] = mapped_column(Float, default=1.0)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    skilled_people: Mapped[List["Person"]] = relationship(
        secondary=person_skills, back_populates="skills"
    )
    task_requirements: Mapped[List["TaskResource"]] = relationship(back_populates="resource")

    def __repr__(self):
        return f"<Resource(id={self.id}, name='{self.name}', type='{self.type.value}')>"


class Task(Base):
    """Task model representing work to be done."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1-10 scale
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False)
    actual_hours: Mapped[Optional[float]] = mapped_column(Float)

    # Scheduling
    earliest_start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    latest_end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scheduled_start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scheduled_end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    actual_start: Mapped[Optional[datetime]] = mapped_column(DateTime)
    actual_end: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Foreign keys
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"))
    assigned_person_id: Mapped[Optional[int]] = mapped_column(ForeignKey("people.id"))
    parent_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    team: Mapped[Optional["Team"]] = relationship(back_populates="tasks")
    assigned_person: Mapped[Optional["Person"]] = relationship(back_populates="assigned_tasks")
    parent_task: Mapped[Optional["Task"]] = relationship(
        "Task", remote_side=[id], back_populates="subtasks"
    )
    subtasks: Mapped[List["Task"]] = relationship("Task", back_populates="parent_task")
    resource_requirements: Mapped[List["TaskResource"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )
    dependencies: Mapped[List["TaskDependency"]] = relationship(
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    dependent_on: Mapped[List["TaskDependency"]] = relationship(
        foreign_keys="TaskDependency.depends_on_task_id",
        back_populates="depends_on_task",
    )
    exceptions: Mapped[List["TaskException"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status.value}')>"


class TaskResource(Base):
    """Association between tasks and required resources."""

    __tablename__ = "task_resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"), nullable=False)
    quantity_required: Mapped[float] = mapped_column(Float, default=1.0)

    # Relationships
    task: Mapped["Task"] = relationship(back_populates="resource_requirements")
    resource: Mapped["Resource"] = relationship(back_populates="task_requirements")

    def __repr__(self):
        return f"<TaskResource(task_id={self.task_id}, resource_id={self.resource_id})>"


class TaskDependency(Base):
    """Task dependency relationships."""

    __tablename__ = "task_dependencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    depends_on_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    dependency_type: Mapped[str] = mapped_column(
        String(20), default="finish_to_start"
    )  # finish_to_start, start_to_start, etc.

    # Relationships
    task: Mapped["Task"] = relationship(foreign_keys=[task_id], back_populates="dependencies")
    depends_on_task: Mapped["Task"] = relationship(
        foreign_keys=[depends_on_task_id], back_populates="dependent_on"
    )

    def __repr__(self):
        return f"<TaskDependency(task_id={self.task_id}, depends_on={self.depends_on_task_id})>"


class TaskException(Base):
    """Task exceptions for tracking issues and rescheduling."""

    __tablename__ = "task_exceptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    exception_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    task: Mapped["Task"] = relationship(back_populates="exceptions")

    def __repr__(self):
        return (
            f"<TaskException(id={self.id}, task_id={self.task_id}, type='{self.exception_type}')>"
        )


class Schedule(Base):
    """Schedule model representing a planned schedule."""

    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Schedule(id={self.id}, name='{self.name}')>"
