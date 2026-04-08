"""Tests for conversation list and message history endpoints.

Ref: specs/003-chatkit-frontend/contracts/conversations-api.md
Task: T004
"""

from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.auth import get_current_user
from backend.db import get_session
from backend.main import app
from backend.models import Conversation, Message

USER_ID = "test-user-1"
OTHER_USER = "test-user-2"


def mock_current_user():
    """Mock auth: return test-user-1."""
    return {"sub": USER_ID, "email": "test@example.com"}


def mock_other_user():
    """Mock auth: return test-user-2."""
    return {"sub": OTHER_USER, "email": "other@example.com"}


@pytest.fixture(name="session")
def session_fixture():
    """In-memory SQLite session for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Test client with mocked DB and auth."""
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_current_user] = mock_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def _create_conversation(session: Session, user_id: str) -> Conversation:
    """Helper: create a conversation in the DB."""
    conv = Conversation(user_id=user_id)
    session.add(conv)
    session.commit()
    session.refresh(conv)
    return conv


def _create_message(
    session: Session,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
) -> Message:
    """Helper: create a message in the DB."""
    msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg


class TestListConversations:
    """GET /api/{user_id}/conversations"""

    def test_empty_list(self, client: TestClient):
        """Returns empty list when user has no conversations."""
        res = client.get(f"/api/{USER_ID}/conversations")
        assert res.status_code == 200
        assert res.json() == []

    def test_list_with_conversations(self, client: TestClient, session: Session):
        """Returns conversations with preview snippets."""
        conv = _create_conversation(session, USER_ID)
        _create_message(session, conv.id, USER_ID, "user", "Hello AI, add a task")
        _create_message(session, conv.id, USER_ID, "assistant", "Done!")

        res = client.get(f"/api/{USER_ID}/conversations")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["id"] == conv.id
        assert data[0]["preview"] == "Hello AI, add a task"

    def test_preview_truncated(self, client: TestClient, session: Session):
        """Preview is truncated to 50 characters."""
        conv = _create_conversation(session, USER_ID)
        long_msg = "A" * 100
        _create_message(session, conv.id, USER_ID, "user", long_msg)

        res = client.get(f"/api/{USER_ID}/conversations")
        data = res.json()
        assert len(data[0]["preview"]) == 50

    def test_no_messages_empty_preview(self, client: TestClient, session: Session):
        """Conversation with no messages has empty preview."""
        _create_conversation(session, USER_ID)

        res = client.get(f"/api/{USER_ID}/conversations")
        data = res.json()
        assert data[0]["preview"] == ""

    def test_ownership_isolation(self, client: TestClient, session: Session):
        """User cannot see other user's conversations."""
        _create_conversation(session, USER_ID)
        _create_conversation(session, OTHER_USER)

        res = client.get(f"/api/{USER_ID}/conversations")
        data = res.json()
        assert len(data) == 1

    def test_access_denied(self, client: TestClient):
        """Returns 403 when user_id doesn't match auth."""
        res = client.get(f"/api/{OTHER_USER}/conversations")
        assert res.status_code == 403


class TestGetConversationMessages:
    """GET /api/{user_id}/conversations/{conversation_id}/messages"""

    def test_load_messages(self, client: TestClient, session: Session):
        """Returns messages in chronological order."""
        conv = _create_conversation(session, USER_ID)
        _create_message(session, conv.id, USER_ID, "user", "First message")
        _create_message(session, conv.id, USER_ID, "assistant", "First reply")
        _create_message(session, conv.id, USER_ID, "user", "Second message")

        res = client.get(f"/api/{USER_ID}/conversations/{conv.id}/messages")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 3
        assert data[0]["role"] == "user"
        assert data[0]["content"] == "First message"
        assert data[1]["role"] == "assistant"
        assert data[2]["content"] == "Second message"

    def test_conversation_not_found(self, client: TestClient):
        """Returns 404 for non-existent conversation."""
        res = client.get(f"/api/{USER_ID}/conversations/9999/messages")
        assert res.status_code == 404

    def test_ownership_check(self, client: TestClient, session: Session):
        """Returns 404 when conversation belongs to another user."""
        conv = _create_conversation(session, OTHER_USER)

        res = client.get(f"/api/{USER_ID}/conversations/{conv.id}/messages")
        assert res.status_code == 404

    def test_access_denied(self, client: TestClient, session: Session):
        """Returns 403 when user_id doesn't match auth."""
        conv = _create_conversation(session, USER_ID)

        res = client.get(f"/api/{OTHER_USER}/conversations/{conv.id}/messages")
        assert res.status_code == 403

    def test_empty_conversation(self, client: TestClient, session: Session):
        """Returns empty list for conversation with no messages."""
        conv = _create_conversation(session, USER_ID)

        res = client.get(f"/api/{USER_ID}/conversations/{conv.id}/messages")
        assert res.status_code == 200
        assert res.json() == []
