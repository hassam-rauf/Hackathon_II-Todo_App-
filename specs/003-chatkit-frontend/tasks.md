# Tasks: ChatKit Frontend — AI Chat Panel

**Input**: Design documents from `/specs/003-chatkit-frontend/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Backend endpoint tests included (constitution mandates pytest for every API endpoint). Frontend is manual verification (no Vitest configured).

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, etc.)
- Exact file paths included in descriptions

---

## Phase 1: Setup

**Purpose**: No new project initialization needed — extends existing frontend/ and backend/

- [x] T001 Add slide-in panel and chat-specific CSS animations to frontend/app/globals.css

---

## Phase 2: Foundational (Backend Endpoints + API Client)

**Purpose**: Backend conversation endpoints and frontend API methods that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Create conversation list and message history endpoints in backend/routes/conversations.py (GET /api/{user_id}/conversations, GET /api/{user_id}/conversations/{conversation_id}/messages) per contracts/conversations-api.md
- [x] T003 Register conversations router in backend/main.py
- [x] T004 Create backend tests for conversation endpoints in tests/backend/test_conversations.py (list conversations, load messages, empty list, ownership isolation, not found)
- [x] T005 Add chat API methods to frontend/lib/api.ts (sendChatMessage, getConversations, getMessages) and add TypeScript interfaces (ChatMessage, ChatConversation, ToolCall) per contracts/chat-ui-props.md

**Checkpoint**: Backend endpoints tested, API client ready — user story implementation can begin

---

## Phase 3: User Story 1+2 — Send Messages + Conversation Continuity (Priority: P1) MVP

**Goal**: User opens chat panel, sends a message, sees AI response with tool call chips, task list refreshes. Multi-turn conversation works with context preserved.

**Independent Test**: Open dashboard → click AI Chat → type "Add a task called Test" → send → see response bubble + tool chip → verify task appears in task list → send follow-up "now mark it done" → verify context understood

### Implementation for User Story 1+2

- [x] T006 [P] [US1] Create ToolCallChip component in frontend/components/ToolCallChip.tsx — compact chip with icon per tool type (add/complete/delete/update/list), error state styling
- [x] T007 [P] [US1] Create ChatInput component in frontend/components/ChatInput.tsx — glass-input textarea, send button (emerald), Enter to send, Shift+Enter newline, disabled while loading, ARIA labels
- [x] T008 [US1] Create ChatMessages component in frontend/components/ChatMessages.tsx — message bubbles (user=right/emerald, assistant=left/purple), ToolCallChip rendering between messages, auto-scroll via useRef, loading dots indicator
- [x] T009 [US1] Create ChatPanel container in frontend/components/ChatPanel.tsx — slide-in panel (fixed right, w-96 desktop), state management (messages, conversationId, loading, error), calls api.sendChatMessage, triggers onTasksChanged when tool_calls present, inline error with retry
- [x] T010 [US1] Integrate ChatPanel into dashboard in frontend/app/dashboard/page.tsx — add "AI Chat" sidebar button, chatOpen state, render ChatPanel with onTasksChanged={() => fetchTasks()}, adjust main content when panel open

**Checkpoint**: Core chat is fully functional — send messages, see responses, tool chips visible, task list refreshes, multi-turn context works

---

## Phase 4: User Story 3 — Resume Past Conversations (Priority: P2)

**Goal**: User can see past conversations in a dropdown, select one to load its history, or start a new conversation.

**Independent Test**: Have 2+ conversations → open chat → see dropdown with previews → select older conversation → verify messages load → send new message → verify it continues that conversation

### Implementation for User Story 3

- [x] T011 [US3] Create ChatConversationSelector component in frontend/components/ChatConversationSelector.tsx — dropdown with "New Conversation" + past conversations list (preview snippet + relative time), glass-card dropdown styling
- [x] T012 [US3] Integrate conversation selector into ChatPanel in frontend/components/ChatPanel.tsx — fetch conversations on open, pass to selector, handle onSelect (load messages or clear for new), update conversationId state

**Checkpoint**: Users can resume past conversations and start new ones

---

## Phase 5: User Story 4 — Toggle and Responsive Behavior (Priority: P2)

**Goal**: Chat panel works on mobile as full-width overlay with close button. Floating action button visible on mobile. Panel state preserved on toggle.

**Independent Test**: Toggle panel open/close on desktop → verify tasks visible beside panel → resize to mobile → verify full-width overlay → toggle closed → reopen → verify conversation preserved

### Implementation for User Story 4

- [x] T013 [US4] Add mobile responsive styles to ChatPanel in frontend/components/ChatPanel.tsx — full-width overlay on <768px, close button visible, backdrop overlay on mobile
- [x] T014 [US4] Add floating action button (FAB) for mobile in frontend/app/dashboard/page.tsx — emerald circle bottom-right, chat icon, visible only on md:hidden, toggles chatOpen

**Checkpoint**: Chat panel is fully responsive — side panel on desktop, overlay on mobile

---

## Phase 6: User Story 5 — Tool Call Visibility Polish (Priority: P3)

**Goal**: Enhanced tool call chips with per-tool icons and detailed result summaries, including error states.

**Independent Test**: Ask AI to "add a task" → verify chip shows "✓ Added: Buy groceries" → ask to "list tasks" → verify "Listed 5 tasks" → trigger error → verify red chip

### Implementation for User Story 5

- [x] T015 [US5] Enhance ToolCallChip in frontend/components/ToolCallChip.tsx — per-tool icons (✓ add, ✓ complete, 🗑 delete, ✏ update, 📋 list), extract title/count from result, red border + "Failed" for error results, multiple chip layout

**Checkpoint**: Tool call chips provide clear, icon-based feedback for all 5 tool types

---

## Phase 7: Polish & Verification

**Purpose**: Build verification and full test suite confirmation

- [x] T016 Verify frontend build passes with npx next build in frontend/
- [x] T017 Run full backend test suite with uv run pytest tests/backend/ -v and confirm all tests pass (target: ~107+ total)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (CSS) — BLOCKS all user stories
- **US1+2 (Phase 3)**: Depends on Phase 2 (API client + backend endpoints)
- **US3 (Phase 4)**: Depends on Phase 3 (ChatPanel exists to integrate selector into)
- **US4 (Phase 5)**: Depends on Phase 3 (ChatPanel exists to make responsive)
- **US5 (Phase 6)**: Depends on Phase 3 (ToolCallChip exists to enhance)
- **Polish (Phase 7)**: Depends on all previous phases

### User Story Dependencies

- **US1+2 (P1)**: Can start after Foundational — no other story dependencies
- **US3 (P2)**: Depends on US1+2 (ChatPanel must exist) + Foundational (backend endpoints)
- **US4 (P2)**: Depends on US1+2 (ChatPanel must exist to add responsive styles)
- **US5 (P3)**: Depends on US1+2 (ToolCallChip must exist to enhance)

### Within Each User Story

- Components with [P] can be built in parallel (different files)
- Container components depend on their child components
- Integration tasks depend on all components being ready

### Parallel Opportunities

- T006 + T007 can run in parallel (ToolCallChip + ChatInput — different files)
- T011 can start as soon as Phase 2 is complete (only depends on API client)
- T013 + T014 can run in parallel (panel styles + FAB — different concerns)
- US4 and US5 can run in parallel after US1+2 completes

---

## Parallel Example: Phase 3 (US1+2)

```bash
# Launch child components in parallel:
Task T006: "Create ToolCallChip component in frontend/components/ToolCallChip.tsx"
Task T007: "Create ChatInput component in frontend/components/ChatInput.tsx"

