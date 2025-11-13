"""
Project API endpoints for a2rp schema.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....models.a2rp.database import get_db
from ....services.a2rp import ProjectService
from ...schemas_a2rp import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=201,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)  # type: ignore[misc]
def create_project(project: ProjectCreate, db: Session = Depends(get_db)) -> ProjectResponse:
    """Create a new project."""
    try:
        service = ProjectService(db)
        db_project = service.create_project(
            name=project.name,
            description=project.description,
            project_type_id=project.project_type_id,
            project_status_id=project.project_status_id,
            start_date=project.start_date,
            end_date=project.end_date,
        )

        return ProjectResponse.model_validate(db_project)
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)  # type: ignore[misc]
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectResponse:
    """Get a project by ID."""
    try:
        service = ProjectService(db)
        project = service.get_project(project_id)

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return ProjectResponse.model_validate(project)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=List[ProjectResponse],
    responses={500: {"description": "Internal Server Error"}},
)  # type: ignore[misc]
def list_projects(
    project_status_id: Optional[int] = None,
    project_type_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[ProjectResponse]:
    """List all projects."""
    try:
        service = ProjectService(db)
        projects = service.list_projects(
            project_status_id=project_status_id, project_type_id=project_type_id, limit=limit
        )

        return [ProjectResponse.model_validate(p) for p in projects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)  # type: ignore[misc]
def update_project(
    project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)
) -> ProjectResponse:
    """Update a project."""
    try:
        service = ProjectService(db)
        updated_project = service.update_project(
            project_id=project_id,
            name=project.name,
            description=project.description,
            project_status_id=project.project_status_id,
            start_date=project.start_date,
            end_date=project.end_date,
        )

        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")

        return ProjectResponse.model_validate(updated_project)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{project_id}",
    status_code=204,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)  # type: ignore[misc]
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a project."""
    try:
        service = ProjectService(db)
        deleted = service.delete_project(project_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
