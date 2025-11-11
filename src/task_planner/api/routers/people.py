"""
Person API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.database import get_db
from ...services import PersonService
from ..schemas import PersonCreate, PersonUpdate, PersonResponse

router = APIRouter()


@router.post("/", response_model=PersonResponse, status_code=201)
def create_person(person: PersonCreate, db: Session = Depends(get_db)) -> PersonResponse:
    """Create a new person."""
    service = PersonService(db)
    return service.create_person(
        name=person.name,
        email=person.email,
        role=person.role,
        team_id=person.team_id,
        skills=person.skills,
        max_concurrent_tasks=person.max_concurrent_tasks,
    )


@router.get("/{person_id}", response_model=PersonResponse)
def get_person(person_id: int, db: Session = Depends(get_db)) -> PersonResponse:
    """Get a person by ID."""
    service = PersonService(db)
    person = service.get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.get("/", response_model=List[PersonResponse])
def list_people(
    team_id: Optional[int] = None,
    available_only: bool = False,
    db: Session = Depends(get_db),
) -> List[PersonResponse]:
    """List all people."""
    service = PersonService(db)
    return service.list_people(team_id=team_id, available_only=available_only)


@router.patch("/{person_id}", response_model=PersonResponse)
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
    return updated


@router.delete("/{person_id}", status_code=204)
def delete_person(person_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a person."""
    service = PersonService(db)
    if not service.delete_person(person_id):
        raise HTTPException(status_code=404, detail="Person not found")
