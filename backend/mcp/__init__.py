"""MCP tool server for AI agent integration.

Ref: specs/001-mcp-server-tools/plan.md
Tasks: T042, T059
"""

from backend.mcp.dispatcher import execute_tool, process_tool_calls
from backend.mcp.schemas import TOOL_SCHEMAS

__all__ = ["TOOL_SCHEMAS", "execute_tool", "process_tool_calls"]
