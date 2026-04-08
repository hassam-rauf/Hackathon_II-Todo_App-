# Quickstart: MCP Server + Tools

**Feature**: 001-mcp-server-tools | **Date**: 2026-04-07

## What This Feature Adds

A `backend/mcp/` package with 5 tool functions that an AI agent can call to manage user tasks:
- `add_task` — create a new task
- `list_tasks` — list tasks with optional status filter
- `complete_task` — mark a task as done
- `delete_task` — remove a task
- `update_task` — change title or description

## Prerequisites

- Existing backend running (FastAPI + SQLModel + Neon DB)
- Python 3.13+ with UV
- All Phase II tests passing (`uv run pytest tests/backend/ -v`)

## Files Created

```
backend/mcp/__init__.py       — Package init
backend/mcp/schemas.py        — OpenAI function calling schemas
backend/mcp/tools.py          — 5 tool implementations
backend/mcp/dispatcher.py     — Central dispatcher
tests/backend/test_mcp_tools.py — ~21 tests
```

## No Files Modified

This is a pure additive change. No existing files are touched.

## Running Tests

```bash
# MCP tools tests only
uv run pytest tests/backend/test_mcp_tools.py -v

# All backend tests (existing + new)
uv run pytest tests/backend/ -v
```

## Using Tools Directly (for testing/debugging)

```python
from sqlmodel import Session
from backend.db import engine
from backend.mcp.tools import add_task, list_tasks
from backend.mcp.dispatcher import execute_tool

with Session(engine) as session:
    # Direct call
    result = add_task(session, user_id="user1", title="Buy groceries")
    print(result)  # {"task_id": 1, "title": "Buy groceries", "status": "created", ...}

    # Via dispatcher
    result = execute_tool("list_tasks", session, user_id="user1")
    print(result)  # {"tasks": [...], "count": 1, "status": "success", ...}
```

## Next Steps

- **Cycle 2**: AI Agent + Chat Endpoint — connects OpenAI Agents SDK to these tools
- **Cycle 3**: ChatKit Frontend — chat UI that sends messages to the agent
