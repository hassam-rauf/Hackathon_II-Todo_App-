"""OpenAI function calling schemas for MCP tools.

Ref: specs/001-mcp-server-tools/contracts/tools-api.md
Task: T043
"""

TOOL_SCHEMAS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": (
                "Add a new todo task for the user. "
                "Use when user says 'add', 'create', 'remember', 'new task'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (1-200 chars)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": (
                "List all tasks or filter by status. "
                "Use when user says 'show', 'list', 'what tasks', 'pending'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status (default: all)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": (
                "Mark a task as completed. "
                "Use when user says 'done', 'complete', 'finished', 'mark as done'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": (
                "Delete a task permanently. "
                "Use when user says 'delete', 'remove', 'get rid of'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": (
                "Update a task's title or description. "
                "Use when user says 'change', 'rename', 'update', 'edit'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task",
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
]
