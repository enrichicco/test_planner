"""
Reports API endpoints for a2rp schema.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ....models.a2rp.database import get_db
from ....services.a2rp import ReportGenerator

router = APIRouter()


@router.get("/projects/summary", response_model=Dict[str, Any])  # type: ignore[misc]
def get_project_summary(
    project_status_id: Optional[int] = Query(None, description="Filter by project status ID"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get project summary report.

    Returns statistics about projects including total count, status breakdown,
    and average duration.
    """
    generator = ReportGenerator(db)
    return generator.generate_project_summary(project_status_id=project_status_id)


@router.get("/tasks/summary", response_model=Dict[str, Any])  # type: ignore[misc]
def get_task_summary(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    task_status_id: Optional[int] = Query(None, description="Filter by task status ID"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get task summary report.

    Returns statistics about tasks including total count, status breakdown,
    total work hours, and overdue tasks.
    """
    generator = ReportGenerator(db)
    return generator.generate_task_summary(
        project_id=project_id, task_status_id=task_status_id
    )


@router.get("/resources/workload", response_model=List[Dict[str, Any]])  # type: ignore[misc]
def get_resource_workload(
    resource_type_id: Optional[int] = Query(None, description="Filter by resource type ID"),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    Get resource workload report.

    Returns workload information for each resource including total assigned work,
    actual work completed, and utilization percentage.
    """
    generator = ReportGenerator(db)
    return generator.generate_resource_workload_report(
        resource_type_id=resource_type_id
    )


@router.get("/assignments", response_model=List[Dict[str, Any]])  # type: ignore[misc]
def get_assignment_report(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    resource_id: Optional[int] = Query(None, description="Filter by resource ID"),
    include_completed: bool = Query(True, description="Include completed assignments"),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    Get detailed assignment report.

    Returns detailed information about assignments including task names,
    resource names, assigned work vs actual work, and variance.
    """
    generator = ReportGenerator(db)
    return generator.generate_assignment_report(
        project_id=project_id,
        resource_id=resource_id,
        include_completed=include_completed,
    )


@router.get("/projects/timeline", response_model=List[Dict[str, Any]])  # type: ignore[misc]
def get_project_timeline(
    project_id: Optional[int] = Query(None, description="Filter by specific project ID"),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    Get project timeline report.

    Returns timeline information for projects including start/end dates,
    task counts, completion percentage, and overdue status.
    """
    generator = ReportGenerator(db)
    return generator.generate_project_timeline_report(project_id=project_id)
