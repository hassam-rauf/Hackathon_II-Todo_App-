"""Central dispatcher for MCP tool calls.

Routes tool calls by name to the correct function.
Handles unknown tools and unexpected exceptions gracefully.

Ref: specs/001-mcp-server-tools/contracts/tools-api.md
Tasks: T049, T050
"""

import json

from sqlmodel import Session

from backend.mcp.tools import (
    add_task,
    complete_task,
    delete_task,
    list_tasks,
    update_task,
)

TOOL_MAP: dict = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}


def execute_tool(
    tool_name: str,
    session: Session,
    user_id: str,
    **kwargs: object,
) -> dict:
    """Execute an MCP tool by name with given arguments.

    Task: T049 | FR-008, FR-009
    """
    if tool_name not in TOOL_MAP:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}

    try:
        return TOOL_MAP[tool_name](session=session, user_id=user_id, **kwargs)
    except Exception as e:
        return {"status": "error", "message": f"Something went wrong: {e!s}"}


def process_tool_calls(
    tool_calls: list,
    session: Session,
    user_id: str,
) -> list[dict]:
    """Process OpenAI tool_calls and return results for the message array.

    Task: T050 | FR-008
    """
    results: list[dict] = []

    for tc in tool_calls:
        args = tc.function.arguments
        if isinstance(args, str):
            args = json.loads(args)

        result = execute_tool(tc.function.name, session, user_id, **args)

        results.append({
            "tool_call_id": tc.id,
            "role": "tool",
            "content": json.dumps(result),
        })

    return results
