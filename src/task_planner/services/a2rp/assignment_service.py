"""
Service for managing assignments in the a2rp schema.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from ...models.a2rp import Assignment, Resource, Task


class AssignmentService:
    """Service for assignment operations in a2rp schema."""

    def __init__(self, db: Session) -> None:
        """Initialize assignment service with database session."""
        self.db = db

    def create_assignment(
        self,
        task_id: int,
        resource_id: int,
        work: Optional[float] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        **kwargs: object,
    ) -> Assignment:
        """Create a new assignment."""
        # Validate task exists
        task = self.db.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            raise LookupError(f"Task {task_id} not found")

        # Validate resource exists
        resource = self.db.query(Resource).filter(Resource.resource_id == resource_id).first()
        if not resource:
            raise LookupError(f"Resource {resource_id} not found")

        assignment = Assignment(
            task_id=task_id,
            resource_id=resource_id,
            work=work,
            start_date=start_date,
            end_date=end_date,
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_assignment(self, assignment_id: int) -> Optional[Assignment]:
        """Get an assignment by ID."""
        return self.db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()

    def list_assignments(
        self,
        task_id: Optional[int] = None,
        resource_id: Optional[int] = None,
        limit: int = 100,
    ) -> List[Assignment]:
        """List assignments, optionally filtered by task or resource."""
        query = self.db.query(Assignment)

        if task_id is not None:
            query = query.filter(Assignment.task_id == task_id)

        if resource_id is not None:
            query = query.filter(Assignment.resource_id == resource_id)

        return query.limit(limit).all()

    def update_assignment(
        self,
        assignment_id: int,
        work: Optional[float] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        actual_work: Optional[float] = None,
    ) -> Optional[Assignment]:
        """Update an assignment."""
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return None

        if work is not None:
            assignment.work = Decimal(work)
        if start_date is not None:
            assignment.start_date = start_date
        if end_date is not None:
            assignment.end_date = end_date
        if actual_work is not None:
            assignment.actual_work = Decimal(actual_work)

        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def delete_assignment(self, assignment_id: int) -> bool:
        """Delete an assignment."""
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return False

        self.db.delete(assignment)
        self.db.commit()
        return True
