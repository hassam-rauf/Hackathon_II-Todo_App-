# FastAPI Patterns Reference

## Project Structure
```
backend/
├── main.py              ← App entry, middleware, routers
├── db.py                ← Engine, session dependency
├── models.py            ← SQLModel table models
├── auth.py              ← JWT middleware
├── routes/
│   ├── tasks.py         ← Task CRUD endpoints
│   └── chat.py          ← Chat endpoint (Phase III)
└── pyproject.toml
```

## Router Registration
```python
# main.py
from fastapi import FastAPI
from routes.tasks import router as tasks_router

app = FastAPI(title="Todo API")
app.include_router(tasks_router)
```

## Dependency Injection
```python
# db.py
from sqlmodel import Session
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

# Usage in route:
@router.get("/tasks")
async def list_tasks(session: Session = Depends(get_session)):
    ...
```

## Testing Pattern
```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_create_task(client):
    resp = await client.post("/api/user1/tasks", json={"title": "Test"})
    assert resp.status_code == 201
```

## Query Parameters
```python
from enum import Enum

class TaskStatus(str, Enum):
    all = "all"
    pending = "pending"
    completed = "completed"

@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    status: TaskStatus = TaskStatus.all,
    session: Session = Depends(get_session),
):
    query = select(Task).where(Task.user_id == user_id)
    if status == TaskStatus.pending:
        query = query.where(Task.completed == False)
    elif status == TaskStatus.completed:
        query = query.where(Task.completed == True)
    return session.exec(query).all()
```
