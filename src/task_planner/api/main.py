"""
Main FastAPI application.
"""

from pathlib import Path
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from ..config import settings
from .routers.a2rp import assignments, projects, reports, resources, scheduler, tasks
from .web import router as web_router

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

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include a2rp routers
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Resources"])
app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["Assignments"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(scheduler.router, prefix="/api/v1/scheduler", tags=["Scheduler"])

# Include web UI routes (must be last to allow API routes to take precedence)
app.include_router(web_router)


@app.get("/api")
async def api_root() -> Dict[str, str]:
    """API root endpoint."""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "status": "running",
    }


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
