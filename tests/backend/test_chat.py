"""Tests for AI chat endpoint and agent.

All tests mock the Agents SDK Runner — no API key needed.

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


def make_run_result(content: str, tool_calls: list[dict] | None = None):
    """Build a mock RunResult mimicking Agents SDK Runner.run_sync output.

    Args:
        content: The assistant's final text response.
        tool_calls: List of dicts with keys: name, arguments (dict), output (dict).
    """
    items = []

    if tool_calls:
        for tc in tool_calls:
            # function_call item
            items.append(SimpleNamespace(
                type="function_call",
                name=tc["name"],
                arguments=json.dumps(tc.get("arguments", {})),
            ))
            # function_call_output item
            items.append(SimpleNamespace(
                type="function_call_output",
                output=json.dumps(tc.get("output", {})),
            ))

    # Final assistant message
    items.append(SimpleNamespace(
        role="assistant",
        content=content,
    ))

    result = MagicMock()
    result.to_input_list.return_value = items
    result.final_output_as.return_value = content
    return result


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
    @patch("backend.agent.Runner")
    def test_new_conversation(self, mock_runner, client: TestClient):
        """Sending a message without conversation_id creates a new conversation."""
        mock_runner.run_sync.return_value = make_run_result(
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
    @patch("backend.agent.Runner")
    def test_continue_conversation(
        self, mock_runner, client: TestClient, session: Session
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

        mock_runner.run_sync.return_value = make_run_result(
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
    @patch("backend.agent.Runner")
    def test_agent_calls_tool(self, mock_runner, client: TestClient):
        """Agent calls add_task tool when user requests it."""
        mock_runner.run_sync.return_value = make_run_result(
            "Done! I've added 'buy groceries' to your list.",
            tool_calls=[{
                "name": "add_task",
                "arguments": {"title": "buy groceries"},
                "output": {"task_id": 1, "title": "buy groceries"},
            }],
        )

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
    @patch("backend.agent.Runner")
    def test_agent_no_tool_response(self, mock_runner, client: TestClient):
        """Agent responds conversationally without calling tools."""
        mock_runner.run_sync.return_value = make_run_result(
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
    @patch("backend.agent.Runner")
    def test_multi_turn_tool_calling(self, mock_runner, client: TestClient):
        """Agent calls multiple tools before final response."""
        mock_runner.run_sync.return_value = make_run_result(
            "Added both tasks for you!",
            tool_calls=[
                {
                    "name": "add_task",
                    "arguments": {"title": "task one"},
                    "output": {"task_id": 1, "title": "task one"},
                },
                {
                    "name": "add_task",
                    "arguments": {"title": "task two"},
                    "output": {"task_id": 2, "title": "task two"},
                },
            ],
        )

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
    @patch("backend.agent.Runner")
    def test_history_loaded_for_agent(
        self, mock_runner, client: TestClient, session: Session
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

        mock_runner.run_sync.return_value = make_run_result(
            "I see your prior messages."
        )

        response = client.post(
            f"/api/{USER_ID}/chat",
            json={"conversation_id": conv.id, "message": "What was said before?"},
        )

        assert response.status_code == 200

        # Verify run_sync was called with the message history
        call_args = mock_runner.run_sync.call_args
        input_messages = call_args.kwargs["input"]
        # run_agent strips system messages, so: 3 history + 1 new user = 4
        assert len(input_messages) == 4
        assert input_messages[0]["content"] == "Message 0"


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
    @patch("backend.agent.Runner")
    def test_each_tool_dispatched(self, mock_runner, client: TestClient):
        """Each of the 5 MCP tools is dispatched correctly."""
        # add_task
        mock_runner.run_sync.return_value = make_run_result(
            "Task added!",
            tool_calls=[{
                "name": "add_task",
                "arguments": {"title": "test task"},
                "output": {"task_id": 1, "title": "test task"},
            }],
        )
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Add test task"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "add_task"

        # list_tasks
        mock_runner.run_sync.return_value = make_run_result(
            "Here are your tasks.",
            tool_calls=[{
                "name": "list_tasks",
                "arguments": {},
                "output": {"tasks": []},
            }],
        )
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Show my tasks"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "list_tasks"

        # complete_task
        mock_runner.run_sync.return_value = make_run_result(
            "Marked as done!",
            tool_calls=[{
                "name": "complete_task",
                "arguments": {"task_id": 1},
                "output": {"status": "completed"},
            }],
        )
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Mark task as done"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "complete_task"

        # delete_task
        mock_runner.run_sync.return_value = make_run_result(
            "Deleted!",
            tool_calls=[{
                "name": "delete_task",
                "arguments": {"task_id": 1},
                "output": {"status": "deleted"},
            }],
        )
        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Delete that task"},
        )
        assert resp.status_code == 200
        assert resp.json()["tool_calls"][0]["tool"] == "delete_task"

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"})
    @patch("backend.agent.Runner")
    def test_multi_tool_single_response(self, mock_runner, client: TestClient):
        """Agent calls multiple tools in a single turn."""
        mock_runner.run_sync.return_value = make_run_result(
            "Added both tasks!",
            tool_calls=[
                {
                    "name": "add_task",
                    "arguments": {"title": "first"},
                    "output": {"task_id": 1, "title": "first"},
                },
                {
                    "name": "add_task",
                    "arguments": {"title": "second"},
                    "output": {"task_id": 2, "title": "second"},
                },
            ],
        )

        resp = client.post(
            f"/api/{USER_ID}/chat",
            json={"message": "Add first and second"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["tool_calls"]) == 2
