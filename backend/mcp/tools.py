"""MCP tool implementations for AI agent integration.

5 tools: add_task, list_tasks, complete_task, delete_task, update_task.
All tools enforce user_id ownership isolation.

Ref: specs/001-mcp-server-tools/spec.md — FR-001 to FR-012
Tasks: T044, T045, T046, T047, T048
"""

from sqlmodel import Session, select

from backend.models import Task


def add_task(
    session: Session,
    user_id: str,
    title: str,
    description: str | None = None,
) -> dict:
    """Add a new todo task for the user.

    Task: T044 | FR-001
    """
    if not title or not title.strip():
        return {"status": "error", "message": "Title is required"}

    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description or "",
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "task_id": task.id,
        "title": task.title,
        "status": "created",
        "message": f"Task '{task.title}' created successfully",
    }


def list_tasks(
    session: Session,
    user_id: str,
    status: str | None = None,
) -> dict:
    """List tasks for the user, optionally filtered by status.

    Task: T045 | FR-002
    """
    query = select(Task).where(Task.user_id == user_id)

    if status == "pending":
        query = query.where(Task.completed == False)  # noqa: E712
    elif status == "completed":
        query = query.where(Task.completed == True)  # noqa: E712

    tasks = session.exec(query).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "completed": t.completed,
                "description": t.description,
            }
            for t in tasks
        ],
        "count": len(tasks),
        "status": "success",
        "message": f"Found {len(tasks)} task(s)",
    }


def complete_task(
    session: Session,
    user_id: str,
    task_id: int,
) -> dict:
    """Mark a task as completed. Idempotent — completing twice returns success.

    Task: T046 | FR-003, FR-012
    """
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}

    task.completed = True
    session.commit()

    return {
        "task_id": task.id,
        "title": task.title,
        "status": "completed",
        "message": f"Task '{task.title}' marked as complete",
    }


def delete_task(
    session: Session,
    user_id: str,
    task_id: int,
) -> dict:
    """Delete a task permanently.

    Task: T047 | FR-004
    """
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}

    title = task.title
    session.delete(task)
    session.commit()

    return {
        "task_id": task_id,
        "title": title,
        "status": "deleted",
        "message": f"Task '{title}' deleted",
    }


def update_task(
    session: Session,
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> dict:
    """Update a task's title and/or description.

    Task: T048 | FR-005
    """
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}

    if title is not None:
        task.title = title.strip()
    if description is not None:
        task.description = description

    session.commit()

    return {
        "task_id": task.id,
        "title": task.title,
        "status": "updated",
        "message": f"Task '{task.title}' updated",
    }
