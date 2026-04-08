# Implementation Plan: AI Agent + Chat Endpoint

**Branch**: `002-ai-chat-endpoint` | **Date**: 2026-04-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-ai-chat-endpoint/spec.md`

## Summary

Add a stateless chat endpoint (POST /api/{user_id}/chat) that connects an OpenAI-powered AI agent to the MCP tools from Cycle 1. Introduce Conversation and Message SQLModel tables for persistent chat history in Neon DB. The agent uses a system prompt for todo management, selects tools based on user intent, and returns natural language responses. All conversation state lives in the database — the server holds zero state.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, OpenAI SDK (openai package)
**Storage**: Neon Serverless PostgreSQL (production), SQLite in-memory (tests)
**Testing**: pytest with mocked OpenAI responses, SQLite in-memory
**Target Platform**: Linux server (WSL2 development)
**Project Type**: Web application (monorepo: backend/ + frontend/)
**Performance Goals**: Chat responses within 5 seconds (dominated by LLM latency)
**Constraints**: Stateless endpoint, user isolation, API key optional (fallback message), max 50 messages per conversation history
**Scale/Scope**: 2 new models, 1 new endpoint, 1 agent module, ~300 lines of code, ~150 lines of tests

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Spec → plan in progress |
| II. Tech Stack (Locked) | PASS | FastAPI, SQLModel, OpenAI SDK — all in locked stack |
| III. Code Quality | PASS | Type hints, async endpoint, <50 line functions |
| IV. Testing (Mandatory) | PASS | Mocked LLM responses, happy + error paths |
| V. Security | PASS | User isolation on conversations, no secrets in code, rate limiting noted |
| VI. UI/UX Principles | N/A | Backend-only cycle |
| VII. Architecture | PASS | Stateless, monorepo, smallest diff |
| VIII. Performance | PASS | LLM-bound (<5s), DB queries indexed on user_id |

**GATE RESULT: PASS**

## Project Structure

### Documentation

```text
specs/002-ai-chat-endpoint/
├── spec.md
├── plan.md              # This file
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── chat-api.md
└── checklists/
    └── requirements.md
```

### Source Code

```text
backend/
├── models.py            # MODIFIED — add Conversation, Message models
├── main.py              # MODIFIED — register chat router
├── mcp/                 # existing (Cycle 1, no changes)
│   ├── __init__.py
│   ├── tools.py
│   ├── schemas.py
│   └── dispatcher.py
├── agent.py             # NEW — OpenAI agent config, run_agent function
└── routes/
    ├── tasks.py         # existing (no changes)
    └── chat.py          # NEW — POST /api/{user_id}/chat

tests/
└── backend/
    ├── test_mcp_tools.py   # existing
    ├── test_tasks_api.py   # existing
    ├── test_auth.py        # existing
    └── test_chat.py        # NEW — chat endpoint + agent tests
```

## Design Decisions

### D1: OpenAI SDK Direct (Not Agents SDK Framework)

Use the `openai` Python package's `client.chat.completions.create()` with tools parameter directly, rather than the higher-level Agents SDK framework.

**Rationale**: The Agents SDK adds abstraction layers we don't need for a simple tool-calling loop. Direct SDK gives us full control over the tool-call → result → response cycle. The constitution specifies "OpenAI Agents SDK" but the core capability (tool calling) is in the base SDK. Simpler = fewer failure modes.

### D2: Conversation History Cap at 50 Messages

Load at most 50 recent messages from DB when building the agent's context.

**Rationale**: OpenAI models have token limits. 50 messages (~25 user + 25 assistant) is a reasonable cap that provides good context without exceeding limits. Configurable via constant.

### D3: Graceful Degradation Without API Key

If `OPENAI_API_KEY` is not set, the chat endpoint returns a static fallback message instead of crashing.

**Rationale**: User doesn't have the API key yet. The system must be buildable and testable. Tests use mocked responses, production needs the key.

### D4: Store Only User and Assistant Messages

Store messages with role "user" and "assistant" in the DB. Tool call/result messages are transient (used in the agent loop but not persisted).

**Rationale**: Tool messages are implementation details. The conversation history that matters for context is what the user said and what the agent replied. This keeps the DB schema simple and the history readable.

## Component Design

### Component 1: Database Models (`backend/models.py` — additions)

```
Conversation:
  - id: int (PK, auto)
  - user_id: str (indexed)
  - created_at: datetime (auto UTC)
  - updated_at: datetime (auto UTC)

