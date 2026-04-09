"""Tests for MCP tools, dispatcher, and user isolation.

Tasks: T051-T057
Ref: specs/001-mcp-server-tools/spec.md — User Stories 1-6
"""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.mcp.dispatcher import execute_tool, process_tool_calls
from backend.mcp.tools import (
    add_task,
    complete_task,
    delete_task,
    list_tasks,
    update_task,
)
from backend.models import Task

USER_ID = "test-user-1"
OTHER_USER = "test-user-2"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="sample_task")
def sample_task_fixture(session: Session) -> Task:
    """Create a sample task for tests that need an existing task."""
    task = Task(user_id=USER_ID, title="Buy groceries", description="Milk and eggs")
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# ── T051: TestAddTask ──────────────────────────────────────────────


class TestAddTask:
    """Task: T051 | US1 — add_task tool tests."""

    def test_add_with_title_only(self, session: Session) -> None:
        result = add_task(session, user_id=USER_ID, title="Buy milk")
        assert result["status"] == "created"
        assert result["title"] == "Buy milk"
        assert "task_id" in result
        assert "message" in result

    def test_add_with_title_and_description(self, session: Session) -> None:
        result = add_task(
            session,
            user_id=USER_ID,
            title="Buy milk",
            description="From the store",
        )
        assert result["status"] == "created"
        assert result["task_id"] is not None
        task = session.get(Task, result["task_id"])
        assert task is not None
        assert task.description == "From the store"

    def test_add_rejects_empty_title(self, session: Session) -> None:
        result = add_task(session, user_id=USER_ID, title="")
        assert result["status"] == "error"
        assert "Title is required" in result["message"]


# ── T052: TestListTasks ────────────────────────────────────────────


class TestListTasks:
    """Task: T052 | US2 — list_tasks tool tests."""

    def test_empty_list(self, session: Session) -> None:
        result = list_tasks(session, user_id=USER_ID)
        assert result["count"] == 0
        assert result["tasks"] == []
        assert result["status"] == "success"

    def test_list_all(self, session: Session) -> None:
        add_task(session, user_id=USER_ID, title="Task 1")
        add_task(session, user_id=USER_ID, title="Task 2")
        add_task(session, user_id=USER_ID, title="Task 3")
        result = list_tasks(session, user_id=USER_ID)
        assert result["count"] == 3

    def test_filter_pending(self, session: Session, sample_task: Task) -> None:
        complete_task(session, user_id=USER_ID, task_id=sample_task.id)
        add_task(session, user_id=USER_ID, title="Pending task")
        result = list_tasks(session, user_id=USER_ID, status="pending")
        assert result["count"] == 1
        assert result["tasks"][0]["title"] == "Pending task"

    def test_filter_completed(self, session: Session, sample_task: Task) -> None:
        complete_task(session, user_id=USER_ID, task_id=sample_task.id)
        add_task(session, user_id=USER_ID, title="Pending task")
        result = list_tasks(session, user_id=USER_ID, status="completed")
        assert result["count"] == 1
        assert result["tasks"][0]["completed"] is True


# ── T053: TestCompleteTask ─────────────────────────────────────────


class TestCompleteTask:
    """Task: T053 | US3 — complete_task tool tests."""

    def test_complete_pending_task(
        self, session: Session, sample_task: Task
    ) -> None:
        result = complete_task(session, user_id=USER_ID, task_id=sample_task.id)
        assert result["status"] == "completed"
        assert result["task_id"] == sample_task.id
        task = session.get(Task, sample_task.id)
        assert task is not None
        assert task.completed is True

    def test_complete_already_completed_is_idempotent(
        self, session: Session, sample_task: Task
    ) -> None:
        complete_task(session, user_id=USER_ID, task_id=sample_task.id)
        result = complete_task(session, user_id=USER_ID, task_id=sample_task.id)
        assert result["status"] == "completed"

    def test_complete_not_found(self, session: Session) -> None:
        result = complete_task(session, user_id=USER_ID, task_id=9999)
        assert result["status"] == "error"
        assert "not found" in result["message"]


# ── T054: TestDeleteTask ───────────────────────────────────────────


