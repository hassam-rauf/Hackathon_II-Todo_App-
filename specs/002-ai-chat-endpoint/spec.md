# Feature Specification: AI Agent + Chat Endpoint

**Feature Branch**: `002-ai-chat-endpoint`  
**Created**: 2026-04-08  
**Status**: Draft  
**Input**: User description: "Phase III Cycle 2: AI Agent + Chat Endpoint — OpenAI Agents SDK agent with system prompt for todo management. Conversation and Message SQLModel tables persisted in Neon DB. Stateless POST /api/{user_id}/chat endpoint. Flow: receive message → load/create conversation → fetch history → run OpenAI agent with MCP tools → store messages → return response. Agent uses tools from backend/mcp/. Conversations survive server restart. Mock LLM for tests."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Sends a Chat Message and Gets AI Response (Priority: P1)

An authenticated user sends a natural language message (e.g., "Add a task to buy groceries") to the chat endpoint. The system creates or loads a conversation, passes the message to an AI agent configured with todo management tools, the agent decides which tool(s) to call, executes them, and returns a natural language response (e.g., "Done! I've added 'buy groceries' to your task list."). Both the user's message and the agent's response are stored in the database.

**Why this priority**: This is the core feature — without the ability to send a message and get an AI-powered response, the chatbot doesn't exist. Every other story depends on this working.

**Independent Test**: Send a POST request with a message, verify the response contains natural language text, verify the user's message and agent's response are both stored in the database.

**Acceptance Scenarios**:

1. **Given** an authenticated user with no prior conversations, **When** they send a message, **Then** a new conversation is created, the message is stored, the AI agent processes it, and a response is returned.
2. **Given** an authenticated user with an existing conversation, **When** they send a message with a conversation_id, **Then** the message is appended to that conversation and the response includes context from prior messages.
3. **Given** a message that triggers a tool call (e.g., "Add task: buy milk"), **When** the agent processes it, **Then** the appropriate MCP tool is called, the task is created, and the response confirms the action.
4. **Given** a message that does NOT require a tool (e.g., "Hello!"), **When** the agent processes it, **Then** the agent responds conversationally without calling any tools.

---

### User Story 2 - Conversations Persist Across Sessions (Priority: P1)

A user's conversation history is stored in the database and survives server restarts. When the user returns and continues a conversation, the AI agent has access to the full message history, enabling contextual follow-ups (e.g., "Mark the task I just added as complete").

**Why this priority**: Without persistence, every server restart loses all conversations, making the chatbot unreliable. Users expect continuity.

**Independent Test**: Create a conversation with messages, simulate a server restart (new session), load the conversation by ID, verify all messages are intact and the agent can reference prior context.

**Acceptance Scenarios**:

1. **Given** a conversation with 5 messages, **When** the server restarts and the user sends a new message with the same conversation_id, **Then** the agent responds with awareness of the previous 5 messages.
2. **Given** a user with multiple conversations, **When** they send a message with a specific conversation_id, **Then** only that conversation's history is loaded.

---

### User Story 3 - Agent Handles Errors Gracefully (Priority: P2)

When something goes wrong — the AI service is unavailable, a tool call fails, or the user sends invalid input — the system returns a friendly error message instead of crashing or exposing technical details.

**Why this priority**: Error handling is essential for production readiness but secondary to core functionality.

**Independent Test**: Send requests that trigger each error type (missing message, invalid conversation_id, simulated AI service failure) and verify friendly error responses.

**Acceptance Scenarios**:

1. **Given** a request with an empty message, **When** the endpoint processes it, **Then** a friendly error is returned ("Please type a message").
2. **Given** a conversation_id that doesn't exist or belongs to another user, **When** the endpoint processes it, **Then** a friendly error is returned ("Conversation not found").
3. **Given** the AI service is unavailable (no API key or timeout), **When** the endpoint processes it, **Then** a friendly fallback message is returned ("I'm having trouble right now. Please try again shortly.").
4. **Given** a tool call fails during agent processing, **When** the error occurs, **Then** the agent receives the error and communicates it naturally to the user.

---

### User Story 4 - Agent Selects Correct Tool Based on Intent (Priority: P2)

The AI agent correctly interprets user intent from natural language and selects the appropriate MCP tool. "Add milk to my list" triggers add_task. "What's on my list?" triggers list_tasks. "I finished the grocery shopping" triggers complete_task. The agent confirms its action after each tool call.

