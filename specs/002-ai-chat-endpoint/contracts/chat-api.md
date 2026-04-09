# Chat API Contract

**Feature**: 002-ai-chat-endpoint | **Date**: 2026-04-08

## POST /api/{user_id}/chat

### Request
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```
- `conversation_id` (optional int): Omit to start new conversation
- `message` (required string): Non-empty user message

### Response (200)
```json
{
  "conversation_id": 123,
  "response": "Done! I've added 'buy groceries' to your task list.",
  "tool_calls": [
    {"tool": "add_task", "args": {"title": "buy groceries"}, "result": {"task_id": 1, "status": "created"}}
  ]
}
```

### Errors
- 400: `{"detail": "Message is required"}`
- 404: `{"detail": "Conversation not found"}`
- 403: `{"detail": "Access denied"}`
- 503: `{"detail": "I'm having trouble right now. Please try again shortly."}`