class TestDeleteTask:
    """Task: T054 | US4 — delete_task tool tests."""

    def test_delete_existing(self, session: Session, sample_task: Task) -> None:
        task_id = sample_task.id
        result = delete_task(session, user_id=USER_ID, task_id=task_id)
        assert result["status"] == "deleted"
        assert result["task_id"] == task_id
        assert session.get(Task, task_id) is None

    def test_delete_not_found(self, session: Session) -> None:
        result = delete_task(session, user_id=USER_ID, task_id=9999)
        assert result["status"] == "error"
        assert "not found" in result["message"]


# ── T055: TestUpdateTask ──────────────────────────────────────────


class TestUpdateTask:
    """Task: T055 | US5 — update_task tool tests."""

    def test_update_title_only(
        self, session: Session, sample_task: Task
    ) -> None:
        result = update_task(
            session, user_id=USER_ID, task_id=sample_task.id, title="Call mom"
        )
        assert result["status"] == "updated"
        assert result["title"] == "Call mom"
        task = session.get(Task, sample_task.id)
        assert task is not None
        assert task.description == "Milk and eggs"  # unchanged

    def test_update_description_only(
        self, session: Session, sample_task: Task
    ) -> None:
        result = update_task(
            session,
            user_id=USER_ID,
            task_id=sample_task.id,
            description="New desc",
        )
        assert result["status"] == "updated"
        task = session.get(Task, sample_task.id)
        assert task is not None
        assert task.description == "New desc"
        assert task.title == "Buy groceries"  # unchanged

    def test_update_both_fields(
        self, session: Session, sample_task: Task
    ) -> None:
        result = update_task(
            session,
            user_id=USER_ID,
            task_id=sample_task.id,
            title="New title",
            description="New desc",
        )
        assert result["status"] == "updated"
        task = session.get(Task, sample_task.id)
        assert task is not None
        assert task.title == "New title"
        assert task.description == "New desc"

    def test_update_not_found(self, session: Session) -> None:
        result = update_task(
            session, user_id=USER_ID, task_id=9999, title="Nope"
        )
        assert result["status"] == "error"
        assert "not found" in result["message"]


# ── T056: TestDispatcher ──────────────────────────────────────────


class TestDispatcher:
    """Task: T056 | US6 — dispatcher tests."""

    def test_routes_to_correct_tool(self, session: Session) -> None:
        result = execute_tool(
            "add_task", session, user_id=USER_ID, title="Via dispatcher"
        )
        assert result["status"] == "created"
        assert result["title"] == "Via dispatcher"

    def test_unknown_tool(self, session: Session) -> None:
        result = execute_tool("nonexistent_tool", session, user_id=USER_ID)
        assert result["status"] == "error"
        assert "Unknown tool" in result["message"]

    def test_exception_handling(self, session: Session) -> None:
        """Dispatcher catches unexpected exceptions from tools."""
        # Pass unexpected kwarg to trigger a TypeError in the tool function
        result = execute_tool(
            "add_task",
            session,
            user_id=USER_ID,
            title="Test",
            nonexistent_param="bad",
        )
        assert result["status"] == "error"
        assert "Something went wrong" in result["message"]


# ── T057: TestUserIsolation ───────────────────────────────────────


class TestUserIsolation:
    """Task: T057 — cross-user isolation tests."""

    def test_read_isolation(self, session: Session) -> None:
        """User2 cannot see User1's tasks."""
        add_task(session, user_id=USER_ID, title="User1 secret task")
        result = list_tasks(session, user_id=OTHER_USER)
        assert result["count"] == 0

    def test_write_isolation(self, session: Session, sample_task: Task) -> None:
        """User2 cannot complete/delete/update User1's tasks."""
        complete_result = complete_task(
            session, user_id=OTHER_USER, task_id=sample_task.id
        )
        assert complete_result["status"] == "error"

        delete_result = delete_task(
            session, user_id=OTHER_USER, task_id=sample_task.id
        )
        assert delete_result["status"] == "error"

        update_result = update_task(
            session,
            user_id=OTHER_USER,
            task_id=sample_task.id,
            title="Hacked",
        )
        assert update_result["status"] == "error"

        # Verify task is unchanged
        task = session.get(Task, sample_task.id)
        assert task is not None
        assert task.title == "Buy groceries"
        assert task.completed is False
