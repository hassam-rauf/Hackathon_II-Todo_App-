# Implementation Plan: ChatKit Frontend — AI Chat Panel

**Branch**: `003-chatkit-frontend` | **Date**: 2026-04-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-chatkit-frontend/spec.md`

## Summary

Build a slide-in chat panel on the dashboard that connects to the existing `POST /api/{user_id}/chat` endpoint. The panel provides message input, message bubbles (user/assistant), tool call indicator chips, conversation selector for resuming past chats, and auto-refresh of the task list when AI performs tool actions. Two small backend endpoints will be added to support listing conversations and loading message history. Custom React components — no third-party ChatKit package.

## Technical Context

**Language/Version**: TypeScript (frontend), Python 3.13+ (backend additions)
**Primary Dependencies**: Next.js 16+ (App Router), React 19, Tailwind CSS 4, FastAPI, SQLModel
**Storage**: Neon Serverless PostgreSQL (existing Conversation + Message tables)
**Testing**: pytest (backend endpoints), manual verification (frontend — no Vitest configured)
**Target Platform**: Web (desktop + mobile responsive)
**Project Type**: Web application (frontend/ + backend/ monorepo)
**Performance Goals**: Chat response display < 500ms after backend responds; panel slide animation 300ms
**Constraints**: Must match dark space/galaxy theme; no new npm dependencies needed; Bearer JWT auth on all API calls
**Scale/Scope**: Single user per session; up to 50 messages per conversation (existing MAX_HISTORY_MESSAGES cap)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec complete, plan in progress |
| II. Tech Stack (Locked) | ✅ PASS | TypeScript, Next.js 16+, Tailwind CSS, FastAPI, SQLModel — all locked stack. Note: constitution says "Chat UI: OpenAI ChatKit" — we deviate to custom components (justified: ChatKit requires OpenAI domain registration and doesn't connect to our backend) |
| III. Code Quality | ✅ PASS | Type hints, Pydantic models, single responsibility |
| IV. Testing | ✅ PASS | pytest for new backend endpoints; frontend manual (no Vitest configured in project) |
| V. Security | ✅ PASS | Bearer JWT on all new endpoints, user_id ownership check, no secrets |
| VI. UI/UX | ✅ PASS | Mobile-first, Tailwind only, ARIA labels, loading/error states |
| VII. Architecture | ✅ PASS | Stateless API, RESTful, monorepo, smallest viable diff |
| VIII. Performance | ✅ PASS | < 500ms p95, no N+1 queries |

**Deviation: OpenAI ChatKit → Custom Components**
The constitution lists "Chat UI: OpenAI ChatKit" but ChatKit requires domain registration with OpenAI, connects to OpenAI's API (not our backend), and doesn't match our space theme. Custom components are the correct approach here. This should be documented in an ADR if the user consents.

## Project Structure

### Documentation (this feature)

```text
specs/003-chatkit-frontend/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── conversations-api.md
│   └── chat-ui-props.md
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── routes/
│   ├── chat.py              ← EXISTING: POST /api/{user_id}/chat
│   └── conversations.py     ← NEW: GET conversations, GET messages
└── main.py                  ← MODIFY: register conversations router

frontend/
├── components/
│   ├── ChatPanel.tsx         ← NEW: Slide-in chat panel container
│   ├── ChatMessages.tsx      ← NEW: Message list with bubbles + tool chips
│   ├── ChatInput.tsx         ← NEW: Text input + send button
│   ├── ChatConversationSelector.tsx  ← NEW: Conversation dropdown
│   └── ToolCallChip.tsx      ← NEW: Tool call indicator chip
├── lib/
│   └── api.ts               ← MODIFY: add chat + conversations API methods
└── app/
    └── dashboard/
        └── page.tsx          ← MODIFY: integrate ChatPanel, add onTasksChanged callback

