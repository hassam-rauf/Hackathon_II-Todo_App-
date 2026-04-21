# Feature Specification: ChatKit Frontend — AI Chat Panel

**Feature Branch**: `003-chatkit-frontend`  
**Created**: 2026-04-08  
**Status**: Draft  
**Input**: User description: "Phase III Cycle 3 — ChatKit Frontend: Build a slide-in chat panel on the dashboard that connects to POST /api/{user_id}/chat. Slide-in from right, message bubbles, tool call indicators, conversation selector, auto-scroll, loading states, responsive, dark space/galaxy theme."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Send a Message and See AI Response (Priority: P1)

An authenticated user opens the dashboard, clicks the "AI Chat" button in the sidebar, and a chat panel slides in from the right. The user types a natural language message (e.g., "Add a task called Buy groceries") and presses Send. A loading indicator appears while the AI processes. The AI response appears as a message bubble on the left, and a tool call chip shows "Added task: Buy groceries". The task list in the dashboard refreshes automatically to show the new task.

**Why this priority**: This is the core value — natural language task management through chat. Without this, there is no chat feature.

**Independent Test**: Open dashboard → click AI Chat → type "Add a task called Buy groceries" → send → see response bubble + tool call chip → verify task appears in task list.

**Acceptance Scenarios**:

1. **Given** user is on the dashboard, **When** they click "AI Chat" in sidebar, **Then** a chat panel slides in from the right with an input field and send button.
2. **Given** chat panel is open, **When** user types a message and clicks Send (or presses Enter), **Then** the message appears as a right-aligned bubble (user style) and a loading indicator shows.
3. **Given** a message was sent, **When** the AI responds, **Then** the response appears as a left-aligned bubble (assistant style) and any tool calls appear as indicator chips between the messages.
4. **Given** the AI performed a tool call (add/complete/delete/update), **When** the response arrives, **Then** the dashboard task list refreshes automatically to reflect the change.

---

### User Story 2 — Conversation Continuity Within a Session (Priority: P1)

A user sends multiple messages in the same chat session. Each new message and response appends to the existing conversation thread. The panel auto-scrolls to the latest message. The conversation is persisted in the database so the user can pick up where they left off.

**Why this priority**: Multi-turn conversation is essential for the AI to understand context (e.g., "now mark it as done" refers to the previously discussed task).

**Independent Test**: Send message 1 → see response → send message 2 referencing message 1 → verify AI understands context → verify all messages visible in scrollable thread.

**Acceptance Scenarios**:

1. **Given** user has an active conversation, **When** they send a follow-up message, **Then** it is sent with the existing conversation_id and the AI has full context.
2. **Given** multiple messages exist in the thread, **When** a new response arrives, **Then** the panel auto-scrolls to the bottom.
3. **Given** the user closes and reopens the chat panel within the same dashboard session, **Then** the current conversation thread is preserved.

---

### User Story 3 — Resume Past Conversations (Priority: P2)

A user wants to continue a previous conversation from an earlier session. They open the chat panel and see a conversation selector (dropdown) at the top. They can select a past conversation to load its full message history, or start a new conversation.

**Why this priority**: Valuable for continuity but not required for core chat functionality. The P1 stories deliver a working chat; this adds polish.

**Independent Test**: Have 2+ past conversations → open chat panel → select older conversation from dropdown → verify its messages load → send new message in that conversation → verify it continues correctly.

**Acceptance Scenarios**:

1. **Given** user has past conversations, **When** they open the chat panel, **Then** a dropdown shows their recent conversations (most recent first) with a preview snippet.
2. **Given** user selects a past conversation, **When** it loads, **Then** all previous messages and tool call indicators appear in order.
3. **Given** user wants a fresh start, **When** they select "New Conversation" from the dropdown, **Then** the panel clears and the next message creates a new conversation.

---

### User Story 4 — Toggle and Responsive Behavior (Priority: P2)

The chat panel can be opened and closed without losing state. On desktop, it appears as a side panel alongside the task list. On mobile, it appears as a full-width overlay. The toggle button is accessible from both the sidebar nav and a floating action button on mobile.

**Why this priority**: Responsive design is essential for the existing space theme but the chat works without it at a basic level.

**Independent Test**: Toggle panel open/close on desktop → verify tasks still visible beside panel → resize to mobile → verify panel becomes full-width overlay → toggle closed → verify panel state preserved.

**Acceptance Scenarios**:

1. **Given** desktop viewport (≥768px), **When** chat panel is open, **Then** it occupies the right portion of the screen and the task list remains visible (narrowed).
2. **Given** mobile viewport (<768px), **When** chat panel is open, **Then** it appears as a full-width overlay with a close button.
3. **Given** chat panel is open, **When** user clicks the toggle button or close button, **Then** panel slides out and conversation state is preserved in memory.
4. **Given** chat panel is closed, **When** user clicks "AI Chat" in sidebar or floating button, **Then** panel slides in with the previous conversation restored.

---

### User Story 5 — Tool Call Visibility (Priority: P3)

