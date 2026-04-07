# Task: T-004, T-006, T-008, T-010, T-012, T-014
# Spec: specs/phase1-console/spec.md §FR-001 through FR-008
"""TaskManager — all CRUD operations for in-memory todo tasks."""

from src.models import Task


class TaskManager:
    """Manages an in-memory collection of Task objects.

    Storage: dict keyed by task ID for O(1) lookup.
    IDs auto-increment and are never reused after deletion.
    """

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    # --- US1: Add Task ---

    def add_task(self, title: str, description: str | None = None) -> Task:
        """Create a new task with auto-incremented ID.

        Args:
            title: Required, 1-200 chars after stripping whitespace.
            description: Optional, max 1000 chars.

        Returns:
            The newly created Task.

        Raises:
            ValueError: If title is empty or exceeds 200 chars,
                        or description exceeds 1000 chars.
        """
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less.")

        if description is not None:
            description = description.strip()
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less.")
            if not description:
                description = None

        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    # --- US2: View Tasks ---

    def get_task(self, task_id: int) -> Task | None:
        """Get a single task by ID. Returns None if not found."""
        return self._tasks.get(task_id)

    def list_tasks(self) -> list[Task]:
        """Return all tasks sorted by ID ascending."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    # --- US3: Toggle Complete ---

    def toggle_complete(self, task_id: int) -> Task | None:
        """Toggle a task's completed status.

        Returns:
            The updated Task, or None if not found.
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.completed = not task.completed
        return task

    # --- US4: Update Task ---

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task | None:
        """Update a task's title and/or description.

        If title is provided and non-empty after strip, it replaces the current title.
        If description is provided, it replaces the current description.
        Passing empty string for title keeps the current title.

        Returns:
            The updated Task, or None if not found.

        Raises:
            ValueError: If new title exceeds 200 chars or description exceeds 1000 chars.
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if title is not None:
            title = title.strip()
            if title:
                if len(title) > 200:
                    raise ValueError("Title must be 200 characters or less.")
                task.title = title

        if description is not None:
            description = description.strip()
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less.")
            task.description = description if description else None

        return task

    # --- US5: Delete Task ---

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by ID.

        Returns:
            True if the task was deleted, False if not found.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
