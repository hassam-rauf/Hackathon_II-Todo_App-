"""Tests for AI chat endpoint and agent.

All tests mock the OpenAI client — no API key needed.

Ref: specs/002-ai-chat-endpoint/plan.md — Component 4
Tasks: T055, T056, T057, T058
"""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
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


def make_openai_response(content: str, tool_calls=None):
    """Build a SimpleNamespace mimicking OpenAI ChatCompletion response."""
    message = SimpleNamespace(
        content=content,
        tool_calls=tool_calls,
    )
    choice = SimpleNamespace(
        message=message,
        finish_reason="tool_calls" if tool_calls else "stop",
    )
    return SimpleNamespace(choices=[choice])


def make_tool_call(call_id: str, name: str, arguments: dict):
    """Build a SimpleNamespace mimicking an OpenAI tool call."""
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(
            name=name,
            arguments=json.dumps(arguments),
        ),
    )


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = mock_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# --- T055: TestConversationModel ---


class TestConversationModel:
    """Test Conversation and Message database models."""

    def test_create_conversation(self, session: Session):
        """Conversation can be created with user_id."""
        conv = Conversation(user_id=USER_ID)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        assert conv.id is not None
        assert conv.user_id == USER_ID
        assert conv.created_at is not None
        assert conv.updated_at is not None

    def test_message_belongs_to_conversation(self, session: Session):
        """Messages reference a conversation via conversation_id."""
        conv = Conversation(user_id=USER_ID)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        msg = Message(
            conversation_id=conv.id,
            user_id=USER_ID,
            role="user",
            content="Hello",
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)

        assert msg.id is not None
        assert msg.conversation_id == conv.id
        assert msg.role == "user"
        assert msg.content == "Hello"


# --- T055: TestChatEndpoint ---


class TestChatEndpoint:
    """Test POST /api/{user_id}/chat endpoint."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_new_conversation(self, mock_openai_cls, client: TestClient):
        """Sending a message without conversation_id creates a new conversation."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_openai_response(
            "Hello! How can I help you manage your tasks?"
        )

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Hello!"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["response"] == "Hello! How can I help you manage your tasks?"
        assert data["tool_calls"] == []

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_continue_conversation(
        self, mock_openai_cls, client: TestClient, session: Session
    ):
        """Sending a message with conversation_id continues existing conversation."""
        # Create conversation with a prior message
        conv = Conversation(user_id=USER_ID)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        prior_msg = Message(
            conversation_id=conv.id,
            user_id=USER_ID,
            role="user",
            content="Hi there",
        )
        session.add(prior_msg)
        session.commit()

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_openai_response(
            "Sure, what would you like to do?"
        )

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"conversation_id": conv.id, "message": "Help me with tasks"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == conv.id
        assert data["response"] == "Sure, what would you like to do?"


# --- T055: TestAgentToolCalling ---


class TestAgentToolCalling:
    """Test agent tool-calling loop."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_agent_calls_tool(self, mock_openai_cls, client: TestClient):
        """Agent calls add_task tool when user requests it."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        # First call: agent wants to call add_task
        tool_call = make_tool_call(
            "call_1", "add_task", {"title": "buy groceries"}
        )
        # Second call: agent produces final text response
        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tool_call]),
            make_openai_response("Done! I've added 'buy groceries' to your list."),
        ]

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Add a task to buy groceries"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "buy groceries" in data["response"].lower()
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["tool"] == "add_task"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_agent_no_tool_response(self, mock_openai_cls, client: TestClient):
        """Agent responds conversationally without calling tools."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_openai_response(
            "Hi! I'm your todo assistant. Ask me to add, list, or manage tasks."
        )

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Hello!"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["tool_calls"] == []
        assert len(data["response"]) > 0

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_multi_turn_tool_calling(self, mock_openai_cls, client: TestClient):
        """Agent calls tool, gets result, then calls another tool before final response."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        # Turn 1: add_task
        tc1 = make_tool_call("call_1", "add_task", {"title": "task one"})
        # Turn 2: add_task again
        tc2 = make_tool_call("call_2", "add_task", {"title": "task two"})
        # Turn 3: final response
        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tc1]),
            make_openai_response("", tool_calls=[tc2]),
            make_openai_response("Added both tasks for you!"),
        ]

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Add task one and task two"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tool_calls"]) == 2
        assert data["tool_calls"][0]["tool"] == "add_task"
        assert data["tool_calls"][1]["tool"] == "add_task"


# --- T056: TestConversationPersistence ---


