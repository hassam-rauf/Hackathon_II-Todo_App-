# AGENT.md — The Evolution of Todo: Complete Project Blueprint

> **This is the SINGLE SOURCE OF TRUTH for building this project.**
> Every decision, tool, workflow, skill, environment detail, and implementation guide is here.
> If it's not in this file, it's not part of the plan.

---

## 1. Project Overview

| Item | Detail |
|------|--------|
| **Project** | The Evolution of Todo — From CLI to Cloud-Native AI System |
| **Method** | Spec-Driven Development (SDD) via Claude Code + Spec-Kit Plus |
| **Constraint** | No manual coding — all code generated from specs via Claude Code |
| **Phases** | 5 (each builds on previous — no skipping) |
| **Total Points** | 1000 + 600 bonus |
| **Submission** | Public GitHub repo + deployed app + 90-sec demo video per phase |
| **Submit At** | https://forms.gle/KMKEKaFUD6ZX4UtY8 |

### Scoring

| Phase | Description | Points |
|-------|------------|:------:|
| I | In-Memory Python Console App | 100 |
| II | Full-Stack Web Application | 150 |
| III | AI-Powered Todo Chatbot | 200 |
| IV | Local Kubernetes Deployment | 250 |
| V | Advanced Cloud Deployment | 300 |
| **TOTAL** | | **1000** |

### Bonus Points

| Feature | Points |
|---------|:------:|
| Reusable Intelligence — Subagents & Agent Skills (skill-creator-pro) | +200 |
| Cloud-Native Blueprints via Agent Skills | +200 |
| Multi-language Support — Urdu in chatbot | +100 |
| Voice Commands — Voice input for todo | +200 |
| **TOTAL BONUS** | **+600** |

### Submission Requirements Per Phase

1. **Public GitHub Repo** — all source code, specs, history, CLAUDE.md, README.md
2. **Deployed App Links** — Vercel (Phase II+), Chatbot URL (Phase III+), K8s URL (Phase IV+)
3. **Demo Video** — maximum 90 seconds (judges only watch 90 sec)
4. **WhatsApp Number** — top submissions invited for live presentation

---

## 2. Agent Rules (Non-Negotiable)

Every agent in this project MUST:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating plan.md.**
3. **Never propose features without updating spec.md.**
4. **Never change approach without updating constitution.md.**
5. **Every code file must link to its Task and Spec section.**
6. **Stop and ask** if spec is missing — never improvise.

### Hierarchy of Truth
```
Constitution > Specify > Plan > Tasks > Code
```

### Agent Failure Modes (MUST Avoid)
- Freestyle code or architecture
- Generate missing requirements
- Create tasks without spec backing
- Alter stack choices without justification
- Add endpoints, fields, or flows not in spec
- Ignore acceptance criteria
- Skip PHR creation after interactions
- Auto-create ADRs without user consent

---

## 3. SDD Lifecycle (Every Feature Follows This)

```
Step 1:  /sp.constitution   → Project principles (once, update as needed)
Step 2:  /sp.specify        → WHAT to build (requirements + acceptance criteria)
Step 3:  /sp.clarify        → Clear ambiguities (2-5 targeted questions)
Step 4:  /sp.plan           → HOW to build (architecture + components)
Step 5:  /sp.adr            → Document significant architectural decisions
Step 6:  /sp.tasks          → BREAKDOWN into atomic, testable work units
Step 7:  /sp.analyze        → Verify spec ↔ plan ↔ tasks consistency
Step 8:  /sp.checklist      → Generate acceptance checklist
Step 9:  /sp.implement      → Execute tasks one by one (code generation)
Step 10: /sp.phr            → Record interaction (Prompt History Record)
Step 11: /sp.git.commit_pr  → Commit code and create PR
Step 12: /sp.taskstoissues  → Convert tasks to GitHub issues
```

### ADR Trigger Test (Before Step 5)
Test for significance — if ALL true, suggest ADR:
- **Impact:** Long-term consequences? (framework, data model, API, security)
- **Alternatives:** Multiple viable options considered?
- **Scope:** Cross-cutting, influences system design?

Never auto-create ADRs — always ask user first.

---

## 4. Constitution (Project Principles)

Save this to `.specify/memory/constitution.md`:

### Tech Stack (Locked — Do Not Change)
- **Language:** Python 3.13+ (backend), TypeScript (frontend)
- **Package Manager:** UV (Python), npm (Node.js)
- **Backend Framework:** FastAPI
- **Frontend Framework:** Next.js 16+ (App Router)
- **ORM:** SQLModel (Pydantic + SQLAlchemy)
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth + JWT
- **AI Framework:** OpenAI Agents SDK
- **Tool Protocol:** Official MCP SDK
- **Chat UI:** OpenAI ChatKit
- **Containerization:** Docker
- **Orchestration:** Kubernetes (Minikube local, AKS/GKE/OKE cloud)
- **Package Manager (K8s):** Helm Charts
- **Event Streaming:** Apache Kafka (via Redpanda/Strimzi)
- **Distributed Runtime:** Dapr
- **CI/CD:** GitHub Actions
- **Hosting:** Vercel (frontend), Cloud K8s (backend)

### Code Quality
- Type hints required on all Python functions
- Pydantic models for all API request/response
- async/await preferred for I/O operations
- No hardcoded secrets — always use .env
- Maximum function length: 50 lines
- Single responsibility per function/class

### Testing
- Framework: pytest (backend), Jest or Vitest (frontend)
- Minimum 80% code coverage
- Every API endpoint must have at least 1 happy path + 1 error test
- MCP tools: test each tool independently
- Integration tests for auth flow

### Security
- Never commit .env, credentials, or API keys
- JWT tokens for all API authentication
- User isolation: every query filtered by user_id
- Input validation on all endpoints (Pydantic)
- CORS: only allow known frontend origins
- Rate limiting on chat endpoint (Phase III+)

### UI/UX Principles
- Mobile-first responsive design
- Tailwind CSS for all styling (no inline styles)
- Server components by default, client components only for interactivity
- Accessible (ARIA labels, keyboard navigation)
- Consistent design system across phases
- Loading states and error states for all async operations

### Architecture
- Monorepo structure (frontend/ + backend/ in one repo)
- Stateless APIs (no server-side session storage)
- RESTful API design conventions
- Event-driven for async operations (Phase V)
- Sidecar pattern for infrastructure abstraction (Dapr, Phase V)

### Performance
- API response time: < 500ms p95
- Frontend first contentful paint: < 2s
- Docker images: < 500MB (multi-stage builds)
- Database queries: indexed on user_id and frequently filtered columns

---

## 5. Environment Setup

### Prerequisites (Install Before Starting)

```bash
# Python 3.13+
# Check: python3 --version

# UV (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Node.js 20+ (for Next.js)
# Check: node --version

# Git
# Check: git --version

# Claude Code
npm install -g @anthropic-ai/claude-code

# Docker Desktop (Phase IV)
# Install from: https://www.docker.com/products/docker-desktop/
# Enable Gordon: Settings > Beta features > toggle on

# Minikube (Phase IV)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Helm (Phase IV)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# kubectl (Phase IV)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# kubectl-ai (Phase IV)
# Install from: https://github.com/GoogleCloudPlatform/kubectl-ai

# Dapr CLI (Phase V)
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash
```

