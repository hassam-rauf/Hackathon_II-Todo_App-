"""Conversation list and message history endpoints.

Supports the ChatKit frontend conversation selector and history loading.

Ref: specs/003-chatkit-frontend/contracts/conversations-api.md
Task: T002
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.agent import MAX_HISTORY_MESSAGES
from backend.auth import get_current_user
from backend.db import get_session
from backend.models import Conversation, Message

router = APIRouter(prefix="/api", tags=["conversations"])


class ConversationListItem(BaseModel):
    """Response model for a conversation in the list."""

    id: int
    preview: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    """Response model for a single message."""

    id: int
    role: str
    content: str
    created_at: datetime


def verify_ownership(current_user: dict, user_id: str) -> None:
    """Ensure the authenticated user owns the resource."""
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")


@router.get(
    "/{user_id}/conversations",
    response_model=list[ConversationListItem],
)
def list_conversations(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[ConversationListItem]:
    """List a user's conversations, most recent first.

    Returns max 20 conversations with a preview snippet
    (first user message, truncated to 50 chars).

    Task: T002 | FR-011
    """
    verify_ownership(current_user, user_id)

    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(20)
    )
    conversations = session.exec(query).all()

    result: list[ConversationListItem] = []
    for conv in conversations:
        # Fetch first user message as preview
        preview_query = (
            select(Message)
            .where(Message.conversation_id == conv.id, Message.role == "user")
            .order_by(Message.created_at.asc())
            .limit(1)
        )
        first_msg = session.exec(preview_query).first()
        preview = first_msg.content[:50] if first_msg else ""

        result.append(
            ConversationListItem(
                id=conv.id,
                preview=preview,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
            )
        )

    return result


@router.get(
    "/{user_id}/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> list[MessageResponse]:
    """Load all messages for a specific conversation.

    Returns messages in chronological order, capped at MAX_HISTORY_MESSAGES.

    Task: T002 | FR-011
    """
    verify_ownership(current_user, user_id)

    # Verify conversation exists and belongs to user
    conversation = session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .limit(MAX_HISTORY_MESSAGES)
    )
    messages = session.exec(query).all()

    return [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]
