# Tasks: AI Agent + Chat Endpoint

**Input**: Design documents from `/specs/002-ai-chat-endpoint/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/chat-api.md ✅

**Tests**: Yes — spec SC-006 requires comprehensive test suite with mocked AI responses.

**Organization**: Tasks grouped by user story. US1+US2 share implementation (both P1); US3+US4 add error handling and tool selection verification (P2).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1–US4 maps to spec user stories

---

## Phase 1: Setup

**Purpose**: Add OpenAI dependency, prepare for agent development

- [x] T050 Add `openai` dependency to `backend/pyproject.toml` and run `uv sync`

---

## Phase 2: Foundational — Data Models

**Purpose**: Conversation + Message SQLModel tables needed by ALL user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T051 Add Conversation and Message SQLModel table models to `backend/models.py` per data-model.md (id, user_id indexed, created_at, updated_at for Conversation; id, conversation_id FK indexed, user_id indexed, role, content, created_at for Message)

**Checkpoint**: Data models ready — agent and endpoint implementation can begin

---

## Phase 3: User Story 1 — Send Chat Message, Get AI Response (Priority: P1) 🎯 MVP

**Goal**: User sends a natural language message, AI agent processes it (optionally calling MCP tools), returns a response. Both messages stored in DB.

**Independent Test**: POST to /api/{user_id}/chat with a message, verify response contains text, verify user message and agent response are in the database.

### Implementation for User Story 1

- [x] T052 [P] [US1] Create agent module with SYSTEM_PROMPT constant and `run_agent(messages, session, user_id)` function in `backend/agent.py` — implements tool-calling loop: call OpenAI → check tool_calls → execute via `backend/mcp/dispatcher.py` → append results → repeat until text response. Handle missing API key (return fallback message) and API errors (return friendly message).
- [x] T053 [US1] Create chat endpoint POST /api/{user_id}/chat in `backend/routes/chat.py` — use existing `get_current_user` dependency from `backend/auth.py` for JWT auth, validate message, create/load conversation (verify ownership), fetch last 50 messages, store user message, build message array [system + history + new], call run_agent, store assistant response, update conversation.updated_at, return {conversation_id, response, tool_calls} per contracts/chat-api.md
- [x] T054 [US1] Register chat router in `backend/main.py` — import and include_router for chat routes
- [x] T055 [US1] Create test file `tests/backend/test_chat.py` with mock OpenAI client — TestConversationModel (2 tests: create conversation, message relationship), TestChatEndpoint (2 tests: new conversation creation + response, continue existing conversation), TestAgentToolCalling (3 tests: agent calls tool and confirms, agent responds without tools, multi-turn tool calling)

**Checkpoint**: Core chat flow works — send message, get AI response, tool calls execute. 7 tests passing.

---

## Phase 4: User Story 2 — Conversations Persist Across Sessions (Priority: P1)

**Goal**: Conversation history survives server restarts. Agent has access to full message history for contextual follow-ups.

**Independent Test**: Create conversation with messages, get a new DB session (simulating restart), load conversation by ID, verify all messages intact.

### Implementation for User Story 2

- [x] T056 [US2] Add TestConversationPersistence class to `tests/backend/test_chat.py` — 2 tests: messages survive session reload, history loaded correctly and passed to agent context

**Checkpoint**: Persistence verified — 9 tests passing.

---

## Phase 5: User Story 3 — Error Handling (Priority: P2)

**Goal**: All failure scenarios return friendly, non-technical error messages.

**Independent Test**: Send requests triggering each error (empty message, invalid conversation_id, wrong user, no API key) and verify friendly responses.

### Implementation for User Story 3

- [x] T057 [US3] Add TestErrorHandling class to `tests/backend/test_chat.py` — 3 tests: empty message returns 400 "Message is required", conversation_id not found/wrong user returns 404 "Conversation not found", AI service unavailable returns 503 fallback message. Verify error handling in `backend/routes/chat.py` and `backend/agent.py` covers all cases per contracts/chat-api.md error codes.

**Checkpoint**: Error paths verified — 12 tests passing.

---

## Phase 6: User Story 4 — Agent Selects Correct Tool (Priority: P2)

**Goal**: AI agent correctly maps natural language intent to the right MCP tool.

**Independent Test**: Send messages for all 5 tools, verify correct tool was called.

### Implementation for User Story 4

- [x] T058 [US4] Add TestToolSelection class to `tests/backend/test_chat.py` — mock OpenAI to return tool_calls for each of the 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task), verify dispatcher executes correct tool and response confirms action. ~2 tests (tool call dispatch + multi-tool scenario).

**Checkpoint**: All user stories verified — ~14 tests passing.

---

## Phase 7: Polish & Validation

**Purpose**: Full regression, cross-cutting checks

- [x] T059 Run full test suite `uv run pytest tests/backend/ -v` — verify all ~98 tests pass (84 existing + ~14 new chat tests)
- [x] T060 Validate against quickstart.md — verify endpoint responds correctly (with mock or real key)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (openai installed)
- **US1 (Phase 3)**: Depends on Phase 2 (models exist) — **MVP delivery point**
- **US2 (Phase 4)**: Depends on Phase 3 (endpoint exists to test persistence)
- **US3 (Phase 5)**: Depends on Phase 3 (endpoint exists to test errors)
- **US4 (Phase 6)**: Depends on Phase 3 (agent exists to test tool selection)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: Blocks US2, US3, US4 — core implementation
- **US2 (P1)**: Tests only — can run after US1
- **US3 (P2)**: Tests + minor error path additions — can run after US1, parallel with US2/US4
- **US4 (P2)**: Tests only — can run after US1, parallel with US2/US3

### Within User Story 1 (Critical Path)

```
T050 (setup) → T051 (models) → T052 [P] + T053 (agent + endpoint) → T054 (register) → T055 (tests)
```

### Parallel Opportunities

- T052 (agent.py) and T053 (chat.py) can be written in parallel as separate files, but T053 imports from T052
- T056, T057, T058 (US2/US3/US4 tests) can run in parallel after US1 is complete
- T059 and T060 (polish) are sequential

---

## Parallel Example: After US1 Complete

```bash
# These test classes can be developed in parallel (separate test classes, same file):
T056 [US2]: TestConversationPersistence in tests/backend/test_chat.py
T057 [US3]: TestErrorHandling in tests/backend/test_chat.py
T058 [US4]: TestToolSelection in tests/backend/test_chat.py
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. T050: Add openai dep
2. T051: Conversation + Message models
3. T052–T054: Agent + endpoint + router registration
4. T055: Core tests (7 tests)
5. **STOP and VALIDATE**: `uv run pytest tests/backend/test_chat.py -v`

### Incremental Delivery

1. Setup + Foundational → T050–T051
2. US1 → T052–T055 → **MVP! Chat endpoint works** ✅
3. US2 → T056 → Persistence verified ✅
4. US3 → T057 → Errors handled gracefully ✅
5. US4 → T058 → Tool selection verified ✅
6. Polish → T059–T060 → Full regression ✅

---

## Notes

- All tests mock OpenAI client — no API key needed for testing
- Total new files: 3 (agent.py, routes/chat.py, test_chat.py)
- Modified files: 3 (pyproject.toml, models.py, main.py)
- Estimated ~14 new tests, total project ~98 tests
- OpenAI API key is optional — fallback message when missing