**Why this priority**: Tool selection accuracy is critical for user satisfaction but depends on the AI model's capability, not core architecture.

**Independent Test**: Send a set of natural language messages covering all 5 tools and verify the correct tool was called for each.

**Acceptance Scenarios**:

1. **Given** "Add a task to call mom", **When** the agent processes it, **Then** add_task is called with title "call mom" and the response confirms creation.
2. **Given** "Show me all tasks", **When** the agent processes it, **Then** list_tasks is called and the response lists the user's tasks.
3. **Given** "Mark task 3 as done", **When** the agent processes it, **Then** complete_task is called with task_id 3.
4. **Given** "Delete task 2", **When** the agent processes it, **Then** delete_task is called with task_id 2.
5. **Given** "Change task 1 to 'Call mom'", **When** the agent processes it, **Then** update_task is called with task_id 1 and new title.

---

### Edge Cases

- What happens when a conversation has a very long history (100+ messages)? The system loads only the most recent N messages to stay within token limits.
- What happens when the user sends multiple messages rapidly? Each request is processed independently (stateless endpoint).
- What happens when the AI agent calls multiple tools in one response? The system processes all tool calls, sends results back to the agent, and returns the final response.
- What happens when the user references a task that doesn't exist? The MCP tool returns a friendly "not found" error, and the agent communicates this to the user.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chat endpoint that accepts a user message and optional conversation_id, and returns an AI-generated response.
- **FR-002**: System MUST create a new conversation record when no conversation_id is provided.
- **FR-003**: System MUST load full message history from the database when a conversation_id is provided.
- **FR-004**: System MUST store the user's message in the database before processing.
- **FR-005**: System MUST store the AI agent's response in the database after processing.
- **FR-006**: System MUST configure the AI agent with a system prompt that instructs it to manage todos using the available tools.
- **FR-007**: System MUST pass all 5 MCP tool schemas to the AI agent for tool selection.
- **FR-008**: When the agent requests tool calls, the system MUST execute them via the MCP dispatcher and return results to the agent for a natural language response.
- **FR-009**: System MUST handle multi-turn tool calling (agent may call tools, get results, then call more tools before generating a final response).
- **FR-010**: System MUST enforce user isolation — a user can only access their own conversations.
- **FR-011**: System MUST return friendly error messages for all failure scenarios (empty message, conversation not found, AI service unavailable, tool failure).
- **FR-012**: System MUST be stateless — no server-side session state. All context comes from the database.
- **FR-013**: System MUST include tool call information in the response so the frontend can display what the agent did.
- **FR-014**: System MUST cap conversation history to a configurable maximum message count to respect token limits.

### Key Entities

- **Conversation**: A chat session between a user and the AI agent. Has an owner (user_id), creation timestamp, and last updated timestamp. Contains multiple messages.
- **Message**: A single message within a conversation. Has a role (user or assistant), text content, creation timestamp, and belongs to exactly one conversation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive a relevant AI response within 5 seconds of sending a message.
- **SC-002**: The AI agent correctly selects the appropriate tool for at least 90% of clearly phrased task management requests.
- **SC-003**: Conversation history persists across server restarts — all messages are recoverable by conversation_id.
- **SC-004**: All error scenarios return a friendly, non-technical message to the user.
- **SC-005**: The system processes each chat request independently with zero server-side state — any server instance can handle any request.
- **SC-006**: Test suite covers the chat endpoint, conversation persistence, tool integration, and error handling with all tests passing using mocked AI responses.

## Assumptions

- The MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) from Cycle 1 are available and tested at `backend/mcp/`.
- User authentication is handled by existing middleware — the chat endpoint receives a pre-authenticated user_id.
- The AI model is configured via an API key in environment variables. The system works without the key (returns a fallback message) so it can be built and tested before the key is purchased.
- Message history is capped at 50 messages per conversation (configurable) to stay within token limits.
- The system prompt instructs the agent to be a helpful todo assistant — it does not need to handle off-topic conversations beyond polite deflection.

## Scope

### In Scope
- Conversation and Message database models
- POST /api/{user_id}/chat endpoint
- AI agent configuration with system prompt and tool binding
- Stateless conversation flow (load history → process → store)
- Error handling for all failure modes
- Comprehensive test suite with mocked AI responses

### Out of Scope
- Chat UI frontend (Cycle 3)
- Streaming responses (future enhancement)
- Voice input / output
- Multi-user conversations (group chat)
- Message editing or deletion
- File attachments in messages
