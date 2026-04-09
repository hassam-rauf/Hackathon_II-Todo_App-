# ADR-006: Stateless Chat Architecture

- **Status:** Accepted
- **Date:** 2026-04-08
- **Feature:** 002-ai-chat-endpoint (Phase III Cycle 2)
- **Context:** Phase III Cycle 2 adds an AI chat endpoint where users send natural language messages and an AI agent manages their todos via MCP tools. The system needs to handle multi-turn conversations with context — but the backend must remain horizontally scalable (any server instance handles any request). We need to decide: (1) how conversation state is managed across requests, (2) what messages are persisted and how history is bounded, (3) how the system behaves when the LLM provider is unavailable.

## Decision

- **State management**: Fully stateless — zero server-side session state. Every request loads conversation history from the database, processes the message, stores results, and returns. Any server instance can handle any request.
- **Persistence strategy**: Store only "user" and "assistant" role messages in the database. Tool call/result messages are transient (used during the agent loop, not persisted). Conversation and Message are separate SQLModel tables with user_id ownership isolation.
- **History bounding**: Cap conversation history at 50 most recent messages (configurable constant `MAX_HISTORY_MESSAGES`). Older messages remain in DB but are not sent to the LLM.
- **Data model**: Two new entities — Conversation (id, user_id, created_at, updated_at) and Message (id, conversation_id, user_id, role, content, created_at). Both indexed on user_id for ownership queries.
- **Graceful degradation**: If `OPENAI_API_KEY` is not set or the LLM service is unavailable, the endpoint returns a static fallback message instead of crashing. Development and testing proceed without a key (tests mock the OpenAI client).
- **SDK choice**: Use the base `openai` Python package (`client.chat.completions.create(tools=...)`) directly, not the higher-level OpenAI Agents SDK. The Agents SDK adds framework abstractions (Agent class, Runner, handoffs) designed for complex multi-agent workflows. Our use case is a single agent with a simple tool-calling loop — the base SDK provides full control with fewer failure modes. This deviates from constitution II ("AI Framework: OpenAI Agents SDK") with justification: the core capability (tool calling) is in the base SDK; the Agents SDK can be adopted later if multi-agent workflows are needed. See research.md R1 for alternatives considered.

## Consequences

### Positive

- Horizontally scalable — no sticky sessions, no shared memory, any server handles any request
- Simple deployment — no Redis/Memcached session store needed, just the existing Neon PostgreSQL
- Crash-safe — server restart loses zero state, all conversations recoverable from DB
- Clean conversation history — only human-readable messages (user + assistant) are stored, no complex tool call JSON in the DB
- Token-efficient — 50-message cap prevents runaway costs on long conversations while providing ~25 exchanges of context
- Development-friendly — entire system buildable and testable without an API key
- Ownership isolation baked in — user_id on both Conversation and Message prevents cross-user data access

### Negative

- Database round-trip on every request — each chat message triggers a SELECT for conversation + history before processing (mitigated: queries are indexed, data is small)
- Lost tool context — tool call/result messages are not persisted, so if the agent needs to reference a prior tool interaction across requests, it only has the assistant's summary (mitigated: assistant responses describe tool actions in natural language)
- History truncation — conversations longer than 50 messages lose earlier context from the LLM's perspective (mitigated: configurable cap, old messages still in DB for display)
- No streaming — stateless request/response model returns the full response at once; streaming would require a different architecture (acceptable: out of scope per spec)

## Alternatives Considered

**Alternative A: Server-Side Session State (In-Memory or Redis)**
- Keep conversation history in memory or Redis, load on connection
- Pros: Faster per-request (no DB load), natural fit for WebSocket streaming
- Rejected: Adds infrastructure (Redis), requires sticky sessions or shared state, server restart loses state unless Redis is persistent, premature complexity for a todo chatbot

**Alternative B: Store All Message Types (Including Tool Calls)**
- Persist tool_call and tool_result messages alongside user/assistant messages
- Pros: Complete audit trail, can replay exact agent reasoning
- Rejected: Doubles storage, complicates the message schema (tool messages have nested JSON), makes conversation history display messy, tool messages are implementation details not needed for context

**Alternative C: No History Cap (Send Full Conversation)**
- Send all messages to the LLM every request
- Pros: Complete context always available
- Rejected: Risks hitting token limits on long conversations, linearly increasing cost per message, unnecessary for task management where recent context is sufficient

**Alternative D: Summarize Old Messages**
- When history exceeds cap, use an LLM call to summarize older messages into a single context message
- Pros: Retains information from old messages in compressed form
- Rejected: Adds an extra LLM call (cost + latency), complex implementation, premature optimization for a todo chatbot where 50 messages of context is ample

## References

- Feature Spec: specs/002-ai-chat-endpoint/spec.md
- Implementation Plan: specs/002-ai-chat-endpoint/plan.md
- Research: specs/002-ai-chat-endpoint/research.md (R1-R5)
- Data Model: specs/002-ai-chat-endpoint/data-model.md
- Related ADRs: ADR-005 (MCP Protocol for AI-Tool Interface) — defines the tool interface this architecture consumes