### Windows Users: WSL 2 Required
```bash
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04
```

---

## 6. Environment Variables

### .env.example (Create this file in project root)

```env
# ===== Phase II =====
# Neon Database
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/todo?sslmode=require

# Better Auth
BETTER_AUTH_SECRET=your-shared-jwt-secret-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# ===== Phase III =====
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=dk-your-domain-key

# ===== Phase IV =====
# Docker Registry
DOCKER_REGISTRY=ghcr.io/your-username

# ===== Phase V =====
# Kafka / Redpanda
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
# Or for Redpanda Cloud:
# KAFKA_BOOTSTRAP_SERVERS=your-cluster.cloud.redpanda.com:9092
# KAFKA_SASL_USERNAME=your-username
# KAFKA_SASL_PASSWORD=your-password

# Cloud (pick one)
# Azure
# AZURE_SUBSCRIPTION_ID=your-sub-id
# Google Cloud
# GOOGLE_PROJECT_ID=your-project-id
# Oracle
# OCI_TENANCY=your-tenancy
```

**RULE:** Never commit .env — only .env.example goes to git.

---

## 7. Service Connection Details

### Development (Local)

| Service | URL | Port |
|---------|-----|:----:|
| Next.js Frontend | http://localhost:3000 | 3000 |
| FastAPI Backend | http://localhost:8000 | 8000 |
| FastAPI Docs | http://localhost:8000/docs | 8000 |
| Neon Database | Remote (connection string in .env) | 5432 |
| Dapr Sidecar (Phase V) | http://localhost:3500 | 3500 |

### Frontend → Backend Communication

```typescript
// frontend/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// All backend calls go through this client
export const api = {
  getTasks: (userId: string) => fetch(`${API_BASE}/api/${userId}/tasks`),
  createTask: (userId: string, data: any) => fetch(`${API_BASE}/api/${userId}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(data)
  }),
  // ... etc
};
```

### Docker Compose Networking

```yaml
# Services talk via service names within Docker network:
# frontend → http://backend:8000
# backend  → DATABASE_URL (external Neon)
```

### Kubernetes Networking

```
# Services talk via K8s service names:
# frontend → http://backend-service:8000
# With Dapr: frontend → http://localhost:3500/v1.0/invoke/backend/method/api/...
```

---

## 8. Database Strategy

### ORM: SQLModel

```python
# All models follow this pattern:
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Migration Strategy

| Phase | What Changes | How |
|-------|-------------|-----|
| Phase I | No database (in-memory) | N/A |
| Phase II | Create tasks table | `SQLModel.metadata.create_all(engine)` on startup |
| Phase III | Add conversations, messages tables | Alembic migration: `alembic revision --autogenerate` |
| Phase V | Add priority, tags, due_date, recurrence to tasks | Alembic migration |

### Alembic Setup (Phase II)
```bash
cd backend
uv add alembic
alembic init alembic
# Configure alembic.ini with DATABASE_URL
# alembic revision --autogenerate -m "create tasks table"
# alembic upgrade head
```

### Database Schema Evolution

**Phase II — Tasks Table:**
```
tasks: id, user_id, title, description, completed, created_at, updated_at
```

**Phase III — Add Conversation Tables:**
```
conversations: id, user_id, created_at, updated_at
messages: id, user_id, conversation_id(FK), role, content, created_at
```

**Phase V — Extend Tasks Table:**
```
tasks: + priority(enum), tags(json), due_date(datetime),
       recurrence_pattern(string), next_occurrence(datetime)
```

### Indexes
- `tasks.user_id` — every query filters by user
- `tasks.completed` — status filtering
- `tasks.due_date` — reminder queries (Phase V)
- `messages.conversation_id` — chat history lookup

---

## 9. Testing Strategy

### Backend (pytest + httpx)

```bash
cd backend
uv add --dev pytest pytest-asyncio httpx
uv run pytest
```

| What to Test | How |
|-------------|-----|
| Each API endpoint | Happy path + error cases (404, 400, 401) |
| Auth middleware | Valid JWT, expired JWT, missing JWT, wrong user |
| MCP tools (Phase III) | Each tool independently with mock DB |
| Database models | Create, read, update, delete operations |
| Agent behavior (Phase III) | Mock LLM responses, verify tool calls |

```python
# Example test pattern:
# tests/test_tasks_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers: dict):
    response = await client.post("/api/user1/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"

@pytest.mark.asyncio
async def test_create_task_empty_title(client: AsyncClient, auth_headers: dict):
    response = await client.post("/api/user1/tasks",
        json={"title": ""},
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error
```

### Frontend (Jest/Vitest)

```bash
cd frontend
npm install --save-dev vitest @testing-library/react
npm run test
```

| What to Test | How |
|-------------|-----|
| Components render | @testing-library/react |
| API client functions | Mock fetch, verify calls |
| Auth flow | Mock Better Auth, test redirect |

### E2E Testing (Playwright — Optional but Recommended)

```bash
npm install --save-dev @playwright/test
npx playwright test
```

### Phase-Specific Testing

| Phase | Must Test |
|-------|----------|
| I | All 5 CRUD operations via CLI input/output |
| II | All API endpoints + auth + frontend renders |
| III | MCP tools + agent tool selection + chat flow |
| IV | Docker containers start + K8s pods healthy |
| V | Kafka events flow + Dapr pub/sub + cloud health |

---

## 10. Error Handling Patterns

### Backend (FastAPI)

