"""Custom exceptions for task planner service."""


class PlannerException(Exception):
    """Base exception for task planner."""

    pass


class PlanningException(PlannerException):
    """Exception raised during planning operations."""

    pass


class ResourceConflictException(PlanningException):
    """Exception raised when resources are in conflict."""

    pass


class InfeasibleScheduleException(PlanningException):
    """Exception raised when no feasible schedule can be found."""

    pass


class ValidationException(PlannerException):
    """Exception raised during validation."""

    pass


class DatabaseException(PlannerException):
    """Exception raised during database operations."""

    pass
