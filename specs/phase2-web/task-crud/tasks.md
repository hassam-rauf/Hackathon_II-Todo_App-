# Tasks: Task CRUD API

**Feature**: Task CRUD API (Phase II, Cycle 1)
**Created**: 2026-03-31
**Spec**: `specs/phase2-web/task-crud/spec.md`
**Plan**: `specs/phase2-web/task-crud/plan.md`

## Task List

### T-011: Backend project scaffold
- [ ] Create `backend/` directory
- [ ] `cd backend && uv init` to create pyproject.toml
- [ ] Add dependencies: `fastapi[standard]`, `sqlmodel`, `uvicorn`, `python-dotenv`, `psycopg2-binary`
- [ ] Add dev dependencies: `pytest`, `httpx`
- [ ] Create `backend/main.py`, `backend/db.py`, `backend/models.py`
- [ ] Create `backend/routes/` directory with `__init__.py` and `tasks.py`
- [ ] Create `backend/__init__.py`
- **Acceptance**: `cd backend && uv run python -c "import fastapi; print('ok')"` succeeds

### T-012: SQLModel Task model + Pydantic schemas
- [ ] Define `Task(SQLModel, table=True)` with: id, user_id, title, description, completed, created_at, updated_at
- [ ] Define `TaskCreate(SQLModel)`: title (str, min_length=1, max_length=200), description (Optional[str], max_length=1000)
- [ ] Define `TaskUpdate(SQLModel)`: title (Optional[str], max_length=200), description (Optional[str], max_length=1000)
- [ ] Define `TaskResponse(SQLModel)`: id, user_id, title, description, completed, created_at, updated_at
- [ ] Index on user_id and completed columns
- **Acceptance**: Models importable, field validation works

### T-013: Neon DB connection
- [ ] Create `backend/db.py` with engine from `DATABASE_URL` env var
- [ ] `pool_pre_ping=True`, `pool_size=5`
- [ ] `get_session()` generator yielding `Session(engine)`
- [ ] `init_db()` function calling `SQLModel.metadata.create_all(engine)`
- [ ] Load env vars using `python-dotenv`
- **Acceptance**: `get_session()` yields a valid session; `init_db()` creates tables

### T-014: FastAPI app setup + CORS + health check
- [ ] Create FastAPI app in `backend/main.py` with title="Todo API"
- [ ] Add CORS middleware: allow origin from `FRONTEND_URL` env var
- [ ] Add health check: `GET /health` → `{"status": "ok"}`
- [ ] Register tasks router
- [ ] Call `init_db()` on startup via lifespan
- **Acceptance**: `uv run uvicorn main:app --reload` starts; `/health` returns ok

### T-015: POST /api/{user_id}/tasks — Create task
- [ ] Input: `TaskCreate` body, strip whitespace
- [ ] Create Task with user_id, commit, refresh
- [ ] Return `TaskResponse` with status 201
- **Acceptance**: Valid title → 201; empty title → 422

### T-016: GET /api/{user_id}/tasks — List tasks
- [ ] Query param: `status` enum (all, pending, completed)
- [ ] Filter by user_id, optional completed filter, order by created_at desc
- [ ] Return `list[TaskResponse]`
- **Acceptance**: Returns filtered tasks; empty → `[]`

### T-017: GET /api/{user_id}/tasks/{task_id} — Get single task
- [ ] Find by id, verify user_id matches (404 if not)
- [ ] Return `TaskResponse`
- **Acceptance**: Valid → task; not found → 404; wrong user → 404

### T-018: PUT /api/{user_id}/tasks/{task_id} — Update task
- [ ] Input: `TaskUpdate`, update only provided fields
- [ ] Strip whitespace, update `updated_at`
- [ ] Return `TaskResponse`
- **Acceptance**: Update works; not found → 404

### T-019: DELETE /api/{user_id}/tasks/{task_id} — Delete task
- [ ] Find by id, verify user_id, delete, commit
- [ ] Return `{"ok": true}`
- **Acceptance**: Delete → 200; not found → 404

### T-020: PATCH /api/{user_id}/tasks/{task_id}/complete — Toggle
- [ ] Flip `completed`, update `updated_at`
- [ ] Return `TaskResponse`
- **Acceptance**: Pending→done; done→pending; not found → 404

### T-021: Error handling standardization
- [ ] All 404s: `HTTPException(status_code=404, detail="Task not found")`
- [ ] Consistent `{"detail": "message"}` shape
- **Acceptance**: Every error returns proper status + detail

### T-022: CORS configuration
- [ ] `FRONTEND_URL` env var, default `http://localhost:3000`
- [ ] credentials=True, methods=*, headers=*
- **Acceptance**: Cross-origin from frontend works

### T-023: API tests
- [ ] SQLite in-memory fixture overriding get_session
- [ ] 17 test functions (see plan.md Testing Strategy)
- **Acceptance**: `uv run pytest tests/backend/` — all pass
