"""
Service for managing resources.
Merged implementation combining features from both versions.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..models import Resource
from .exceptions import ValidationException


class ResourceService:
    """Service for resource operations."""

    def __init__(self, db: Session) -> None:
        """Initialize resource service with database session."""
        self.db = db

    def create_resource(
        self,
        name: str,
        resource_type: str,
        description: Optional[str] = None,
        capacity: float = 1.0,
        is_renewable: bool = True,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Resource:
        """Create a new resource."""
        # Check if resource with name already exists
        existing = self.db.query(Resource).filter(Resource.name == name).first()
        if existing:
            raise ValidationException(f"Resource with name '{name}' already exists")

        resource = Resource(
            name=name,
            resource_type=resource_type,
            description=description,
            capacity=capacity,
            is_renewable=is_renewable,
            properties=properties or {},
        )
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get_resource(self, resource_id: int) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.db.query(Resource).filter(Resource.id == resource_id).first()

    def get_resource_by_name(self, name: str) -> Optional[Resource]:
        """Get a resource by name."""
        return self.db.query(Resource).filter(Resource.name == name).first()

    def list_resources(
        self,
        resource_type: Optional[str] = None,
        available_only: bool = False,
    ) -> List[Resource]:
        """List all resources, optionally filtered by type and availability."""
        query = self.db.query(Resource)

        if resource_type is not None:
            query = query.filter(Resource.resource_type == resource_type)

        if available_only:
            query = query.filter(Resource.is_available == True)  # noqa: E712

        return query.all()

    def update_resource(
        self,
        resource_id: int,
        name: Optional[str] = None,
        resource_type: Optional[str] = None,
        description: Optional[str] = None,
        capacity: Optional[float] = None,
        is_renewable: Optional[bool] = None,
        is_available: Optional[bool] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Optional[Resource]:
        """Update a resource."""
        resource = self.get_resource(resource_id)
        if not resource:
            return None

        # Check name uniqueness if updating name
        if name is not None and name != resource.name:
            existing = self.db.query(Resource).filter(Resource.name == name).first()
            if existing:
                raise ValidationException(f"Resource with name '{name}' already exists")

        if name is not None:
            resource.name = name
        if resource_type is not None:
            resource.resource_type = resource_type
        if description is not None:
            resource.description = description
        if capacity is not None:
            resource.capacity = capacity
        if is_renewable is not None:
            resource.is_renewable = is_renewable
        if is_available is not None:
            resource.is_available = is_available
        if properties is not None:
            resource.properties = properties

        self.db.commit()
        self.db.refresh(resource)
        return resource

    def delete_resource(self, resource_id: int) -> bool:
        """Delete a resource."""
        resource = self.get_resource(resource_id)
        if not resource:
            return False

        self.db.delete(resource)
        self.db.commit()
        return True
