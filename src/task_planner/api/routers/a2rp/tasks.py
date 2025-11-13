"""
Task API endpoints for a2rp schema.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....models.a2rp.database import get_db
from ....services.a2rp import TaskService
from ...schemas_a2rp import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=201)  # type: ignore[misc]
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    """Create a new task."""
    service = TaskService(db)
    db_task = service.create_task(
        name=task.name,
        description=task.description,
        project_id=task.project_id,
        task_status_id=task.task_status_id,
        start_date=task.start_date,
        end_date=task.end_date,
        work=task.work,
    )
    return TaskResponse.model_validate(db_task)


@router.get("/{task_id}", response_model=TaskResponse)  # type: ignore[misc]
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """Get a task by ID."""
    service = TaskService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse.model_validate(task)


@router.get("/", response_model=List[TaskResponse])  # type: ignore[misc]
def list_tasks(
    project_id: Optional[int] = None,
    task_status_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[TaskResponse]:
    """List all tasks."""
    service = TaskService(db)
    tasks = service.list_tasks(
        project_id=project_id, task_status_id=task_status_id, limit=limit
    )
    return [TaskResponse.model_validate(t) for t in tasks]


@router.patch("/{task_id}", response_model=TaskResponse)  # type: ignore[misc]
def update_task(
    task_id: int, task: TaskUpdate, db: Session = Depends(get_db)
) -> TaskResponse:
    """Update a task."""
    service = TaskService(db)
    updated_task = service.update_task(
        task_id=task_id,
        name=task.name,
        description=task.description,
        task_status_id=task.task_status_id,
        start_date=task.start_date,
        end_date=task.end_date,
        work=task.work,
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse.model_validate(updated_task)


@router.delete("/{task_id}", status_code=204)  # type: ignore[misc]
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a task."""
    service = TaskService(db)
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
