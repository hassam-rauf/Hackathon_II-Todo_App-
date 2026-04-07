# Feature Specification: Task CRUD API

**Feature Branch**: `phase2-task-crud-api`
**Created**: 2026-03-31
**Status**: Draft
**Input**: Phase II Cycle 1 — RESTful API for task management with FastAPI + SQLModel + Neon PostgreSQL

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Task via API (Priority: P1)

A frontend client sends a POST request with a title (required) and optional description to create a new task for a specific user. The API returns the created task with auto-generated ID and timestamps.

**Why this priority**: Core functionality — without task creation, nothing else works.

**Independent Test**: POST `/api/{user_id}/tasks` with `{"title": "Buy groceries"}` returns 201 with task object.

**Acceptance Scenarios**:

1. **Given** a valid user_id, **When** POST with `{"title": "Buy groceries"}`, **Then** return 201 with task (id, title, completed=false, created_at, updated_at)
2. **Given** a valid user_id, **When** POST with `{"title": "Buy groceries", "description": "Milk, eggs, bread"}`, **Then** return 201 with task including description
3. **Given** a valid user_id, **When** POST with `{"title": ""}` or missing title, **Then** return 422 validation error
4. **Given** a valid user_id, **When** POST with title > 200 chars, **Then** return 422 validation error

---

### User Story 2 - List Tasks via API (Priority: P1)

A frontend client requests all tasks for a specific user. The API returns a list of tasks with optional filtering by completion status.

**Why this priority**: Users need to see their tasks — second core operation after creation.

**Independent Test**: GET `/api/{user_id}/tasks` returns array of task objects.

**Acceptance Scenarios**:

1. **Given** user has 3 tasks, **When** GET `/api/{user_id}/tasks`, **Then** return all 3 tasks sorted by created_at desc
2. **Given** user has tasks (2 pending, 1 completed), **When** GET with `?status=pending`, **Then** return only 2 pending tasks
3. **Given** user has tasks, **When** GET with `?status=completed`, **Then** return only completed tasks
4. **Given** user has no tasks, **When** GET `/api/{user_id}/tasks`, **Then** return empty array `[]`

---

### User Story 3 - Get Single Task (Priority: P2)

A frontend client requests details of a specific task by ID.

**Why this priority**: Needed for edit/detail views, but list view is sufficient for MVP.

**Independent Test**: GET `/api/{user_id}/tasks/{task_id}` returns single task object.

**Acceptance Scenarios**:

1. **Given** task with id=1 exists for user, **When** GET `/api/{user_id}/tasks/1`, **Then** return task object with all fields
2. **Given** task with id=999 does not exist, **When** GET `/api/{user_id}/tasks/999`, **Then** return 404 "Task not found"
3. **Given** task belongs to another user, **When** GET `/api/{user_id}/tasks/{id}`, **Then** return 404 (do not leak existence)

---

### User Story 4 - Update a Task (Priority: P2)

A frontend client sends a PUT request to update a task's title and/or description.

**Why this priority**: Important but users can delete + recreate as workaround.

**Independent Test**: PUT `/api/{user_id}/tasks/{id}` with updated fields returns modified task.

**Acceptance Scenarios**:

1. **Given** task exists, **When** PUT with `{"title": "New title"}`, **Then** return updated task with new title, updated_at changed
2. **Given** task exists, **When** PUT with `{"description": "New desc"}`, **Then** return updated task with new description
3. **Given** task exists, **When** PUT with `{"title": "", ...}`, **Then** return 422 (title cannot be empty)
4. **Given** task id=999 not found, **When** PUT, **Then** return 404

---

### User Story 5 - Delete a Task (Priority: P2)

A frontend client sends a DELETE request to remove a task.

**Why this priority**: Cleanup function — needed but not blocking core workflow.

**Independent Test**: DELETE `/api/{user_id}/tasks/{id}` returns 200 with confirmation.

**Acceptance Scenarios**:

1. **Given** task exists, **When** DELETE `/api/{user_id}/tasks/{id}`, **Then** return 200 with `{"ok": true}`
2. **Given** task id=999 not found, **When** DELETE, **Then** return 404 "Task not found"
3. **Given** task deleted, **When** GET same task, **Then** return 404

---

### User Story 6 - Toggle Task Completion (Priority: P2)

A frontend client sends a PATCH request to toggle the completed status of a task.

**Why this priority**: Key UX action but PATCH is a convenience — PUT could do it.

**Independent Test**: PATCH `/api/{user_id}/tasks/{id}/complete` toggles and returns updated task.

**Acceptance Scenarios**:

1. **Given** task is pending (completed=false), **When** PATCH, **Then** return task with completed=true
2. **Given** task is completed (completed=true), **When** PATCH, **Then** return task with completed=false
3. **Given** task not found, **When** PATCH, **Then** return 404

---

### Edge Cases

- What happens when user_id is empty string? → 422 validation
- What happens when database connection fails? → 500 with generic error message
- What happens when title is only whitespace? → Strip and reject as empty (422)
- What happens when description is > 1000 chars? → 422 validation
- What happens on concurrent update of same task? → Last-write-wins (acceptable for this scale)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose RESTful endpoints under `/api/{user_id}/tasks`
- **FR-002**: System MUST validate all input using Pydantic models (title required, max 200 chars; description optional, max 1000 chars)
- **FR-003**: System MUST auto-generate task ID (auto-increment primary key)
- **FR-004**: System MUST auto-set `created_at` and `updated_at` timestamps
- **FR-005**: System MUST update `updated_at` on every modification
- **FR-006**: System MUST filter tasks by `user_id` on all queries (user isolation)
- **FR-007**: System MUST support status filtering via query param (`?status=all|pending|completed`)
- **FR-008**: System MUST return appropriate HTTP status codes (201, 200, 404, 422)
- **FR-009**: System MUST connect to Neon PostgreSQL via `DATABASE_URL` environment variable
- **FR-010**: System MUST configure CORS to allow frontend origin
- **FR-011**: System MUST expose health check endpoint at GET `/health`
- **FR-012**: System MUST strip whitespace from title and description before saving

### Key Entities

- **Task**: The core entity — id (PK, auto-increment), user_id (indexed), title (required, max 200), description (optional, max 1000), completed (boolean, indexed), created_at, updated_at
- **TaskCreate**: Input model for POST — title (required), description (optional)
- **TaskUpdate**: Input model for PUT — title (optional), description (optional); at least one must be provided
- **TaskResponse**: Output model — all Task fields exposed to client

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 API endpoints return correct status codes and response bodies
- **SC-002**: API response time < 500ms p95 for all endpoints
- **SC-003**: All tasks are filtered by user_id (no data leakage between users)
- **SC-004**: `uv run pytest` passes all API tests (minimum 12 test functions: happy path + error per endpoint)
- **SC-005**: FastAPI auto-docs accessible at `/docs` with all endpoints documented
- **SC-006**: Health check returns `{"status": "ok"}` at GET `/health`
