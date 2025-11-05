"""Tests for the task planner service."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from task_planner.models import Base, ResourceType, TaskStatus
from task_planner.services import (
    TeamService,
    PersonService,
    ResourceService,
    TaskService,
    PlanningService,
)
from task_planner.reports import ReportGenerator


@pytest.fixture
def db_session():
    """Create a test database session."""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def team_service(db_session):
    """Create a team service instance."""
    return TeamService(db_session)


@pytest.fixture
def person_service(db_session):
    """Create a person service instance."""
    return PersonService(db_session)


@pytest.fixture
def resource_service(db_session):
    """Create a resource service instance."""
    return ResourceService(db_session)


@pytest.fixture
def task_service(db_session):
    """Create a task service instance."""
    return TaskService(db_session)


@pytest.fixture
def planning_service(db_session):
    """Create a planning service instance."""
    return PlanningService(db_session)


@pytest.fixture
def report_gen(db_session):
    """Create a report generator instance."""
    return ReportGenerator(db_session)


class TestTeamService:
    """Tests for TeamService."""

    def test_create_team(self, team_service):
        """Test creating a team."""
        team = team_service.create_team("Dev Team", "Development team")
        assert team.id is not None
        assert team.name == "Dev Team"
        assert team.description == "Development team"

    def test_get_team(self, team_service):
        """Test getting a team by ID."""
        team = team_service.create_team("Dev Team")
        retrieved = team_service.get_team(team.id)
        assert retrieved.id == team.id
        assert retrieved.name == team.name

    def test_add_member(self, team_service, person_service):
        """Test adding a member to a team."""
        team = team_service.create_team("Dev Team")
        person = person_service.create_person("Alice", "alice@example.com")

        team_service.add_member(team.id, person.id)

        retrieved_team = team_service.get_team(team.id)
        assert len(retrieved_team.members) == 1
        assert retrieved_team.members[0].id == person.id


class TestPersonService:
    """Tests for PersonService."""

    def test_create_person(self, person_service):
        """Test creating a person."""
        person = person_service.create_person(
            "Alice Johnson",
            "alice@example.com",
            role="Developer",
            availability_hours_per_day=8.0,
        )
        assert person.id is not None
        assert person.name == "Alice Johnson"
        assert person.email == "alice@example.com"
        assert person.role == "Developer"
        assert person.is_active is True

    def test_get_person(self, person_service):
        """Test getting a person by ID."""
        person = person_service.create_person("Bob", "bob@example.com")
        retrieved = person_service.get_person(person.id)
        assert retrieved.id == person.id
        assert retrieved.name == person.name

    def test_add_skill(self, person_service, resource_service):
        """Test adding a skill to a person."""
        person = person_service.create_person("Alice", "alice@example.com")
        skill = resource_service.create_resource("Python", ResourceType.SKILL, "Python programming")

        person_service.add_skill(person.id, skill.id)

        retrieved_person = person_service.get_person(person.id)
        assert len(retrieved_person.skills) == 1
        assert retrieved_person.skills[0].id == skill.id


class TestResourceService:
    """Tests for ResourceService."""

    def test_create_resource(self, resource_service):
        """Test creating a resource."""
        resource = resource_service.create_resource(
            "Python",
            ResourceType.SKILL,
            "Python programming skill",
            capacity=5.0,
        )
        assert resource.id is not None
        assert resource.name == "Python"
        assert resource.type == ResourceType.SKILL
        assert resource.capacity == 5.0
        assert resource.available is True

    def test_get_resource(self, resource_service):
        """Test getting a resource by ID."""
        resource = resource_service.create_resource("Python", ResourceType.SKILL)
        retrieved = resource_service.get_resource(resource.id)
        assert retrieved.id == resource.id
        assert retrieved.name == resource.name


class TestTaskService:
    """Tests for TaskService."""

    def test_create_task(self, task_service, team_service, person_service):
        """Test creating a task."""
        team = team_service.create_team("Dev Team")
        person = person_service.create_person("Alice", "alice@example.com")

        task = task_service.create_task(
            name="Build feature",
            estimated_hours=16.0,
            description="Build a new feature",
            priority=10,
            team_id=team.id,
            assigned_person_id=person.id,
        )

        assert task.id is not None
        assert task.name == "Build feature"
        assert task.estimated_hours == 16.0
        assert task.status == TaskStatus.PENDING
        assert task.team_id == team.id
        assert task.assigned_person_id == person.id

    def test_add_dependency(self, task_service):
        """Test adding a dependency between tasks."""
        task1 = task_service.create_task("Task 1", 8.0)
        task2 = task_service.create_task("Task 2", 8.0)

        task_service.add_dependency(task2.id, task1.id)

        retrieved_task2 = task_service.get_task(task2.id)
        assert len(retrieved_task2.dependencies) == 1
        assert retrieved_task2.dependencies[0].depends_on_task_id == task1.id

    def test_record_exception(self, task_service):
        """Test recording a task exception."""
        task = task_service.create_task("Task 1", 8.0)

        exception = task_service.record_exception(
            task.id,
            "resource_unavailable",
            "Resource is not available",
        )

        assert exception.id is not None
        assert exception.task_id == task.id
        assert exception.exception_type == "resource_unavailable"
        assert exception.resolved is False

    def test_update_task_status(self, task_service):
        """Test updating task status."""
        task = task_service.create_task("Task 1", 8.0)

        updated_task = task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert updated_task.status == TaskStatus.IN_PROGRESS
        assert updated_task.actual_start is not None


class TestPlanningService:
    """Tests for PlanningService."""

    def test_create_schedule_empty(self, planning_service):
        """Test creating a schedule with no tasks."""
        schedule = planning_service.create_schedule([])
        assert schedule == {}

    def test_create_schedule_single_task(self, planning_service, task_service, person_service):
        """Test creating a schedule with a single task."""
        person = person_service.create_person("Alice", "alice@example.com")
        task = task_service.create_task(
            "Task 1",
            8.0,
            assigned_person_id=person.id,
        )

        start_date = datetime.now()
        schedule = planning_service.create_schedule([task], start_date)

        assert task.id in schedule
        start, end = schedule[task.id]
        assert start >= start_date
        assert end > start


class TestReportGenerator:
    """Tests for ReportGenerator."""

    def test_generate_task_summary(self, report_gen, task_service):
        """Test generating a task summary report."""
        task_service.create_task("Task 1", 8.0)
        task_service.create_task("Task 2", 16.0)

        summary = report_gen.generate_task_summary()

        assert summary["total_tasks"] == 2
        assert summary["total_estimated_hours"] == 24.0
        assert "status_counts" in summary

    def test_generate_person_workload_report(self, report_gen, person_service, task_service):
        """Test generating a person workload report."""
        person = person_service.create_person("Alice", "alice@example.com")
        task_service.create_task("Task 1", 8.0, assigned_person_id=person.id)
        task_service.create_task("Task 2", 16.0, assigned_person_id=person.id)

        report = report_gen.generate_person_workload_report()

        assert len(report) == 1
        assert report[0]["person_id"] == person.id
        assert report[0]["active_tasks"] == 2
        assert report[0]["total_estimated_hours"] == 24.0

    def test_generate_resource_utilization_report(self, report_gen, resource_service):
        """Test generating a resource utilization report."""
        resource_service.create_resource("Python", ResourceType.SKILL)
        resource_service.create_resource("Selenium", ResourceType.EQUIPMENT)

        report = report_gen.generate_resource_utilization_report()

        assert len(report) == 2
