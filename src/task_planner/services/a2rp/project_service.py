"""
Service for managing projects in the a2rp schema.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from ...models.a2rp import Project, ProjectStatus, ProjectType
from ..exceptions import ValidationException


class ProjectService:
    """Service for project operations in a2rp schema."""

    def __init__(self, db: Session) -> None:
        """Initialize project service with database session."""
        self.db = db

    def create_project(
        self,
        name: str,
        project_type_id: int,
        project_status_id: int,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        **kwargs: object,
    ) -> Project:
        """Create a new project."""
        # Validate project type exists
        project_type = (
            self.db.query(ProjectType)
            .filter(ProjectType.project_type_id == project_type_id)
            .first()
        )
        if not project_type:
            raise ValidationException(f"ProjectType {project_type_id} not found")

        # Validate project status exists
        project_status = (
            self.db.query(ProjectStatus)
            .filter(ProjectStatus.project_status_id == project_status_id)
            .first()
        )
        if not project_status:
            raise ValidationException(f"ProjectStatus {project_status_id} not found")

        project = Project(
            name=name,
            description=description,
            project_type_id=project_type_id,
            project_status_id=project_status_id,
            start_date=start_date,
            end_date=end_date,
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return self.db.query(Project).filter(Project.project_id == project_id).first()

    def list_projects(
        self,
        project_status_id: Optional[int] = None,
        project_type_id: Optional[int] = None,
        limit: int = 100,
    ) -> List[Project]:
        """List projects, optionally filtered by status and type."""
        query = self.db.query(Project)

        if project_status_id is not None:
            query = query.filter(Project.project_status_id == project_status_id)

        if project_type_id is not None:
            query = query.filter(Project.project_type_id == project_type_id)

        return query.limit(limit).all()

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        project_status_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[Project]:
        """Update a project."""
        project = self.get_project(project_id)
        if not project:
            return None

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if project_status_id is not None:
            project.project_status_id = project_status_id
        if start_date is not None:
            project.start_date = start_date
        if end_date is not None:
            project.end_date = end_date

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project_id: int) -> bool:
        """Delete a project."""
        project = self.get_project(project_id)
        if not project:
            return False

        self.db.delete(project)
        self.db.commit()
        return True