When the AI agent calls tools (add_task, complete_task, etc.), the user sees visual indicators showing what happened. These appear as compact chips between message bubbles, providing transparency about AI actions.

**Why this priority**: Nice-to-have transparency layer. The chat works without explicit tool indicators since the AI's text response already describes what happened.

**Independent Test**: Ask AI to "add a task" → verify a chip like "✓ Added task: Buy groceries" appears → ask to "list my tasks" → verify a chip like "📋 Listed 5 tasks" appears.

**Acceptance Scenarios**:

1. **Given** the AI calls a tool, **When** the response arrives, **Then** a tool call indicator chip appears above the assistant message showing the tool name and a brief result summary.
2. **Given** the AI calls multiple tools in one turn, **When** the response arrives, **Then** multiple chips appear, one per tool call.
3. **Given** a tool call fails, **When** the response arrives, **Then** the chip shows an error indicator (e.g., red styling with "Failed: ...").

---

### Edge Cases

- What happens when the user sends a message while a previous response is still loading? → The send button is disabled during loading; input remains editable for drafting.
- What happens when the network request fails? → An error message appears inline in the chat thread with a "Retry" option.
- What happens when the user has no past conversations? → The dropdown shows "New Conversation" only; no empty state issue.
- What happens when the chat panel is open and the user navigates away from the dashboard? → Panel closes; conversation ID is preserved for resumption on return.
- What happens when the AI response is very long? → Message bubbles expand vertically with word wrapping; no horizontal overflow.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a chat panel that slides in from the right side of the dashboard when activated.
- **FR-002**: System MUST provide a text input field and a send button at the bottom of the chat panel.
- **FR-003**: System MUST send user messages to `POST /api/{user_id}/chat` with the authenticated user's ID and Bearer token.
- **FR-004**: System MUST display user messages as right-aligned bubbles with emerald accent styling.
- **FR-005**: System MUST display assistant messages as left-aligned bubbles with purple accent styling.
- **FR-006**: System MUST show a loading/typing indicator while waiting for the AI response.
- **FR-007**: System MUST auto-scroll the message area to the latest message when new messages arrive.
- **FR-008**: System MUST display tool call indicators as compact chips between message bubbles, showing tool name and brief result.
- **FR-009**: System MUST refresh the dashboard task list when the AI response includes tool calls that modify tasks (add, complete, delete, update).
- **FR-010**: System MUST maintain conversation continuity by sending the `conversation_id` with subsequent messages in the same session.
- **FR-011**: System MUST provide a conversation selector dropdown to list past conversations and allow resuming or starting a new one.
- **FR-012**: System MUST disable the send button while a response is pending to prevent duplicate submissions.
- **FR-013**: System MUST show inline error messages in the chat thread when requests fail, with a retry option.
- **FR-014**: System MUST render as a side panel on desktop (≥768px) and a full-width overlay on mobile (<768px).
- **FR-015**: System MUST match the existing dark space/galaxy theme (glass-card styling, space background, emerald/purple accents).
- **FR-016**: System MUST allow sending messages via Enter key (Shift+Enter for new line).
- **FR-017**: System MUST preserve chat panel state (open/closed, current conversation) when toggling the panel.

### Dependencies

- **DEP-001**: Backend must expose endpoints to list a user's conversations and load messages for a given conversation. Currently only `POST /api/{user_id}/chat` exists. New endpoints needed:
  - `GET /api/{user_id}/conversations` — list conversations (id, created_at, preview snippet)
  - `GET /api/{user_id}/conversations/{conversation_id}/messages` — load message history

### Key Entities

- **ChatMessage**: A single message in the UI thread — has role (user/assistant), content text, optional tool calls array, and timestamp.
- **ChatConversation**: A conversation session — has ID, preview snippet (first user message or truncated), and last activity timestamp.
- **ToolCallIndicator**: Visual representation of an AI tool action — has tool name, arguments summary, result summary, and success/failure status.

## Assumptions

- The backend `POST /api/{user_id}/chat` endpoint is fully functional and returns `{ conversation_id, response, tool_calls }`.
- The `tool_calls` array in the response contains objects with `{ tool, args, result }` structure.
- Authentication via Better Auth with JWT is working; Bearer tokens are available via `authClient.token()`.
- The dashboard page (`/dashboard`) already has a sidebar navigation, stats bar, and task list that can be adjusted to accommodate the chat panel.
- New backend endpoints for listing conversations and loading messages will be added as part of this cycle (small backend additions to support frontend needs).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can send a natural language message and receive an AI response within the chat panel in a single interaction.
- **SC-002**: When the AI manages a task (add/complete/delete), the dashboard task list updates within 2 seconds of receiving the response.
- **SC-003**: Users can resume a previous conversation and continue with full context preserved.
- **SC-004**: The chat panel renders correctly on both desktop (side panel) and mobile (full overlay) viewports.
- **SC-005**: Tool call actions are visually indicated so users understand what the AI did without reading the full response text.
- **SC-006**: The chat UI matches the existing dark space/galaxy theme and feels like an integrated part of the application.
