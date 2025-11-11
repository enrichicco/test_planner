"""
Resource API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.database import get_db
from ...services import ResourceService
from ..schemas import ResourceCreate, ResourceUpdate, ResourceResponse

router = APIRouter()


@router.post("/", response_model=ResourceResponse, status_code=201)
def create_resource(
    resource: ResourceCreate, db: Session = Depends(get_db)
) -> ResourceResponse:
    """Create a new resource."""
    service = ResourceService(db)
    return service.create_resource(
        name=resource.name,
        resource_type=resource.resource_type,
        description=resource.description,
        capacity=resource.capacity,
        is_renewable=resource.is_renewable,
        properties=resource.properties,
    )


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)) -> ResourceResponse:
    """Get a resource by ID."""
    service = ResourceService(db)
    resource = service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.get("/", response_model=List[ResourceResponse])
def list_resources(
    resource_type: Optional[str] = None,
    available_only: bool = False,
    db: Session = Depends(get_db),
) -> List[ResourceResponse]:
    """List all resources."""
    service = ResourceService(db)
    return service.list_resources(resource_type=resource_type, available_only=available_only)


@router.patch("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)
) -> ResourceResponse:
    """Update a resource."""
    service = ResourceService(db)
    updated = service.update_resource(
        resource_id=resource_id,
        name=resource.name,
        resource_type=resource.resource_type,
        description=resource.description,
        capacity=resource.capacity,
        is_renewable=resource.is_renewable,
        is_available=resource.is_available,
        properties=resource.properties,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a resource."""
    service = ResourceService(db)
    if not service.delete_resource(resource_id):
        raise HTTPException(status_code=404, detail="Resource not found")