```python
from fastapi import HTTPException

# Standard error responses:
# 400 Bad Request    — invalid input
# 401 Unauthorized   — missing/invalid JWT
# 403 Forbidden      — user accessing another user's data
# 404 Not Found      — task/conversation doesn't exist
# 422 Unprocessable  — validation error (Pydantic)
# 500 Internal Error — unexpected server error

# Pattern:
@app.get("/api/{user_id}/tasks/{task_id}")
async def get_task(user_id: str, task_id: int, current_user: str = Depends(get_current_user)):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access denied")
    task = await get_task_by_id(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

### Frontend (Next.js)

```typescript
// Pattern: try-catch with user-friendly messages
try {
  const tasks = await api.getTasks(userId);
  setTasks(tasks);
} catch (error) {
  if (error.status === 401) {
    redirect("/signin");  // Token expired
  } else {
    setError("Failed to load tasks. Please try again.");
  }
}
```

### MCP Tools (Phase III)

```python
# Every MCP tool must handle:
# - Task not found → return error message (not crash)
# - Invalid input → return validation error
# - DB connection error → return friendly error
# Agent will relay error message to user naturally
```

### Kafka (Phase V)

```python
# Producer: if Kafka unavailable → log error, don't block main operation
# Consumer: if processing fails → retry 3 times, then dead-letter queue
# Dapr handles retries automatically when used
```

---

## 11. Skill Creation Schedule (via skill-creator-pro)

### What is skill-creator-pro?
A meta-skill at `.claude/skills/skill-creator-pro/` that creates production-grade, reusable skills with embedded domain expertise. Each skill becomes a zero-shot domain expert.

### When to Create Skills (Phase-Wise)

| Phase | Skills to Create | Count |
|-------|-----------------|:-----:|
| Before Phase II | frontend-ui-builder, fastapi-backend-builder, database-sqlmodel-builder, auth-builder | 4 |
| Before Phase III | mcp-server-builder | 1 |
| Before Phase IV | docker-builder, helm-k8s-builder | 2 |
| Before Phase V | dapr-builder | 1 |
| **Total** | | **8** |

### Skill Definitions

#### Skill 1: frontend-ui-builder (Phase II)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | Next.js 16+ App Router, Tailwind CSS, TypeScript |
| **Reuse** | Phase II, III, IV, V |
| **Skills** | `scaffold_nextjs`, `create_page`, `create_component`, `api_client_setup`, `tailwind_styling`, `form_builder`, `responsive_layout` |
| **Domain Knowledge** | App Router patterns, server vs client components, Tailwind design system, accessibility, loading/error states |

#### Skill 2: fastapi-backend-builder (Phase II)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | FastAPI, Pydantic, async Python |
| **Reuse** | Phase II, III, IV, V |
| **Skills** | `scaffold_fastapi`, `create_endpoint`, `request_validation`, `error_handling`, `cors_setup`, `middleware`, `dependency_injection` |
| **Domain Knowledge** | REST conventions, async patterns, Pydantic v2, HTTPException hierarchy, OpenAPI docs |

#### Skill 3: database-sqlmodel-builder (Phase II)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | SQLModel, Neon PostgreSQL, Alembic |
| **Reuse** | Phase II, III, V |
| **Skills** | `create_model`, `neon_db_setup`, `create_migration`, `query_builder`, `db_session_manager`, `seed_data` |
| **Domain Knowledge** | SQLModel patterns, Neon serverless gotchas, connection pooling, Alembic migrations, indexing strategy |

#### Skill 4: auth-builder (Phase II)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | Better Auth, JWT, cross-service auth |
| **Reuse** | Phase II, III, IV, V |
| **Skills** | `setup_better_auth`, `jwt_middleware`, `protect_routes`, `user_isolation`, `shared_secret_config` |
| **Domain Knowledge** | JWT flow, token refresh, Better Auth plugins, session management, security best practices |

#### Skill 5: mcp-server-builder (Phase III)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | Official MCP SDK, tool design |
| **Reuse** | Phase III, V |
| **Skills** | `scaffold_mcp_server`, `create_mcp_tool`, `tool_input_schema`, `tool_error_handling`, `register_tools`, `test_mcp_tool` |
| **Domain Knowledge** | MCP protocol, tool design patterns, stdio/SSE transport, error handling, input validation |

#### Skill 6: docker-builder (Phase IV)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | Docker, multi-stage builds, optimization |
| **Reuse** | Phase IV, V |
| **Skills** | `create_dockerfile`, `create_docker_compose`, `optimize_image`, `health_check`, `multi_stage_build` |
| **Domain Knowledge** | Multi-stage builds, layer caching, .dockerignore, health checks, security scanning, base image selection |

#### Skill 7: helm-k8s-builder (Phase IV)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | Helm Charts, Kubernetes manifests |
| **Reuse** | Phase IV, V |
| **Skills** | `scaffold_helm_chart`, `create_deployment`, `create_service`, `create_ingress`, `create_configmap`, `create_secret`, `values_template` |
| **Domain Knowledge** | K8s resource types, Helm templating, values.yaml patterns, resource limits, probe configuration, ingress rules |

#### Skill 8: dapr-builder (Phase V)
| Field | Value |
|-------|-------|
| **Type** | Builder |
| **Domain** | Dapr sidecar, component configuration |
| **Reuse** | Phase V |
| **Skills** | `dapr_init`, `pubsub_component`, `state_component`, `binding_component`, `secret_component`, `service_invocation`, `dapr_jobs_api` |
| **Domain Knowledge** | Dapr architecture, component YAML, pub/sub patterns, state management, service invocation, Jobs API vs cron, secrets management |

### What Does NOT Need a Skill

| Agent/Task | Why No Skill |
|-----------|-------------|
| SDD Workflow | Already exists as Spec-Kit Plus commands (`.claude/commands/sp.*`) |
| Python Console Agent | Phase I only, too simple, no reuse |
| Chat UI Agent | ChatKit is one-time setup |
| AI Agent Builder | OpenAI SDK setup is straightforward |
| K8s Deploy Agent | kubectl commands, better as scripts |
| Kafka Agent | Absorbed into Dapr Builder (Dapr abstracts Kafka) |
| Cloud Deploy Agent | One-time per cloud, script is better |
| CI/CD Agent | GitHub Actions YAML template is enough |

---

## 12. Todo App Feature Levels

### Basic Level (Phase I & II)
1. **Add Task** — Create new todo items (title required, description optional)
2. **Delete Task** — Remove tasks by ID
3. **Update Task** — Modify title and/or description
4. **View Task List** — Display all tasks with status indicators
5. **Mark as Complete** — Toggle completion status

### Intermediate Level (Phase V — Part A)
1. **Priorities** — high / medium / low
2. **Tags/Categories** — work / home / personal / custom labels
3. **Search** — by keyword in title/description
4. **Filter** — by status, priority, date range
5. **Sort** — by due date, priority, alphabetical, created date

### Advanced Level (Phase V — Part A)
1. **Recurring Tasks** — daily / weekly / monthly auto-reschedule
2. **Due Dates & Reminders** — date picker + notification when due

---

## 13. Complete Project File Structure

```
Todo_App/
│
├── .specify/
│   ├── memory/constitution.md              ← Project principles (Section 4 of this file)
│   ├── templates/                          ← SDD templates (auto-generated)
│   └── scripts/bash/                       ← Automation scripts
│
├── .claude/
│   ├── commands/                           ← Spec-Kit Plus commands
│   │   ├── sp.specify.md, sp.plan.md, sp.tasks.md, sp.implement.md
│   │   ├── sp.clarify.md, sp.analyze.md, sp.checklist.md
│   │   ├── sp.adr.md, sp.phr.md, sp.git.commit_pr.md
│   │   ├── sp.constitution.md, sp.reverse-engineer.md, sp.taskstoissues.md
│   │   └── ...
│   └── skills/
│       ├── skill-creator-pro/              ← Meta-skill (creates other skills)
│       ├── frontend-ui-builder/            ← Created Phase II (skill-creator-pro)
│       ├── fastapi-backend-builder/        ← Created Phase II
│       ├── database-sqlmodel-builder/      ← Created Phase II
│       ├── auth-builder/                   ← Created Phase II
│       ├── mcp-server-builder/             ← Created Phase III
│       ├── docker-builder/                 ← Created Phase IV
│       ├── helm-k8s-builder/              ← Created Phase IV
│       └── dapr-builder/                   ← Created Phase V
│
├── specs/                                  ← All specifications
│   ├── phase1-console/
│   │   ├── spec.md, plan.md, tasks.md
│   ├── phase2-web/
│   │   ├── task-crud/          spec.md, plan.md, tasks.md
│   │   ├── frontend-ui/        spec.md, plan.md, tasks.md
│   │   └── authentication/     spec.md, plan.md, tasks.md
│   ├── phase3-chatbot/
│   │   ├── mcp-server/         spec.md, plan.md, tasks.md
│   │   ├── ai-agent/           spec.md, plan.md, tasks.md
│   │   └── chatkit-ui/         spec.md, plan.md, tasks.md
│   ├── phase4-k8s/
│   │   ├── containerization/   spec.md, plan.md, tasks.md
│   │   └── helm-deploy/        spec.md, plan.md, tasks.md
│   └── phase5-cloud/
│       ├── advanced-features/  spec.md, plan.md, tasks.md
│       ├── kafka-events/       spec.md, plan.md, tasks.md
│       ├── dapr-integration/   spec.md, plan.md, tasks.md
│       └── cloud-deploy/       spec.md, plan.md, tasks.md
│
├── history/                                ← Records
│   ├── prompts/                            ← PHR (Prompt History Records)
│   │   ├── constitution/
│   │   ├── phase1-console/
│   │   ├── phase2-web/
│   │   ├── phase3-chatbot/
│   │   ├── phase4-k8s/
│   │   ├── phase5-cloud/
│   │   └── general/
│   └── adr/                                ← Architecture Decision Records
│       ├── 001-in-memory-storage.md
│       ├── ...through...
│       └── 012-cloud-provider-selection.md
│
├── src/                                    ← Phase I: Console app
│   ├── __init__.py
│   ├── main.py                             ← CLI entry point
│   ├── models.py                           ← Task dataclass
│   └── task_manager.py                     ← CRUD operations
│
├── frontend/                               ← Phase II+: Next.js
│   ├── CLAUDE.md                           ← Frontend-specific agent instructions
│   ├── package.json
│   ├── app/
│   │   ├── layout.tsx                      ← Root layout
│   │   ├── page.tsx                        ← Home/dashboard
│   │   ├── signin/page.tsx
│   │   ├── signup/page.tsx
│   │   └── chat/page.tsx                   ← Phase III
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskCard.tsx
│   │   └── ChatInterface.tsx               ← Phase III
│   └── lib/
│       ├── api.ts                          ← Backend API client
│       └── auth.ts                         ← Better Auth client
│
├── backend/                                ← Phase II+: FastAPI
│   ├── CLAUDE.md                           ← Backend-specific agent instructions
│   ├── pyproject.toml
│   ├── main.py                             ← FastAPI app entry
│   ├── db.py                               ← Neon DB connection
│   ├── models.py                           ← SQLModel models
│   ├── auth.py                             ← JWT middleware
│   ├── routes/
│   │   ├── tasks.py                        ← Task CRUD endpoints
│   │   └── chat.py                         ← Phase III: Chat endpoint
│   ├── mcp/                                ← Phase III: MCP Server
│   │   ├── server.py
│   │   └── tools.py                        ← add_task, list_tasks, etc.
│   ├── services/                           ← Phase V: Kafka consumers
│   │   ├── notification_service.py
│   │   ├── recurring_task_service.py
│   │   └── audit_service.py
│   └── alembic/                            ← Database migrations
│       ├── alembic.ini
│       └── versions/
│
├── helm-chart/                             ← Phase IV+: K8s deployment
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml
│       ├── backend-deployment.yaml
│       ├── backend-service.yaml
│       ├── configmap.yaml
│       ├── secret.yaml
│       └── ingress.yaml
│
├── dapr-components/                        ← Phase V: Dapr config
│   ├── pubsub.yaml                         ← Kafka abstraction
│   ├── statestore.yaml                     ← PostgreSQL state
│   ├── secretstore.yaml                    ← K8s secrets
│   └── subscription.yaml                   ← Event subscriptions
│
├── .github/workflows/                      ← Phase V: CI/CD
│   └── deploy.yml
│
├── tests/                                  ← All tests
│   ├── phase1/
│   │   └── test_task_manager.py
│   ├── backend/
│   │   ├── test_tasks_api.py
│   │   ├── test_auth.py
│   │   ├── test_mcp_tools.py
│   │   └── test_chat.py
│   └── frontend/
│       └── components/
│
├── Dockerfile.frontend                     ← Phase IV
├── Dockerfile.backend                      ← Phase IV
├── docker-compose.yml                      ← Phase IV
├── .env.example                            ← Template (committed)
├── .env                                    ← Actual secrets (NOT committed)
├── .gitignore
├── CLAUDE.md                               ← Root Claude Code instructions
├── AGENT.md                                ← THIS FILE (master blueprint)
├── README.md                               ← Project documentation
└── requirement.md                          ← Original hackathon requirements
```

---

## 14. Phase I: In-Memory Python Console App (100 Points)

### Objective
Build a command-line todo app storing tasks in memory using Python + UV.

### Tech Stack
| Tech | Role |
|------|------|
| Python 3.13+ | Language |
| UV | Package/project manager |
| Claude Code | Code generator |
| Spec-Kit Plus | SDD workflow |

### Features
- Add task (title + description)
- Delete task by ID
- Update task (title and/or description)
- View all tasks with status
- Toggle complete/incomplete

### Skills to Create: NONE (too simple, no reuse)

### SDD Cycle

```
/sp.specify   → specs/phase1-console/spec.md
/sp.clarify   → Task ID auto-increment? Fields? Toggle behavior?
/sp.plan      → specs/phase1-console/plan.md
/sp.adr       → history/adr/001-in-memory-storage.md
/sp.tasks     → specs/phase1-console/tasks.md
/sp.analyze   → Consistency check
/sp.checklist → Acceptance criteria
/sp.implement → Execute T-001 → T-010
/sp.phr       → history/prompts/phase1-console/
/sp.git.commit_pr → Commit
```

### Tasks: T-001 → T-010

```
T-001: UV project scaffold
       - uv init todo_app
       - pyproject.toml with Python 3.13+
       - src/ and tests/ directories

