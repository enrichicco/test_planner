"""
Team API endpoints.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...models.database import get_db
from ...services import TeamService
from ..schemas import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter()


@router.post("/", response_model=TeamResponse, status_code=201)  # type: ignore[misc]
def create_team(team: TeamCreate, db: Session = Depends(get_db)) -> TeamResponse:
    """Create a new team."""
    service = TeamService(db)
    db_team = service.create_team(name=team.name, description=team.description)

    return TeamResponse.model_validate(db_team)


@router.get("/{team_id}", response_model=TeamResponse)  # type: ignore[misc]
def get_team(team_id: int, db: Session = Depends(get_db)) -> TeamResponse:
    """Get a team by ID."""
    service = TeamService(db)
    team = service.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return TeamResponse.model_validate(team)


@router.get("/", response_model=List[TeamResponse])  # type: ignore[misc]
def list_teams(active_only: bool = True, db: Session = Depends(get_db)) -> List[TeamResponse]:
    """List all teams."""
    service = TeamService(db)
    teams = service.list_teams(active_only=active_only)

    return [TeamResponse.model_validate(t) for t in teams]


@router.patch("/{team_id}", response_model=TeamResponse)  # type: ignore[misc]
def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)) -> TeamResponse:
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

    return TeamResponse.model_validate(updated)


@router.delete("/{team_id}", status_code=204)  # type: ignore[misc]
def delete_team(team_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a team."""
    service = TeamService(db)
    if not service.delete_team(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
