"""Auth middleware and user isolation tests.

Task: T-041
Ref: specs/phase2-web/authentication/plan.md — Testing Strategy

Tests use dependency override for get_current_user since the real
middleware verifies EdDSA JWT tokens via JWKS (requires running frontend).
Protected endpoint tests use NO override to verify HTTPBearer rejects
requests without tokens.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.auth import get_current_user
from backend.db import get_session
from backend.main import app

USER_ID = "auth-user-1"
OTHER_USER = "auth-user-2"


def mock_user(sub: str, email: str = "test@example.com"):
    """Create a mock user payload matching JWT structure."""
    return {"sub": sub, "email": email, "name": "Test User"}


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
    """Client with auth mocked as USER_ID."""
    def get_session_override():
        return session

    def mock_current_user():
        return mock_user(USER_ID)

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = mock_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()



@pytest.fixture(name="unauth_client")
def unauth_client_fixture(session: Session):
    """Client with NO auth override — tests real HTTPBearer rejection."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --- User Isolation Tests ---

class TestUserIsolation:
    def test_user_cannot_access_other_users_tasks(self, client: TestClient):
        """Token for user A, accessing user B's endpoint -> 403."""
        response = client.get(f"/api/{OTHER_USER}/tasks")
        assert response.status_code == 403
        assert response.json()["detail"] == "Access denied"

    def test_user_cannot_create_task_for_other_user(self, client: TestClient):
        response = client.post(
            f"/api/{OTHER_USER}/tasks",
            json={"title": "Sneaky task"},
        )
        assert response.status_code == 403

    def test_user_can_access_own_tasks(self, client: TestClient):
        # Create a task
        response = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": "My task"},
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # Read it back
        response = client.get(f"/api/{USER_ID}/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "My task"

    def test_user_cannot_delete_other_users_task(self, client: TestClient):
        # User A creates a task
        r = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": "A's task"},
        )
        task_id = r.json()["id"]

        # Switch to User B
        app.dependency_overrides[get_current_user] = lambda: mock_user(
            OTHER_USER, "other@example.com"
        )

        # User B tries to delete it via User A's URL -> 403
        response = client.delete(f"/api/{USER_ID}/tasks/{task_id}")
        assert response.status_code == 403

        # Restore User A
        app.dependency_overrides[get_current_user] = lambda: mock_user(USER_ID)

    def test_user_cannot_toggle_other_users_task(self, client: TestClient):
        r = client.post(
            f"/api/{USER_ID}/tasks",
            json={"title": "A's task"},
        )
        task_id = r.json()["id"]

        # Switch to User B
        app.dependency_overrides[get_current_user] = lambda: mock_user(
            OTHER_USER, "other@example.com"
        )

        response = client.patch(f"/api/{USER_ID}/tasks/{task_id}/complete")
        assert response.status_code == 403

        # Restore User A
        app.dependency_overrides[get_current_user] = lambda: mock_user(USER_ID)


# --- Protected Endpoints Tests (no auth override) ---

class TestProtectedEndpoints:
    """All 6 task endpoints require authentication."""

    def test_create_requires_auth(self, unauth_client: TestClient):
        r = unauth_client.post(f"/api/{USER_ID}/tasks", json={"title": "Test"})
        assert r.status_code in (401, 403)

    def test_list_requires_auth(self, unauth_client: TestClient):
        r = unauth_client.get(f"/api/{USER_ID}/tasks")
        assert r.status_code in (401, 403)

    def test_get_requires_auth(self, unauth_client: TestClient):
        r = unauth_client.get(f"/api/{USER_ID}/tasks/1")
        assert r.status_code in (401, 403)

    def test_update_requires_auth(self, unauth_client: TestClient):
        r = unauth_client.put(f"/api/{USER_ID}/tasks/1", json={"title": "x"})
        assert r.status_code in (401, 403)

    def test_delete_requires_auth(self, unauth_client: TestClient):
        r = unauth_client.delete(f"/api/{USER_ID}/tasks/1")
        assert r.status_code in (401, 403)

    def test_toggle_requires_auth(self, unauth_client: TestClient):
        r = unauth_client.patch(f"/api/{USER_ID}/tasks/1/complete")
        assert r.status_code in (401, 403)
