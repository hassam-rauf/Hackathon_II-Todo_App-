# Todo App Constitution — The Evolution of Todo

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
No agent writes code until the specification is complete and approved. All code must be generated via Claude Code from specs. Manual coding is not allowed. Every code file must reference its Task ID and Spec section.

Lifecycle: Constitution → Specify → Plan → Tasks → Implement

### II. Tech Stack (Locked)
- **Language:** Python 3.13+ (backend), TypeScript (frontend)
- **Package Manager:** UV (Python), npm (Node.js)
- **Backend:** FastAPI
- **Frontend:** Next.js 16+ (App Router)
- **ORM:** SQLModel (Pydantic + SQLAlchemy)
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth + JWT
- **AI Framework:** OpenAI Agents SDK
- **Tool Protocol:** Official MCP SDK
- **Chat UI:** OpenAI ChatKit
- **Containerization:** Docker
- **Orchestration:** Kubernetes (Minikube local, AKS/GKE/OKE cloud)
- **K8s Packaging:** Helm Charts
- **Event Streaming:** Apache Kafka (Redpanda/Strimzi)
- **Distributed Runtime:** Dapr
- **CI/CD:** GitHub Actions
- **Hosting:** Vercel (frontend), Cloud K8s (backend)

No substitutions without ADR justification and user consent.

### III. Code Quality
- Type hints required on all Python functions
- Pydantic models for all API request/response validation
- async/await preferred for all I/O operations
- Maximum function length: 50 lines
- Single responsibility per function and class
- Clean imports, no unused code, no commented-out code

### IV. Testing (Mandatory)
- Framework: pytest (backend), Vitest (frontend)
- Minimum 80% code coverage target
- Every API endpoint: at least 1 happy path + 1 error test
- MCP tools: each tool tested independently
- Integration tests for authentication flow
- Tests must pass before any commit

### V. Security (NON-NEGOTIABLE)
- Never commit .env, credentials, API keys, or secrets
- JWT tokens for all API authentication
- User isolation: every database query filtered by user_id
- Input validation on all endpoints via Pydantic
- CORS: only allow known frontend origins
- Rate limiting on chat endpoint (Phase III+)
- No hardcoded secrets — always use environment variables

### VI. UI/UX Principles
- Mobile-first responsive design
- Tailwind CSS for all styling (no inline styles)
- Server components by default, client components only for interactivity
- Accessible: ARIA labels, keyboard navigation, semantic HTML
- Consistent design system across all phases
- Loading states and error states for all async operations
- Clear user feedback on every action (success/error toasts)

### VII. Architecture
- Monorepo structure: frontend/ + backend/ in one repository
- Stateless APIs: no server-side session storage
- RESTful conventions for all endpoints
- Event-driven for async operations (Phase V)
- Sidecar pattern for infrastructure abstraction (Dapr, Phase V)
- Smallest viable diff: do not refactor unrelated code

### VIII. Performance
- API response time: < 500ms p95
- Frontend first contentful paint: < 2 seconds
- Docker images: < 500MB (multi-stage builds)
- Database: indexed on user_id and frequently filtered columns
- No N+1 query patterns

## Development Workflow

### SDD Lifecycle (Every Feature)
1. /sp.specify — Write requirements with acceptance criteria
2. /sp.clarify — Clear ambiguities (2-5 targeted questions)
3. /sp.plan — Design architecture and components
4. /sp.adr — Document significant architectural decisions (user consent required)
5. /sp.tasks — Break into atomic, testable work units
6. /sp.analyze — Verify spec ↔ plan ↔ tasks consistency
7. /sp.implement — Execute tasks one by one
8. /sp.phr — Record prompt history
9. /sp.git.commit_pr — Commit and PR

### Hierarchy of Truth
Constitution > Specify > Plan > Tasks > Code

If conflict arises, higher-level artifact wins.

## Governance

- This constitution supersedes all other practices
- Amendments require: documentation of change, user approval, migration plan
- All code must be traceable to a Task ID
- All PRs must verify compliance with these principles
- Complexity must be justified — start simple (YAGNI)

**Version**: 1.0.0 | **Ratified**: 2026-03-29 | **Last Amended**: 2026-03-29
