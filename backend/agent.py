"""AI agent for todo management via natural language.

Implements a tool-calling loop using the OpenAI chat completions API.
The agent uses MCP tools from backend/mcp/ to manage tasks.

Ref: specs/002-ai-chat-endpoint/plan.md — Component 2
Task: T052
"""

import json
import os

from openai import OpenAI
from sqlmodel import Session

from backend.mcp.dispatcher import execute_tool
from backend.mcp.schemas import TOOL_SCHEMAS

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


def run_agent(
    messages: list[dict],
    session: Session,
    user_id: str,
) -> tuple[str, list[dict]]:
    """Run the AI agent with tool-calling loop.

    Args:
        messages: Conversation history (system + user/assistant messages).
        session: SQLModel database session for tool execution.
        user_id: Authenticated user's ID for tool ownership.

    Returns:
        Tuple of (response_text, tool_calls_made).
        tool_calls_made is a list of dicts with tool, args, result.

    Task: T052 | FR-006, FR-007, FR-008, FR-009
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return FALLBACK_MESSAGE, []

    try:
        client = OpenAI(api_key=api_key)
    except Exception:
        return FALLBACK_MESSAGE, []

    tool_calls_made: list[dict] = []

    try:
        for _ in range(10):  # max iterations to prevent infinite loops
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=TOOL_SCHEMAS,
            )

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" or choice.message.tool_calls:
                # Agent wants to call tools
                assistant_msg = {
                    "role": "assistant",
                    "content": choice.message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in choice.message.tool_calls
                    ],
                }
                messages.append(assistant_msg)

                for tc in choice.message.tool_calls:
                    args = tc.function.arguments
                    if isinstance(args, str):
                        args = json.loads(args)

                    result = execute_tool(
                        tc.function.name, session, user_id, **args
                    )

                    tool_calls_made.append({
                        "tool": tc.function.name,
                        "args": args,
                        "result": result,
                    })

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    })
            else:
                # Agent produced a text response — done
                return choice.message.content or "", tool_calls_made

        # Exhausted iterations
        return FALLBACK_MESSAGE, tool_calls_made

    except Exception:
        return FALLBACK_MESSAGE, tool_calls_made
