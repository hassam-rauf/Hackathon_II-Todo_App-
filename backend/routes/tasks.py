"""Task CRUD endpoints with JWT authentication.

Ref: specs/phase2-web/task-crud/spec.md — User Stories 1-6
Tasks: T-015 through T-022, T-039 (auth integration)
"""

from datetime import UTC, datetime
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.auth import get_current_user
from backend.db import get_session
from backend.models import Task, TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api", tags=["tasks"])


class TaskStatus(str, Enum):
    all = "all"
    pending = "pending"
    completed = "completed"


def verify_ownership(current_user: dict, user_id: str) -> None:
    """Ensure the authenticated user owns the resource. 403 if mismatch."""
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=201,
)
def create_task(
    user_id: str,
    body: TaskCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> Task:
    """Create a new task for the user. (T-015, T-039)"""
    verify_ownership(current_user, user_id)

    title = body.title.strip()
    description = body.description.strip() if body.description else None

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get(
    "/{user_id}/tasks",
    response_model=list[TaskResponse],
)
def list_tasks(
    user_id: str,
    status: TaskStatus = TaskStatus.all,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[Task]:
    """List all tasks for the user with optional status filter. (T-016, T-039)"""
    verify_ownership(current_user, user_id)

    query = select(Task).where(Task.user_id == user_id)

    if status == TaskStatus.pending:
        query = query.where(Task.completed == False)  # noqa: E712
    elif status == TaskStatus.completed:
        query = query.where(Task.completed == True)  # noqa: E712

    query = query.order_by(Task.created_at.desc())
    return session.exec(query).all()


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> Task:
    """Get a single task by ID. Returns 404 if not found or wrong user. (T-017, T-039)"""
    verify_ownership(current_user, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    user_id: str,
    task_id: int,
    body: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> Task:
    """Update a task's title and/or description. (T-018, T-039)"""
    verify_ownership(current_user, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    if body.title is not None:
        task.title = body.title.strip()
    if body.description is not None:
        task.description = body.description.strip() or None

    task.updated_at = datetime.now(UTC)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Delete a task by ID. (T-019, T-039)"""
    verify_ownership(current_user, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskResponse,
)
def toggle_complete(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> Task:
    """Toggle task completion status. (T-020, T-039)"""
    verify_ownership(current_user, user_id)

    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.now(UTC)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