T-002: Task model
       - dataclass with: id(int), title(str), description(str|None),
         completed(bool), created_at(datetime)
       - __str__ method for display

T-003: TaskManager.add_task
       - Auto-increment ID
       - Validate: title required, non-empty
       - Return created task

T-004: TaskManager.delete_task
       - Find by ID, remove from dict
       - Return success/failure message
       - Handle: task not found

T-005: TaskManager.update_task
       - Find by ID, update title and/or description
       - Handle: task not found, empty title

T-006: TaskManager.list_tasks
       - Display all tasks formatted: [x] or [ ] + ID + title
       - Handle: empty list message

T-007: TaskManager.toggle_complete
       - Find by ID, flip completed boolean
       - Handle: task not found

T-008: CLI menu
       - While loop with numbered options
       - 1:Add 2:View 3:Update 4:Delete 5:Complete 6:Exit
       - Clear prompts for each action

T-009: Input validation
       - Empty title rejection
       - Invalid ID handling (not a number, not found)
       - Invalid menu choice handling

T-010: Tests
       - pytest for all TaskManager methods
       - Happy paths + error cases
       - At least 10 test functions
```

### Acceptance Criteria
- [ ] `uv run python src/main.py` starts the app
- [ ] Can add task with title and description
- [ ] Can view all tasks with [x]/[ ] indicators
- [ ] Can update task title and description
- [ ] Can delete task by ID (with "not found" handling)
- [ ] Can toggle complete/incomplete
- [ ] Invalid input handled gracefully (no crash)
- [ ] `uv run pytest` passes all tests
- [ ] Clean code, type hints, docstrings where needed

### ADRs: 1
- ADR-001: In-Memory Dict (keyed by ID) vs List for Task Storage

### Deliverables
- GitHub repo with constitution, specs, history, src/, tests/, README.md, CLAUDE.md
- Working console app with all 5 features

---

## 15. Phase II: Full-Stack Web Application (150 Points)

### Objective
Transform console app into multi-user web app with persistent DB + auth.

### Tech Stack
| Tech | Role |
|------|------|
| Next.js 16+ (App Router) | Frontend |
| FastAPI | Backend API |
| SQLModel | ORM |
| Neon Serverless PostgreSQL | Database |
| Better Auth + JWT | Authentication |
| Tailwind CSS | Styling |

### Skills to Create: 4 (via skill-creator-pro)
1. `frontend-ui-builder`
2. `fastapi-backend-builder`
3. `database-sqlmodel-builder`
4. `auth-builder`

### API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| GET | /api/{user_id}/tasks | JWT | List all tasks |
| POST | /api/{user_id}/tasks | JWT | Create task |
| GET | /api/{user_id}/tasks/{id} | JWT | Get task details |
| PUT | /api/{user_id}/tasks/{id} | JWT | Update task |
| DELETE | /api/{user_id}/tasks/{id} | JWT | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | JWT | Toggle completion |

### Auth Flow
```
User signup/signin on Next.js → Better Auth creates session + JWT →
Frontend sends JWT in every request header: Authorization: Bearer <token> →
FastAPI middleware verifies JWT using BETTER_AUTH_SECRET →
Decodes user_id from token → Matches with URL user_id →
Returns only that user's data
```

### Database Schema
```sql
-- users (managed by Better Auth, auto-created)
users: id(str PK), email(str unique), name(str), created_at(timestamp)

