"""
Web UI routes for Task Planner.

This module provides HTML page routes for the web interface.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Get the templates directory
templates_dir = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page - overview of system status."""
    return templates.TemplateResponse(
        "pages/dashboard.html",
        {
            "request": request,
            "version": "1.0.0"
        }
    )


@router.get("/projects", response_class=HTMLResponse)
async def projects_list(request: Request):
    """Projects list page."""
    return templates.TemplateResponse(
        "pages/projects.html",
        {
            "request": request,
            "version": "1.0.0"
        }
    )


@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int):
    """Project detail page."""
    return templates.TemplateResponse(
        "pages/project_detail.html",
        {
            "request": request,
            "project_id": project_id,
            "version": "1.0.0"
        }
    )


@router.get("/tasks", response_class=HTMLResponse)
async def tasks_list(request: Request):
    """Tasks list page."""
    return templates.TemplateResponse(
        "pages/tasks.html",
        {
            "request": request,
            "version": "1.0.0"
        }
    )


@router.get("/resources", response_class=HTMLResponse)
async def resources_list(request: Request):
    """Resources list page."""
    return templates.TemplateResponse(
        "pages/resources.html",
        {
            "request": request,
            "version": "1.0.0"
        }
    )


@router.get("/assignments", response_class=HTMLResponse)
async def assignments_list(request: Request):
    """Assignments list page."""
    return templates.TemplateResponse(
        "pages/assignments.html",
        {
            "request": request,
            "version": "1.0.0"
        }
    )


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """Reports page."""
    return templates.TemplateResponse(
        "pages/reports.html",
        {
            "request": request,
            "version": "1.0.0"
        }
    )
