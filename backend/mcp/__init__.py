"""MCP tool server for AI agent integration.

Uses Official MCP SDK (FastMCP) for tool definitions.
Tool implementations in tools.py, dispatching in dispatcher.py.

Ref: specs/001-mcp-server-tools/plan.md
Tasks: T042, T059
"""

from backend.mcp.dispatcher import execute_tool, process_tool_calls
from backend.mcp.schemas import TOOL_SCHEMAS
from backend.mcp.server import mcp_server

__all__ = ["TOOL_SCHEMAS", "execute_tool", "process_tool_calls", "mcp_server"]
