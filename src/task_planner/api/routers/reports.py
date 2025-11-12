"""
Report API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from ...models.database import get_db
from ...reports import ReportGenerator, ScheduleReport
from ...services import SchedulingService

router = APIRouter()


@router.get("/{schedule_id}/json")  # type: ignore[misc]
def generate_json_report(schedule_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    """Generate JSON report for a schedule."""
    service = SchedulingService(db)
    schedule = service.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    assignments = service.get_assignments(schedule_id)
    exceptions = service.get_exceptions(schedule_id)

    # Get tasks and people
    task_ids = [a.task_id for a in assignments]
    from ...models import Person, Task

    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all() if task_ids else []
    person_ids = [a.person_id for a in assignments if a.person_id]
    people = db.query(Person).filter(Person.id.in_(person_ids)).all() if person_ids else []

    # Generate report
    report = ScheduleReport(schedule, assignments, tasks, people, exceptions)
    report_data = report.generate_full_report()

    return JSONResponse(content=report_data)


@router.get("/{schedule_id}/html")  # type: ignore[misc]
def generate_html_report(schedule_id: int, db: Session = Depends(get_db)) -> FileResponse:
    """Generate HTML report for a schedule."""
    service = SchedulingService(db)
    schedule = service.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    assignments = service.get_assignments(schedule_id)
    exceptions = service.get_exceptions(schedule_id)

    # Get tasks and people
    task_ids = [a.task_id for a in assignments]
    from ...models import Person, Task

    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all() if task_ids else []
    person_ids = [a.person_id for a in assignments if a.person_id]
    people = db.query(Person).filter(Person.id.in_(person_ids)).all() if person_ids else []

    # Generate report
    report = ScheduleReport(schedule, assignments, tasks, people, exceptions)
    report_data = report.generate_full_report()

    # Generate HTML file
    generator = ReportGenerator()
    filename = f"schedule_{schedule_id}_report.html"
    file_path = generator.generate_html_report(report_data, filename)

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/html",
    )


@router.get("/{schedule_id}/csv/timeline")  # type: ignore[misc]
def generate_timeline_csv(schedule_id: int, db: Session = Depends(get_db)) -> FileResponse:
    """Generate CSV report for task timeline."""
    service = SchedulingService(db)
    schedule = service.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    assignments = service.get_assignments(schedule_id)
    exceptions = service.get_exceptions(schedule_id)

    # Get tasks and people
    task_ids = [a.task_id for a in assignments]
    from ...models import Person, Task

    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all() if task_ids else []
    person_ids = [a.person_id for a in assignments if a.person_id]
    people = db.query(Person).filter(Person.id.in_(person_ids)).all() if person_ids else []

    # Generate report
    report = ScheduleReport(schedule, assignments, tasks, people, exceptions)
    timeline_data = report.generate_task_timeline()

    # Generate CSV file
    generator = ReportGenerator()
    filename = f"schedule_{schedule_id}_timeline.csv"
    file_path = generator.generate_csv_report(timeline_data, filename)

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv",
    )
