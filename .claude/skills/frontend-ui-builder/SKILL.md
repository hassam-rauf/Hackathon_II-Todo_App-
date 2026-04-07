---
name: frontend-ui-builder
description: |
  Build Next.js 16+ App Router pages, layouts, and components with Tailwind CSS and TypeScript.
  This skill should be used when users ask to create frontend pages, UI components,
  forms, layouts, responsive interfaces, or connect frontend to backend APIs.
---

# Frontend UI Builder

Build production-grade Next.js frontend with Tailwind CSS.

## What This Skill Does
- Scaffold Next.js 16+ App Router projects
- Create pages, layouts, and reusable components
- Build forms with validation and error states
- Set up API client for backend communication
- Implement responsive mobile-first design with Tailwind CSS
- Handle loading states, error states, and empty states

## What This Skill Does NOT Do
- Backend API development (use fastapi-backend-builder)
- Database operations (use database-sqlmodel-builder)
- Authentication logic (use auth-builder)
- Deployment or containerization

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing components, naming conventions, folder structure |
| **Conversation** | Which page/component, what data, what interactions |
| **Skill References** | `references/patterns.md` for component and routing patterns |
| **User Guidelines** | Constitution UI/UX principles |

---

## Required Clarifications

1. **What to build**: "Page, component, layout, or form?"
2. **Data requirements**: "What data does it display or collect?"
3. **Interactivity**: "Server component (default) or client component (needs useState/onClick)?"

---

## Workflow

1. **Determine type**: Page (app/), component (components/), or layout
2. **Check**: Server component first — only use `"use client"` if interactivity needed
3. **Create file** following App Router conventions
4. **Style** with Tailwind CSS — mobile-first breakpoints
5. **Add states**: loading (Suspense/skeleton), error (error.tsx), empty
6. **Connect API** via `lib/api.ts` if data fetching needed
7. **Verify**: accessibility (ARIA), keyboard navigation, responsive

---

## Domain Standards

### Must Follow
- Server components by default — `"use client"` only for interactivity (useState, onClick, forms)
- Tailwind CSS only — no inline styles, no CSS modules
- Mobile-first: base styles for mobile, `sm:` `md:` `lg:` for larger screens
- Semantic HTML: `<main>`, `<section>`, `<nav>`, `<button>` (not div for everything)
- ARIA labels on interactive elements
- Loading state for every async operation
- Error boundary for every page

### Must Avoid
- `useEffect` for data fetching (use server components or React Query)
- Inline styles (`style={{}}`)
- `<div>` for clickable elements (use `<button>`)
- Hardcoded colors (use Tailwind design tokens)
- Giant component files (split at ~100 lines)

---

## Key Patterns

### App Router File Convention
```
app/
├── layout.tsx          ← Root layout (shared UI shell)
├── page.tsx            ← Home page (/)
├── loading.tsx         ← Loading skeleton
├── error.tsx           ← Error boundary
├── signin/page.tsx     ← /signin
├── signup/page.tsx     ← /signup
└── chat/page.tsx       ← /chat (Phase III)
```

### Server Component (default)
```tsx
// No "use client" — runs on server, can be async
export default async function TasksPage() {
  const tasks = await fetchTasks();  // direct fetch
  return <TaskList tasks={tasks} />;
}
```

### Client Component (interactive)
```tsx
"use client";
import { useState } from "react";

export default function TaskForm({ onSubmit }: Props) {
  const [title, setTitle] = useState("");
  // ... interactive logic
}
```

### API Client Pattern
```tsx
// lib/api.ts — single source of truth for all backend calls
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = {
  getTasks: (userId: string, token: string) =>
    fetch(`${API}/api/${userId}/tasks`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(r => r.json()),
  // ... other methods
};
```

### Responsive Pattern
```tsx
// Mobile-first: stack on mobile, row on desktop
<div className="flex flex-col gap-4 md:flex-row md:items-center">
  <h1 className="text-xl md:text-2xl font-bold">Tasks</h1>
  <button className="w-full md:w-auto px-4 py-2 bg-blue-600 text-white rounded">
    Add Task
  </button>
</div>
```

---

## Output Checklist

- [ ] File follows App Router conventions (app/ for pages, components/ for shared)
- [ ] Server component unless interactivity required
- [ ] Tailwind CSS only, mobile-first responsive
- [ ] Loading and error states handled
- [ ] Semantic HTML with ARIA labels
- [ ] API calls through lib/api.ts
- [ ] No console.log or hardcoded data in final output

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/patterns.md` | Component patterns, Tailwind utilities, common layouts |
