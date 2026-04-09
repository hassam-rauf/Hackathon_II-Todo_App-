# MCP Server Patterns Reference

## Project Structure
```
backend/
├── main.py              ← App entry, includes MCP tools router
├── db.py                ← Engine, session dependency
├── models.py            ← Task SQLModel (existing)
├── auth.py              ← JWT middleware (existing)
├── mcp/
│   ├── __init__.py      ← Package init
│   ├── tools.py         ← Tool implementations (add, list, complete, delete, update)
│   ├── schemas.py       ← Tool definitions (OpenAI function calling format)
│   └── dispatcher.py    ← Central tool dispatcher
├── routes/
│   ├── tasks.py         ← Task CRUD endpoints (existing)
│   └── chat.py          ← Chat endpoint (uses MCP tools via agent)
└── pyproject.toml
```

## Tool Implementation Template
```python
# backend/mcp/tools.py

from sqlmodel import Session, select
from backend.models import Task

def add_task(session: Session, user_id: str, title: str, description: str | None = None) -> dict:
    """Add a new todo task."""
    task = Task(user_id=user_id, title=title, description=description or "")
    session.add(task)
    session.commit()
    session.refresh(task)
    return {
        "task_id": task.id,
        "title": task.title,
        "status": "created",
        "message": f"Task '{task.title}' created successfully"
    }

def list_tasks(session: Session, user_id: str, status: str | None = None) -> dict:
    """List tasks, optionally filtered by status."""
    query = select(Task).where(Task.user_id == user_id)
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
    tasks = session.exec(query).all()
    return {
        "tasks": [
            {"id": t.id, "title": t.title, "completed": t.completed, "description": t.description}
            for t in tasks
        ],
        "count": len(tasks),
        "status": "success",
        "message": f"Found {len(tasks)} task(s)"
    }

def complete_task(session: Session, user_id: str, task_id: int) -> dict:
    """Mark a task as completed."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}
    task.completed = True
    session.commit()
    return {
        "task_id": task.id,
        "title": task.title,
        "status": "completed",
        "message": f"Task '{task.title}' marked as complete"
    }

def delete_task(session: Session, user_id: str, task_id: int) -> dict:
    """Delete a task."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}
    title = task.title
    session.delete(task)
    session.commit()
    return {
        "task_id": task_id,
        "title": title,
        "status": "deleted",
        "message": f"Task '{title}' deleted"
    }

def update_task(session: Session, user_id: str, task_id: int,
                title: str | None = None, description: str | None = None) -> dict:
    """Update task title and/or description."""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    session.commit()
    return {
        "task_id": task.id,
        "title": task.title,
        "status": "updated",
        "message": f"Task '{task.title}' updated"
    }
```

## Tool Schemas (OpenAI Format)
```python
# backend/mcp/schemas.py

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new todo task for the user. Use when user says 'add', 'create', 'remember', 'new task'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The task title"},
                    "description": {"type": "string", "description": "Optional task description"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks or filter by status. Use when user says 'show', 'list', 'what tasks', 'pending'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter: all, pending, or completed. Defaults to all.",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed. Use when user says 'done', 'complete', 'finished', 'mark as done'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to complete"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently. Use when user says 'delete', 'remove', 'get rid of'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description. Use when user says 'change', 'rename', 'update', 'edit'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to update"},
                    "title": {"type": "string", "description": "New title for the task"},
                    "description": {"type": "string", "description": "New description for the task"},
                },
                "required": ["task_id"],
            },
        },
    },
]
```

## Dispatcher Pattern
```python
# backend/mcp/dispatcher.py

import json
from sqlmodel import Session
from backend.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task

TOOL_MAP = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}

def execute_tool(tool_name: str, session: Session, user_id: str, **kwargs) -> dict:
    """Execute an MCP tool by name with given arguments."""
    if tool_name not in TOOL_MAP:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}
    try:
        return TOOL_MAP[tool_name](session=session, user_id=user_id, **kwargs)
    except Exception as e:
        return {"status": "error", "message": f"Something went wrong: {str(e)}"}

def process_tool_calls(tool_calls, session: Session, user_id: str) -> list[dict]:
    """Process OpenAI tool_calls and return results."""
    results = []
    for tc in tool_calls:
        args = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments
        result = execute_tool(tc.function.name, session, user_id, **args)
        results.append({
            "tool_call_id": tc.id,
            "role": "tool",
            "content": json.dumps(result),
        })
    return results
```

## Testing Pattern
```python
# tests/backend/test_mcp_tools.py

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task

@pytest.fixture
def session():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s

def test_add_task(session):
    result = add_task(session, user_id="user1", title="Buy milk")
    assert result["status"] == "created"
    assert result["title"] == "Buy milk"
    assert "task_id" in result

def test_list_tasks_empty(session):
    result = list_tasks(session, user_id="user1")
    assert result["count"] == 0
    assert result["tasks"] == []

def test_complete_nonexistent(session):
    result = complete_task(session, user_id="user1", task_id=999)
    assert result["status"] == "error"

def test_user_isolation(session):
    add_task(session, user_id="user1", title="User1 task")
    result = list_tasks(session, user_id="user2")
    assert result["count"] == 0  # user2 sees nothing
```

## Integration with Chat Endpoint
```python
# backend/routes/chat.py (simplified)

from fastapi import APIRouter, Depends
from sqlmodel import Session
from openai import OpenAI
from backend.db import get_session
from backend.mcp.schemas import TOOL_SCHEMAS
from backend.mcp.dispatcher import process_tool_calls

router = APIRouter(prefix="/api", tags=["chat"])
client = OpenAI()  # uses OPENAI_API_KEY env var

SYSTEM_PROMPT = """You are a helpful todo assistant. You help users manage their tasks.
When users want to add, list, complete, delete, or update tasks, use the available tools.
Always confirm what you did after using a tool. Be concise and friendly."""

@router.post("/{user_id}/chat")
async def chat(user_id: str, body: ChatRequest, session: Session = Depends(get_session)):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # ... load history, add user message ...

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOL_SCHEMAS,
    )

    # If agent wants to call tools
    if response.choices[0].message.tool_calls:
        tool_results = process_tool_calls(
            response.choices[0].message.tool_calls, session, user_id
        )
        # Send tool results back to LLM for natural language response
        messages.append(response.choices[0].message)
        messages.extend(tool_results)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

    return {"response": response.choices[0].message.content}
```