Message:
  - id: int (PK, auto)
  - conversation_id: int (FK → Conversation.id, indexed)
  - user_id: str (indexed)
  - role: str ("user" | "assistant")
  - content: str (text)
  - created_at: datetime (auto UTC)
```

### Component 2: Agent Module (`backend/agent.py`)

- `SYSTEM_PROMPT`: Constant string instructing the agent to be a todo assistant
- `run_agent(messages, session, user_id) → tuple[str, list[dict]]`: Core agent loop
  1. Call OpenAI with messages + tool schemas
  2. If tool_calls in response → execute via dispatcher → append results → call OpenAI again
  3. Repeat until agent produces a text response (no more tool calls)
  4. Return (response_text, tool_calls_made)
- Handles: missing API key (return fallback), API errors (return friendly message), multi-turn tool calling

### Component 3: Chat Endpoint (`backend/routes/chat.py`)

```
POST /api/{user_id}/chat
Request:  { conversation_id?: int, message: str }
Response: { conversation_id: int, response: str, tool_calls: list }
```

Flow:
1. Validate message (non-empty)
2. If no conversation_id → create new Conversation
3. If conversation_id → load Conversation (verify user ownership)
4. Fetch last 50 messages for this conversation
5. Store user message in DB
6. Build message array: [system_prompt] + [history] + [new user message]
7. Call run_agent()
8. Store assistant response in DB
9. Update conversation.updated_at
10. Return response + tool_calls

### Component 4: Test Suite (`tests/backend/test_chat.py`)

Mock the OpenAI client to return predetermined responses. Test classes:

| Test Class | Tests | Covers |
|------------|-------|--------|
| TestConversationModel | 2 | Create conversation, message relationship |
| TestChatEndpoint | 4 | New conversation, continue existing, empty message, invalid conversation_id |
| TestAgentToolCalling | 3 | Agent calls tool, agent no-tool response, multi-turn tool call |
| TestErrorHandling | 3 | Missing API key fallback, API error fallback, conversation ownership |
| TestConversationPersistence | 2 | Messages survive reload, history loaded correctly |

**Total: ~14 tests**

## Dependency Graph

```
models.py (Conversation, Message) — no new deps
    ↓
agent.py (imports: openai, backend.mcp.dispatcher, backend.mcp.schemas)
    ↓
routes/chat.py (imports: agent.py, models.py, db.py)
    ↓
main.py (imports: routes/chat.py — register router)
    ↓
test_chat.py (imports: all above + mocks)
```

**Build order**: models → agent → routes/chat → main registration → tests

## Implementation Sequence

| Step | File | What | Depends On |
|------|------|------|------------|
| 1 | `backend/pyproject.toml` | Add openai dependency | Nothing |
| 2 | `backend/models.py` | Add Conversation + Message models | Nothing (additive) |
| 3 | `backend/agent.py` | Agent config + run_agent function | models.py, backend/mcp/ |
| 4 | `backend/routes/chat.py` | Chat endpoint | agent.py, models.py |
| 5 | `backend/main.py` | Register chat router | routes/chat.py |
| 6 | `tests/backend/test_chat.py` | ~14 tests with mocked OpenAI | All above |
| 7 | Verify all tests pass | `uv run pytest tests/backend/ -v` | Step 6 |

## New Dependency

- `openai` package — needs to be added to `backend/pyproject.toml`
