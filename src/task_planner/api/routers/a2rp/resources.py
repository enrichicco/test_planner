"""
Resource API endpoints for a2rp schema.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....models.a2rp.database import get_db
from ....services.a2rp import ResourceService
from ...schemas_a2rp import ResourceCreate, ResourceResponse, ResourceUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=201,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)) -> ResourceResponse:
    """Create a new resource."""
    try:
        service = ResourceService(db)
        db_resource = service.create_resource(
            name=resource.name,
            email=resource.email,
            resource_type_id=resource.resource_type_id,
            resource_status_id=resource.resource_status_id,
        )

        return ResourceResponse.model_validate(db_resource)
    except LookupError as le:
        raise HTTPException(status_code=404, detail=str(le))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)
def get_resource(resource_id: int, db: Session = Depends(get_db)) -> ResourceResponse:
    """Get a resource by ID."""
    try:
        service = ResourceService(db)
        resource = service.get_resource(resource_id)

        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")

        return ResourceResponse.model_validate(resource)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=List[ResourceResponse],
    responses={500: {"description": "Internal Server Error"}},
)
def list_resources(
    resource_type_id: Optional[int] = None,
    resource_status_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[ResourceResponse]:
    """List all resources."""
    try:
        service = ResourceService(db)
        resources = service.list_resources(
            resource_type_id=resource_type_id,
            resource_status_id=resource_status_id,
            limit=limit,
        )

        return [ResourceResponse.model_validate(r) for r in resources]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch(
    "/{resource_id}",
    response_model=ResourceResponse,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)
def update_resource(
    resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)
) -> ResourceResponse:
    """Update a resource."""
    try:
        service = ResourceService(db)
        updated_resource = service.update_resource(
            resource_id=resource_id,
            name=resource.name,
            email=resource.email,
            resource_status_id=resource.resource_status_id,
        )

        if not updated_resource:
            raise HTTPException(status_code=404, detail="Resource not found")

        return ResourceResponse.model_validate(updated_resource)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{resource_id}",
    status_code=204,
    responses={404: {"description": "Not Found"}, 500: {"description": "Internal Server Error"}},
)
def delete_resource(resource_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a resource."""
    try:
        service = ResourceService(db)
        deleted = service.delete_resource(resource_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Resource not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
