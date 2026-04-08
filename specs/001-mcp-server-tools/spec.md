# Feature Specification: MCP Server + Tools

**Feature Branch**: `001-mcp-server-tools`  
**Created**: 2026-04-07  
**Status**: Draft  
**Input**: User description: "Phase III Cycle 1: MCP Server + Tools — In-process MCP tool server inside FastAPI with 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) for AI agent integration. Tools operate on existing Task SQLModel via Neon DB. OpenAI function calling format. Each tool receives user_id for ownership isolation. Structured dict returns. Friendly error messages. Central dispatcher. Independent testing with SQLite in-memory."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - AI Agent Adds a Task on User's Behalf (Priority: P1)

An AI chatbot agent receives a natural language request from an authenticated user (e.g., "Add a task to buy groceries") and uses the `add_task` tool to create a new task in the user's task list. The tool writes to the database and returns a structured confirmation that the agent can relay as a natural language response.

**Why this priority**: Task creation is the most fundamental operation. Without it, no other tool (list, complete, delete, update) has data to act on. This is the entry point for the entire AI-managed todo workflow.

**Independent Test**: Can be fully tested by calling the `add_task` function with a user_id and title, verifying a new task row exists in the database, and confirming the return dict contains `task_id`, `title`, `status: "created"`, and a human-readable `message`.

**Acceptance Scenarios**:

1. **Given** a valid user_id and title, **When** `add_task` is called, **Then** a new task is created in the database and a confirmation dict is returned with `status: "created"`.
2. **Given** a valid user_id, title, and optional description, **When** `add_task` is called, **Then** the task is created with both title and description stored.
3. **Given** an empty title, **When** `add_task` is called, **Then** an error response is returned indicating the title is required.

---

### User Story 2 - AI Agent Lists User's Tasks (Priority: P1)

The AI agent retrieves a user's tasks when asked (e.g., "Show me all tasks" or "What's pending?"). The `list_tasks` tool queries the database filtered by user_id and optional status, returning an array of task objects the agent can present conversationally.

**Why this priority**: Listing is tied with creation as the core read operation. Users need to see their tasks before they can complete, update, or delete them. The agent needs task IDs from list results to perform other operations.

**Independent Test**: Can be tested by creating several tasks for a user, calling `list_tasks` with different status filters (all, pending, completed), and verifying the returned array matches expected counts and contents.

**Acceptance Scenarios**:

1. **Given** a user with 3 tasks (2 pending, 1 completed), **When** `list_tasks` is called with no status filter, **Then** all 3 tasks are returned.
2. **Given** a user with tasks, **When** `list_tasks` is called with `status="pending"`, **Then** only pending tasks are returned.
3. **Given** a user with tasks, **When** `list_tasks` is called with `status="completed"`, **Then** only completed tasks are returned.
4. **Given** a user with no tasks, **When** `list_tasks` is called, **Then** an empty array is returned with `count: 0`.

---

### User Story 3 - AI Agent Completes a Task (Priority: P2)

The user tells the AI "Mark task 3 as done" and the agent calls `complete_task` with the task_id. The tool finds the task, verifies ownership, marks it complete, and returns a confirmation.

**Why this priority**: Completing tasks is the core productivity action — it's the reason users create tasks. Depends on list (to know the task_id) and create (to have tasks).

**Independent Test**: Can be tested by creating a task, calling `complete_task` with its ID, and verifying the task's `completed` field is now `True` in the database.

**Acceptance Scenarios**:

1. **Given** a pending task owned by the user, **When** `complete_task` is called with the task_id, **Then** the task is marked complete and a confirmation dict is returned.
2. **Given** a non-existent task_id, **When** `complete_task` is called, **Then** an error response with a friendly "Task not found" message is returned.
3. **Given** a task owned by a different user, **When** `complete_task` is called, **Then** an error response is returned (ownership violation treated as "not found").

---

### User Story 4 - AI Agent Deletes a Task (Priority: P2)

The user says "Delete task 2" and the agent calls `delete_task`. The tool removes the task from the database after verifying ownership.

**Why this priority**: Deletion is essential for task management hygiene but less frequent than creation, listing, or completion.

**Independent Test**: Can be tested by creating a task, calling `delete_task`, and verifying the task no longer exists in the database.

**Acceptance Scenarios**:

1. **Given** a task owned by the user, **When** `delete_task` is called, **Then** the task is removed from the database and a confirmation dict is returned.
2. **Given** a non-existent task_id, **When** `delete_task` is called, **Then** a friendly "Task not found" error is returned.
3. **Given** a task owned by a different user, **When** `delete_task` is called, **Then** an error response is returned (treated as "not found").

---

### User Story 5 - AI Agent Updates a Task (Priority: P2)

The user says "Change task 1 to 'Call mom'" and the agent calls `update_task` with the new title. The tool updates the specified fields while preserving unchanged ones.

**Why this priority**: Update is important for correcting mistakes but depends on existing tasks and knowledge of task_ids.

**Independent Test**: Can be tested by creating a task, calling `update_task` with a new title, and verifying the title changed while other fields remain intact.

**Acceptance Scenarios**:

1. **Given** a task owned by the user, **When** `update_task` is called with a new title, **Then** only the title is updated and a confirmation is returned.
2. **Given** a task owned by the user, **When** `update_task` is called with a new description only, **Then** only the description is updated.
3. **Given** a task owned by the user, **When** `update_task` is called with both title and description, **Then** both fields are updated.
4. **Given** a non-existent task_id, **When** `update_task` is called, **Then** a friendly "Task not found" error is returned.

---

### User Story 6 - Central Dispatcher Routes Tool Calls (Priority: P1)

The AI agent's response includes one or more tool call requests (with tool name and arguments). The central dispatcher receives each tool call, validates the tool name, routes it to the correct function, passes user_id and arguments, and returns the structured result.

**Why this priority**: The dispatcher is the integration point between the AI agent and the tools. Without it, individual tools cannot be invoked by the agent.

**Independent Test**: Can be tested by calling the dispatcher with each tool name and verifying it routes to the correct function and returns the expected result format.

**Acceptance Scenarios**:

1. **Given** a valid tool name and arguments, **When** the dispatcher is called, **Then** the correct tool function executes and returns a structured result.
2. **Given** an unknown tool name, **When** the dispatcher is called, **Then** an error dict with `status: "error"` and a message is returned.
3. **Given** a tool that throws an unexpected exception, **When** the dispatcher is called, **Then** the error is caught and a friendly error message is returned (no stack trace exposed).

---

### Edge Cases

- What happens when a user tries to complete an already-completed task? The tool should still return success (idempotent).
- What happens when the database connection fails mid-operation? The dispatcher catches the exception and returns a friendly error message.
- What happens when `update_task` is called with no fields to update (no title, no description)? The tool returns the current task state unchanged with a success status.
- What happens when `list_tasks` is called with an invalid status filter value? The tool defaults to listing all tasks.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an `add_task` tool that creates a new task with a required title and optional description for a given user.
- **FR-002**: System MUST provide a `list_tasks` tool that retrieves all tasks for a given user, with optional filtering by status (all, pending, completed).
- **FR-003**: System MUST provide a `complete_task` tool that marks a specified task as completed for the owning user.
- **FR-004**: System MUST provide a `delete_task` tool that permanently removes a specified task for the owning user.
- **FR-005**: System MUST provide an `update_task` tool that modifies the title and/or description of a specified task for the owning user.
- **FR-006**: All tools MUST enforce user ownership — a user can only operate on their own tasks. Unauthorized access MUST be treated as "task not found" (no information leakage).
- **FR-007**: All tools MUST return structured dictionaries containing at minimum: a `status` field and a human-readable `message` field.
- **FR-008**: System MUST provide a central dispatcher that routes tool calls by name to the correct tool function and handles unknown tool names gracefully.
- **FR-009**: All tool errors (not found, invalid input, database failure) MUST be returned as friendly natural language messages suitable for display to end users via the AI agent.
- **FR-010**: Tool schemas MUST be defined in OpenAI function calling format so the AI agent can discover and invoke them.
- **FR-011**: Tools MUST be stateless — no tool retains conversation context or session state between calls.
- **FR-012**: The `complete_task` tool MUST be idempotent — completing an already-completed task returns success.

### Key Entities

- **Tool**: A named function with a defined parameter schema, callable by an AI agent. Each tool performs a specific operation on user tasks. Key attributes: name, description, parameter schema, return schema.
- **Task** (existing): A user-owned todo item with id, title, description, completed status, and user_id. Already defined in the application's data layer.
- **Tool Result**: The structured output from a tool execution. Contains task_id (when applicable), status (created/completed/updated/deleted/error/success), title, and a human-readable message.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 tools (add, list, complete, delete, update) execute successfully and return correct structured results for valid inputs.
- **SC-002**: User ownership isolation is enforced — a user cannot view, modify, or delete another user's tasks through any tool.
- **SC-003**: Every error scenario (not found, invalid input, unknown tool) returns a friendly, human-readable message instead of a technical error or stack trace.
- **SC-004**: Each tool is independently testable without requiring an AI agent or LLM — all tools can be called directly with parameters and verified against expected outputs.
- **SC-005**: The central dispatcher correctly routes all 5 tool names and handles unknown tool names without crashing.
- **SC-006**: All tools complete execution within 500ms under normal database conditions.
- **SC-007**: Test suite achieves 100% coverage of tool functions including happy paths, error paths, and edge cases, with all tests passing.

## Assumptions

- The existing Task SQLModel and database layer (engine, session) are reused as-is — no schema changes needed.
- Tools run in-process within the FastAPI application — no separate MCP server process.
- SQLite in-memory is used for testing; Neon PostgreSQL for production.
- User authentication is handled upstream (by the chat endpoint/auth middleware) — tools receive a pre-validated `user_id`.
- OpenAI function calling format is used for tool schema definitions, compatible with the OpenAI Agents SDK integration in Cycle 2.

## Scope

### In Scope
- 5 MCP tool implementations (add, list, complete, delete, update)
- Tool schema definitions in OpenAI function calling format
- Central dispatcher with error handling
- Comprehensive test suite

### Out of Scope
- AI agent setup and LLM integration (Cycle 2)
- Chat endpoint and conversation persistence (Cycle 2)
- Chat UI and frontend components (Cycle 3)
- Advanced features (priority, tags, due dates) — Phase V