-- tasks (our table)
tasks: id(int PK), user_id(str FK→users.id INDEX), title(str NOT NULL max 200),
       description(text NULL max 1000), completed(bool default false INDEX),
       created_at(timestamp), updated_at(timestamp)
```

### SDD Cycles: 3

#### Cycle 1: Task CRUD API (T-011 → T-023)
```
/sp.specify   → specs/phase2-web/task-crud/spec.md
/sp.plan      → specs/phase2-web/task-crud/plan.md
/sp.adr       → 002-monorepo-structure.md, 003-sqlmodel-orm.md
/sp.tasks     → T-011 to T-023
/sp.implement → Execute
```

```
T-011: Monorepo structure (frontend/ + backend/ + root CLAUDE.md)
T-012: FastAPI scaffold (uv init, pyproject.toml, main.py, routes/, models.py, db.py)
T-013: SQLModel Task model with all fields + indexes
T-014: Neon DB connection (db.py, engine, get_session dependency)
T-015: GET /api/{user_id}/tasks (list with optional status filter)
T-016: POST /api/{user_id}/tasks (create, validate title required)
T-017: GET /api/{user_id}/tasks/{id} (single task, 404 if not found)
T-018: PUT /api/{user_id}/tasks/{id} (update title/description)
T-019: DELETE /api/{user_id}/tasks/{id} (delete, 404 if not found)
T-020: PATCH /api/{user_id}/tasks/{id}/complete (toggle)
T-021: Error handling (HTTPException: 400, 401, 403, 404, 422)
T-022: CORS config (allow frontend origin)
T-023: API tests (pytest + httpx, happy path + error per endpoint)
```

#### Cycle 2: Frontend UI (T-024 → T-032)
```
/sp.specify   → specs/phase2-web/frontend-ui/spec.md
/sp.plan      → specs/phase2-web/frontend-ui/plan.md
/sp.tasks     → T-024 to T-032
/sp.implement → Execute (use frontend-ui-builder skill)
```

```
T-024: Next.js 16 scaffold (App Router, TypeScript, Tailwind CSS)
T-025: API client (frontend/lib/api.ts — centralized, typed)
T-026: Task list page (cards with title, status, created date)
T-027: Create task form (title required, description optional, submit button)
T-028: Edit task (inline edit or modal, save/cancel)
T-029: Delete task (confirm dialog before delete)
T-030: Complete toggle (checkbox or button, optimistic UI update)
T-031: Responsive layout (mobile-first, Tailwind, loading/error states)
T-032: Layered CLAUDE.md (frontend/CLAUDE.md + backend/CLAUDE.md)
```

#### Cycle 3: Authentication (T-033 → T-041)
```
/sp.specify   → specs/phase2-web/authentication/spec.md
/sp.plan      → specs/phase2-web/authentication/plan.md
/sp.adr       → 004-jwt-auth-strategy.md
/sp.tasks     → T-033 to T-041
/sp.implement → Execute (use auth-builder skill)
```

```
T-033: Better Auth install + configure in Next.js
T-034: JWT plugin enable in Better Auth config
T-035: Signup page (/signup — email, password, name)
T-036: Signin page (/signin — email, password)
T-037: JWT middleware in FastAPI (verify signature, extract user_id)
T-038: Protected frontend routes (redirect to /signin if no session)
T-039: User isolation (API filters by user_id from JWT, 403 if mismatch)
T-040: Shared BETTER_AUTH_SECRET in both .env files
T-041: Auth tests (signup flow, login flow, protected access, isolation)
```

### ADRs: 3
- 002: Monorepo vs Separate Repos
- 003: SQLModel as ORM (vs raw SQL, vs Django ORM, vs Tortoise)
- 004: Better Auth + JWT for Cross-Service Authentication

### Acceptance Criteria
- [ ] Frontend loads at localhost:3000
- [ ] Backend docs at localhost:8000/docs
- [ ] User can signup and signin
- [ ] Authenticated user can CRUD tasks
- [ ] User A cannot see User B's tasks
- [ ] Responsive on mobile
- [ ] All API tests pass
- [ ] Deployed on Vercel (frontend) + backend accessible

---

## 16. Phase III: AI-Powered Todo Chatbot (200 Points)

### Objective
Add AI chatbot that manages todos via natural language using MCP tools.

### Tech Stack
| Tech | Role |
|------|------|
| OpenAI ChatKit | Chat UI (pre-built) |
| OpenAI Agents SDK | AI agent with tool-calling |
| Official MCP SDK | Tool protocol (AI ↔ app) |
| FastAPI | Chat endpoint |
| SQLModel | Conversation + Message models |
| Neon DB | Persist conversations |

### Skills to Create: 1 (via skill-creator-pro)
- `mcp-server-builder`

### Architecture
```
ChatKit UI → POST /api/{user_id}/chat → OpenAI Agent → MCP Tools → Neon DB
     ↑                                                                  │
     └──────────────────── response ←───────────────────────────────────┘
