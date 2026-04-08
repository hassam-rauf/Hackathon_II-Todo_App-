---
name: mcp-server-builder
description: |
  Build MCP (Model Context Protocol) servers with tool definitions for AI agent integration.
  This skill should be used when users ask to create MCP tools, AI-callable functions,
  tool schemas, agent-tool interfaces, or in-process MCP servers for FastAPI.
---

# MCP Server Builder

Build MCP tool servers that expose application functions to AI agents via the Model Context Protocol.

## What This Skill Does
- Create MCP tool definitions with typed parameters and return schemas
- In-process MCP server running inside FastAPI (no separate process)
- Tool registration and discovery
- Input validation and error handling for AI-callable tools
- Tool result formatting (structured JSON for agent consumption)
- Integration with existing SQLModel database layer

## What This Skill Does NOT Do
- Frontend development (use frontend-ui-builder)
- Database models/migrations (use database-sqlmodel-builder)
- API endpoint creation (use fastapi-backend-builder)
- Authentication logic (use auth-builder)
- AI agent/LLM configuration (handled in agent setup)

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, DB session, routes, auth patterns |
| **Conversation** | Which tools to expose, what parameters, what actions |
| **Skill References** | `references/patterns.md` for MCP tool patterns |
| **AGENT.md** | Section 16 for tool specifications |

---

## Workflow

1. **Define tool schema** — name, description, parameters (typed), return format
2. **Implement tool function** — receives validated params, operates on DB, returns structured result
3. **Register tool** — add to MCP server tool registry
4. **Handle errors** — task not found, invalid input, DB errors → friendly message strings
5. **Test independently** — each tool tested without LLM dependency
6. **Integrate** — connect tool registry to AI agent's tool-calling interface

---

## Domain Standards

### Must Follow
- Every tool has: name, description, parameter schema, return schema
- All tool functions receive `user_id` for ownership isolation
- Tools operate on the database directly (reuse existing SQLModel session)
- Return structured dicts: `{"task_id": int, "status": str, "title": str}`
- Error responses are friendly strings (consumed by AI, shown to user)
- Tools are stateless — no tool holds conversation context
- Type hints on all parameters and return values

### Must Avoid
- Tools that bypass user ownership checks
- Raw exception propagation (catch and return friendly message)
- Tools that depend on LLM state (tools are pure functions)
- Hardcoded user IDs or task IDs in tool logic
- Side effects beyond the intended DB operation

---

## Key Patterns

### Tool Definition Pattern
```python
from typing import Optional

# Tool schema (used by AI agent for tool selection)
TOOLS = [
    {
        "name": "add_task",
        "description": "Add a new todo task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Optional task description"},
            },
            "required": ["title"],
        },
    },
]
```

### Tool Implementation Pattern
```python
from sqlmodel import Session, select
from backend.models import Task

def add_task(session: Session, user_id: str, title: str, description: str | None = None) -> dict:
    """Add a new task. Returns confirmation with task details."""
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
```

### Tool Error Handling Pattern
```python
def complete_task(session: Session, user_id: str, task_id: int) -> dict:
    """Mark a task as complete."""
    task = session.get(Task, task_id)
    if not task:
        return {"status": "error", "message": f"Task {task_id} not found"}
    if task.user_id != user_id:
        return {"status": "error", "message": f"Task {task_id} not found"}
    task.completed = True
    session.commit()
    return {
        "task_id": task.id,
        "title": task.title,
        "status": "completed",
        "message": f"Task '{task.title}' marked as complete"
    }
```

### Tool Dispatcher Pattern
```python
def execute_tool(tool_name: str, session: Session, user_id: str, **kwargs) -> dict:
    """Central dispatcher — routes tool calls to implementations."""
    tools = {
        "add_task": add_task,
        "list_tasks": list_tasks,
        "complete_task": complete_task,
        "delete_task": delete_task,
        "update_task": update_task,
    }
    if tool_name not in tools:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}
    try:
        return tools[tool_name](session=session, user_id=user_id, **kwargs)
    except Exception as e:
        return {"status": "error", "message": f"Tool error: {str(e)}"}
```

### OpenAI Function Calling Integration
```python
import json
from openai import OpenAI

# Tools formatted for OpenAI API
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"],
        },
    }
    for tool in TOOLS
]

# Process tool calls from OpenAI response
def process_tool_calls(response, session: Session, user_id: str) -> list[dict]:
    """Execute tool calls from LLM response."""
    results = []
    for tool_call in response.choices[0].message.tool_calls or []:
        args = json.loads(tool_call.function.arguments)
        result = execute_tool(tool_call.function.name, session, user_id, **args)
        results.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "content": json.dumps(result),
        })
    return results
```

---

## Tool Specifications (Phase III)

| Tool | Parameters | Returns |
|------|-----------|---------|
| `add_task` | title (required), description (optional) | {task_id, status, title, message} |
| `list_tasks` | status? (all/pending/completed) | [{id, title, completed, description}...] |
| `complete_task` | task_id | {task_id, status, title, message} |
| `delete_task` | task_id | {task_id, status, title, message} |
| `update_task` | task_id, title?, description? | {task_id, status, title, message} |

All tools implicitly receive `user_id` from the authenticated session.

---

## Output Checklist

- [ ] All tools have name, description, and parameter schema
- [ ] All tool functions receive user_id for ownership isolation
- [ ] Structured dict return format on every tool
- [ ] Friendly error messages (not raw exceptions)
- [ ] Each tool independently testable (no LLM dependency)
- [ ] Tool dispatcher routes calls correctly
- [ ] OpenAI function calling format exported
- [ ] No hardcoded values

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/patterns.md` | MCP tool patterns, testing, integration |
