# Architecture Plan: Frontend UI

**Feature**: Frontend UI (Phase II, Cycle 2)
**Created**: 2026-03-31
**Status**: Draft

## Scope

### In Scope
- Next.js 16+ App Router scaffold with TypeScript + Tailwind CSS
- Task list page with CRUD operations
- Centralized API client
- Loading, error, empty states
- Responsive mobile-first layout

### Out of Scope
- Authentication (Cycle 3)
- Chat page (Phase III)
- Deployment to Vercel

## Architecture

### Project Structure
```
frontend/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── .env.local              ← NEXT_PUBLIC_API_URL
├── app/
│   ├── layout.tsx          ← Root layout (html, body, font, shared UI shell)
│   ├── page.tsx            ← Home page → redirects or shows task list
│   ├── loading.tsx         ← Global loading skeleton
│   └── error.tsx           ← Global error boundary
├── components/
│   ├── TaskList.tsx        ← Maps tasks to TaskCard components
│   ├── TaskCard.tsx        ← Single task display (checkbox, title, actions)
│   ├── TaskForm.tsx        ← Create/edit form (client component)
│   └── EmptyState.tsx      ← "No tasks yet" display
└── lib/
    └── api.ts              ← Centralized API client
```

### Component Hierarchy
```
layout.tsx
└── page.tsx (server component → fetches tasks)
    ├── TaskForm (client — "use client", useState for form)
    ├── TaskList (client — needs onClick handlers)
    │   └── TaskCard × N (client — checkbox, edit, delete)
    └── EmptyState (server — static display)
```

### Data Flow
```
page.tsx (initial load)
  → lib/api.ts → GET /api/{user_id}/tasks → render TaskList

TaskForm (create)
  → lib/api.ts → POST /api/{user_id}/tasks → refetch list

TaskCard (toggle)
  → lib/api.ts → PATCH /api/{user_id}/tasks/{id}/complete → update local state

TaskCard (delete)
  → confirm dialog → lib/api.ts → DELETE → remove from local state

TaskCard (edit)
  → inline edit mode → lib/api.ts → PUT → update local state
```

### API Client (`lib/api.ts`)
```typescript
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// All methods: getTasks, createTask, updateTask, deleteTask, toggleComplete
// Each returns parsed JSON or throws with error detail
```

### State Management
- No external state library (React useState + useCallback sufficient)
- page.tsx is a client component (needs interactivity for CRUD)
- Tasks stored in `useState<Task[]>` on the main page
- Mutations update local state immediately (optimistic for toggle)

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Server vs Client page | Client component | Page needs useState for task list, onClick handlers, form state |
| State management | useState | Simple enough for single-page CRUD; no need for Redux/Zustand |
| Edit UX | Inline edit on card | Simpler than modal, keeps context |
| user_id | Hardcoded "demo-user" for now | Auth not yet implemented (Cycle 3 replaces this) |
| Styling | Tailwind CSS only | Constitution mandate, no inline styles |

## Risks

1. **No auth yet** — using hardcoded "demo-user" as user_id; replaced in Cycle 3
2. **CORS issues** — backend must allow frontend origin; already configured in Cycle 1
3. **API must be running** — frontend needs backend at localhost:8000; documented in README
