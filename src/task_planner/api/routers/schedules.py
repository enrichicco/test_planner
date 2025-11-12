"""
Schedule API endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...models import ScheduleStatus as ScheduleStatusModel
from ...models.database import get_db
from ...services import SchedulingService
from ..schemas import (
    AssignmentResponse,
    ExceptionResolve,
    ExceptionResponse,
    ScheduleCreate,
    ScheduleResponse,
)

router = APIRouter()


@router.post("/", response_model=ScheduleResponse, status_code=201)  # type: ignore[misc]
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)) -> ScheduleResponse:
    """Create a new schedule."""
    service = SchedulingService(db)
    try:
        db_schedule = service.create_schedule(
            name=schedule.name,
            start_date=schedule.start_date,
            end_date=schedule.end_date,
            task_ids=schedule.task_ids,
            team_id=schedule.team_id,
        )

        return ScheduleResponse.model_validate(db_schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{schedule_id}", response_model=ScheduleResponse)  # type: ignore[misc]
def get_schedule(schedule_id: int, db: Session = Depends(get_db)) -> ScheduleResponse:
    """Get a schedule by ID."""
    service = SchedulingService(db)
    schedule = service.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return ScheduleResponse.model_validate(schedule)


@router.get("/", response_model=List[ScheduleResponse])  # type: ignore[misc]
def list_schedules(
    status: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[ScheduleResponse]:
    """List all schedules."""
    service = SchedulingService(db)
    status_filter = ScheduleStatusModel[status.upper()] if status else None
    schedules = service.list_schedules(status=status_filter, limit=limit)

    return [ScheduleResponse.model_validate(s) for s in schedules]


@router.post("/{schedule_id}/reschedule", response_model=ScheduleResponse)  # type: ignore[misc]
def reschedule(
    schedule_id: int,
    exclude_task_ids: Optional[List[int]] = None,
    db: Session = Depends(get_db),
) -> ScheduleResponse:
    """Reschedule an existing schedule."""
    service = SchedulingService(db)
    try:
        rescheduled = service.reschedule(schedule_id=schedule_id, exclude_task_ids=exclude_task_ids)

        return ScheduleResponse.model_validate(rescheduled)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{schedule_id}/assignments", response_model=List[AssignmentResponse])  # type: ignore[misc]
def get_assignments(schedule_id: int, db: Session = Depends(get_db)) -> List[AssignmentResponse]:
    """Get all assignments for a schedule."""
    service = SchedulingService(db)
    assignments = service.get_assignments(schedule_id)

    return [AssignmentResponse.model_validate(a) for a in assignments]


@router.get("/{schedule_id}/exceptions", response_model=List[ExceptionResponse])  # type: ignore[misc]
def get_exceptions(
    schedule_id: int,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db),
) -> List[ExceptionResponse]:
    """Get all exceptions for a schedule."""
    service = SchedulingService(db)
    exceptions = service.get_exceptions(schedule_id, resolved=resolved)

    return [ExceptionResponse.model_validate(e) for e in exceptions]


@router.post("/exceptions/{exception_id}/resolve", response_model=ExceptionResponse)  # type: ignore[misc]
def resolve_exception(
    exception_id: int,
    resolution: ExceptionResolve,
    db: Session = Depends(get_db),
) -> ExceptionResponse:
    """Resolve a schedule exception."""
    service = SchedulingService(db)
    try:
        exception = service.handle_exception(
            exception_id=exception_id,
            resolution=resolution.resolution_notes,
            reschedule=resolution.reschedule,
        )

        return ExceptionResponse.model_validate(exception)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
