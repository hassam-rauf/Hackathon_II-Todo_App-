# Research: AI Agent + Chat Endpoint

**Feature**: 002-ai-chat-endpoint | **Date**: 2026-04-08

## Research Items

### R1: OpenAI SDK vs Agents SDK

**Decision**: Use the base `openai` Python package with `client.chat.completions.create(tools=...)` directly.

**Rationale**: The Agents SDK adds a framework layer (Agent class, Runner, handoffs) designed for complex multi-agent workflows. Our use case is a single agent with tool calling — the base SDK handles this perfectly with a simple loop: call → check for tool_calls → execute → call again.

**Alternatives considered**:
- OpenAI Agents SDK — overkill for single-agent tool calling, adds framework dependency
- LangChain — heavy dependency, unnecessary abstraction for simple tool calling

### R2: Message Storage Strategy

**Decision**: Store only "user" and "assistant" role messages. Tool call/result messages are transient.

**Rationale**: The conversation history that needs to persist is what was said (user) and what was replied (assistant). Tool messages are execution details — they're reconstructed during each agent run if the agent needs tools again. This halves DB storage and keeps the schema clean.

**Alternatives considered**:
- Store all messages including tool calls — doubles storage, complicates history display, tool messages have complex JSON structure
- Store tool calls as metadata on assistant messages — adds complexity to the message schema

### R3: API Key Handling

**Decision**: Check for `OPENAI_API_KEY` at runtime. If missing, return a static fallback message. No crash.

**Rationale**: User hasn't purchased the API key yet. Development and testing must work without it. Tests mock the OpenAI client entirely.

**Alternatives considered**:
- Fail fast on startup if no key — blocks all development until key is purchased
- Require key in .env for tests — unnecessary, tests mock the client

### R4: Conversation History Limit

**Decision**: Cap at 50 most recent messages (configurable constant `MAX_HISTORY_MESSAGES = 50`).

**Rationale**: GPT-4o-mini has ~128K context window, but sending full history of a long conversation wastes tokens and money. 50 messages provides ~25 exchanges of context — sufficient for task management. Configurable if needs change.

**Alternatives considered**:
- No limit — risks hitting token limits, expensive on long conversations
- Token-based counting — adds complexity (need tiktoken), premature optimization
- Summarize old messages — adds LLM call overhead, complex to implement

### R5: Mocking Strategy for Tests

**Decision**: Use `unittest.mock.patch` to mock `openai.OpenAI` client. Return `SimpleNamespace` objects mimicking OpenAI response structure.

**Rationale**: Tests must run without API key. Mocking at the client level lets us test the full flow (endpoint → agent → tool dispatch → response) without hitting the real API. SimpleNamespace is lightweight and matches the attribute-access pattern of OpenAI responses.

**Alternatives considered**:
- VCR/cassette recording — requires initial real API calls, complex setup
- Custom fake client class — more code than simple mock patches
