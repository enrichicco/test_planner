"""
Scheduling service for managing schedules and assignments.
"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..config import settings
from ..models import (
    Assignment,
    ExceptionType,
    Person,
    Resource,
    Schedule,
    ScheduleException,
    ScheduleStatus,
    Task,
    TaskStatus,
)
from ..scheduler import SchedulerEngine


class SchedulingService:
    """Service for creating and managing schedules."""

    def __init__(self, db: Session) -> None:
        """
        Initialize the scheduling service.

        Args:
            db: Database session
        """
        self.db = db
        self.engine = SchedulerEngine(
            solver=settings.default_solver,
            time_limit=settings.solver_time_limit,
        )

    def create_schedule(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        task_ids: Optional[List[int]] = None,
        team_id: Optional[int] = None,
    ) -> Schedule:
        """
        Create a new schedule.

        Args:
            name: Name of the schedule
            start_date: Start date for scheduling
            end_date: End date for scheduling
            task_ids: Optional list of specific task IDs to schedule
            team_id: Optional team ID to filter tasks

        Returns:
            Created schedule with assignments

        Raises:
            ValueError: If no tasks available for scheduling
        """
        # Fetch tasks to schedule
        query = self.db.query(Task).filter(Task.status == TaskStatus.PENDING)

        if task_ids:
            query = query.filter(Task.id.in_(task_ids))
        elif team_id:
            query = query.filter(Task.team_id == team_id)

        tasks = query.all()

        if not tasks:
            raise ValueError("No tasks available for scheduling")

        # Fetch available people
        people_query = self.db.query(Person).filter(Person.is_available)
        if team_id:
            people_query = people_query.filter(Person.team_id == team_id)
        people = people_query.all()

        if not people:
            raise ValueError("No people available for scheduling")

        # Fetch available resources
        resources = self.db.query(Resource).filter(Resource.is_available).all()

        # Create schedule using the engine
        schedule, assignments, exceptions = self.engine.create_schedule(
            tasks=tasks,
            people=people,
            resources=resources,
            start_date=start_date,
            end_date=end_date,
            schedule_name=name,
        )

        # Save schedule to database
        self.db.add(schedule)
        self.db.flush()  # Get the schedule ID

        # Save assignments
        for assignment in assignments:
            self.db.add(assignment)

            # Update task status
            task = self.db.query(Task).filter(Task.id == assignment.task_id).first()
            if task:
                task.status = TaskStatus.SCHEDULED
                task.schedule_id = schedule.id

        # Save exceptions
        for exc_data in exceptions:
            exception = ScheduleException(
                schedule_id=schedule.id,
                exception_type=ExceptionType[exc_data["type"]],
                severity=exc_data["severity"],
                message=exc_data["message"],
                task_id=exc_data.get("task_id"),
            )
            self.db.add(exception)

        self.db.commit()
        self.db.refresh(schedule)

        return schedule

    def reschedule(
        self,
        schedule_id: int,
        exclude_task_ids: Optional[List[int]] = None,
    ) -> Schedule:
        """
        Reschedule an existing schedule.

        Args:
            schedule_id: ID of the schedule to reschedule
            exclude_task_ids: Optional list of task IDs to exclude from rescheduling

        Returns:
            Updated schedule

        Raises:
            ValueError: If schedule not found
        """
        schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError(f"Schedule {schedule_id} not found")

        # Get tasks from the schedule
        task_query = self.db.query(Task).filter(Task.schedule_id == schedule_id)
        if exclude_task_ids:
            task_query = task_query.filter(~Task.id.in_(exclude_task_ids))

        tasks = task_query.all()

        # Delete existing assignments for tasks being rescheduled
        task_ids_to_reschedule = [t.id for t in tasks]
        self.db.query(Assignment).filter(Assignment.task_id.in_(task_ids_to_reschedule)).delete(
            synchronize_session=False
        )

        # Fetch available people
        people = self.db.query(Person).filter(Person.is_available).all()
        resources = self.db.query(Resource).filter(Resource.is_available).all()

        # Create new schedule
        new_schedule, assignments, exceptions = self.engine.create_schedule(
            tasks=tasks,
            people=people,
            resources=resources,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            schedule_name=f"{schedule.name} (Rescheduled)",
        )

        # Update schedule
        schedule.objective_value = new_schedule.objective_value
        schedule.solver_used = new_schedule.solver_used
        schedule.solve_time = new_schedule.solve_time
        schedule.optimization_metadata = new_schedule.optimization_metadata
        schedule.updated_at = datetime.now(timezone.utc)

        # Save new assignments
        for assignment in assignments:
            self.db.add(assignment)

        # Mark old exceptions as resolved
        self.db.query(ScheduleException).filter(
            and_(
                ScheduleException.schedule_id == schedule_id,
                ~ScheduleException.resolved,
            )
        ).update({"resolved": True, "resolved_at": datetime.now(timezone.utc)})

        # Save new exceptions
        for exc_data in exceptions:
            exception = ScheduleException(
                schedule_id=schedule.id,
                exception_type=ExceptionType[exc_data["type"]],
                severity=exc_data["severity"],
                message=exc_data["message"],
                task_id=exc_data.get("task_id"),
            )
            self.db.add(exception)

        self.db.commit()
        self.db.refresh(schedule)

        return schedule

    def handle_exception(
        self,
        exception_id: int,
        resolution: str,
        reschedule: bool = True,
    ) -> ScheduleException:
        """
        Handle a schedule exception.

        Args:
            exception_id: ID of the exception
            resolution: Resolution notes
            reschedule: Whether to trigger rescheduling

        Returns:
            Updated exception

        Raises:
            ValueError: If exception not found
        """
        exception = (
            self.db.query(ScheduleException).filter(ScheduleException.id == exception_id).first()
        )
        if not exception:
            raise ValueError(f"Exception {exception_id} not found")

        exception.resolved = True
        exception.resolved_at = datetime.now(timezone.utc)
        exception.resolution_notes = resolution

        self.db.commit()

        # Optionally trigger rescheduling
        if reschedule:
            self.reschedule(exception.schedule_id)

        return exception

    def get_schedule(self, schedule_id: int) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self.db.query(Schedule).filter(Schedule.id == schedule_id).first()

    def list_schedules(
        self,
        status: Optional[ScheduleStatus] = None,
        limit: int = 100,
    ) -> List[Schedule]:
        """
        List schedules.

        Args:
            status: Optional status filter
            limit: Maximum number of schedules to return

        Returns:
            List of schedules
        """
        query = self.db.query(Schedule).order_by(Schedule.created_at.desc())
        if status:
            query = query.filter(Schedule.status == status)
        return query.limit(limit).all()

    def get_assignments(self, schedule_id: int) -> List[Assignment]:
        """Get all assignments for a schedule."""
        return self.db.query(Assignment).join(Task).filter(Task.schedule_id == schedule_id).all()

    def get_exceptions(
        self,
        schedule_id: int,
        resolved: Optional[bool] = None,
    ) -> List[ScheduleException]:
        """
        Get exceptions for a schedule.

        Args:
            schedule_id: Schedule ID
            resolved: Optional filter by resolved status

        Returns:
            List of exceptions
        """
        query = self.db.query(ScheduleException).filter(
            ScheduleException.schedule_id == schedule_id
        )
        if resolved is not None:
            query = query.filter(ScheduleException.resolved == resolved)
        return query.all()
