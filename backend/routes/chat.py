"""Chat endpoint for AI-powered todo management.

Stateless endpoint: loads conversation from DB, processes message,
stores result, returns response. No server-side session state.

Ref: specs/002-ai-chat-endpoint/contracts/chat-api.md
Task: T053
"""

from datetime import UTC, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.agent import MAX_HISTORY_MESSAGES, SYSTEM_PROMPT, run_agent
from backend.auth import get_current_user
from backend.db import get_session
from backend.models import Conversation, Message

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """POST /api/{user_id}/chat request body."""

    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """POST /api/{user_id}/chat response body."""

    conversation_id: int
    response: str
    tool_calls: list[dict]


def verify_ownership(current_user: dict, user_id: str) -> None:
    """Ensure the authenticated user owns the resource."""
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")


@router.post("/{user_id}/chat", response_model=ChatResponse)
def chat(
    user_id: str,
    body: ChatRequest,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    """Process a chat message and return AI response.

    Flow:
    1. Validate message (non-empty)
    2. Create or load conversation (verify ownership)
    3. Fetch recent message history
    4. Store user message
    5. Build message array and call agent
    6. Store assistant response
    7. Return response with tool calls

    Task: T053 | FR-001 through FR-014
    """
    verify_ownership(current_user, user_id)

    # FR-011: Validate message
    if not body.message or not body.message.strip():
        raise HTTPException(status_code=400, detail="Message is required")

    # FR-002, FR-003, FR-010: Create or load conversation
    if body.conversation_id is not None:
        conversation = session.get(Conversation, body.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=404, detail="Conversation not found"
            )
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # FR-003, FR-014: Fetch recent history (capped)
    history_query = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.desc())
        .limit(MAX_HISTORY_MESSAGES)
    )
    history_rows = list(reversed(session.exec(history_query).all()))

    # FR-004: Store user message
    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=body.message.strip(),
    )
    session.add(user_msg)
    session.commit()

    # Build message array: system + history + new user message
    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history_rows:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": body.message.strip()})

    # FR-006, FR-007, FR-008, FR-009: Run agent
    response_text, tool_calls_made = run_agent(messages, session, user_id)

    # FR-005: Store assistant response
    assistant_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=response_text,
    )
    session.add(assistant_msg)

    # Update conversation timestamp
    conversation.updated_at = datetime.now(UTC)
    session.add(conversation)
    session.commit()

    # FR-013: Return response with tool call info
    return ChatResponse(
        conversation_id=conversation.id,
        response=response_text,
        tool_calls=tool_calls_made,
    )
