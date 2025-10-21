"""
Task Planner Service - A comprehensive task planning service using PyJobShop and PostgreSQL.

This package provides:
- Team, person, and resource management
- Task creation and dependency management
- Scheduling using PyJobShop
- Exception handling and rescheduling
- Report generation
"""

__version__ = "0.1.0"

from task_planner.config import settings
from task_planner.utils import init_db, get_db, get_db_session
from task_planner.services import (
    TeamService,
    PersonService,
    ResourceService,
    TaskService,
    PlanningService,
)
from task_planner.reports import ReportGenerator

__all__ = [
    "settings",
    "init_db",
    "get_db",
    "get_db_session",
    "TeamService",
    "PersonService",
    "ResourceService",
    "TaskService",
    "PlanningService",
    "ReportGenerator",
]
