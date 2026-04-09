"""AI agent for todo management using OpenAI Agents SDK.

Uses the official Agents SDK (Agent + Runner) with function_tool decorators.
Tools route through the MCP dispatcher (execute_tool) so the agent flow is:
  Agent → MCP dispatcher → MCP tool implementations → DB

Ref: specs/002-ai-chat-endpoint/plan.md — Component 2
Task: T052
"""

import json
import os
from dataclasses import dataclass

from agents import Agent, Runner, function_tool, RunContextWrapper
from sqlmodel import Session

from backend.mcp.dispatcher import execute_tool

MAX_HISTORY_MESSAGES = 50

SYSTEM_PROMPT = (
    "You are a helpful todo assistant. You help users manage their tasks "
    "using the available tools. When a user asks to add, list, complete, "
    "delete, or update tasks, use the appropriate tool. After calling a tool, "
    "confirm the action in a friendly, concise response. If the user's message "
    "doesn't require a tool (e.g., a greeting), respond conversationally. "
    "Keep responses short and helpful."
)

FALLBACK_MESSAGE = "I'm having trouble right now. Please try again shortly."


@dataclass
class AgentContext:
    """Context passed to all agent tools via RunContextWrapper."""

    session: Session
    user_id: str


@function_tool
def add_task(
    ctx: RunContextWrapper[AgentContext], title: str, description: str = ""
) -> str:
    """Add a new todo task. Use when user says 'add', 'create', 'remember', 'new task'."""
    result = execute_tool(
        "add_task", ctx.context.session, ctx.context.user_id,
        title=title, description=description,
    )
    return json.dumps(result)


@function_tool
def list_tasks(
    ctx: RunContextWrapper[AgentContext], status: str = "all"
) -> str:
    """List tasks, optionally filtered. Use when user says 'show', 'list', 'what tasks', 'pending'."""
    result = execute_tool(
        "list_tasks", ctx.context.session, ctx.context.user_id,
        status=status,
    )
    return json.dumps(result)


@function_tool
def complete_task(
    ctx: RunContextWrapper[AgentContext], task_id: int
) -> str:
    """Mark a task as done. Use when user says 'done', 'complete', 'finished'."""
    result = execute_tool(
        "complete_task", ctx.context.session, ctx.context.user_id,
        task_id=task_id,
    )
    return json.dumps(result)


@function_tool
def delete_task(
    ctx: RunContextWrapper[AgentContext], task_id: int
) -> str:
    """Delete a task. Use when user says 'delete', 'remove', 'get rid of'."""
    result = execute_tool(
        "delete_task", ctx.context.session, ctx.context.user_id,
        task_id=task_id,
    )
    return json.dumps(result)


@function_tool
def update_task(
    ctx: RunContextWrapper[AgentContext],
    task_id: int,
    title: str = "",
    description: str = "",
) -> str:
    """Update a task's title or description. Use when user says 'change', 'rename', 'update'."""
    result = execute_tool(
        "update_task", ctx.context.session, ctx.context.user_id,
        task_id=task_id, title=title or None, description=description or None,
    )
    return json.dumps(result)


# Agent definition using OpenAI Agents SDK
todo_agent = Agent(
    name="Todo Assistant",
    instructions=SYSTEM_PROMPT,
    tools=[add_task, list_tasks, complete_task, delete_task, update_task],
    model="gpt-4o-mini",
)


def run_agent(
    messages: list[dict],
    session: Session,
    user_id: str,
) -> tuple[str, list[dict]]:
    """Run the AI agent with tool-calling loop via Agents SDK.

    Args:
        messages: Conversation history (system + user/assistant messages).
        session: SQLModel database session for tool execution.
        user_id: Authenticated user's ID for tool ownership.

    Returns:
        Tuple of (response_text, tool_calls_made).

    Task: T052 | FR-006, FR-007, FR-008, FR-009
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return FALLBACK_MESSAGE, []

    context = AgentContext(session=session, user_id=user_id)

    # Build input from messages (skip system prompt — agent has its own instructions)
    input_messages = []
    for msg in messages:
        if msg["role"] == "system":
            continue
        input_messages.append({
            "role": msg["role"],
            "content": msg["content"],
        })

    try:
        result = Runner.run_sync(
            starting_agent=todo_agent,
            input=input_messages,
            context=context,
            max_turns=10,
        )

        # Extract response text
        response_text = ""
        tool_calls_made: list[dict] = []

        # Get the final output from the result
        items = result.to_input_list()
        for item in items:
            # Extract assistant messages and tool calls
            if hasattr(item, "role") and getattr(item, "role", None) == "assistant":
                content = getattr(item, "content", None)
                if content and isinstance(content, str):
                    response_text = content
                elif content and isinstance(content, list):
                    for part in content:
                        if hasattr(part, "text"):
                            response_text = part.text

            # Extract tool use information
            if hasattr(item, "type") and getattr(item, "type", None) == "function_call":
                name = getattr(item, "name", "")
                args_str = getattr(item, "arguments", "{}")
                try:
                    args = json.loads(args_str) if isinstance(args_str, str) else args_str
                except json.JSONDecodeError:
                    args = {}
                tool_calls_made.append({
                    "tool": name,
                    "args": args,
                    "result": {},
                })

            if hasattr(item, "type") and getattr(item, "type", None) == "function_call_output":
                output_str = getattr(item, "output", "{}")
                try:
                    output = json.loads(output_str) if isinstance(output_str, str) else output_str
                except json.JSONDecodeError:
                    output = {}
                if tool_calls_made:
                    tool_calls_made[-1]["result"] = output

        if not response_text:
            # Fallback: try to get the last text from output
            response_text = str(result.final_output_as(str, raise_if_incorrect_type=False) or FALLBACK_MESSAGE)

        return response_text, tool_calls_made

    except Exception:
        return FALLBACK_MESSAGE, []
