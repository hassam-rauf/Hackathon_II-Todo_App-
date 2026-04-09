# ADR-005: MCP Protocol for AI-Tool Interface

- **Status:** Accepted
- **Date:** 2026-04-07
- **Feature:** 001-mcp-server-tools (Phase III Cycle 1)
- **Context:** Phase III adds an AI chatbot that manages todos via natural language. The AI agent needs to call application functions (add, list, complete, delete, update tasks) when the user sends a chat message. We need to decide: (1) how tools are hosted and invoked, (2) what format tool schemas use, (3) how tools communicate results and errors back to the agent.

## Decision

- **Tool hosting**: In-process — tools are plain Python functions inside `backend/mcp/tools.py`, called directly by a central dispatcher within the FastAPI process. No separate MCP server process, no IPC, no network transport.
- **Schema format**: OpenAI function calling format (`{"type": "function", "function": {"name", "description", "parameters"}}`) — matches what `client.chat.completions.create(tools=...)` expects.
- **Result format**: Structured dicts with `status`, `message`, and operation-specific fields. Errors return `{"status": "error", "message": "friendly text"}` — no exceptions raised from tools.
- **Security pattern**: Ownership violations return "Task not found" (same as non-existent task) — no information leakage.
- **Idempotency**: Completing an already-completed task returns success, not an error.

## Consequences

### Positive

- Simplest possible integration — no process management, no serialization overhead, direct SQLModel session access
- Zero transformation needed when connecting to OpenAI Agents SDK in Cycle 2 — schemas are already in the right format
- Tools are independently testable without LLM — call functions directly with pytest
- Uniform interface — agent always gets a dict, always checks `status` field
- Extractable to a real MCP server later if the architecture needs to scale (functions stay the same, only transport changes)
- Security by design — ownership check baked into every tool, no leakage

### Negative

- Tight coupling to FastAPI process — tools can't run independently or be shared with other services
- OpenAI-specific schema format — switching to a different LLM provider requires schema transformation
- Dict returns are untyped — no compile-time guarantees on return shape (mitigated by comprehensive tests)
- In-process means a tool failure could affect the FastAPI server (mitigated by dispatcher try/except)

## Alternatives Considered

**Alternative A: Separate MCP Server Process (stdio transport)**
- Tools run as a standalone process, communicate via stdio with the MCP SDK
- Pros: Language-agnostic, process isolation, official MCP pattern
- Rejected: Adds process management, IPC serialization, startup latency — overkill for a monolith where agent and tools share the same Python process

**Alternative B: Direct Function Calls (No MCP/Schema Layer)**
- Agent code directly imports and calls tool functions, no schema registry or dispatcher
- Pros: Even simpler, fewer files
- Rejected: No tool discovery mechanism for the LLM, no schema validation, no central error handling. Would need to be rebuilt when connecting to OpenAI anyway

**Alternative C: HTTP-based Tool Endpoints**
- Each tool exposed as a separate API endpoint, agent calls via HTTP
- Pros: Tools accessible from anywhere, standard REST
- Rejected: Unnecessary network hop within the same process, duplicates existing task CRUD endpoints, adds latency

## References

- Feature Spec: specs/001-mcp-server-tools/spec.md
- Implementation Plan: specs/001-mcp-server-tools/plan.md
- Research: specs/001-mcp-server-tools/research.md (R1-R4)
- Related ADRs: None (first Phase III ADR)
- AGENT.md Section 16: MCP Server Transport — recommends in-process for this project
