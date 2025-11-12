"""
Service for managing teams.
Merged implementation combining features from both versions.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ..models import Person, Team
from .exceptions import ValidationException


class TeamService:
    """Service for team operations."""

    def __init__(self, db: Session) -> None:
        """Initialize team service with database session."""
        self.db = db

    def create_team(self, name: str, description: Optional[str] = None) -> Team:
        """Create a new team."""
        # Check if team with name already exists
        existing = self.db.query(Team).filter(Team.name == name).first()
        if existing:
            raise ValidationException(f"Team with name '{name}' already exists")

        team = Team(name=name, description=description)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def get_team(self, team_id: int) -> Optional[Team]:
        """Get a team by ID."""
        return self.db.query(Team).filter(Team.id == team_id).first()

    def get_team_by_name(self, name: str) -> Optional[Team]:
        """Get a team by name."""
        return self.db.query(Team).filter(Team.name == name).first()

    def list_teams(self, active_only: bool = True) -> List[Team]:
        """List all teams, optionally filtered by active status."""
        query = self.db.query(Team)

        if active_only:
            query = query.filter(Team.is_active == True)  # noqa: E712

        return query.all()

    def add_member(self, team_id: int, person_id: int) -> Optional[Team]:
        """Add a person to a team."""
        team = self.get_team(team_id)
        if not team:
            raise ValidationException(f"Team {team_id} not found")

        person = self.db.query(Person).filter(Person.id == person_id).first()
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        # Just update the person's team_id
        person.team_id = team_id
        self.db.commit()
        self.db.refresh(team)
        return team

    def remove_member(self, team_id: int, person_id: int) -> Optional[Team]:
        """Remove a person from a team."""
        team = self.get_team(team_id)
        if not team:
            raise ValidationException(f"Team {team_id} not found")

        person = self.db.query(Person).filter(Person.id == person_id).first()
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        if person.team_id == team_id:
            person.team_id = None
            self.db.commit()
            self.db.refresh(team)

        return team

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

        # Check name uniqueness if updating name
        if name is not None and name != team.name:
            existing = self.db.query(Team).filter(Team.name == name).first()
            if existing:
                raise ValidationException(f"Team with name '{name}' already exists")

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
