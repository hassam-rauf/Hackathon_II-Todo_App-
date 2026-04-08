# Research: MCP Server + Tools

**Feature**: 001-mcp-server-tools | **Date**: 2026-04-07

## Research Items

### R1: MCP Tool Integration Pattern (In-Process vs Server)

**Decision**: In-process — tools are plain Python functions called directly by the dispatcher inside FastAPI.

**Rationale**: The official MCP SDK supports both transport modes. For a monolith where the AI agent and tools run in the same process, in-process is simpler. No IPC overhead, no serialization at the tool boundary, direct access to the SQLModel session.

**Alternatives considered**:
- Separate MCP server process (stdio transport) — adds complexity, process management, serialization overhead. Better for multi-language or distributed setups.
- HTTP-based MCP server — unnecessary network hop when tools are in the same process.

### R2: Tool Return Format

**Decision**: Structured dicts with `status`, `message`, and operation-specific fields (`task_id`, `title`, `tasks`, `count`).

**Rationale**: The AI agent needs structured data to understand what happened, plus a human-readable message to relay to the user. Dicts are JSON-serializable and compatible with OpenAI's tool result format.

**Alternatives considered**:
- Pydantic models — adds overhead for internal tool returns that are immediately serialized to JSON. Dicts are simpler and sufficient.
- Plain strings — loses structured data the agent might need for follow-up tool calls.

### R3: Error Handling Strategy

**Decision**: Tools return error dicts (`{"status": "error", "message": "..."}`) instead of raising exceptions. Dispatcher wraps in try/except as safety net.

**Rationale**: Tools are called by an AI agent loop, not by HTTP request handlers. Exceptions would need to be caught at the agent level anyway. Returning error dicts keeps the interface uniform — the agent always gets a dict, always checks `status`.

**Alternatives considered**:
- Custom ToolError exception class — adds a class hierarchy for what is essentially a dict with status="error". Over-engineering.
- HTTPException — wrong layer. Tools aren't HTTP endpoints.

### R4: OpenAI Function Calling Schema Format

**Decision**: Use OpenAI's function calling format (`{"type": "function", "function": {"name", "description", "parameters"}}`) for tool schemas.

**Rationale**: Constitution mandates OpenAI Agents SDK. This format is what `client.chat.completions.create(tools=...)` expects. Using it from the start means zero transformation needed in Cycle 2.

**Alternatives considered**:
- MCP SDK native schema format — would need transformation to OpenAI format. Extra code, no benefit.
- Custom schema format — non-standard, requires custom parsing.

### R5: Testing Strategy

**Decision**: pytest with SQLite in-memory engine, sync sessions. Same pattern as existing `test_tasks_api.py`.

**Rationale**: Tools use sync SQLModel sessions (matching existing backend pattern). SQLite in-memory is fast, isolated, and already proven in the project's test suite (63 tests passing).

**Alternatives considered**:
- Async tests with async SQLite — adds complexity, existing backend uses sync sessions.
- Real Neon DB for tests — slow, requires network, environment-dependent.
