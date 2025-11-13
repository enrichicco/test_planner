"""
Tests for a2rp service layer.
"""

from datetime import datetime, timedelta
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.task_planner.models.a2rp.base import A2RPBase
from src.task_planner.services.a2rp import (
    AssignmentService,
    ProjectService,
    ResourceService,
    TaskService,
)


@pytest.fixture  # type: ignore[misc]
def db_session() -> Generator[Session, Any, None]:
    """Create a test database session for a2rp schema."""
    engine = create_engine("sqlite:///:memory:")
    A2RPBase.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


def test_project_service_create(db_session: Session) -> None:
    """Test creating a project."""
    service = ProjectService(db_session)
    project = service.create_project(
        name="Test Project",
        description="A test project",
        project_type_id=1,
        project_status_id=1,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
    )
    assert project.project_id is not None
    assert project.name == "Test Project"
    assert project.description == "A test project"


def test_project_service_get(db_session: Session) -> None:
    """Test getting a project."""
    service = ProjectService(db_session)
    project = service.create_project(
        name="Test Project",
        project_type_id=1,
        project_status_id=1,
    )
    retrieved = service.get_project(project.project_id)
    assert retrieved is not None
    assert retrieved.project_id == project.project_id
    assert retrieved.name == "Test Project"


def test_resource_service_create(db_session: Session) -> None:
    """Test creating a resource."""
    service = ResourceService(db_session)
    resource = service.create_resource(
        name="Alice Johnson",
        email="alice@example.com",
        resource_type_id=1,
        resource_status_id=1,
    )
    assert resource.resource_id is not None
    assert resource.name == "Alice Johnson"
    assert resource.email == "alice@example.com"


def test_resource_service_list(db_session: Session) -> None:
    """Test listing resources."""
    service = ResourceService(db_session)
    service.create_resource(
        name="Alice", email="alice@example.com", resource_type_id=1, resource_status_id=1
    )
    service.create_resource(
        name="Bob", email="bob@example.com", resource_type_id=1, resource_status_id=1
    )
    resources = service.list_resources(limit=10)
    assert len(resources) == 2


def test_task_service_create(db_session: Session) -> None:
    """Test creating a task."""
    # First create a project
    project_service = ProjectService(db_session)
    project = project_service.create_project(
        name="Test Project", project_type_id=1, project_status_id=1
    )

    # Create task
    task_service = TaskService(db_session)
    task = task_service.create_task(
        name="Test Task",
        description="A test task",
        project_id=project.project_id,
        task_status_id=1,
        work=16.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=2),
    )
    assert task.task_id is not None
    assert task.name == "Test Task"
    assert task.work == 16.0
    assert task.project_id == project.project_id


def test_task_service_list_by_project(db_session: Session) -> None:
    """Test listing tasks by project."""
    # Create project
    project_service = ProjectService(db_session)
    project = project_service.create_project(
        name="Test Project", project_type_id=1, project_status_id=1
    )

    # Create tasks
    task_service = TaskService(db_session)
    task_service.create_task(
        name="Task 1", project_id=project.project_id, task_status_id=1
    )
    task_service.create_task(
        name="Task 2", project_id=project.project_id, task_status_id=1
    )

    tasks = task_service.list_tasks(project_id=project.project_id)
    assert len(tasks) == 2


def test_assignment_service_create(db_session: Session) -> None:
    """Test creating an assignment."""
    # Create project
    project_service = ProjectService(db_session)
    project = project_service.create_project(
        name="Test Project", project_type_id=1, project_status_id=1
    )

    # Create task
    task_service = TaskService(db_session)
    task = task_service.create_task(
        name="Test Task", project_id=project.project_id, task_status_id=1
    )

    # Create resource
    resource_service = ResourceService(db_session)
    resource = resource_service.create_resource(
        name="Alice", resource_type_id=1, resource_status_id=1
    )

    # Create assignment
    assignment_service = AssignmentService(db_session)
    assignment = assignment_service.create_assignment(
        task_id=task.task_id,
        resource_id=resource.resource_id,
        work=16.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=2),
    )

    assert assignment.assignment_id is not None
    assert assignment.task_id == task.task_id
    assert assignment.resource_id == resource.resource_id
    assert assignment.work == 16.0


def test_assignment_service_update(db_session: Session) -> None:
    """Test updating an assignment with actual work."""
    # Setup
    project_service = ProjectService(db_session)
    project = project_service.create_project(
        name="Test Project", project_type_id=1, project_status_id=1
    )

    task_service = TaskService(db_session)
    task = task_service.create_task(
        name="Test Task", project_id=project.project_id, task_status_id=1
    )

    resource_service = ResourceService(db_session)
    resource = resource_service.create_resource(
        name="Alice", resource_type_id=1, resource_status_id=1
    )

    assignment_service = AssignmentService(db_session)
    assignment = assignment_service.create_assignment(
        task_id=task.task_id, resource_id=resource.resource_id, work=16.0
    )

    # Update with actual work
    updated = assignment_service.update_assignment(
        assignment_id=assignment.assignment_id, actual_work=18.0
    )

    assert updated is not None
    assert updated.actual_work == 18.0
