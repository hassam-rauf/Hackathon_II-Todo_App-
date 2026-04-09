# Tool API Contracts: MCP Server + Tools

**Feature**: 001-mcp-server-tools | **Date**: 2026-04-07

## Tool Schemas (OpenAI Function Calling Format)

### add_task

```json
{
  "type": "function",
  "function": {
    "name": "add_task",
    "description": "Add a new todo task for the user",
    "parameters": {
      "type": "object",
      "properties": {
        "title": { "type": "string", "description": "Task title (1-200 chars)" },
        "description": { "type": "string", "description": "Optional task description" }
      },
      "required": ["title"]
    }
  }
}
```

**Returns**: `{ "task_id": int, "title": str, "status": "created", "message": str }`

### list_tasks

```json
{
  "type": "function",
  "function": {
    "name": "list_tasks",
    "description": "List all tasks or filter by status",
    "parameters": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["all", "pending", "completed"],
          "description": "Filter tasks by status (default: all)"
        }
      }
    }
  }
}
```

**Returns**: `{ "tasks": [{ "id": int, "title": str, "completed": bool, "description": str }], "count": int, "status": "success", "message": str }`

### complete_task

```json
{
  "type": "function",
  "function": {
    "name": "complete_task",
    "description": "Mark a task as completed",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": { "type": "integer", "description": "ID of the task to complete" }
      },
      "required": ["task_id"]
    }
  }
}
```

**Returns**: `{ "task_id": int, "title": str, "status": "completed", "message": str }`

### delete_task

```json
{
  "type": "function",
  "function": {
    "name": "delete_task",
    "description": "Delete a task permanently",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": { "type": "integer", "description": "ID of the task to delete" }
      },
      "required": ["task_id"]
    }
  }
}
```

**Returns**: `{ "task_id": int, "title": str, "status": "deleted", "message": str }`

### update_task

```json
{
  "type": "function",
  "function": {
    "name": "update_task",
    "description": "Update a task's title or description",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": { "type": "integer", "description": "ID of the task to update" },
        "title": { "type": "string", "description": "New title" },
        "description": { "type": "string", "description": "New description" }
      },
      "required": ["task_id"]
    }
  }
}
```

**Returns**: `{ "task_id": int, "title": str, "status": "updated", "message": str }`

## Dispatcher Contract

### execute_tool

```
execute_tool(tool_name: str, session: Session, user_id: str, **kwargs) → dict
```

- Valid tool_name → routes to function, returns tool result dict
- Unknown tool_name → `{ "status": "error", "message": "Unknown tool: {name}" }`
- Exception in tool → `{ "status": "error", "message": "Something went wrong: {error}" }`

### process_tool_calls

```
process_tool_calls(tool_calls: list, session: Session, user_id: str) → list[dict]
```

- Input: OpenAI `tool_calls` array from `response.choices[0].message.tool_calls`
- Output: list of `{ "tool_call_id": str, "role": "tool", "content": json_string }`
- Each content is JSON-serialized tool result dict

## Error Response Contract

All error responses follow this shape:

```json
{ "status": "error", "message": "Human-readable error description" }
```

Error messages:
- Task not found: `"Task {task_id} not found"`
- Unknown tool: `"Unknown tool: {tool_name}"`
- Unexpected error: `"Something went wrong: {error_message}"`
- Empty title: `"Title is required"`