```

### MCP Server Transport
- **In-process** (recommended for this project) — MCP server runs inside FastAPI
- Agent connects to MCP tools directly via function calls
- No separate process needed

### New Database Tables
```sql
conversations: id(int PK), user_id(str INDEX), created_at, updated_at
messages: id(int PK), user_id(str), conversation_id(int FK INDEX),
          role(str: 'user'|'assistant'), content(text), created_at
```

### MCP Tools

| Tool | Parameters | Returns | Triggers On |
|------|-----------|---------|-------------|
| add_task | user_id, title, description? | {task_id, status, title} | "Add...", "Remember..." |
| list_tasks | user_id, status? | [{id, title, completed}...] | "Show...", "What's pending?" |
| complete_task | user_id, task_id | {task_id, status, title} | "Done...", "Finished..." |
| delete_task | user_id, task_id | {task_id, status, title} | "Delete...", "Remove..." |
| update_task | user_id, task_id, title?, desc? | {task_id, status, title} | "Change...", "Rename..." |

### Chat Endpoint

```
POST /api/{user_id}/chat
Request:  { conversation_id?: int, message: string }
Response: { conversation_id: int, response: string, tool_calls: array }
```

### Stateless Conversation Flow
```
1. Receive message + optional conversation_id
2. If no conversation_id → create new conversation in DB
3. Fetch message history from DB (by conversation_id)
4. Build message array: [history...] + new user message
5. Store user message in DB
6. Run OpenAI agent with MCP tools available
7. Agent decides which tool(s) to call
8. MCP tool executes on DB, returns result
9. Agent generates natural language response
10. Store assistant response in DB
11. Return response + tool_calls to frontend
12. Server holds ZERO state — any instance can handle next request
```

### ChatKit Setup
1. Install ChatKit component in Next.js
2. Deploy frontend → get production URL
3. Add URL to OpenAI domain allowlist
4. Get domain key → `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`
5. Connect ChatKit to POST /api/{user_id}/chat

### SDD Cycles: 3

#### Cycle 1: MCP Server + Tools (T-042 → T-049)
```
T-042: MCP Server setup (Official MCP SDK, in-process)
T-043: add_task tool (validate title, create in DB, return confirmation)
T-044: list_tasks tool (filter by status: all/pending/completed)
T-045: complete_task tool (find task, toggle, return confirmation)
T-046: delete_task tool (find task, delete, return confirmation)
T-047: update_task tool (find task, update fields, return confirmation)
T-048: Tool error handling (task not found, invalid input, DB error → friendly message)
T-049: MCP tools tests (each tool independently)
```

#### Cycle 2: AI Agent + Chat Endpoint (T-050 → T-058)
```
T-050: Conversation SQLModel
T-051: Message SQLModel
T-052: Alembic migration for new tables
T-053: OpenAI Agents SDK setup (agent config, system prompt, tool binding)
T-054: Agent behavior: detect intent → select correct tool → confirm action
T-055: POST /api/{user_id}/chat endpoint (stateless)
T-056: Conversation flow implementation (fetch history → run agent → store)
T-057: Resume conversations after restart (history from DB)
T-058: Agent integration tests (mock LLM, verify tool selection)
```

#### Cycle 3: ChatKit Frontend (T-059 → T-065)
```
T-059: ChatKit component install + configure
T-060: OpenAI domain allowlist setup
T-061: Connect ChatKit → POST /api/{user_id}/chat
T-062: Display conversation history (load previous chats)
T-063: Show tool call indicators (what agent did)
T-064: Chat styling (responsive, matches app design)
T-065: E2E test (type message → agent calls tool → response shows)
```

### ADRs: 2
- 005: MCP Protocol for AI-Tool Interface (vs direct function calls)
- 006: Stateless Chat Architecture with DB Persistence (vs in-memory sessions)

### Acceptance Criteria
- [ ] "Add a task to buy groceries" → task created
- [ ] "Show me all tasks" → tasks listed
- [ ] "Mark task 3 as complete" → task completed
- [ ] "Delete task 2" → task removed
- [ ] "Change task 1 to 'Call mom'" → task updated
- [ ] Chat history persists across page refresh
- [ ] Server restart doesn't lose conversations
- [ ] Errors handled gracefully ("Task not found" as natural language)

---

## 17. Phase IV: Local Kubernetes Deployment (250 Points)

### Objective
Containerize and deploy on local Kubernetes (Minikube) with Helm.

### Tech Stack
| Tech | Role |
|------|------|
| Docker | Containerization |
| Docker Desktop + Gordon | AI Docker assistant |
| Minikube | Local K8s cluster |
| Helm Charts | K8s package manager |
| kubectl-ai | AI K8s commands |
| Kagent | Advanced K8s operations |

### Skills to Create: 2 (via skill-creator-pro)
- `docker-builder`
- `helm-k8s-builder`

### SDD Cycles: 2

#### Cycle 1: Containerization (T-066 → T-073)
```
T-066: Backend Dockerfile
       FROM python:3.13-slim AS builder
       Multi-stage: deps → production
       Target size: < 300MB

T-067: Frontend Dockerfile
       FROM node:20-alpine AS builder
       Multi-stage: deps → build → production (standalone output)
       Target size: < 500MB

T-068: .dockerignore (node_modules, __pycache__, .env, .git, tests/)

T-069: docker-compose.yml
       services:
         frontend: build ./frontend, port 3000, depends_on backend
         backend: build ./backend, port 8000, env_file .env
       network: todo-network

T-070: Health checks
       Backend: GET /health → 200
       Frontend: GET / → 200

T-071: Image optimization (minimize layers, clean caches, non-root user)

T-072: Gordon AI verification
       docker ai "analyze my Dockerfiles for best practices"

T-073: Docker build + run tests (both containers start, communicate, API works)
```

#### Cycle 2: Helm + Minikube (T-074 → T-085)
```
T-074: Minikube start (minikube start --memory=4096 --cpus=2)

T-075: Helm chart scaffold
       helm-chart/
       ├── Chart.yaml (name: todo-app, version: 1.0.0)
       ├── values.yaml
       └── templates/

T-076: Frontend K8s resources
       - Deployment (2 replicas, resource limits, liveness probe)
       - Service (ClusterIP, port 3000)

T-077: Backend K8s resources
       - Deployment (2 replicas, resource limits, liveness/readiness probe)
       - Service (ClusterIP, port 8000)

T-078: ConfigMap
       - NEXT_PUBLIC_API_URL, APP_ENV, LOG_LEVEL

T-079: Kubernetes Secret
       - DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY

T-080: Ingress (path-based routing)
       - / → frontend-service:3000
       - /api → backend-service:8000

T-081: values.yaml
       - image.repository, image.tag
       - replicaCount, resources.limits/requests
       - env overrides

T-082: Deploy + verify
       helm install todo ./helm-chart
       kubectl get pods (all Running)
       kubectl get services
       minikube service list

T-083: kubectl-ai troubleshooting
       kubectl-ai "check pod status"
       kubectl-ai "show logs for backend pod"

T-084: Kagent health check
       kagent "analyze cluster health"

