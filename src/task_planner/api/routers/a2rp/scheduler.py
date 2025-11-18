"""
Scheduler API routes for generating schedules using PyJobShop.
"""

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....models.a2rp.database import get_db
from ....scheduler.engine import SchedulerEngine
from ....services.a2rp import (
    AssignmentService,
    ResourceService,
    TaskService,
)

router = APIRouter()


class ScheduleRequest(BaseModel):
    """Request model for schedule generation."""

    start_date: str  # ISO format date
    end_date: str  # ISO format date
    solver: str = "ortools"
    time_limit: int = 60


class ScheduleResponse(BaseModel):
    """Response model for schedule generation."""

    assignments: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    exceptions: List[Dict[str, Any]]


@router.post("/generate", response_model=ScheduleResponse)
async def generate_schedule(
    request: ScheduleRequest,
    db: Session = Depends(get_db),
) -> ScheduleResponse:
    """
    Generate an optimized schedule using PyJobShop.

    Args:
        request: Schedule generation parameters
        db: Database session

    Returns:
        Schedule with assignments, metadata, and exceptions
    """
    # Parse dates
    start_date = datetime.fromisoformat(request.start_date)
    end_date = datetime.fromisoformat(request.end_date)

    # Get services
    task_service = TaskService(db)
    resource_service = ResourceService(db)
    assignment_service = AssignmentService(db)

    # Fetch all tasks and resources
    tasks = task_service.get_all_tasks()
    resources = resource_service.get_all_resources()
    existing_assignments = assignment_service.get_all_assignments()

    # Create scheduler engine
    engine = SchedulerEngine(
        solver=request.solver,
        time_limit=request.time_limit,
    )

    # Generate schedule
    new_assignments, metadata, exceptions = engine.create_schedule(
        tasks=tasks,
        resources=resources,
        assignments=existing_assignments,
        start_date=start_date,
        end_date=end_date,
    )

    # Convert assignments to dictionaries
    assignment_dicts = [
        {
            "assignment_id": a.assignment_id if hasattr(a, "assignment_id") else None,
            "task_id": a.task_id,
            "resource_id": a.resource_id,
            "start_date": a.start_date.isoformat() if a.start_date else None,
            "end_date": a.end_date.isoformat() if a.end_date else None,
            "allocated_hours": float(a.allocated_hours) if a.allocated_hours else None,
            "status": a.status if hasattr(a, "status") else "scheduled",
        }
        for a in new_assignments
    ]

    return ScheduleResponse(
        assignments=assignment_dicts,
        metadata=metadata,
        exceptions=exceptions,
    )
