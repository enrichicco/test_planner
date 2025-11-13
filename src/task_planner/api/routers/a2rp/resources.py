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


@router.post("/", response_model=ResourceResponse, status_code=201)  # type: ignore[misc]
def create_resource(
    resource: ResourceCreate, db: Session = Depends(get_db)
) -> ResourceResponse:
    """Create a new resource."""
    service = ResourceService(db)
    db_resource = service.create_resource(
        name=resource.name,
        email=resource.email,
        resource_type_id=resource.resource_type_id,
        resource_status_id=resource.resource_status_id,
    )
    return ResourceResponse.model_validate(db_resource)


@router.get("/{resource_id}", response_model=ResourceResponse)  # type: ignore[misc]
def get_resource(resource_id: int, db: Session = Depends(get_db)) -> ResourceResponse:
    """Get a resource by ID."""
    service = ResourceService(db)
    resource = service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return ResourceResponse.model_validate(resource)


@router.get("/", response_model=List[ResourceResponse])  # type: ignore[misc]
def list_resources(
    resource_type_id: Optional[int] = None,
    resource_status_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[ResourceResponse]:
    """List all resources."""
    service = ResourceService(db)
    resources = service.list_resources(
        resource_type_id=resource_type_id,
        resource_status_id=resource_status_id,
        limit=limit,
    )
    return [ResourceResponse.model_validate(r) for r in resources]


@router.patch("/{resource_id}", response_model=ResourceResponse)  # type: ignore[misc]
def update_resource(
    resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)
) -> ResourceResponse:
    """Update a resource."""
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


@router.delete("/{resource_id}", status_code=204)  # type: ignore[misc]
def delete_resource(resource_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a resource."""
    service = ResourceService(db)
    deleted = service.delete_resource(resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")
