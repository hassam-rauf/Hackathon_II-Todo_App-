# Task: T-003 | Spec: specs/phase1-console/spec.md §User Story 1-5
"""Task model for the Todo console application."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique auto-incremented identifier.
        title: Task title (1-200 chars, required).
        description: Optional task description (max 1000 chars).
        completed: Whether the task is done.
        created_at: Timestamp when the task was created.
    """

    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = "[x]" if self.completed else "[ ]"
        date_str = self.created_at.strftime("%Y-%m-%d")
        return f"{status} {self.id}. {self.title} ({date_str})"
