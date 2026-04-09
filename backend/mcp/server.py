"""MCP Server using Official MCP SDK (FastMCP).

Defines 5 task management tools using @mcp.tool() decorators.
Tool implementations delegate to backend.mcp.tools for DB operations.

Ref: specs/001-mcp-server-tools/spec.md
"""

from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP(
    "todo-mcp-server",
    instructions=(
        "MCP server for todo task management. Provides tools to "
        "add, list, complete, delete, and update tasks."
    ),
)


@mcp_server.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Add a new todo task for the user.

    Use when user says 'add', 'create', 'remember', 'new task'.
    """
    from backend.mcp.tools import add_task as _add_task
    from backend.db import get_session

    session = next(get_session())
    try:
        return _add_task(session=session, user_id=user_id, title=title, description=description)
    finally:
        session.close()


@mcp_server.tool()
def list_tasks(user_id: str, status: str = "all") -> dict:
    """List all tasks or filter by status (all/pending/completed).

    Use when user says 'show', 'list', 'what tasks', 'pending'.
    """
    from backend.mcp.tools import list_tasks as _list_tasks
    from backend.db import get_session

    session = next(get_session())
    try:
        return _list_tasks(session=session, user_id=user_id, status=status)
    finally:
        session.close()


@mcp_server.tool()
def complete_task(user_id: str, task_id: int) -> dict:
    """Mark a task as completed.

    Use when user says 'done', 'complete', 'finished', 'mark as done'.
    """
    from backend.mcp.tools import complete_task as _complete_task
    from backend.db import get_session

    session = next(get_session())
    try:
        return _complete_task(session=session, user_id=user_id, task_id=task_id)
    finally:
        session.close()


@mcp_server.tool()
def delete_task(user_id: str, task_id: int) -> dict:
    """Delete a task permanently.

    Use when user says 'delete', 'remove', 'get rid of'.
    """
    from backend.mcp.tools import delete_task as _delete_task
    from backend.db import get_session

    session = next(get_session())
    try:
        return _delete_task(session=session, user_id=user_id, task_id=task_id)
    finally:
        session.close()


@mcp_server.tool()
def update_task(
    user_id: str, task_id: int, title: str = "", description: str = ""
) -> dict:
    """Update a task's title or description.

    Use when user says 'change', 'rename', 'update', 'edit'.
    """
    from backend.mcp.tools import update_task as _update_task
    from backend.db import get_session

    session = next(get_session())
    try:
        return _update_task(
            session=session,
            user_id=user_id,
            task_id=task_id,
            title=title or None,
            description=description or None,
        )
    finally:
        session.close()
