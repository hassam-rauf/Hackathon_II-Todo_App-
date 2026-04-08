# Data Model: AI Agent + Chat Endpoint

**Feature**: 002-ai-chat-endpoint | **Date**: 2026-04-08

## New Entities

### Conversation

A chat session between a user and the AI agent.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | int (PK) | auto-increment | Referenced by Message.conversation_id |
| user_id | str | indexed, required | Ownership isolation key |
| created_at | datetime | auto UTC | Immutable |
| updated_at | datetime | auto UTC | Updated on each new message |

### Message

A single message within a conversation.

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | int (PK) | auto-increment | Unique message identifier |
| conversation_id | int (FK) | indexed, references Conversation.id | Groups messages by conversation |
| user_id | str | indexed | Denormalized for query efficiency |
| role | str | "user" or "assistant" | Who sent this message |
| content | str (text) | required, no length limit | Message text content |
| created_at | datetime | auto UTC | Ordering within conversation |

## Relationships

- Conversation → Message: one-to-many (a conversation has many messages)
- Message → Conversation: many-to-one (each message belongs to one conversation)
- User → Conversation: one-to-many (a user has many conversations)
- Both entities filtered by user_id for ownership isolation

## Existing Entities (No Changes)

- **Task**: Unchanged from Cycle 1. MCP tools operate on tasks via the dispatcher.

## No Migrations

Tables will be created via `SQLModel.metadata.create_all()` on app startup (same pattern as existing Task table). For production Neon DB, tables need to be created manually or via init script (same as Phase II).
