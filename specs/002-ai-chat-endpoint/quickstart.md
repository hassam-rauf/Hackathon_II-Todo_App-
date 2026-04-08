# Quickstart: AI Agent + Chat Endpoint

**Feature**: 002-ai-chat-endpoint | **Date**: 2026-04-08

## What This Feature Adds
- POST /api/{user_id}/chat endpoint for AI-powered todo management
- Conversation and Message database models
- OpenAI agent with system prompt and MCP tool binding

## Prerequisites
- Cycle 1 MCP tools at backend/mcp/ (already done)
- `openai` package added to backend/pyproject.toml
- OPENAI_API_KEY in .env (optional — works without it using fallback)

## Testing
```bash
uv run pytest tests/backend/test_chat.py -v    # Chat tests only
uv run pytest tests/backend/ -v                # All backend tests
```

## Usage (with API key)
```bash
curl -X POST http://localhost:8000/api/user1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```
