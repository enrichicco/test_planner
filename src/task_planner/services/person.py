"""Service for managing people."""

from typing import List, Optional
from sqlalchemy.orm import Session

from task_planner.models import Person, Resource
from task_planner.services.exceptions import ValidationException


class PersonService:
    """Service for managing people."""

    def __init__(self, db: Session):
        """Initialize person service with database session."""
        self.db = db

    def create_person(
        self,
        name: str,
        email: str,
        role: Optional[str] = None,
        availability_hours_per_day: float = 8.0,
    ) -> Person:
        """Create a new person."""
        # Check if person with email already exists
        existing = self.db.query(Person).filter(Person.email == email).first()

        if existing:
            return existing

        person = Person(
            name=name,
            email=email,
            role=role,
            availability_hours_per_day=availability_hours_per_day,
        )
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def get_person(self, person_id: int) -> Optional[Person]:
        """Get person by ID."""
        return self.db.query(Person).filter(Person.id == person_id).first()

    def get_all_people(self, active_only: bool = True) -> List[Person]:
        """Get all people."""
        query = self.db.query(Person)
        if active_only:
            query = query.filter(Person.is_active)
        return query.all()

    def add_skill(self, person_id: int, resource_id: int):
        """Add a skill (resource) to a person."""
        person = self.get_person(person_id)
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        resource = self.db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            raise ValidationException(f"Resource {resource_id} not found")

        if resource not in person.skills:
            person.skills.append(resource)
            self.db.commit()

    def remove_skill(self, person_id: int, resource_id: int):
        """Remove a skill (resource) from a person."""
        person = self.get_person(person_id)
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        resource = self.db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            raise ValidationException(f"Resource {resource_id} not found")

        if resource in person.skills:
            person.skills.remove(resource)
            self.db.commit()

    def update_person(
        self,
        person_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        availability_hours_per_day: Optional[float] = None,
        is_active: Optional[bool] = None,
    ) -> Person:
        """Update person information."""
        person = self.get_person(person_id)
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        if name is not None:
            person.name = name
        if email is not None:
            person.email = email
        if role is not None:
            person.role = role
        if availability_hours_per_day is not None:
            person.availability_hours_per_day = availability_hours_per_day
        if is_active is not None:
            person.is_active = is_active

        self.db.commit()
        self.db.refresh(person)
        return person

    def delete_person(self, person_id: int):
        """Delete a person (soft delete by marking inactive)."""
        person = self.get_person(person_id)
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        person.is_active = False
        self.db.commit()
