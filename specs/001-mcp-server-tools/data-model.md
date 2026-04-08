# Data Model: MCP Server + Tools

**Feature**: 001-mcp-server-tools | **Date**: 2026-04-07

## Entities

### Task (Existing — No Changes)

Reused as-is from `backend/models.py`.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | int (PK) | auto-increment | Used as task_id in tool params |
| user_id | str | indexed, required | Ownership isolation key |
| title | str | 1-200 chars, required | Primary display field |
| description | str? | 0-1000 chars, optional | Secondary detail |
| completed | bool | default False, indexed | Toggle via complete_task |
| created_at | datetime | auto UTC | Immutable |
| updated_at | datetime | auto UTC | Updated on changes |

### Tool Result (Runtime — Not Persisted)

Returned by every tool function. Not a database entity.

| Field | Type | Present In | Notes |
|-------|------|-----------|-------|
| task_id | int | add, complete, delete, update | The affected task |
| title | str | add, complete, delete, update | Task title for confirmation |
| status | str | all tools | "created", "completed", "deleted", "updated", "success", "error" |
| message | str | all tools | Human-readable confirmation or error |
| tasks | list[dict] | list_tasks only | Array of task objects |
| count | int | list_tasks only | Number of tasks returned |

## Relationships

- Tool functions → Task: read/write via SQLModel Session
- Dispatcher → Tool functions: lookup by name in TOOL_MAP dict
- No new database tables, foreign keys, or migrations needed

## State Transitions

```
Task.completed: False → True  (via complete_task, idempotent)
Task lifecycle:  created → [updated]* → completed → [deleted]
                 created → [updated]* → deleted
```

## No Schema Changes

This feature adds no database tables, columns, or migrations. All operations use the existing Task table.
