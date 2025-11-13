"""
Main FastAPI application.
"""

from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import settings
from .routers.a2rp import assignments, projects, resources, tasks

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="A comprehensive task planning and scheduling service using PyJobShop",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include a2rp routers
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["Assignments"])


@app.get("/")  # type: ignore[misc]
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "status": "running",
    }


@app.get("/health")  # type: ignore[misc]
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