# Then sequentially:
Task T008: "Create ChatMessages component" (depends on T006 ToolCallChip)
Task T009: "Create ChatPanel container" (depends on T007, T008)
Task T010: "Dashboard integration" (depends on T009)
```

---

## Implementation Strategy

### MVP First (US1+2 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002–T005)
3. Complete Phase 3: US1+2 (T006–T010)
4. **STOP and VALIDATE**: Send a message, see response, verify tool chips, verify task list refresh
5. This is a shippable MVP — chat works end-to-end

### Incremental Delivery

1. Setup + Foundational → Backend ready, API client ready
2. US1+2 → Core chat works → **MVP!**
3. US3 → Conversation history → Can resume past chats
4. US4 → Responsive → Works on mobile
5. US5 → Tool chip polish → Enhanced transparency
6. Each story adds value without breaking previous stories

---

## Summary

| Phase | Story | Tasks | Files |
|-------|-------|:-----:|-------|
| 1. Setup | — | 1 | globals.css |
| 2. Foundational | — | 4 | conversations.py, main.py, test_conversations.py, api.ts |
| 3. US1+2 (P1) | Core Chat | 5 | ToolCallChip, ChatInput, ChatMessages, ChatPanel, dashboard/page.tsx |
| 4. US3 (P2) | Resume Chats | 2 | ChatConversationSelector, ChatPanel update |
| 5. US4 (P2) | Responsive | 2 | ChatPanel responsive, FAB |
| 6. US5 (P3) | Tool Chips | 1 | ToolCallChip enhancement |
| 7. Polish | — | 2 | Build + test verification |
| **Total** | | **17** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Backend tests included per constitution (every endpoint needs happy + error test)
- Frontend testing is manual (no Vitest in project)
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
