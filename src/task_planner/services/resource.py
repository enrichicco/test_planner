"""Service for managing resources."""

from typing import List, Optional

from sqlalchemy.orm import Session

from task_planner.models import Resource, ResourceType
from task_planner.services.exceptions import ValidationException


class ResourceService:
    """Service for managing resources."""

    def __init__(self, db: Session):
        """Initialize resource service with database session."""
        self.db = db

    def create_resource(
        self,
        name: str,
        resource_type: ResourceType,
        description: Optional[str] = None,
        capacity: float = 1.0,
    ) -> Resource:
        """Create a new resource."""
        resource = Resource(
            name=name,
            type=resource_type,
            description=description,
            capacity=capacity,
        )
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get_resource(self, resource_id: int) -> Optional[Resource]:
        """Get resource by ID."""
        return self.db.query(Resource).filter(Resource.id == resource_id).first()

    def get_all_resources(
        self,
        resource_type: Optional[ResourceType] = None,
        available_only: bool = False,
    ) -> List[Resource]:
        """Get all resources, optionally filtered by type and availability."""
        query = self.db.query(Resource)

        if resource_type is not None:
            query = query.filter(Resource.type == resource_type)

        if available_only:
            query = query.filter(Resource.available)

        return query.all()

    def update_resource(
        self,
        resource_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        capacity: Optional[float] = None,
        available: Optional[bool] = None,
    ) -> Resource:
        """Update resource information."""
        resource = self.get_resource(resource_id)
        if not resource:
            raise ValidationException(f"Resource {resource_id} not found")

        if name is not None:
            resource.name = name
        if description is not None:
            resource.description = description
        if capacity is not None:
            resource.capacity = capacity
        if available is not None:
            resource.available = available

        self.db.commit()
        self.db.refresh(resource)
        return resource

    def delete_resource(self, resource_id: int) -> None:
        """Delete a resource."""
        resource = self.get_resource(resource_id)
        if not resource:
            raise ValidationException(f"Resource {resource_id} not found")

        self.db.delete(resource)
        self.db.commit()
