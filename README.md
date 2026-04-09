# The Evolution of Todo

AI-powered todo app built with Spec-Driven Development (SDD) using Claude Code and Spec-Kit Plus.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (App Router), React 19, Tailwind CSS 4, OpenAI ChatKit |
| Backend | Python 3.13+, FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK |
| Database | Neon Serverless PostgreSQL |
| Auth | Better Auth (frontend) + JWT/HS256 (backend) |
| Migrations | Alembic |

## Project Structure

```
Todo_App/
├── frontend/                 # Next.js app
│   ├── app/                  # App Router pages (dashboard, signin, signup)
│   ├── components/           # ChatKitPanel, TaskList, TaskCard, TaskForm, etc.
│   └── lib/                  # API client, auth config
├── backend/                  # FastAPI server
│   ├── routes/               # tasks.py, chat.py, conversations.py
│   ├── mcp/                  # MCP server + tools (FastMCP, dispatcher, schemas)
│   ├── agent.py              # OpenAI Agents SDK (Agent + Runner + @function_tool)
│   ├── auth.py               # JWT verification middleware
│   ├── models.py             # Task, Conversation, Message (SQLModel)
│   ├── db.py                 # Neon PostgreSQL connection
│   └── alembic/              # Database migration scripts
├── specs/                    # SDD specification files
│   ├── 001-mcp-server-tools/ # MCP server spec, plan, tasks
│   ├── 002-ai-chat-endpoint/ # AI agent + chat spec, plan, tasks
│   └── 003-chatkit-frontend/ # ChatKit frontend spec, plan, tasks
├── tests/                    # 78 backend tests
└── src/                      # Phase I console app
```

## Prerequisites

- Python 3.13+ with [UV](https://docs.astral.sh/uv/)
- Node.js 18+
- Neon PostgreSQL database ([neon.tech](https://neon.tech))
- OpenAI API key ([platform.openai.com](https://platform.openai.com))

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd Todo_App

# Backend (Python)
uv sync

# Frontend (Node)
cd frontend && npm install && cd ..
```

### 2. Configure environment variables

**Backend** — create `backend/.env`:

```env
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
AUTH_SECRET=your-shared-auth-secret
OPENAI_API_KEY=sk-your-openai-api-key
FRONTEND_URL=http://localhost:3000
```

**Frontend** — create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
AUTH_SECRET=your-shared-auth-secret
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
```

> `AUTH_SECRET` must be the same in both files for JWT verification to work.

### 3. Run database migrations

```bash
cd backend
uv run alembic upgrade head
cd ..
```

### 4. Start development servers

```bash
# Terminal 1 — Backend (port 8000)
cd backend && uv run uvicorn backend.main:app --reload

# Terminal 2 — Frontend (port 3000)
cd frontend && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. **Sign up** at `/signup` with name, email, and password
2. **Sign in** at `/signin`
3. **Dashboard** — add, edit, complete, and delete tasks manually
4. **AI Chat** — click "AI Chat" in the sidebar to open the ChatKit panel and manage tasks via natural language:
   - "Add a task to buy groceries"
   - "Show me all my pending tasks"
   - "Mark task 3 as complete"
   - "Delete the meeting task"
   - "Change task 1 to 'Call mom tonight'"

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/{user_id}/tasks` | Create task |
| GET | `/api/{user_id}/tasks` | List tasks |
| GET | `/api/{user_id}/tasks/{id}` | Get task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| POST | `/api/{user_id}/chat` | Send chat message |
| GET | `/api/{user_id}/conversations` | List conversations |
| GET | `/api/{user_id}/conversations/{id}/messages` | Get messages |

All endpoints (except `/health`) require a valid JWT token in the `Authorization: Bearer <token>` header.

## MCP Server

The MCP server is mounted at `/mcp` and exposes 5 tools via the Official MCP SDK (FastMCP):

- `add_task` — Create a new task
- `list_tasks` — List tasks (all/pending/completed)
- `complete_task` — Mark task as done
- `delete_task` — Remove a task
- `update_task` — Modify title/description

## Architecture

```
ChatKit UI → POST /api/{user_id}/chat → OpenAI Agents SDK → MCP Dispatcher → MCP Tools → Neon DB
```

The chat endpoint is fully stateless — conversation history is stored in the database and loaded on each request.

## Running Tests

```bash
uv run pytest tests/backend/ -v    # 78 tests
uv run pytest tests/phase1/ -v     # 32 tests (Phase I console app)
```

## Building for Production

```bash
cd frontend && npx next build
```

## Phase Summary

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Console App | Complete (32 tests) |
| II | Full-Stack Web App (CRUD + Auth) | Complete (36 tests) |
| III | AI-Powered Chatbot (MCP + Agents SDK + ChatKit) | Complete (78 total tests) |

## SDD Artifacts

All phases follow Spec-Driven Development. Specs, plans, and tasks are in the `specs/` directory. Prompt History Records are in `history/prompts/`.
