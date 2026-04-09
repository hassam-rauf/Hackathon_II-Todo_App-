# Data Model: ChatKit Frontend

**Feature**: 003-chatkit-frontend | **Date**: 2026-04-08

## Existing Entities (No Changes)

### Conversation (backend/models.py:56-62)

Already exists from Cycle 2. No schema changes needed.

| Field | Type | Notes |
|-------|------|-------|
| id | int (PK) | Auto-increment |
| user_id | str (indexed) | Owner |
| created_at | datetime | UTC |
| updated_at | datetime | UTC, updated on new message |

### Message (backend/models.py:65-73)

Already exists from Cycle 2. No schema changes needed.

| Field | Type | Notes |
|-------|------|-------|
| id | int (PK) | Auto-increment |
| conversation_id | int (FK, indexed) | References conversation.id |
| user_id | str (indexed) | Owner |
| role | str | "user" or "assistant" |
| content | str | Message text |
| created_at | datetime | UTC |

## New Pydantic Response Models (Backend)

### ConversationListItem

Used by `GET /api/{user_id}/conversations` response.

| Field | Type | Notes |
|-------|------|-------|
| id | int | Conversation ID |
| preview | str | First user message, truncated to 50 chars |
| created_at | datetime | When conversation started |
| updated_at | datetime | Last activity |

### MessageResponse

Used by `GET /api/{user_id}/conversations/{id}/messages` response.

| Field | Type | Notes |
|-------|------|-------|
| id | int | Message ID |
| role | str | "user" or "assistant" |
| content | str | Message text |
| created_at | datetime | UTC timestamp |

## Frontend TypeScript Interfaces

### ChatMessage (UI state)

| Field | Type | Notes |
|-------|------|-------|
| id | number | Unique per message |
| role | "user" \| "assistant" | Sender |
| content | string | Message text |
| toolCalls | ToolCall[] \| undefined | Only on assistant messages with tool actions |
| createdAt | string | ISO timestamp |

### ToolCall (from API response)

| Field | Type | Notes |
|-------|------|-------|
| tool | string | Tool name (add_task, list_tasks, etc.) |
| args | Record<string, unknown> | Tool arguments |
| result | Record<string, unknown> | Tool execution result |

### ChatConversation (for selector)

| Field | Type | Notes |
|-------|------|-------|
| id | number | Conversation ID |
| preview | string | Truncated first message |
| updatedAt | string | ISO timestamp of last activity |

## State Transitions

```
No Conversation → User sends first message → New Conversation created (API returns conversation_id)
Active Conversation → User sends message → Message added to existing conversation
Active Conversation → User selects different conversation → Load messages from API
Active Conversation → User selects "New Conversation" → Clear messages, reset conversationId to null
```
