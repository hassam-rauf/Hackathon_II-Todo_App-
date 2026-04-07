# Backend — Claude Code Instructions

## Stack
- FastAPI, SQLModel, Neon PostgreSQL, Python 3.13+

## Conventions
- Type hints on all functions
- Pydantic models for all request/response
- HTTPException for errors (400, 401, 403, 404, 422)
- `get_session` dependency injection for DB
- async/await for I/O when using async drivers

## Running
```bash
cd backend && uv run uvicorn backend.main:app --reload  # localhost:8000
```

## Environment
- `DATABASE_URL` — Neon PostgreSQL connection string
- `FRONTEND_URL` — allowed CORS origin (default: http://localhost:3000)

## Testing
```bash
uv run pytest tests/backend/ -v
```
