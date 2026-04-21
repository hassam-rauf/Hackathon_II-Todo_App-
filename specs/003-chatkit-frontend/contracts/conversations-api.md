# API Contract: Conversation Endpoints

**Feature**: 003-chatkit-frontend | **Date**: 2026-04-08

## GET /api/{user_id}/conversations

List a user's conversations, most recent first.

**Auth**: Bearer JWT (same as existing endpoints)
**Ownership**: `user_id` in path must match JWT subject

### Request

```
GET /api/{user_id}/conversations
Authorization: Bearer <jwt_token>
```

No query parameters.

### Response 200

```json
[
  {
    "id": 1,
    "preview": "Add a task called Buy groceries",
    "created_at": "2026-04-08T10:00:00Z",
    "updated_at": "2026-04-08T10:05:00Z"
  },
  {
    "id": 2,
    "preview": "What tasks do I have pending?",
    "created_at": "2026-04-07T15:00:00Z",
    "updated_at": "2026-04-07T15:02:00Z"
  }
]
```

### Response 403

```json
{ "detail": "Access denied" }
```

### Notes

- Returns max 20 conversations
- `preview` is the first user message in the conversation, truncated to 50 characters
- If a conversation has no messages, preview is empty string
- Ordered by `updated_at` descending

---

## GET /api/{user_id}/conversations/{conversation_id}/messages

Load all messages for a specific conversation.

**Auth**: Bearer JWT
**Ownership**: `user_id` must match JWT subject AND conversation must belong to user

### Request

```
GET /api/{user_id}/conversations/{conversation_id}/messages
Authorization: Bearer <jwt_token>
```

### Response 200

```json
[
  {
    "id": 1,
    "role": "user",
    "content": "Add a task called Buy groceries",
    "created_at": "2026-04-08T10:00:00Z"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "I've added \"Buy groceries\" to your task list!",
    "created_at": "2026-04-08T10:00:02Z"
  }
]
```

### Response 404

```json
{ "detail": "Conversation not found" }
```

### Response 403

```json
{ "detail": "Access denied" }
```

### Notes

- Messages ordered by `created_at` ascending (chronological)
- Returns up to 50 messages (matches MAX_HISTORY_MESSAGES)
- `role` is "user" or "assistant"
- Tool call information is NOT stored in messages (it's returned live from POST /chat only). The frontend must handle that tool call chips only appear for the current session's responses, not for loaded history.
