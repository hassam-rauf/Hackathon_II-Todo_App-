# Implementation Plan: MCP Server + Tools

**Branch**: `001-mcp-server-tools` | **Date**: 2026-04-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-mcp-server-tools/spec.md`

## Summary

Implement 5 in-process MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) inside the existing FastAPI backend. Tools operate on the existing Task SQLModel, enforce user ownership isolation, and return structured dicts with friendly messages. A central dispatcher routes tool calls by name. Tool schemas are defined in OpenAI function calling format for AI agent integration in Cycle 2. All tools are independently testable with SQLite in-memory.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, OpenAI SDK (schemas only — no API calls in this cycle)
**Storage**: Neon Serverless PostgreSQL (production), SQLite in-memory (tests)
**Testing**: pytest with SQLite in-memory engine, sync sessions
**Target Platform**: Linux server (WSL2 development)
**Project Type**: Web application (monorepo: backend/ + frontend/)
**Performance Goals**: All tools complete within 500ms p95
**Constraints**: Tools are stateless, in-process (no separate MCP server process), user_id ownership on all operations
**Scale/Scope**: 5 tools, 1 dispatcher, ~200 lines of tool code, ~150 lines of test code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec completed, clarify passed, plan in progress |
| II. Tech Stack (Locked) | PASS | Python 3.13+, FastAPI, SQLModel, OpenAI function calling format — all locked stack |
| III. Code Quality | PASS | Type hints, single responsibility, <50 line functions planned |
| IV. Testing (Mandatory) | PASS | Each tool tested independently with pytest + SQLite, happy + error paths |
| V. Security | PASS | user_id isolation on all tools, no secrets in code, ownership = "not found" pattern |
| VI. UI/UX Principles | N/A | Backend-only cycle, no UI changes |
| VII. Architecture | PASS | Monorepo, stateless tools, smallest viable diff, RESTful patterns |
| VIII. Performance | PASS | <500ms p95 target, indexed on user_id (existing) |

**GATE RESULT: PASS** — No violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-server-tools/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── tools-api.md     # Tool schemas and dispatcher contract
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
backend/
├── __init__.py          # existing
├── main.py              # existing (no changes needed)
├── db.py                # existing (reused by tools)
├── models.py            # existing (Task model reused)
├── auth.py              # existing (no changes needed)
├── mcp/                 # NEW — MCP tool package
│   ├── __init__.py      # Package init, exports execute_tool
│   ├── tools.py         # 5 tool implementations
│   ├── schemas.py       # OpenAI function calling schemas
│   └── dispatcher.py    # Central dispatcher + process_tool_calls
└── routes/
    ├── __init__.py      # existing
    └── tasks.py         # existing (no changes)

tests/
└── backend/
    ├── test_tasks_api.py  # existing
    ├── test_auth.py       # existing
    └── test_mcp_tools.py  # NEW — MCP tools test suite
```

**Structure Decision**: New `backend/mcp/` package added alongside existing structure. No existing files modified. Tools import from `backend.models` and `backend.db` patterns. Tests follow existing pattern in `tests/backend/`.

## Complexity Tracking

No constitution violations — no justification needed.

## Design Decisions

### D1: In-Process Tools (Not Separate MCP Server)

Tools are plain Python functions inside `backend/mcp/tools.py`, called directly by the dispatcher. No separate process, no IPC, no network transport for tool calls.

**Rationale**: Simplest approach for a monolith. The AI agent (Cycle 2) calls the dispatcher directly. Extractable to a real MCP server later if needed.

### D2: Error Responses as Dicts (Not Exceptions)

Tools return `{"status": "error", "message": "..."}` instead of raising exceptions. The dispatcher catches unexpected exceptions as a safety net.

**Rationale**: Tools are called by an AI agent, not by HTTP clients. The agent needs structured responses it can relay as natural language. HTTPException would be caught by FastAPI middleware, not the agent.

### D3: Ownership Violation = "Not Found"

