"""
Web UI routes for Task Planner.

This module provides HTML page routes for the web interface.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Any

from ...branding import BrandName, get_brand_config, get_brand_from_domain

# Get the templates directory
templates_dir = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


def get_brand_context(request: Request) -> dict[str, Any]:
    """
    Get brand configuration based on cookie or domain.

    Cookie takes precedence over domain for testing purposes.

    Args:
        request: FastAPI request object

    Returns:
        Dictionary with brand configuration for template context
    """
    # Check for brand cookie first (highest priority)
    brand_name: BrandName | None = request.cookies.get("brand")  # type: ignore

    # Fall back to domain detection
    if not brand_name or brand_name not in ("plugin", "mcr"):
        host = request.headers.get("host", "")
        brand_name = get_brand_from_domain(host)

    # Get brand configuration
    brand = get_brand_config(brand_name)

    return {
        "brand": brand,
        "brand_name": brand.name,
        "brand_display_name": brand.display_name,
        "version": "1.0.0",
    }


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page - overview of system status."""
    context = get_brand_context(request)
    context["request"] = request
    return templates.TemplateResponse("pages/dashboard.html", context)


@router.get("/projects", response_class=HTMLResponse)
async def projects_list(request: Request):
    """Projects list page."""
    context = get_brand_context(request)
    context["request"] = request
    return templates.TemplateResponse("pages/projects.html", context)


@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int):
    """Project detail page."""
    context = get_brand_context(request)
    context["request"] = request
    context["project_id"] = project_id
    return templates.TemplateResponse("pages/project_detail.html", context)


@router.get("/tasks", response_class=HTMLResponse)
async def tasks_list(request: Request):
    """Tasks list page."""
    context = get_brand_context(request)
    context["request"] = request
    return templates.TemplateResponse("pages/tasks.html", context)


@router.get("/resources", response_class=HTMLResponse)
async def resources_list(request: Request):
    """Resources list page."""
    context = get_brand_context(request)
    context["request"] = request
    return templates.TemplateResponse("pages/resources.html", context)


@router.get("/assignments", response_class=HTMLResponse)
async def assignments_list(request: Request):
    """Assignments list page."""
    context = get_brand_context(request)
    context["request"] = request
    return templates.TemplateResponse("pages/assignments.html", context)


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """Reports page."""
    context = get_brand_context(request)
    context["request"] = request
    return templates.TemplateResponse("pages/reports.html", context)


@router.get("/set-brand/{brand_name}")
async def set_brand(brand_name: BrandName, request: Request):
    """
    Set the brand cookie for testing purposes.

    This endpoint allows switching between brands without changing the domain.

    Args:
        brand_name: Brand to switch to (plugin or mcr)
        request: FastAPI request object

    Returns:
        Redirect to dashboard with brand cookie set
    """
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="brand", value=brand_name, max_age=86400 * 30)  # 30 days
    return response
