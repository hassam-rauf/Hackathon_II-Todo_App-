# Feature Specification: Todo In-Memory Python Console App

**Feature Branch**: `phase1-console-app`
**Created**: 2026-03-29
**Status**: Draft
**Input**: User description: "Build a command-line todo application that stores tasks in memory using Python, UV, Claude Code, and Spec-Kit Plus. Implement all 5 Basic Level features."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a New Task (Priority: P1)

As a user, I want to add a new task with a title and optional description so that I can track things I need to do.

**Why this priority**: Core functionality — without adding tasks, the app has no purpose.

**Independent Test**: Can be fully tested by running the app, selecting "Add Task", entering a title and description, and verifying the task appears in the list.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** user selects "Add Task" and enters title "Buy groceries", **Then** a new task is created with auto-incremented ID, title "Buy groceries", completed=False, and a created_at timestamp. A confirmation message is shown.
2. **Given** the app is running, **When** user selects "Add Task" and enters title "Call mom" with description "Ask about weekend plans", **Then** the task is created with both title and description stored.
3. **Given** the app is running, **When** user selects "Add Task" and enters an empty title, **Then** an error message "Title cannot be empty" is shown and no task is created.

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to view all my tasks with their status so that I can see what needs to be done.

**Why this priority**: Without viewing tasks, user cannot interact with the app meaningfully.

**Independent Test**: Add 2-3 tasks, select "View Tasks", verify all tasks display with ID, title, and completion status.

**Acceptance Scenarios**:

1. **Given** 3 tasks exist (2 pending, 1 completed), **When** user selects "View Tasks", **Then** all 3 tasks are displayed with format: `[x]` for completed, `[ ]` for pending, along with ID and title.
2. **Given** no tasks exist, **When** user selects "View Tasks", **Then** a message "No tasks found. Add a task to get started!" is displayed.

---

### User Story 3 - Mark Task as Complete/Incomplete (Priority: P2)

As a user, I want to toggle a task's completion status so that I can track my progress.

**Why this priority**: Essential for a todo app — marking tasks done is the core value proposition.

**Independent Test**: Add a task, toggle it to complete, verify status changes. Toggle again, verify it reverts to incomplete.

**Acceptance Scenarios**:

1. **Given** a pending task with ID 1 exists, **When** user selects "Toggle Complete" and enters ID 1, **Then** the task's completed status changes to True and a confirmation "Task 1 marked as complete" is shown.
2. **Given** a completed task with ID 1 exists, **When** user selects "Toggle Complete" and enters ID 1, **Then** the task's completed status changes to False and a confirmation "Task 1 marked as incomplete" is shown.
3. **Given** no task with ID 99 exists, **When** user selects "Toggle Complete" and enters ID 99, **Then** an error "Task with ID 99 not found" is shown.

---

### User Story 4 - Update a Task (Priority: P2)

As a user, I want to update a task's title or description so that I can correct or refine my tasks.

**Why this priority**: Important for usability — users need to fix typos or update task details.

**Independent Test**: Add a task, update its title, verify the change persists in the task list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 (title: "Buy groceries") exists, **When** user selects "Update Task", enters ID 1, and provides new title "Buy groceries and fruits", **Then** the task title is updated and confirmation "Task 1 updated" is shown.
2. **Given** a task with ID 1 exists, **When** user selects "Update Task", enters ID 1, and provides only a new description (leaving title blank to keep current), **Then** only the description is updated; the title remains unchanged.
3. **Given** no task with ID 99 exists, **When** user selects "Update Task" and enters ID 99, **Then** an error "Task with ID 99 not found" is shown.
4. **Given** a task with ID 1 exists, **When** user provides an empty title during update, **Then** the title is NOT changed (kept as is) and the user is informed.

---

### User Story 5 - Delete a Task (Priority: P3)

As a user, I want to delete a task so that I can remove tasks I no longer need.

**Why this priority**: Useful but less critical than adding, viewing, and completing tasks.

**Independent Test**: Add a task, delete it by ID, verify it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** user selects "Delete Task" and enters ID 1, **Then** the task is removed and confirmation "Task 1 deleted" is shown. The task no longer appears in the list.
2. **Given** no task with ID 99 exists, **When** user selects "Delete Task" and enters ID 99, **Then** an error "Task with ID 99 not found" is shown.

---

### Edge Cases

- What happens when user enters a non-numeric ID? → Show "Please enter a valid number" error.
- What happens when user enters a negative ID? → Show "Please enter a valid task ID" error.
- What happens when user selects an invalid menu option? → Show "Invalid choice. Please select 1-6." message.
- What happens when user presses Ctrl+C? → Graceful exit with "Goodbye!" message.
- What happens when there are 100+ tasks? → All tasks display correctly (no pagination needed for Phase I).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a task with a required title (1-200 chars) and optional description (max 1000 chars).
- **FR-002**: System MUST auto-generate a unique integer ID for each task (auto-increment starting from 1).
- **FR-003**: System MUST display all tasks with their ID, title, completion status indicator (`[x]`/`[ ]`), and created date.
- **FR-004**: System MUST allow users to update a task's title and/or description by ID.
- **FR-005**: System MUST allow users to delete a task by ID.
- **FR-006**: System MUST allow users to toggle a task's completion status by ID.
- **FR-007**: System MUST validate all user input and display clear error messages for invalid input.
- **FR-008**: System MUST store all tasks in memory (Python dict keyed by task ID).
- **FR-009**: System MUST provide an interactive CLI menu with numbered options that loops until user exits.
- **FR-010**: System MUST handle graceful exit (menu option or Ctrl+C).

### Non-Functional Requirements

- **NFR-001**: Application MUST run with `uv run python src/main.py`.
- **NFR-002**: Application MUST use Python 3.13+ features where appropriate.
- **NFR-003**: All functions MUST have type hints.
- **NFR-004**: Application MUST have pytest tests with minimum 80% coverage.
- **NFR-005**: Application MUST follow the project constitution principles.

### Key Entities

- **Task**: Represents a todo item. Attributes: id (int, auto-increment), title (str, required), description (str | None), completed (bool, default False), created_at (datetime).
- **TaskManager**: Manages the in-memory collection of tasks. Provides methods for add, delete, update, list, and toggle_complete operations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can add, view, update, delete, and complete tasks via CLI without errors.
- **SC-002**: All invalid inputs (empty title, wrong ID, non-numeric input) produce clear error messages without crashing.
- **SC-003**: `uv run pytest` passes all tests with 80%+ coverage.
- **SC-004**: Application starts and runs with `uv run python src/main.py` without errors.
- **SC-005**: Code follows constitution: type hints, clean structure, no hardcoded values.