When a user tries to access another user's task, the tool returns "Task not found" (same as non-existent task).

**Rationale**: Security best practice — no information leakage about whether a task_id exists for another user.

### D4: Idempotent Complete

Calling `complete_task` on an already-completed task returns success, not an error.

**Rationale**: The AI agent may retry or the user may say "mark it done" without knowing current state. Idempotency avoids unnecessary error messages.

## Component Design

### Component 1: Tool Implementations (`backend/mcp/tools.py`)

5 pure functions, each receiving `(session, user_id, **kwargs)` and returning a `dict`.

| Function | Params | Returns | DB Operations |
|----------|--------|---------|---------------|
| `add_task` | title, description? | `{task_id, title, status:"created", message}` | INSERT Task |
| `list_tasks` | status? | `{tasks:[...], count, status:"success", message}` | SELECT Task WHERE user_id, optional completed filter |
| `complete_task` | task_id | `{task_id, title, status:"completed", message}` | UPDATE Task SET completed=True |
| `delete_task` | task_id | `{task_id, title, status:"deleted", message}` | DELETE Task |
| `update_task` | task_id, title?, description? | `{task_id, title, status:"updated", message}` | UPDATE Task SET title/description |

**Ownership pattern** (used by complete, delete, update):
```python
task = session.get(Task, task_id)
if not task or task.user_id != user_id:
    return {"status": "error", "message": f"Task {task_id} not found"}
```

### Component 2: Tool Schemas (`backend/mcp/schemas.py`)

OpenAI function calling format — list of dicts with `type: "function"`, `function.name`, `function.description`, `function.parameters` (JSON Schema).

Descriptions include trigger phrases to help the AI agent select the right tool.

### Component 3: Central Dispatcher (`backend/mcp/dispatcher.py`)

- `TOOL_MAP`: dict mapping tool names to functions
- `execute_tool(tool_name, session, user_id, **kwargs) → dict`: lookup + call + catch
- `process_tool_calls(tool_calls, session, user_id) → list[dict]`: iterate OpenAI tool_calls, parse JSON args, call execute_tool, format results

### Component 4: Test Suite (`tests/backend/test_mcp_tools.py`)

Tests use SQLite in-memory engine (same pattern as existing `test_tasks_api.py`).

| Test Class | Tests | Covers |
|------------|-------|--------|
| `TestAddTask` | 3 | create with title only, with description, empty title |
| `TestListTasks` | 4 | empty list, all tasks, filter pending, filter completed |
| `TestCompleteTask` | 3 | complete pending, complete already-completed (idempotent), not found |
| `TestDeleteTask` | 2 | delete existing, not found |
| `TestUpdateTask` | 4 | update title, update description, update both, not found |
| `TestDispatcher` | 3 | valid tool routing, unknown tool, exception handling |
| `TestUserIsolation` | 2 | cross-user read isolation, cross-user write isolation |

**Total: ~21 tests**

## Dependency Graph

```
schemas.py (no deps — pure data)
    ↓
tools.py (imports: backend.models.Task, sqlmodel.Session)
    ↓
dispatcher.py (imports: tools.py functions, schemas.py optional)
    ↓
test_mcp_tools.py (imports: all three + test fixtures)
```

**Build order**: schemas → tools → dispatcher → tests

## Implementation Sequence

| Step | File | What | Depends On |
|------|------|------|------------|
| 1 | `backend/mcp/__init__.py` | Package init | Nothing |
| 2 | `backend/mcp/schemas.py` | 5 tool schemas in OpenAI format | Nothing |
| 3 | `backend/mcp/tools.py` | 5 tool functions | backend/models.py |
| 4 | `backend/mcp/dispatcher.py` | execute_tool + process_tool_calls | tools.py |
| 5 | `tests/backend/test_mcp_tools.py` | ~21 tests | all mcp/* files |
| 6 | Verify all tests pass | `uv run pytest tests/backend/ -v` | Step 5 |

**No existing files are modified.** This is a pure additive change.
