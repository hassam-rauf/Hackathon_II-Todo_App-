# Quickstart: ChatKit Frontend

**Feature**: 003-chatkit-frontend | **Date**: 2026-04-08

## Prerequisites

- Backend running: `cd backend && uv run uvicorn backend.main:app --reload` (port 8000)
- Frontend running: `cd frontend && npm run dev` (port 3000)
- Neon DB with existing tables (user, session, account, verification, jwks, task, conversation, message)
- OPENAI_API_KEY in backend `.env` (or agent returns fallback message)
- Authenticated user session (sign up / sign in via frontend)

## What This Feature Adds

1. **Backend**: Two new GET endpoints for listing conversations and loading messages
2. **Frontend**: Chat panel with 5 new components integrated into the dashboard
3. **Tests**: ~8-10 new backend tests for conversation endpoints

## Development Order

1. Backend conversation endpoints + tests
2. Frontend API client extensions
3. ToolCallChip component
4. ChatInput component
5. ChatMessages component
6. ChatConversationSelector component
7. ChatPanel container
8. Dashboard integration (sidebar button, panel mount, task refresh callback)

## Verification

```bash
# Backend tests
uv run pytest tests/backend/ -v

# Frontend build
cd frontend && npx next build

# Manual test
# 1. Sign in at localhost:3000/signin
# 2. Go to dashboard
# 3. Click "AI Chat" in sidebar
# 4. Type "Add a task called Test from chat"
# 5. Verify response appears + task list updates
```

## Key Files

| File | Role |
|------|------|
| `backend/routes/conversations.py` | NEW — GET conversations + messages |
| `frontend/components/ChatPanel.tsx` | NEW — Container panel |
| `frontend/components/ChatMessages.tsx` | NEW — Message display |
| `frontend/components/ChatInput.tsx` | NEW — Input + send |
| `frontend/components/ChatConversationSelector.tsx` | NEW — History dropdown |
| `frontend/components/ToolCallChip.tsx` | NEW — Tool action indicator |
| `frontend/lib/api.ts` | MODIFIED — Add chat API methods |
| `frontend/app/dashboard/page.tsx` | MODIFIED — Integrate ChatPanel |
| `backend/main.py` | MODIFIED — Register conversations router |
| `tests/backend/test_conversations.py` | NEW — Endpoint tests |
