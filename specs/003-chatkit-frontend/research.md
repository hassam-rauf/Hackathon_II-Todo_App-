# Research: ChatKit Frontend

**Feature**: 003-chatkit-frontend | **Date**: 2026-04-08

## R1: OpenAI ChatKit vs Custom Components

**Decision**: Custom React components
**Rationale**: OpenAI ChatKit (npm `@openai/chatkit`) is designed to connect directly to OpenAI's API with domain-key authentication. Our architecture uses a custom backend endpoint (`POST /api/{user_id}/chat`) that wraps the OpenAI agent with MCP tool calling. ChatKit cannot be pointed at a custom endpoint without significant modification. Additionally, ChatKit's styling doesn't match our dark space/galaxy theme.
**Alternatives considered**:
- OpenAI ChatKit — rejected: requires domain registration, connects to OpenAI directly, doesn't route through our backend
- Vercel AI SDK `useChat` — rejected: adds dependency, designed for streaming (our endpoint is request/response), would need adapter
- Custom components — selected: full control over styling, direct integration with our API client pattern, no new dependencies

## R2: Chat Panel Layout Pattern

**Decision**: Fixed-position slide-in panel from right (translateX animation)
**Rationale**: The dashboard already uses a flex layout with sidebar (left) + main content (right). A slide-in panel from the right keeps the existing layout intact while overlaying the chat. On desktop, the main content area narrows; on mobile, the panel takes full width.
**Alternatives considered**:
- Dedicated /chat route — rejected: loses task list context, user can't see tasks update in real-time
- Floating widget (Intercom-style) — rejected: too small for multi-turn conversation with tool indicators
- Split-pane resizable — rejected: over-engineered for this use case

## R3: Backend Conversation List Endpoint

**Decision**: Add `GET /api/{user_id}/conversations` and `GET /api/{user_id}/conversations/{id}/messages`
**Rationale**: The frontend needs to list past conversations and load their message history for the conversation selector (FR-011, US-3). These don't exist yet. Following the existing route pattern in `backend/routes/tasks.py` with auth + ownership checks.
**Alternatives considered**:
- Store conversations client-side in localStorage — rejected: doesn't survive device switches, conversations are already in DB
- Single endpoint returning conversations + all messages — rejected: over-fetches, poor performance with many conversations

## R4: Task List Refresh Strategy

**Decision**: Callback-based refresh (`onTasksChanged` prop)
**Rationale**: When the AI agent performs tool calls (add/complete/delete/update), the ChatPanel receives `tool_calls` in the response. If any tool calls are present, it invokes `onTasksChanged()` which triggers `fetchTasks()` in the dashboard. Simple, reliable, no WebSocket needed.
**Alternatives considered**:
- WebSocket/SSE for real-time updates — rejected: over-engineered, our endpoint is synchronous request/response
- Polling — rejected: wasteful, unnecessary when we know exactly when to refresh
- React context/global state — rejected: callback is simpler and the dashboard already manages task state

## R5: Conversation State Management

**Decision**: Component-level state in ChatPanel (useState)
**Rationale**: Chat state (messages, conversationId, loading) is scoped to the panel. No other component needs this state. React useState is sufficient. The conversationId persists across panel toggles because ChatPanel stays mounted (just hidden via translateX).
**Alternatives considered**:
- React Context — rejected: over-engineering for single-consumer state
- External state (Zustand, Redux) — rejected: adds dependency, single-component state doesn't justify it
- URL state (searchParams) — rejected: chat is a panel overlay, not a route
