"""
Assignment API endpoints for a2rp schema.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....models.a2rp.database import get_db
from ....services.a2rp import AssignmentService
from ...schemas_a2rp import AssignmentCreate, AssignmentResponse, AssignmentUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=AssignmentResponse,
    status_code=201,
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def create_assignment(
    assignment: AssignmentCreate, db: Session = Depends(get_db)
) -> AssignmentResponse:
    """Create a new assignment."""
    try:
        service = AssignmentService(db)
        db_assignment = service.create_assignment(
            task_id=assignment.task_id,
            resource_id=assignment.resource_id,
            work=assignment.work,
            start_date=assignment.start_date,
            end_date=assignment.end_date,
        )

        return AssignmentResponse.model_validate(db_assignment)
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{assignment_id}",
    response_model=AssignmentResponse,
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)) -> AssignmentResponse:
    """Get an assignment by ID."""
    try:
        service = AssignmentService(db)
        assignment = service.get_assignment(assignment_id)

        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        return AssignmentResponse.model_validate(assignment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=List[AssignmentResponse],
    responses={
        500: {"description": "Internal Server Error"},
    },
)
def list_assignments(
    task_id: Optional[int] = None,
    resource_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[AssignmentResponse]:
    """List all assignments."""
    try:
        service = AssignmentService(db)
        assignments = service.list_assignments(
            task_id=task_id, resource_id=resource_id, limit=limit
        )

        return [AssignmentResponse.model_validate(a) for a in assignments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/{assignment_id}",
    response_model=AssignmentResponse,
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def update_assignment(
    assignment_id: int, assignment: AssignmentUpdate, db: Session = Depends(get_db)
) -> AssignmentResponse:
    """Update an assignment."""
    try:
        service = AssignmentService(db)
        updated_assignment = service.update_assignment(
            assignment_id=assignment_id,
            work=assignment.work,
            start_date=assignment.start_date,
            end_date=assignment.end_date,
            actual_work=assignment.actual_work,
        )

        if not updated_assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        return AssignmentResponse.model_validate(updated_assignment)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{assignment_id}",
    status_code=204,
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an assignment."""
    try:
        service = AssignmentService(db)
        deleted = service.delete_assignment(assignment_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Assignment not found")

        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
