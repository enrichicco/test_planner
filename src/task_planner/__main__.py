"""
Main entry point for the task planner application.

Run with: python -m task_planner
"""

import uvicorn

from .config import settings


def main() -> None:
    """Run the FastAPI application."""
    uvicorn.run(
        "task_planner.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
