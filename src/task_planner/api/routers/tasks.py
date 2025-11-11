"""
Task API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.database import get_db
from ...models import TaskStatus as TaskStatusModel, TaskPriority as TaskPriorityModel
from ...services import TaskService
from ..schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    """Create a new task."""
    service = TaskService(db)

    # Convert enum to model enum
    priority = TaskPriorityModel(task.priority.value)

    return service.create_task(
        name=task.name,
        duration=task.duration,
        description=task.description,
        team_id=task.team_id,
        priority=priority,
        earliest_start=task.earliest_start,
        deadline=task.deadline,
        due_date=task.due_date,
        required_skills=task.required_skills,
        required_resources=task.required_resources,
        predecessor_id=task.predecessor_id,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """Get a task by ID."""
    service = TaskService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    team_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[TaskResponse]:
    """List all tasks."""
    service = TaskService(db)
    status_filter = TaskStatusModel[status.upper()] if status else None
    return service.list_tasks(team_id=team_id, status=status_filter, limit=limit)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task: TaskUpdate, db: Session = Depends(get_db)
) -> TaskResponse:
    """Update a task."""
    service = TaskService(db)

    # Convert enums if provided
    status = TaskStatusModel[task.status.value.upper()] if task.status else None
    priority = TaskPriorityModel(task.priority.value) if task.priority else None

    updated = service.update_task(
        task_id=task_id,
        name=task.name,
        description=task.description,
        duration=task.duration,
        status=status,
        priority=priority,
        earliest_start=task.earliest_start,
        deadline=task.deadline,
        due_date=task.due_date,
        required_skills=task.required_skills,
        required_resources=task.required_resources,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a task."""
    service = TaskService(db)
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
