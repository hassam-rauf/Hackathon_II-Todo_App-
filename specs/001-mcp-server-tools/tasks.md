# Tasks: MCP Server + Tools

**Input**: Design documents from `/specs/001-mcp-server-tools/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Included — constitution mandates testing (Principle IV), spec requires independent tool testing (SC-004, SC-007).

**Organization**: Tasks follow the plan's dependency graph (schemas → tools → dispatcher → tests) and map to AGENT.md task IDs T-042 → T-049.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US6)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create MCP package structure

- [x] T042 Create MCP package with `__init__.py` in `backend/mcp/__init__.py`

---

## Phase 2: Foundational (Tool Schemas)

**Purpose**: Define all tool schemas in OpenAI function calling format — MUST complete before tools can be tested against schema contracts

- [x] T043 [P] Define all 5 tool schemas in OpenAI function calling format in `backend/mcp/schemas.py` (add_task, list_tasks, complete_task, delete_task, update_task with parameter types, descriptions, required fields per contracts/tools-api.md)

**Checkpoint**: Schema definitions ready — tool implementations can reference these for consistency

---

## Phase 3: Core Tools — Add & List (Priority: P1) 🎯 MVP

**Goal**: Implement the two foundational tools — creating and reading tasks. Together these form the minimum viable toolset.

**Independent Test**: Call `add_task` with a title, then `list_tasks` — verify task appears in the list.

### Implementation

- [x] T044 [US1] Implement `add_task` function in `backend/mcp/tools.py` — create Task with title (required) and description (optional), validate empty title, return `{task_id, title, status:"created", message}`
- [x] T045 [US2] Implement `list_tasks` function in `backend/mcp/tools.py` — query by user_id, filter by status param (all/pending/completed), return `{tasks:[...], count, status:"success", message}`

**Checkpoint**: Can create and list tasks via direct function calls

---

## Phase 4: Management Tools — Complete, Delete, Update (Priority: P2)

**Goal**: Add the remaining 3 task management operations. Each enforces ownership and returns friendly errors.

**Independent Test**: Create a task, then complete/delete/update it — verify each operation works and ownership is enforced.

### Implementation

- [x] T046 [US3] Implement `complete_task` function in `backend/mcp/tools.py` — find task by id, verify ownership (not found = same response for wrong user), set completed=True (idempotent), return `{task_id, title, status:"completed", message}`
- [x] T047 [US4] Implement `delete_task` function in `backend/mcp/tools.py` — find task by id, verify ownership, delete from DB, return `{task_id, title, status:"deleted", message}`
- [x] T048 [US5] Implement `update_task` function in `backend/mcp/tools.py` — find task by id, verify ownership, update title and/or description (preserve unchanged fields), return `{task_id, title, status:"updated", message}`

**Checkpoint**: All 5 tools implemented with ownership isolation and friendly error messages

---

## Phase 5: Central Dispatcher (Priority: P1)

**Goal**: Route tool calls by name to the correct function, handle unknown tools and unexpected exceptions.

**Independent Test**: Call dispatcher with each tool name — verify correct routing. Call with unknown name — verify error dict returned.

### Implementation

- [x] T049 [US6] Implement `execute_tool` dispatcher in `backend/mcp/dispatcher.py` — TOOL_MAP dict mapping names to functions, lookup + call + try/except safety net, return error dict for unknown tools
- [x] T050 [US6] Implement `process_tool_calls` in `backend/mcp/dispatcher.py` — iterate OpenAI tool_calls list, parse JSON arguments, call execute_tool for each, return list of `{tool_call_id, role:"tool", content: json_string}`

**Checkpoint**: Full tool pipeline working — schema → dispatcher → tool → result

---

## Phase 6: Test Suite

**Purpose**: Comprehensive tests for all tools, dispatcher, and cross-user isolation

### Tests

- [x] T051 [P] [US1] Write tests for `add_task` in `tests/backend/test_mcp_tools.py` — create with title only, create with title+description, reject empty title (3 tests)
- [x] T052 [P] [US2] Write tests for `list_tasks` in `tests/backend/test_mcp_tools.py` — empty list, list all, filter pending, filter completed (4 tests)
- [x] T053 [P] [US3] Write tests for `complete_task` in `tests/backend/test_mcp_tools.py` — complete pending task, complete already-completed (idempotent), task not found (3 tests)
- [x] T054 [P] [US4] Write tests for `delete_task` in `tests/backend/test_mcp_tools.py` — delete existing, task not found (2 tests)
- [x] T055 [P] [US5] Write tests for `update_task` in `tests/backend/test_mcp_tools.py` — update title only, update description only, update both, task not found (4 tests)
- [x] T056 [P] [US6] Write tests for dispatcher in `tests/backend/test_mcp_tools.py` — valid tool routing, unknown tool name, exception handling in tool (3 tests)
- [x] T057 [P] Write user isolation tests in `tests/backend/test_mcp_tools.py` — cross-user read isolation (user2 can't see user1 tasks), cross-user write isolation (user2 can't complete/delete/update user1 tasks) (2 tests)

### Verification

- [x] T058 Run full test suite: `uv run pytest tests/backend/ -v` — all new MCP tests + all existing backend tests must pass

**Checkpoint**: ~21 new tests passing, total backend suite green

---

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T059 Update `backend/mcp/__init__.py` with public exports (execute_tool, process_tool_calls, TOOL_SCHEMAS)
- [x] T060 Run quickstart.md validation — verify direct tool usage example works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Schemas)**: Depends on Phase 1
- **Phase 3 (Core Tools)**: Depends on Phase 1 (uses Task model, not schemas)
- **Phase 4 (Management Tools)**: Depends on Phase 1
- **Phase 5 (Dispatcher)**: Depends on Phase 3 + Phase 4 (imports tool functions)
- **Phase 6 (Tests)**: Depends on Phase 2 + Phase 3 + Phase 4 + Phase 5
- **Phase 7 (Polish)**: Depends on Phase 6

### Parallel Opportunities

- T043 (schemas) can run in parallel with T044-T048 (tools) — different files
- T044 (add_task) and T045 (list_tasks) can run in parallel — same file but independent functions
- T046, T047, T048 can run in parallel — independent functions
- T051-T057 can ALL run in parallel — different test classes in same file
- Phases 2, 3, 4 can run in parallel (different files, no cross-deps)

### Within Each Phase

- Models before services (N/A — reusing existing Task model)
- Tools before dispatcher (dispatcher imports tools)
- Implementation before tests (tests import all modules)

---

## Parallel Example: Phase 3 + Phase 4

```bash
# These can run in parallel (independent functions, same file is OK):
Task T044: "Implement add_task in backend/mcp/tools.py"
Task T045: "Implement list_tasks in backend/mcp/tools.py"
Task T046: "Implement complete_task in backend/mcp/tools.py"
Task T047: "Implement delete_task in backend/mcp/tools.py"
Task T048: "Implement update_task in backend/mcp/tools.py"
```

---

## Implementation Strategy

### MVP First (Phase 1 + 2 + 3 Only)

1. Complete Phase 1: Package setup
2. Complete Phase 2: Schemas
3. Complete Phase 3: add_task + list_tasks
4. **STOP and VALIDATE**: Can create and list tasks via direct calls
5. These 2 tools alone demonstrate the MCP pattern

### Full Delivery

1. Setup + Schemas + Core Tools → MVP
2. Add Management Tools (Phase 4) → Full 5-tool set
3. Add Dispatcher (Phase 5) → Agent-ready pipeline
4. Add Tests (Phase 6) → Verified and safe
5. Polish (Phase 7) → Clean exports, validated quickstart

---

## Task-to-AGENT.md Mapping

| tasks.md | AGENT.md | Description |
|----------|----------|-------------|
| T042 | T-042 | MCP Server setup |
| T043-T044 | T-043 | add_task tool + schema |
| T045 | T-044 | list_tasks tool |
| T046 | T-045 | complete_task tool |
| T047 | T-046 | delete_task tool |
| T048 | T-047 | update_task tool |
| T049-T050 | T-048 | Dispatcher + error handling |
| T051-T058 | T-049 | MCP tools tests |

---

## Notes

- All tools live in ONE file (`backend/mcp/tools.py`) — this is intentional per plan.md (simple, ~200 lines)
- No existing files are modified — pure additive change
- SQLite in-memory for all tests (same pattern as existing test suite)
- Task IDs T042-T060 continue from Phase II's T-041