T-085: Integration test on K8s (curl endpoints, verify responses)
```

### Resource Limits (values.yaml)
```yaml
frontend:
  resources:
    requests: { cpu: 100m, memory: 128Mi }
    limits: { cpu: 500m, memory: 512Mi }
backend:
  resources:
    requests: { cpu: 100m, memory: 128Mi }
    limits: { cpu: 500m, memory: 512Mi }
```

### ADRs: 2
- 007: Multi-stage Docker Build Strategy
- 008: Helm Charts vs Raw K8s Manifests

### Acceptance Criteria
- [ ] `docker-compose up` runs both services locally
- [ ] `helm install todo ./helm-chart` deploys to Minikube
- [ ] All pods in Running state
- [ ] Frontend accessible via Minikube ingress
- [ ] API works through K8s service
- [ ] Health checks passing

---

## 18. Phase V: Advanced Cloud Deployment (300 Points)

### Objective
Add advanced features + Kafka event streaming + Dapr + deploy to cloud K8s.

### Tech Stack
| Tech | Role |
|------|------|
| Kafka (Redpanda/Strimzi) | Event streaming |
| Dapr | Distributed runtime (sidecar) |
| AKS / GKE / OKE | Cloud Kubernetes |
| GitHub Actions | CI/CD pipeline |

### Skills to Create: 1 (via skill-creator-pro)
- `dapr-builder`

### Part A: Advanced Features (T-086 → T-094)

```
T-086: Priority field (enum: high/medium/low)
       - Add to Task SQLModel + Alembic migration
       - API: accept priority in create/update, filter by priority
       - UI: priority badge, priority selector

T-087: Tags/Categories (JSON array field)
       - Add to Task SQLModel + migration
       - API: accept tags, filter by tag
       - UI: tag chips, tag input

T-088: Search (keyword in title/description)
       - API: ?search=keyword query param (ILIKE query)
       - UI: search bar with debounce

T-089: Filter (by status + priority + date range)
       - API: ?status=pending&priority=high&from=2025-01-01&to=2025-12-31
       - UI: filter panel/dropdown

T-090: Sort (by due_date, priority, alphabetical, created_at)
       - API: ?sort=due_date&order=asc
       - UI: sort dropdown

T-091: Due date field
       - Add to Task SQLModel + migration
       - API: accept due_date in create/update
       - UI: date picker component

T-092: Recurring tasks
       - Add recurrence_pattern(str) + next_occurrence(datetime) to Task
       - Migration
       - Logic: on complete, if recurring → create next occurrence

T-093: MCP tools update
       - All tools support: priority, tags, due_date, recurrence
       - list_tasks supports: filter, sort, search params

T-094: Agent behavior update
       - Understand: "Add high priority task...", "Show urgent tasks"
       - Understand: "Set recurring weekly meeting", "What's due tomorrow?"
```

### Part B: Kafka Events (T-095 → T-102)

#### Kafka Architecture
```
MCP Tools (producer) → Kafka Topics → Consumer Services
                          │
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
    task-events      reminders     task-updates
         │              │              │
         ↓              ↓              ↓
  ┌──────────┐  ┌────────────┐  ┌──────────┐
  │Recurring │  │Notification│  │WebSocket │
  │Task Svc  │  │  Service   │  │  Sync    │
  └──────────┘  └────────────┘  └──────────┘
```

#### Kafka Topics
| Topic | Producer | Consumer | Events |
|-------|----------|----------|--------|
| task-events | MCP tools | Recurring Svc, Audit Svc | created, updated, completed, deleted |
| reminders | MCP tools (on due_date set) | Notification Svc | reminder.scheduled, reminder.due |
| task-updates | MCP tools | WebSocket Svc (optional) | Real-time sync |

#### Event Schemas
```python
# Task Event
{ "event_type": "created|updated|completed|deleted",
  "task_id": 1, "task_data": {...}, "user_id": "abc", "timestamp": "ISO8601" }

# Reminder Event
{ "task_id": 1, "title": "Buy groceries",
  "due_at": "ISO8601", "remind_at": "ISO8601", "user_id": "abc" }
```

```
T-095: Kafka setup (Strimzi operator on K8s or Redpanda Cloud)
T-096: Create topics (task-events, reminders, task-updates)
T-097: Event schema dataclasses (TaskEvent, ReminderEvent)
T-098: Producer in MCP tools (publish event after every operation)
T-099: Notification Service (consume reminders → log/notify)
T-100: Recurring Task Service (consume task-completed → create next if recurring)
T-101: Audit Service (consume task-events → store activity log)
T-102: Kafka integration tests
```

### Part C: Dapr Integration (T-103 → T-112)

#### Dapr Components
| Component | Type | Purpose | Config File |
|-----------|------|---------|------------|
| kafka-pubsub | pubsub.kafka | Replace direct Kafka calls | dapr-components/pubsub.yaml |
| statestore | state.postgresql | Conversation state via HTTP | dapr-components/statestore.yaml |
| kubernetes-secrets | secretstores.kubernetes | Credentials via HTTP | dapr-components/secretstore.yaml |

#### Without Dapr vs With Dapr
```python
# WITHOUT (direct Kafka):
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers="kafka:9092")
producer.send("task-events", value=event)

# WITH DAPR (HTTP):
await httpx.post("http://localhost:3500/v1.0/publish/kafka-pubsub/task-events", json=event)
# Benefits: no Kafka library, swap to RabbitMQ via YAML change, built-in retries
```

```
T-103: Dapr install (dapr init -k on Minikube)
T-104: pubsub.yaml (pubsub.kafka → Kafka broker)
T-105: statestore.yaml (state.postgresql → Neon DB)
T-106: secretstore.yaml (secretstores.kubernetes)
T-107: subscription.yaml (which endpoints consume which topics)
T-108: Replace Kafka producer with Dapr pub/sub HTTP calls
T-109: Replace conversation state with Dapr state API (optional)
T-110: Service invocation (frontend → backend via Dapr sidecar)
T-111: Dapr Jobs API for scheduled reminders (exact time, no polling)
T-112: Dapr integration tests
```

### Part D: Cloud Deployment (T-113 → T-122)

#### Cloud Options
| Provider | Service | Free Tier |
|----------|---------|-----------|
| Azure | AKS | $200 / 30 days |
| Google Cloud | GKE | $300 / 90 days |
| Oracle | OKE | **Always free** (4 OCPUs, 24GB RAM) |

#### Kafka Cloud Options
| Service | Tier | Recommendation |
|---------|------|---------------|
| Redpanda Cloud | Free serverless | Best for hackathon |
| Strimzi on K8s | Free (self-hosted) | Best for learning |
| Confluent Cloud | $400 credit / 30 days | Most features |

```
T-113: Cloud K8s cluster create (AKS/GKE/OKE)
T-114: kubectl context switch to cloud cluster
T-115: Dapr install on cloud cluster (dapr init -k)
T-116: Kafka on cloud (Strimzi self-hosted OR Redpanda Cloud)
T-117: Helm deploy to cloud (same charts, different values.yaml)
T-118: GitHub Actions CI/CD
       on: push to main
       steps: checkout → test → docker build → push to registry → helm upgrade
