# Task: T-005, T-007, T-009, T-011, T-013
# Spec: specs/phase1-console/spec.md §User Stories 1-5
"""Tests for all TaskManager CRUD operations."""

import pytest

from src.task_manager import TaskManager


# --- Fixtures ---

@pytest.fixture
def manager() -> TaskManager:
    """Fresh TaskManager for each test."""
    return TaskManager()


@pytest.fixture
def manager_with_tasks() -> TaskManager:
    """TaskManager pre-loaded with 3 tasks."""
    m = TaskManager()
    m.add_task("Buy groceries", "Milk, eggs, bread")
    m.add_task("Call mom")
    m.add_task("Write report", "Quarterly report for Q1")
    return m


# ===== US1: Add Task (T-005) =====

class TestAddTask:

    def test_add_task_with_title(self, manager: TaskManager) -> None:
        task = manager.add_task("Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.completed is False

    def test_add_task_with_description(self, manager: TaskManager) -> None:
        task = manager.add_task("Buy groceries", "Milk, eggs, bread")
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_add_task_auto_increment_id(self, manager: TaskManager) -> None:
        t1 = manager.add_task("Task 1")
        t2 = manager.add_task("Task 2")
        t3 = manager.add_task("Task 3")
        assert t1.id == 1
        assert t2.id == 2
        assert t3.id == 3

    def test_add_task_empty_title_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager.add_task("")

    def test_add_task_whitespace_title_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager.add_task("   ")

    def test_add_task_strips_whitespace(self, manager: TaskManager) -> None:
        task = manager.add_task("  Buy groceries  ")
        assert task.title == "Buy groceries"

    def test_add_task_title_too_long_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="200 characters"):
            manager.add_task("x" * 201)

    def test_add_task_description_too_long_raises(self, manager: TaskManager) -> None:
        with pytest.raises(ValueError, match="1000 characters"):
            manager.add_task("Task", "x" * 1001)

    def test_add_task_empty_description_becomes_none(self, manager: TaskManager) -> None:
        task = manager.add_task("Task", "   ")
        assert task.description is None


# ===== US2: View Tasks (T-007) =====

class TestListTasks:

    def test_list_tasks_empty(self, manager: TaskManager) -> None:
        assert manager.list_tasks() == []

    def test_list_tasks_multiple(self, manager_with_tasks: TaskManager) -> None:
        tasks = manager_with_tasks.list_tasks()
        assert len(tasks) == 3

    def test_list_tasks_sorted_by_id(self, manager_with_tasks: TaskManager) -> None:
        tasks = manager_with_tasks.list_tasks()
        assert tasks[0].id < tasks[1].id < tasks[2].id

    def test_list_tasks_shows_completed_status(self, manager: TaskManager) -> None:
        task = manager.add_task("Test task")
        manager.toggle_complete(task.id)
        tasks = manager.list_tasks()
        assert tasks[0].completed is True

    def test_get_task_exists(self, manager_with_tasks: TaskManager) -> None:
        task = manager_with_tasks.get_task(1)
        assert task is not None
        assert task.title == "Buy groceries"

    def test_get_task_not_found(self, manager: TaskManager) -> None:
        assert manager.get_task(99) is None


# ===== US3: Toggle Complete (T-009) =====

class TestToggleComplete:

    def test_toggle_pending_to_done(self, manager: TaskManager) -> None:
        manager.add_task("Test task")
        result = manager.toggle_complete(1)
        assert result is not None
        assert result.completed is True

    def test_toggle_done_to_pending(self, manager: TaskManager) -> None:
        manager.add_task("Test task")
        manager.toggle_complete(1)
        result = manager.toggle_complete(1)
        assert result is not None
        assert result.completed is False

    def test_toggle_not_found(self, manager: TaskManager) -> None:
        assert manager.toggle_complete(99) is None


# ===== US4: Update Task (T-011) =====

class TestUpdateTask:

    def test_update_title(self, manager_with_tasks: TaskManager) -> None:
        result = manager_with_tasks.update_task(1, title="Buy fruits")
        assert result is not None
        assert result.title == "Buy fruits"

    def test_update_description(self, manager_with_tasks: TaskManager) -> None:
        result = manager_with_tasks.update_task(1, description="New description")
        assert result is not None
        assert result.description == "New description"
        assert result.title == "Buy groceries"  # unchanged

    def test_update_both(self, manager_with_tasks: TaskManager) -> None:
        result = manager_with_tasks.update_task(1, title="New title", description="New desc")
        assert result is not None
        assert result.title == "New title"
        assert result.description == "New desc"

    def test_update_not_found(self, manager: TaskManager) -> None:
        assert manager.update_task(99, title="Nope") is None

    def test_update_empty_title_keeps_current(self, manager_with_tasks: TaskManager) -> None:
        result = manager_with_tasks.update_task(1, title="")
        assert result is not None
        assert result.title == "Buy groceries"  # unchanged

    def test_update_title_too_long_raises(self, manager_with_tasks: TaskManager) -> None:
        with pytest.raises(ValueError, match="200 characters"):
            manager_with_tasks.update_task(1, title="x" * 201)


# ===== US5: Delete Task (T-013) =====

class TestDeleteTask:

    def test_delete_exists(self, manager_with_tasks: TaskManager) -> None:
        assert manager_with_tasks.delete_task(1) is True
        assert manager_with_tasks.get_task(1) is None

    def test_delete_not_found(self, manager: TaskManager) -> None:
        assert manager.delete_task(99) is False

    def test_delete_id_not_reused(self, manager: TaskManager) -> None:
        manager.add_task("Task 1")  # ID 1
        manager.delete_task(1)
        task = manager.add_task("Task 2")  # should be ID 2, not 1
        assert task.id == 2

    def test_delete_removes_from_list(self, manager_with_tasks: TaskManager) -> None:
        manager_with_tasks.delete_task(2)
        tasks = manager_with_tasks.list_tasks()
        assert len(tasks) == 2
        assert all(t.id != 2 for t in tasks)
