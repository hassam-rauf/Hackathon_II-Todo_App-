# Feature Specification: Frontend UI

**Feature Branch**: `phase2-frontend-ui`
**Created**: 2026-03-31
**Status**: Draft
**Input**: Phase II Cycle 2 — Next.js 16+ App Router frontend with Tailwind CSS connecting to FastAPI backend

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Task List (Priority: P1)

User opens the app and sees all their tasks displayed as cards showing title, completion status, and created date. Empty state shown when no tasks exist.

**Why this priority**: The primary view — everything else builds on this.

**Independent Test**: Load page → task cards render with correct data; empty state shows when no tasks.

**Acceptance Scenarios**:

1. **Given** user has 3 tasks, **When** page loads, **Then** 3 task cards display with title, status indicator, created date
2. **Given** user has no tasks, **When** page loads, **Then** empty state message "No tasks yet" with prompt to add
3. **Given** tasks are loading, **When** page loads, **Then** loading skeleton shown until data arrives
4. **Given** API returns error, **When** page loads, **Then** error message displayed with retry option

---

### User Story 2 - Create a Task (Priority: P1)

User fills in a form with title (required) and optional description, submits, and the new task appears in the list.

**Why this priority**: Cannot use the app without creating tasks.

**Independent Test**: Fill form → submit → new task appears in list.

**Acceptance Scenarios**:

1. **Given** form is open, **When** user types title and submits, **Then** task is created via API and appears in list
2. **Given** form is open, **When** user submits with empty title, **Then** validation error shown (client-side)
3. **Given** form is open, **When** user adds title + description and submits, **Then** both saved correctly

---

### User Story 3 - Toggle Task Completion (Priority: P1)

User clicks a checkbox or button to mark a task as complete/incomplete. The UI updates immediately (optimistic).

**Why this priority**: Core interaction — most frequently used action.

**Independent Test**: Click checkbox → task status toggles visually and persists on reload.

**Acceptance Scenarios**:

1. **Given** task is pending, **When** user clicks toggle, **Then** task shows as completed (visual change immediately)
2. **Given** task is completed, **When** user clicks toggle, **Then** task shows as pending
3. **Given** API call fails after toggle, **When** error occurs, **Then** revert to previous state and show error

---

### User Story 4 - Delete a Task (Priority: P2)

User clicks delete on a task, confirms in a dialog, and the task is removed from the list.

**Why this priority**: Cleanup function, needed but not blocking primary workflow.

**Independent Test**: Click delete → confirm → task disappears from list.

**Acceptance Scenarios**:

1. **Given** task exists, **When** user clicks delete, **Then** confirmation dialog appears
2. **Given** confirmation dialog open, **When** user confirms, **Then** task removed from list via API
3. **Given** confirmation dialog open, **When** user cancels, **Then** task remains unchanged

---

### User Story 5 - Edit a Task (Priority: P2)

User can edit a task's title and description inline or via a modal.

**Why this priority**: Important for corrections but users can delete + recreate.

**Independent Test**: Click edit → modify fields → save → changes visible in list.

**Acceptance Scenarios**:

1. **Given** task card, **When** user clicks edit, **Then** fields become editable (or modal opens)
2. **Given** editing, **When** user saves changes, **Then** task updated via API and changes visible
3. **Given** editing, **When** user cancels, **Then** original values restored

---

### Edge Cases

- What happens when API is unreachable? → Show error state with retry button
- What happens on slow network? → Loading states on all async operations
- What happens on mobile viewport? → Responsive layout, touch-friendly targets

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: App MUST render task list from GET `/api/{user_id}/tasks`
- **FR-002**: App MUST provide form to create tasks via POST endpoint
- **FR-003**: App MUST allow toggling completion via PATCH endpoint
- **FR-004**: App MUST allow deleting tasks via DELETE endpoint with confirmation
- **FR-005**: App MUST allow editing task title/description via PUT endpoint
- **FR-006**: App MUST show loading skeleton during data fetch
- **FR-007**: App MUST show error state when API calls fail
- **FR-008**: App MUST show empty state when no tasks exist
- **FR-009**: App MUST use centralized API client (`lib/api.ts`)
- **FR-010**: App MUST be responsive (mobile-first, Tailwind CSS)

### Key Entities

- **TaskCard**: Display component — title, status checkbox, created date, edit/delete buttons
- **TaskForm**: Input component — title field (required), description field (optional), submit button
- **API Client**: Centralized fetch wrapper with base URL from env

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 CRUD operations work end-to-end (create, read, update, delete, toggle)
- **SC-002**: Loading, error, and empty states render correctly
- **SC-003**: Mobile responsive — usable on 375px viewport
- **SC-004**: No hardcoded API URLs (uses NEXT_PUBLIC_API_URL env var)
- **SC-005**: All interactive elements have ARIA labels
