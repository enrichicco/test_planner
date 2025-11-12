"""Service for managing teams."""

from typing import List, Optional

from sqlalchemy.orm import Session

from task_planner.models import Person, Team
from task_planner.services.exceptions import ValidationException


class TeamService:
    """Service for managing teams."""

    def __init__(self, db: Session):
        """Initialize team service with database session."""
        self.db = db

    def create_team(self, name: str, description: Optional[str] = None) -> Team:
        """Create a new team."""
        # Check if team with name already exists
        existing = self.db.query(Team).filter(Team.name == name).first()

        if existing:
            return existing

        team = Team(name=name, description=description)
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def get_team(self, team_id: int) -> Optional[Team]:
        """Get team by ID."""
        return self.db.query(Team).filter(Team.id == team_id).first()

    def get_all_teams(self) -> List[Team]:
        """Get all teams."""
        teams: List[Team] = self.db.query(Team).all()
        return teams

    def add_member(self, team_id: int, person_id: int) -> None:
        """Add a person to a team."""
        team = self.get_team(team_id)
        if not team:
            raise ValidationException(f"Team {team_id} not found")

        person = self.db.query(Person).filter(Person.id == person_id).first()
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        if person not in team.members:
            team.members.append(person)
            self.db.commit()

    def remove_member(self, team_id: int, person_id: int) -> None:
        """Remove a person from a team."""
        team = self.get_team(team_id)
        if not team:
            raise ValidationException(f"Team {team_id} not found")

        person = self.db.query(Person).filter(Person.id == person_id).first()
        if not person:
            raise ValidationException(f"Person {person_id} not found")

        if person in team.members:
            team.members.remove(person)
            self.db.commit()

    def update_team(
        self, team_id: int, name: Optional[str] = None, description: Optional[str] = None
    ) -> Team:
        """Update team information."""
        team = self.get_team(team_id)
        if not team:
            raise ValidationException(f"Team {team_id} not found")

        if name is not None:
            team.name = name
        if description is not None:
            team.description = description

        self.db.commit()
        self.db.refresh(team)
        return team

    def delete_team(self, team_id: int) -> None:
        """Delete a team."""
        team = self.get_team(team_id)
        if not team:
            raise ValidationException(f"Team {team_id} not found")

        self.db.delete(team)
        self.db.commit()
