"""
Person API endpoints.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...models.database import get_db
from ...services import PersonService
from ..schemas import PersonCreate, PersonResponse, PersonUpdate

router = APIRouter()


@router.post("/", response_model=PersonResponse, status_code=201)  # type: ignore[misc]
def create_person(person: PersonCreate, db: Session = Depends(get_db)) -> PersonResponse:
    """Create a new person."""
    service = PersonService(db)
    created_person = service.create_person(
        name=person.name,
        email=person.email,
        role=person.role,
        team_id=person.team_id,
        skills=person.skills,
        max_concurrent_tasks=person.max_concurrent_tasks,
    )

    return PersonResponse.model_validate(created_person)


@router.get("/{person_id}", response_model=PersonResponse)  # type: ignore[misc]
def get_person(person_id: int, db: Session = Depends(get_db)) -> PersonResponse:
    """Get a person by ID."""
    service = PersonService(db)
    person = service.get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return PersonResponse.model_validate(person)


@router.get("/", response_model=List[PersonResponse])  # type: ignore[misc]
def list_people(
    team_id: Optional[int] = None,
    available_only: bool = False,
    db: Session = Depends(get_db),
) -> List[PersonResponse]:
    """List all people."""
    service = PersonService(db)
    people = service.list_people(team_id=team_id, available_only=available_only)

    return [PersonResponse.model_validate(person) for person in people]


@router.patch("/{person_id}", response_model=PersonResponse)  # type: ignore[misc]
def update_person(
    person_id: int, person: PersonUpdate, db: Session = Depends(get_db)
) -> PersonResponse:
    """Update a person."""
    service = PersonService(db)
    updated = service.update_person(
        person_id=person_id,
        name=person.name,
        email=person.email,
        role=person.role,
        team_id=person.team_id,
        skills=person.skills,
        is_available=person.is_available,
        max_concurrent_tasks=person.max_concurrent_tasks,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Person not found")

    return PersonResponse.model_validate(updated)


@router.delete("/{person_id}", status_code=204)  # type: ignore[misc]
def delete_person(person_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a person."""
    service = PersonService(db)
    if not service.delete_person(person_id):
        raise HTTPException(status_code=404, detail="Person not found")
