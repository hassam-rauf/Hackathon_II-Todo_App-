"""SQLModel table and Pydantic schemas for Task CRUD API.

Ref: specs/phase2-web/task-crud/spec.md — Key Entities
Task: T-012
"""

from datetime import UTC, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Shared fields between create, response, and table models."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskCreate(TaskBase):
    """POST request body — title required, description optional."""

    pass


class TaskUpdate(SQLModel):
    """PUT request body — all fields optional."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class Task(TaskBase, table=True):
    """Database table model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TaskResponse(TaskBase):
    """API response model — all Task fields exposed to client."""

    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime


# --- Chat models (Phase III Cycle 2, T-051) ---


class Conversation(SQLModel, table=True):
    """A chat session between a user and the AI agent."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Message(SQLModel, table=True):
    """A single message within a conversation."""

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(index=True, foreign_key="conversation.id")
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
