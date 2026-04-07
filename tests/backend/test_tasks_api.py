"""API tests for Task CRUD endpoints.

Task: T-023, T-041 (updated with auth override)
Ref: specs/phase2-web/task-crud/plan.md — Testing Strategy
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.auth import get_current_user
from backend.db import get_session
from backend.main import app


USER_ID = "test-user-1"
OTHER_USER = "test-user-2"


def mock_current_user():
    """Mock auth: return test-user-1 as the authenticated user."""
    return {"sub": USER_ID, "email": "test@example.com"}


def mock_other_user():
    """Mock auth: return test-user-2 as the authenticated user."""
    return {"sub": OTHER_USER, "email": "other@example.com"}


@pytest.fixture(name="session")
def session_fixture():
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
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = mock_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# --- Health Check ---

class TestHealth:
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


# --- Create Task (POST) ---

class TestCreateTask:
    def test_create_task(self, client: TestClient):
        response = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": "Buy groceries"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["user_id"] == USER_ID
        assert data["completed"] is False
        assert data["description"] is None
        assert "id" in data
        assert "created_at" in data

    def test_create_task_with_description(self, client: TestClient):
        response = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": "Buy groceries", "description": "Milk, eggs, bread"},
        )
        assert response.status_code == 201
        assert response.json()["description"] == "Milk, eggs, bread"

    def test_create_task_empty_title(self, client: TestClient):
        response = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": ""},
        )
        assert response.status_code == 422

    def test_create_task_strips_whitespace(self, client: TestClient):
        response = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": "  Buy groceries  "},
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Buy groceries"


# --- List Tasks (GET) ---

class TestListTasks:
    def test_list_tasks_empty(self, client: TestClient):
        response = client.get(f"/api/{USER_ID}/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks(self, client: TestClient):
        client.post(f"/api/{USER_ID}/tasks", json={"title": "Task 1"})
        client.post(f"/api/{USER_ID}/tasks", json={"title": "Task 2"})
        response = client.get(f"/api/{USER_ID}/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_tasks_filter_pending(self, client: TestClient):
        r1 = client.post(f"/api/{USER_ID}/tasks", json={"title": "Task 1"})
        client.post(f"/api/{USER_ID}/tasks", json={"title": "Task 2"})
        task_id = r1.json()["id"]
        client.patch(f"/api/{USER_ID}/tasks/{task_id}/complete")

        response = client.get(f"/api/{USER_ID}/tasks?status=pending")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Task 2"

    def test_list_tasks_filter_completed(self, client: TestClient):
        r1 = client.post(f"/api/{USER_ID}/tasks", json={"title": "Task 1"})
        client.post(f"/api/{USER_ID}/tasks", json={"title": "Task 2"})
        task_id = r1.json()["id"]
        client.patch(f"/api/{USER_ID}/tasks/{task_id}/complete")

        response = client.get(f"/api/{USER_ID}/tasks?status=completed")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Task 1"


# --- Get Single Task (GET) ---

class TestGetTask:
    def test_get_task(self, client: TestClient):
        r = client.post(f"/api/{USER_ID}/tasks", json={"title": "My task"})
        task_id = r.json()["id"]
        response = client.get(f"/api/{USER_ID}/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "My task"

    def test_get_task_not_found(self, client: TestClient):
        response = client.get(f"/api/{USER_ID}/tasks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


# --- Update Task (PUT) ---

class TestUpdateTask:
    def test_update_task_title(self, client: TestClient):
        r = client.post(f"/api/{USER_ID}/tasks", json={"title": "Old title"})
        task_id = r.json()["id"]
        response = client.put(
            f"/api/{USER_ID}/tasks/{task_id}",
            json={"title": "New title"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "New title"

    def test_update_task_not_found(self, client: TestClient):
        response = client.put(
            f"/api/{USER_ID}/tasks/999",
            json={"title": "New title"},
        )
        assert response.status_code == 404


# --- Delete Task (DELETE) ---

class TestDeleteTask:
    def test_delete_task(self, client: TestClient):
        r = client.post(f"/api/{USER_ID}/tasks", json={"title": "Delete me"})
        task_id = r.json()["id"]
        response = client.delete(f"/api/{USER_ID}/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json() == {"ok": True}

        # Verify deleted
        response = client.get(f"/api/{USER_ID}/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        response = client.delete(f"/api/{USER_ID}/tasks/999")
        assert response.status_code == 404


# --- Toggle Complete (PATCH) ---

class TestToggleComplete:
    def test_toggle_pending_to_completed(self, client: TestClient):
        r = client.post(f"/api/{USER_ID}/tasks", json={"title": "Toggle me"})
        task_id = r.json()["id"]
        assert r.json()["completed"] is False

        response = client.patch(f"/api/{USER_ID}/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.json()["completed"] is True

    def test_toggle_completed_to_pending(self, client: TestClient):
        r = client.post(f"/api/{USER_ID}/tasks", json={"title": "Toggle me"})
        task_id = r.json()["id"]
        client.patch(f"/api/{USER_ID}/tasks/{task_id}/complete")  # → True

        response = client.patch(f"/api/{USER_ID}/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.json()["completed"] is False

    def test_toggle_not_found(self, client: TestClient):
        response = client.patch(f"/api/{USER_ID}/tasks/999/complete")
        assert response.status_code == 404


# --- User Isolation ---

class TestUserIsolation:
    def test_user_cannot_see_other_users_tasks(self, client: TestClient, session: Session):
        # User 1 creates a task (already mocked as USER_ID)
        r = client.post(f"/api/{USER_ID}/tasks", json={"title": "User 1 task"})
        task_id = r.json()["id"]

        # Switch to other user
        app.dependency_overrides[get_current_user] = mock_other_user

        # Other user tries to access User 1's task via their own URL → 404
        response = client.get(f"/api/{OTHER_USER}/tasks/{task_id}")
        assert response.status_code == 404

        # Restore
        app.dependency_overrides[get_current_user] = mock_current_user

    def test_user_list_only_own_tasks(self, client: TestClient, session: Session):
        # User 1 creates a task
        client.post(f"/api/{USER_ID}/tasks", json={"title": "User 1 task"})

        # Switch to other user and create their task
        app.dependency_overrides[get_current_user] = mock_other_user
        client.post(f"/api/{OTHER_USER}/tasks", json={"title": "User 2 task"})

        # Other user only sees their own
        response = client.get(f"/api/{OTHER_USER}/tasks")
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["user_id"] == OTHER_USER

        # Restore
        app.dependency_overrides[get_current_user] = mock_current_user
