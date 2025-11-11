"""
Team API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...models.database import get_db
from ...services import TeamService
from ..schemas import TeamCreate, TeamUpdate, TeamResponse

router = APIRouter()


@router.post("/", response_model=TeamResponse, status_code=201)
def create_team(team: TeamCreate, db: Session = Depends(get_db)) -> TeamResponse:
    """Create a new team."""
    service = TeamService(db)
    return service.create_team(name=team.name, description=team.description)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)) -> TeamResponse:
    """Get a team by ID."""
    service = TeamService(db)
    team = service.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.get("/", response_model=List[TeamResponse])
def list_teams(active_only: bool = True, db: Session = Depends(get_db)) -> List[TeamResponse]:
    """List all teams."""
    service = TeamService(db)
    return service.list_teams(active_only=active_only)


@router.patch("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int, team: TeamUpdate, db: Session = Depends(get_db)
) -> TeamResponse:
    """Update a team."""
    service = TeamService(db)
    updated = service.update_team(
        team_id=team_id,
        name=team.name,
        description=team.description,
        is_active=team.is_active,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a team."""
    service = TeamService(db)
    if not service.delete_team(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