T-119: Monitoring + logging (kubectl logs, basic health dashboard)
T-120: Domain + SSL (optional — cloud provider's default URL is fine)
T-121: Production scaling test (2+ replicas, resource limits verified)
T-122: E2E cloud test (frontend accessible, chat works, events flow)
```

#### GitHub Actions Workflow Pattern
```yaml
# .github/workflows/deploy.yml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Backend tests
        run: cd backend && uv run pytest
      - name: Frontend tests
        run: cd frontend && npm test

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build & push backend image
        run: docker build -f Dockerfile.backend -t $REGISTRY/todo-backend:$SHA .
      - name: Build & push frontend image
        run: docker build -f Dockerfile.frontend -t $REGISTRY/todo-frontend:$SHA .
      - name: Deploy to K8s
        run: |
          helm upgrade --install todo ./helm-chart \
            --set backend.image.tag=$SHA \
            --set frontend.image.tag=$SHA
```

### ADRs: 4
- 009: Event-Driven Architecture with Kafka
- 010: Kafka Provider (Redpanda vs Strimzi vs Confluent)
- 011: Dapr Sidecar Pattern
- 012: Cloud Provider Selection

### Acceptance Criteria
- [ ] Priority, tags, search, filter, sort all working
- [ ] Recurring tasks auto-create on completion
- [ ] Kafka events flowing (task-events, reminders)
- [ ] Dapr pub/sub replacing direct Kafka calls
- [ ] Cloud K8s cluster running with all services
- [ ] CI/CD deploys on push to main
- [ ] Chat works end-to-end on cloud URL

---

## 19. README Template

Every phase must update README.md following this structure:

```markdown
# Todo App — Evolution of Todo (Hackathon II)

## Phase [X]: [Phase Name]

### Overview
[1-2 sentences about what this phase implements]

### Tech Stack
[Table of technologies used]

### Setup Instructions

#### Prerequisites
[List what to install]

#### Environment Variables
[List required .env variables]

#### Running Locally
```bash
# Step-by-step commands to run
```

#### Running Tests
```bash
# How to run tests
```

### Features
[List features with checkmarks]

### API Documentation
[Link to /docs or list endpoints]

### Architecture
[Brief description or diagram]

### Demo Video
[Link to 90-sec demo]

### Spec-Driven Development
All code was generated via Claude Code using Spec-Kit Plus.
- Constitution: `.specify/memory/constitution.md`
- Specs: `specs/phase[X]-[name]/`
- History: `history/prompts/phase[X]-[name]/`
```

---

## 20. Master Counts

### Tasks: 122 Total
| Phase | Range | Count |
|-------|-------|:-----:|
| I | T-001 → T-010 | 10 |
| II | T-011 → T-041 | 31 |
| III | T-042 → T-065 | 24 |
| IV | T-066 → T-085 | 20 |
| V | T-086 → T-122 | 37 |

### ADRs: 12 Total
| # | Phase | Decision |
|---|-------|----------|
| 001 | I | In-Memory Storage |
| 002 | II | Monorepo Structure |
| 003 | II | SQLModel ORM |
| 004 | II | JWT Auth Strategy |
| 005 | III | MCP Protocol |
| 006 | III | Stateless Chat |
| 007 | IV | Docker Strategy |
| 008 | IV | Helm Charts |
| 009 | V | Event-Driven Architecture |
| 010 | V | Kafka Provider |
| 011 | V | Dapr Sidecar |
| 012 | V | Cloud Provider |

### Skills: 8 Total (via skill-creator-pro)
| # | Skill | Created Before |
|---|-------|---------------|
| 1 | frontend-ui-builder | Phase II |
| 2 | fastapi-backend-builder | Phase II |
| 3 | database-sqlmodel-builder | Phase II |
| 4 | auth-builder | Phase II |
| 5 | mcp-server-builder | Phase III |
| 6 | docker-builder | Phase IV |
| 7 | helm-k8s-builder | Phase IV |
| 8 | dapr-builder | Phase V |

### SDD Cycles: 13 Total (39 spec files)
| Phase | Cycles | Features |
|-------|:------:|----------|
| I | 1 | Console CRUD |
| II | 3 | API, Frontend, Auth |
| III | 3 | MCP, Agent, ChatKit |
| IV | 2 | Docker, Helm |
| V | 4 | Advanced, Kafka, Dapr, Cloud |

### Spec-Kit Commands Used Per Cycle
```
/sp.specify, /sp.clarify, /sp.plan, /sp.adr (if significant),
/sp.tasks, /sp.analyze, /sp.checklist, /sp.implement,
/sp.phr, /sp.git.commit_pr, /sp.taskstoissues
```

---

## 21. Quick Reference Commands

```bash
# ===== Spec-Kit Plus =====
/sp.constitution          # Define/update principles
/sp.specify               # Write requirements
/sp.clarify               # Ask clarification questions
/sp.plan                  # Design architecture
/sp.adr <title>           # Document decision
/sp.tasks                 # Generate task breakdown
/sp.analyze               # Verify consistency
/sp.checklist             # Acceptance checklist
/sp.implement             # Execute tasks
/sp.phr                   # Record prompt history
/sp.git.commit_pr         # Commit and PR
/sp.taskstoissues         # Tasks → GitHub issues

# ===== Development =====
uv init <project>                          # New Python project
uv add <package>                           # Install dependency
uv run python src/main.py                  # Run Phase I
cd frontend && npm run dev                 # Next.js dev server
cd backend && uvicorn main:app --reload    # FastAPI dev server
docker-compose up                          # Both services

# ===== Testing =====
cd backend && uv run pytest                # Backend tests
cd frontend && npm test                    # Frontend tests

# ===== Docker =====
docker build -f Dockerfile.backend -t todo-backend .
docker build -f Dockerfile.frontend -t todo-frontend .
docker-compose up --build
docker ai "analyze my images"              # Gordon

# ===== Kubernetes =====
minikube start --memory=4096 --cpus=2
helm install todo ./helm-chart
helm upgrade todo ./helm-chart
kubectl get pods
kubectl logs <pod-name>
kubectl-ai "check pod status"
kagent "cluster health"

# ===== Dapr =====
dapr init -k                               # Install on K8s
kubectl apply -f dapr-components/          # Apply configs

# ===== Cloud =====
az aks get-credentials --name <cluster>    # Azure
gcloud container clusters get-credentials  # GKE
```

---

## 22. Per-Phase Execution Checklist

Use this for EVERY phase:

```
[ ] Read AGENT.md section for this phase
[ ] Create skills if scheduled (skill-creator-pro)
[ ] Run SDD cycle for each feature:
    [ ] /sp.specify
    [ ] /sp.clarify
    [ ] /sp.plan
    [ ] /sp.adr (if significant decision)
    [ ] /sp.tasks
    [ ] /sp.analyze
    [ ] /sp.implement (task by task)
    [ ] /sp.phr
    [ ] /sp.git.commit_pr
[ ] All tests passing
[ ] Acceptance criteria met (check boxes above)
[ ] README.md updated
[ ] Demo video ready (90 sec max)
[ ] Submitted via Google Form
```
