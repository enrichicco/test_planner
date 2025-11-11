"""
Tests for service layer.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.task_planner.models import Base, TaskStatus, TaskPriority
from src.task_planner.services import (
    TeamService,
    PersonService,
    ResourceService,
    TaskService,
    SchedulingService,
)


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_team_service_create(db_session):
    """Test creating a team."""
    service = TeamService(db_session)
    team = service.create_team(name="Test Team", description="A test team")
    assert team.id is not None
    assert team.name == "Test Team"
    assert team.is_active is True


def test_person_service_create(db_session):
    """Test creating a person."""
    # First create a team
    team_service = TeamService(db_session)
    team = team_service.create_team(name="Test Team")

    # Create person
    person_service = PersonService(db_session)
    person = person_service.create_person(
        name="John Doe",
        email="john@example.com",
        role="Developer",
        team_id=team.id,
        skills={"python": 5},
    )
    assert person.id is not None
    assert person.name == "John Doe"
    assert person.team_id == team.id


def test_resource_service_create(db_session):
    """Test creating a resource."""
    service = ResourceService(db_session)
    resource = service.create_resource(
        name="Conference Room A",
        resource_type="room",
        capacity=10.0,
    )
    assert resource.id is not None
    assert resource.name == "Conference Room A"
    assert resource.capacity == 10.0


def test_task_service_create(db_session):
    """Test creating a task."""
    # Create team
    team_service = TeamService(db_session)
    team = team_service.create_team(name="Test Team")

    # Create task
    task_service = TaskService(db_session)
    task = task_service.create_task(
        name="Test Task",
        duration=8.0,
        description="A test task",
        team_id=team.id,
        priority=TaskPriority.HIGH,
    )
    assert task.id is not None
    assert task.name == "Test Task"
    assert task.duration == 8.0
    assert task.status == TaskStatus.PENDING


def test_scheduling_service_create_schedule(db_session):
    """Test creating a schedule."""
    # Setup: Create team, person, and task
    team_service = TeamService(db_session)
    team = team_service.create_team(name="Test Team")

    person_service = PersonService(db_session)
    person = person_service.create_person(
        name="John Doe",
        email="john@example.com",
        team_id=team.id,
    )

    task_service = TaskService(db_session)
    task = task_service.create_task(
        name="Test Task",
        duration=8.0,
        team_id=team.id,
    )

    # Create schedule
    scheduling_service = SchedulingService(db_session)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)

    schedule = scheduling_service.create_schedule(
        name="Test Schedule",
        start_date=start_date,
        end_date=end_date,
        team_id=team.id,
    )

    assert schedule.id is not None
    assert schedule.name == "Test Schedule"
    # Note: Actual scheduling may fail without PyJobShop properly configured
