"""
Service for managing people.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..models import Person


class PersonService:
    """Service for person operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_person(
        self,
        name: str,
        email: str,
        role: Optional[str] = None,
        team_id: Optional[int] = None,
        skills: Optional[Dict[str, Any]] = None,
        max_concurrent_tasks: int = 5,
    ) -> Person:
        """Create a new person."""
        person = Person(
            name=name,
            email=email,
            role=role,
            team_id=team_id,
            skills=skills or {},
            max_concurrent_tasks=max_concurrent_tasks,
        )
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def get_person(self, person_id: int) -> Optional[Person]:
        """Get a person by ID."""
        return self.db.query(Person).filter(Person.id == person_id).first()

    def list_people(
        self,
        team_id: Optional[int] = None,
        available_only: bool = False,
    ) -> List[Person]:
        """List all people."""
        query = self.db.query(Person)
        if team_id:
            query = query.filter(Person.team_id == team_id)
        if available_only:
            query = query.filter(Person.is_available)
        return query.all()

    def update_person(
        self,
        person_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        team_id: Optional[int] = None,
        skills: Optional[Dict[str, Any]] = None,
        is_available: Optional[bool] = None,
        max_concurrent_tasks: Optional[int] = None,
    ) -> Optional[Person]:
        """Update a person."""
        person = self.get_person(person_id)
        if not person:
            return None

        if name is not None:
            person.name = name
        if email is not None:
            person.email = email
        if role is not None:
            person.role = role
        if team_id is not None:
            person.team_id = team_id
        if skills is not None:
            person.skills = skills
        if is_available is not None:
            person.is_available = is_available
        if max_concurrent_tasks is not None:
            person.max_concurrent_tasks = max_concurrent_tasks

        self.db.commit()
        self.db.refresh(person)
        return person

    def delete_person(self, person_id: int) -> bool:
        """Delete a person."""
        person = self.get_person(person_id)
        if not person:
            return False

        self.db.delete(person)
        self.db.commit()
        return True
