"""
Service for managing teams.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import Team


class TeamService:
    """Service for team operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_team(self, name: str, description: Optional[str] = None) -> Team:
        """Create a new team."""
        team = Team(name=name, description=description)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def get_team(self, team_id: int) -> Optional[Team]:
        """Get a team by ID."""
        return self.db.query(Team).filter(Team.id == team_id).first()

    def list_teams(self, active_only: bool = True) -> List[Team]:
        """List all teams."""
        query = self.db.query(Team)
        if active_only:
            query = query.filter(Team.is_active)
        return query.all()

    def update_team(
        self,
        team_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[Team]:
        """Update a team."""
        team = self.get_team(team_id)
        if not team:
            return None

        if name is not None:
            team.name = name
        if description is not None:
            team.description = description
        if is_active is not None:
            team.is_active = is_active

        self.db.commit()
        self.db.refresh(team)
        return team

    def delete_team(self, team_id: int) -> bool:
        """Delete a team."""
        team = self.get_team(team_id)
        if not team:
            return False

        self.db.delete(team)
        self.db.commit()
        return True
