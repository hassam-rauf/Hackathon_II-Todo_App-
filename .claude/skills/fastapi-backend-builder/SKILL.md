---
name: fastapi-backend-builder
description: |
  Build FastAPI REST API endpoints with Pydantic validation and async patterns.
  This skill should be used when users ask to create API endpoints, routes,
  middleware, request validation, error handling, or backend services.
---

# FastAPI Backend Builder

Build production REST APIs with FastAPI, Pydantic, and async Python.

## What This Skill Does
- Create RESTful API endpoints (GET, POST, PUT, DELETE, PATCH)
- Request/response validation with Pydantic models
- Error handling with HTTPException
- Middleware (CORS, auth, logging)
- Dependency injection patterns
- OpenAPI documentation

## What This Skill Does NOT Do
- Frontend development (use frontend-ui-builder)
- Database models/migrations (use database-sqlmodel-builder)
- Authentication logic (use auth-builder)

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing routes, models, middleware, project structure |
| **Conversation** | Which endpoints, what data, what auth requirements |
| **Skill References** | `references/patterns.md` for endpoint and error patterns |
| **User Guidelines** | Constitution API conventions |

---

## Workflow

1. **Define Pydantic schemas** — request body, response model, query params
2. **Create route function** — async, type-hinted, docstring
3. **Add validation** — Pydantic handles input, manual for business rules
4. **Handle errors** — HTTPException with correct status codes
5. **Register route** — in router or main app
6. **Test** — happy path + error cases

---

## Domain Standards

### Must Follow
- async/await for all I/O operations
- Pydantic models for ALL request/response bodies
- HTTPException for all error responses (not raw dicts)
- Dependency injection for DB sessions, auth
- Type hints on every function parameter and return
- Docstrings on every endpoint (shows in OpenAPI docs)

### Must Avoid
- Sync I/O in async functions (blocks event loop)
- Raw dict responses (use Pydantic response_model)
- Catching broad `Exception` (catch specific errors)
- Business logic in route functions (delegate to services)
- Hardcoded CORS origins (use env var)

---

## Key Patterns

### Endpoint Structure
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(user_id: str, body: TaskCreate, session=Depends(get_session)):
    """Create a new task for the user."""
    task = Task(user_id=user_id, title=body.title, description=body.description)
    session.add(task)
    await session.commit()
    return task
```

### Error Handling
```python
# Standard HTTP errors:
# 400 Bad Request    — invalid input beyond Pydantic
# 401 Unauthorized   — missing/invalid auth
# 403 Forbidden      — wrong user accessing resource
# 404 Not Found      — resource doesn't exist
# 422 Unprocessable  — Pydantic validation (automatic)

@router.get("/{user_id}/tasks/{task_id}")
async def get_task(user_id: str, task_id: int, session=Depends(get_session)):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return task
```

### CORS Setup
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Health Check
```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

## Output Checklist

- [ ] All endpoints async with type hints
- [ ] Pydantic models for request/response
- [ ] HTTPException for errors (correct status codes)
- [ ] Dependency injection for session/auth
- [ ] CORS configured
- [ ] Health check endpoint exists
- [ ] No hardcoded values

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/patterns.md` | Endpoint patterns, middleware, testing |
