"""
Service for managing resources in the a2rp schema.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ...models.a2rp import Resource, ResourceStatus, ResourceType
from ..exceptions import ValidationException


class ResourceService:
    """Service for resource operations in a2rp schema."""

    def __init__(self, db: Session) -> None:
        """Initialize resource service with database session."""
        self.db = db

    def create_resource(
        self,
        name: str,
        resource_type_id: int,
        resource_status_id: int,
        email: Optional[str] = None,
        **kwargs: object,
    ) -> Resource:
        """Create a new resource."""
        # Validate resource type exists
        resource_type = (
            self.db.query(ResourceType)
            .filter(ResourceType.resource_type_id == resource_type_id)
            .first()
        )
        if not resource_type:
            raise ValidationException(f"ResourceType {resource_type_id} not found")

        # Validate resource status exists
        resource_status = (
            self.db.query(ResourceStatus)
            .filter(ResourceStatus.resource_status_id == resource_status_id)
            .first()
        )
        if not resource_status:
            raise ValidationException(f"ResourceStatus {resource_status_id} not found")

        resource = Resource(
            name=name,
            email=email,
            resource_type_id=resource_type_id,
            resource_status_id=resource_status_id,
        )
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def get_resource(self, resource_id: int) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.db.query(Resource).filter(Resource.resource_id == resource_id).first()

    def list_resources(
        self,
        resource_type_id: Optional[int] = None,
        resource_status_id: Optional[int] = None,
        limit: int = 100,
    ) -> List[Resource]:
        """List resources, optionally filtered by type and status."""
        query = self.db.query(Resource)

        if resource_type_id is not None:
            query = query.filter(Resource.resource_type_id == resource_type_id)

        if resource_status_id is not None:
            query = query.filter(Resource.resource_status_id == resource_status_id)

        return query.limit(limit).all()

    def update_resource(
        self,
        resource_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        resource_status_id: Optional[int] = None,
    ) -> Optional[Resource]:
        """Update a resource."""
        resource = self.get_resource(resource_id)
        if not resource:
            return None

        if name is not None:
            resource.name = name
        if email is not None:
            resource.email = email
        if resource_status_id is not None:
            resource.resource_status_id = resource_status_id

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
