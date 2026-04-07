# Tasks: Frontend UI

**Feature**: Frontend UI (Phase II, Cycle 2)
**Created**: 2026-03-31
**Spec**: `specs/phase2-web/frontend-ui/spec.md`
**Plan**: `specs/phase2-web/frontend-ui/plan.md`

## Task List

### T-024: Next.js 16 scaffold
- [ ] `npx create-next-app@latest frontend` with TypeScript, Tailwind CSS, App Router
- [ ] Verify: `cd frontend && npm run dev` starts at localhost:3000
- [ ] Add `NEXT_PUBLIC_API_URL=http://localhost:8000` to `.env.local`
- **Acceptance**: Dev server starts, Tailwind works, TypeScript compiles

### T-025: API client (`lib/api.ts`)
- [ ] Create `frontend/lib/api.ts`
- [ ] Base URL from `NEXT_PUBLIC_API_URL` env var
- [ ] Methods: getTasks, createTask, updateTask, deleteTask, toggleComplete
- [ ] Error handling: parse error detail from response
- [ ] TypeScript types: Task, TaskCreate, TaskUpdate
- **Acceptance**: All 5 API methods callable, types exported

### T-026: Task list page
- [ ] `app/page.tsx` as client component with useState for tasks
- [ ] Fetch tasks on mount via api.getTasks()
- [ ] Display TaskList component with fetched tasks
- [ ] Loading state while fetching
- [ ] Error state if fetch fails
- [ ] Empty state if no tasks
- **Acceptance**: Page renders tasks from API; shows loading/error/empty states

### T-027: Create task form (TaskForm component)
- [ ] `components/TaskForm.tsx` — client component
- [ ] Title input (required), description textarea (optional)
- [ ] Client-side validation: title cannot be empty
- [ ] On submit: call api.createTask(), add to task list
- [ ] Clear form after successful creation
- **Acceptance**: Submit creates task, appears in list; empty title shows error

### T-028: Edit task
- [ ] Inline edit mode on TaskCard (toggle between view/edit)
- [ ] Editable title input + description textarea
- [ ] Save button → api.updateTask() → update in list
- [ ] Cancel button → revert to original values
- **Acceptance**: Edit saves changes; cancel reverts; changes visible in list

### T-029: Delete task
- [ ] Delete button on TaskCard
- [ ] Confirmation: window.confirm() or custom dialog
- [ ] On confirm: api.deleteTask() → remove from list
- **Acceptance**: Confirm deletes; cancel keeps task; deleted task gone from list

### T-030: Complete toggle
- [ ] Checkbox on TaskCard
- [ ] On click: api.toggleComplete() → update completed status in list
- [ ] Visual: completed tasks show strikethrough or muted style
- **Acceptance**: Toggle changes status; visual indicator updates

### T-031: Responsive layout + states
- [ ] Mobile-first: single column on mobile, comfortable on desktop
- [ ] Loading skeleton component
- [ ] Error boundary (app/error.tsx)
- [ ] Tailwind responsive: base → sm → md → lg
- [ ] Touch-friendly: min 44px tap targets
- **Acceptance**: Usable on 375px viewport; loading/error states render

### T-032: Layered CLAUDE.md
- [ ] Create `frontend/CLAUDE.md` with frontend-specific instructions
- [ ] Create `backend/CLAUDE.md` with backend-specific instructions
- **Acceptance**: Both files exist with relevant context