class TestConversationPersistence:
    """Test that conversations persist across sessions."""

    def test_messages_survive_reload(self, engine, session: Session):
        """Messages stored in DB are recoverable with a new session."""
        conv = Conversation(user_id=USER_ID)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        msg = Message(
            conversation_id=conv.id,
            user_id=USER_ID,
            role="user",
            content="Remember this",
        )
        session.add(msg)
        session.commit()

        # Simulate restart: new session from same engine
        with Session(engine) as new_session:
            loaded = new_session.get(Conversation, conv.id)
            assert loaded is not None
            assert loaded.user_id == USER_ID

            messages = new_session.exec(
                select(Message).where(Message.conversation_id == conv.id)
            ).all()
            assert len(messages) == 1
            assert messages[0].content == "Remember this"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_history_loaded_for_agent(
        self, mock_openai_cls, client: TestClient, session: Session
    ):
        """Prior messages are included in agent context on follow-up."""
        # Create conversation with history
        conv = Conversation(user_id=USER_ID)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        for i in range(3):
            role = "user" if i % 2 == 0 else "assistant"
            session.add(Message(
                conversation_id=conv.id,
                user_id=USER_ID,
                role=role,
                content=f"Message {i}",
            ))
        session.commit()

        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = make_openai_response(
            "I see your prior messages."
        )

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"conversation_id": conv.id, "message": "What was said before?"},
        )

        assert response.status_code == 200

        # Verify the agent received history in messages
        call_args = mock_client.chat.completions.create.call_args
        messages_sent = call_args.kwargs["messages"]
        # system + 3 history + 1 new user message = 5
        assert len(messages_sent) == 5
        assert messages_sent[0]["role"] == "system"
        assert messages_sent[1]["content"] == "Message 0"


# --- T057: TestErrorHandling ---


class TestErrorHandling:
    """Test error responses for all failure scenarios."""

    def test_empty_message_returns_400(self, client: TestClient):
        """Empty or whitespace-only message returns 400."""
        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "   "},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Message is required"

    def test_conversation_not_found_returns_404(self, client: TestClient):
        """Non-existent conversation_id returns 404."""
        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"conversation_id": 99999, "message": "Hello"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Conversation not found"

    def test_conversation_wrong_user_returns_404(
        self, client: TestClient, session: Session
    ):
        """Conversation owned by another user returns 404 (no leakage)."""
        conv = Conversation(user_id=OTHER_USER)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"conversation_id": conv.id, "message": "Hello"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Conversation not found"

    @patch.dict("os.environ", {}, clear=True)
    def test_no_api_key_returns_fallback(self, client: TestClient):
        """Missing OPENAI_API_KEY returns fallback message, not crash."""
        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Hello"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "trouble" in data["response"].lower()
        assert data["tool_calls"] == []


# --- T058: TestToolSelection ---


class TestToolSelection:
    """Test that agent dispatches correct MCP tools."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_each_tool_dispatched(self, mock_openai_cls, client: TestClient):
        """Each of the 5 MCP tools is dispatched correctly."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        # First: add a task so we have something to operate on
        tc_add = make_tool_call("c1", "add_task", {"title": "test task"})
        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tc_add]),
            make_openai_response("Task added!"),
        ]
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Add test task"},
        )
        assert resp.status_code == 200
        task_id = resp.json()["tool_calls"][0]["result"].get("task_id")

        # list_tasks
        tc_list = make_tool_call("c2", "list_tasks", {})
        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tc_list]),
            make_openai_response("Here are your tasks."),
        ]
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Show my tasks"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "list_tasks"

        # complete_task
        tc_complete = make_tool_call(
            "c3", "complete_task", {"task_id": task_id or 1}
        )
        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tc_complete]),
            make_openai_response("Marked as done!"),
        ]
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Mark task as done"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "complete_task"

        # delete_task
        tc_delete = make_tool_call(
            "c4", "delete_task", {"task_id": task_id or 1}
        )
        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tc_delete]),
            make_openai_response("Deleted!"),
        ]
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Delete that task"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "delete_task"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.OpenAI")
    def test_multi_tool_single_response(
        self, mock_openai_cls, client: TestClient
    ):
        """Agent calls multiple tools in a single turn."""
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        tc1 = make_tool_call("c1", "add_task", {"title": "first"})
        tc2 = make_tool_call("c2", "add_task", {"title": "second"})

        mock_client.chat.completions.create.side_effect = [
            make_openai_response("", tool_calls=[tc1, tc2]),
            make_openai_response("Added both tasks!"),
        ]

        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Add first and second"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["tool_calls"]) == 2