tests/backend/
└── test_conversations.py     ← NEW: tests for conversation list + messages endpoints
```

**Structure Decision**: Extends existing frontend/backend monorepo. 5 new frontend components, 1 new backend route file, modifications to 3 existing files.

## Complexity Tracking

| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Custom chat components instead of OpenAI ChatKit | ChatKit requires OpenAI domain registration and connects to their API, not ours | Using ChatKit would require complete architecture change — our backend endpoint would be bypassed |

## Component Design

### Component 1: Backend — Conversation Endpoints (DEP-001)

Two new GET endpoints in `backend/routes/conversations.py`:

1. **GET /api/{user_id}/conversations** — List user's conversations
   - Auth: Bearer JWT + ownership check (same pattern as chat.py)
   - Query: `SELECT * FROM conversation WHERE user_id = ? ORDER BY updated_at DESC LIMIT 20`
   - Response includes a preview snippet (first user message, truncated to 50 chars)
   - Preview fetched via subquery on Message table

2. **GET /api/{user_id}/conversations/{conversation_id}/messages** — Load messages
   - Auth: Bearer JWT + ownership check
   - Query: `SELECT * FROM message WHERE conversation_id = ? ORDER BY created_at ASC`
   - Returns full message list (capped at 50 per existing MAX_HISTORY_MESSAGES)

Both follow the existing pattern in `backend/routes/tasks.py` and `backend/routes/chat.py`.

### Component 2: Frontend — API Client Extensions

Add to `frontend/lib/api.ts`:
- `getConversations(userId)` → `GET /api/{userId}/conversations`
- `getMessages(userId, conversationId)` → `GET /api/{userId}/conversations/{conversationId}/messages`
- `sendChatMessage(userId, message, conversationId?)` → `POST /api/{userId}/chat`

All use existing `request()` helper with Bearer token injection.

### Component 3: Frontend — ChatPanel (Container)

`frontend/components/ChatPanel.tsx` — "use client" component:
- Props: `isOpen`, `onClose`, `userId`, `onTasksChanged` callback
- State: `messages[]`, `conversationId`, `loading`, `error`
- Layout: Fixed position right panel (w-96 on desktop, full-width on mobile)
- Glass-card styling with border-left accent
- Slide-in/out CSS transition (transform translateX, 300ms)
- Composes: ChatConversationSelector, ChatMessages, ChatInput

### Component 4: Frontend — ChatMessages (Display)

`frontend/components/ChatMessages.tsx`:
- Props: `messages[]` (each with role, content, toolCalls?)
- Renders message bubbles: user (right, emerald bg), assistant (left, purple bg)
- Between assistant messages with tool_calls: renders ToolCallChip for each
- Auto-scroll via `useRef` + `scrollIntoView` on messages change
- Loading indicator: animated dots when `isLoading` prop is true

### Component 5: Frontend — ChatInput (Input)

`frontend/components/ChatInput.tsx`:
- Props: `onSend(message)`, `disabled`, `isLoading`
- Textarea with glass-input styling (auto-resize, max 4 lines)
- Send button (emerald) — disabled while loading
- Enter to send, Shift+Enter for newline
- ARIA label on input and button

### Component 6: Frontend — ChatConversationSelector

`frontend/components/ChatConversationSelector.tsx`:
- Props: `conversations[]`, `activeId`, `onSelect(id | null)`
- Dropdown at top of panel: "New Conversation" + list of past conversations
- Each item shows preview snippet + relative time
- Glass-card dropdown styling

### Component 7: Frontend — ToolCallChip

`frontend/components/ToolCallChip.tsx`:
- Props: `toolCall: { tool, args, result }`
- Compact chip with icon + label based on tool name:
  - add_task → "✓ Added: {title}"
  - complete_task → "✓ Completed: task #{id}"
  - delete_task → "🗑 Deleted: task #{id}"
  - update_task → "✏ Updated: task #{id}"
  - list_tasks → "📋 Listed {count} tasks"
- Error state: red border + "Failed: {message}"

### Component 8: Dashboard Integration

Modify `frontend/app/dashboard/page.tsx`:
- Add "AI Chat" button to sidebar nav (between "My Todos" and "Settings")
- Add state: `chatOpen` boolean
- Render `<ChatPanel>` conditionally with slide-in animation
- Pass `onTasksChanged={() => fetchTasks()}` to refresh task list after AI tool calls
- On mobile: add floating action button (FAB) in bottom-right corner

## Data Flow

```
User types message
  → ChatInput.onSend(text)
  → ChatPanel calls api.sendChatMessage(userId, text, conversationId?)
  → POST /api/{user_id}/chat → Agent → MCP Tools → DB
  → Response: { conversation_id, response, tool_calls }
  → ChatPanel updates messages state
  → ChatMessages renders new bubbles + ToolCallChips
  → If tool_calls.length > 0: ChatPanel calls onTasksChanged()
  → Dashboard re-fetches task list → TaskList updates
```

## Testing Strategy

| Component | Test Type | Details |
|-----------|-----------|---------|
| GET /api/{user_id}/conversations | pytest unit | List conversations, empty list, ownership isolation |
| GET /api/{user_id}/conversations/{id}/messages | pytest unit | Load messages, not found, ownership check |
| POST /api/{user_id}/chat (existing) | Already tested | 15 tests in test_chat.py |
| Frontend components | Manual | Visual verification of panel, bubbles, chips, responsive |

Expected: ~8-10 new backend tests + existing 99 tests = ~107-109 total.
