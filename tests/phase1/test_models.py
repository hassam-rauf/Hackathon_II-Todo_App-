# Task: T-018 | Spec: specs/phase1-console/spec.md
"""Tests for the Task model."""

from src.models import Task


def test_task_creation_defaults() -> None:
    """Task should have correct defaults."""
    task = Task(id=1, title="Buy groceries")
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description is None
    assert task.completed is False
    assert task.created_at is not None


def test_task_creation_with_description() -> None:
    """Task should store description when provided."""
    task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread")
    assert task.description == "Milk, eggs, bread"


def test_task_str_pending() -> None:
    """Pending task string: '[ ] 1. Buy groceries (date)'."""
    task = Task(id=1, title="Buy groceries")
    result = str(task)
    assert result.startswith("[ ] 1. Buy groceries")


def test_task_str_completed() -> None:
    """Completed task string: '[x] 1. Buy groceries (date)'."""
    task = Task(id=1, title="Buy groceries", completed=True)
    result = str(task)
    assert result.startswith("[x] 1. Buy groceries")
