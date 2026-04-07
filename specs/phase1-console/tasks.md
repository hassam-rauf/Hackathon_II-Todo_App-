# Tasks: Todo In-Memory Python Console App

**Input**: Design documents from `/specs/phase1-console/`
**Prerequisites**: plan.md (required), spec.md (required)

## Phase 1: Setup

**Purpose**: Project initialization with UV and basic structure

- [x] T-001 [US-ALL] Create UV project: `uv init` in project root, configure `pyproject.toml` with Python 3.13+, create `src/__init__.py`, `tests/phase1/__init__.py`
- [x] T-002 [P] [US-ALL] Add dev dependency: `uv add --dev pytest`

**Checkpoint**: `uv run python --version` works, `uv run pytest` runs (0 tests)

---

## Phase 2: Foundation — Task Model

**Purpose**: Core Task data structure that all operations depend on

- [x] T-003 [US-ALL] Create Task dataclass in `src/models.py`:
  - Fields: id(int), title(str), description(str|None), completed(bool=False), created_at(datetime)
  - `__str__` method: returns `[x] 1. Buy groceries` or `[ ] 1. Buy groceries` format
  - Title validation: 1-200 chars, strip whitespace
  - Description validation: max 1000 chars or None

- [x] T-004 [P] [US-ALL] Create TaskManager class skeleton in `src/task_manager.py`:
  - `_tasks: dict[int, Task]` — empty dict
  - `_next_id: int = 1` — auto-increment counter
  - Method stubs for: add_task, get_task, list_tasks, update_task, delete_task, toggle_complete

**Checkpoint**: `from src.models import Task` and `from src.task_manager import TaskManager` work without error

---

## Phase 3: User Story 1 — Add Task (Priority: P1)

**Goal**: User can create new tasks with title and optional description
**Independent Test**: Run app → select Add → enter title → see confirmation

### Tests for US1

- [x] T-005 [US1] Write tests in `tests/phase1/test_task_manager.py`:
  - `test_add_task_with_title` — title only, verify ID=1, completed=False
  - `test_add_task_with_description` — title + description, both stored
  - `test_add_task_auto_increment_id` — add 3 tasks, IDs are 1,2,3
  - `test_add_task_empty_title_raises` — empty string raises ValueError
  - `test_add_task_whitespace_title_raises` — "   " raises ValueError

### Implementation for US1

- [x] T-006 [US1] Implement `TaskManager.add_task(title: str, description: str | None = None) -> Task` in `src/task_manager.py`:
  - Validate title: strip whitespace, reject empty, enforce max 200 chars
  - Validate description: strip whitespace, enforce max 1000 chars, allow None
  - Create Task with `_next_id`, increment counter
  - Store in `_tasks` dict
  - Return created Task

**Checkpoint**: All T-005 tests pass

---

## Phase 4: User Story 2 — View All Tasks (Priority: P1)

**Goal**: User can see all tasks with ID, title, status indicator, and date
**Independent Test**: Add 2-3 tasks → view → all display correctly

### Tests for US2

- [x] T-007 [US2] Write tests in `tests/phase1/test_task_manager.py`:
  - `test_list_tasks_empty` — returns empty list
  - `test_list_tasks_multiple` — add 3 tasks, returns list of 3
  - `test_list_tasks_shows_completed_status` — add task, complete it, verify completed=True in list

### Implementation for US2

- [x] T-008 [US2] Implement `TaskManager.list_tasks() -> list[Task]` in `src/task_manager.py`:
  - Return `list(self._tasks.values())`
  - Sorted by ID (ascending)

**Checkpoint**: All T-007 tests pass

---

## Phase 5: User Story 3 — Toggle Complete (Priority: P2)

**Goal**: User can mark a task as complete or incomplete
**Independent Test**: Add task → toggle → shows [x] → toggle again → shows [ ]

### Tests for US3

- [x] T-009 [US3] Write tests in `tests/phase1/test_task_manager.py`:
  - `test_toggle_complete_pending_to_done` — add task, toggle, completed=True
  - `test_toggle_complete_done_to_pending` — toggle twice, completed=False
  - `test_toggle_complete_not_found` — toggle ID 99, returns None

### Implementation for US3

- [x] T-010 [US3] Implement `TaskManager.toggle_complete(task_id: int) -> Task | None` in `src/task_manager.py`:
  - Find task by ID, flip `completed`, return updated Task
  - Return None if not found

**Checkpoint**: All T-009 tests pass

---

## Phase 6: User Story 4 — Update Task (Priority: P2)

**Goal**: User can change a task's title and/or description
**Independent Test**: Add task → update title → verify changed in list

### Tests for US4

- [x] T-011 [US4] Write tests in `tests/phase1/test_task_manager.py`:
  - `test_update_task_title` — update title, old title replaced
  - `test_update_task_description` — update description only, title unchanged
  - `test_update_task_both` — update both title and description
  - `test_update_task_not_found` — update ID 99, returns None
  - `test_update_task_empty_title_keeps_current` — empty new title, original title stays

### Implementation for US4

- [x] T-012 [US4] Implement `TaskManager.update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task | None` in `src/task_manager.py`:
  - Find task by ID
  - If title provided and non-empty after strip: update title
  - If description provided: update description
  - Return updated Task or None if not found

**Checkpoint**: All T-011 tests pass

---

## Phase 7: User Story 5 — Delete Task (Priority: P3)

**Goal**: User can remove a task by ID
**Independent Test**: Add task → delete by ID → no longer in list

### Tests for US5

- [x] T-013 [US5] Write tests in `tests/phase1/test_task_manager.py`:
  - `test_delete_task_exists` — add task, delete, list is empty
  - `test_delete_task_not_found` — delete ID 99, returns False
  - `test_delete_task_id_not_reused` — add ID 1, delete, add new → ID is 2, not 1

### Implementation for US5

- [x] T-014 [US5] Implement `TaskManager.delete_task(task_id: int) -> bool` in `src/task_manager.py`:
  - If task_id in `_tasks`: remove and return True
  - Else return False

**Checkpoint**: All T-013 tests pass

---

## Phase 8: CLI Interface

**Purpose**: Interactive menu connecting all operations to user input

- [x] T-015 [US-ALL] Implement CLI menu in `src/main.py`:
  - Display menu with 6 options (Add, View, Update, Delete, Toggle, Exit)
  - `while True` loop until user selects Exit
  - Match/case for menu dispatch

- [x] T-016 [US-ALL] Implement input handlers in `src/main.py`:
  - `handle_add()` — prompt title + description, call TaskManager.add_task, show confirmation
  - `handle_view()` — call list_tasks, display formatted output with status indicators and summary
  - `handle_update()` — prompt ID + new title/description, call update_task, show result
  - `handle_delete()` — prompt ID, call delete_task, show result
  - `handle_toggle()` — prompt ID, call toggle_complete, show result

- [x] T-017 [US-ALL] Implement input validation in `src/main.py`:
  - Non-numeric ID → "Please enter a valid number"
  - Invalid menu choice → "Invalid choice. Please select 1-6."
  - Empty title on add → "Title cannot be empty"
  - Ctrl+C → graceful exit with "Goodbye!" message (try/except KeyboardInterrupt)

**Checkpoint**: App runs with `uv run python src/main.py`, all 5 operations work interactively

---

## Phase 9: Polish & Final Validation

- [x] T-018 [P] [US-ALL] Add Task model tests in `tests/phase1/test_models.py`:
  - `test_task_creation` — default values correct
  - `test_task_str_pending` — "[ ] 1. Buy groceries" format
  - `test_task_str_completed` — "[x] 1. Buy groceries" format

- [x] T-019 [US-ALL] Run full test suite: `uv run pytest tests/phase1/ -v --tb=short`
  - All tests pass
  - Verify minimum 15 test functions

- [x] T-020 [US-ALL] Manual smoke test:
  - Add 3 tasks → View (3 shown) → Complete task 2 → View ([x] on task 2)
  - Update task 1 → View (updated) → Delete task 3 → View (2 remaining) → Exit

---

## Dependencies & Execution Order

```
T-001, T-002 (Setup)
    ↓
T-003, T-004 (Foundation — can run in parallel)
    ↓
T-005 → T-006 (US1: Add Task — tests first, then implement)
    ↓
T-007 → T-008 (US2: View Tasks)
    ↓
T-009 → T-010 (US3: Toggle Complete)
T-011 → T-012 (US4: Update Task)     ← US3 and US4 can run in parallel
T-013 → T-014 (US5: Delete Task)     ← US5 can run after US3/US4
    ↓
T-015 → T-016 → T-017 (CLI — depends on all CRUD methods)
    ↓
T-018 → T-019 → T-020 (Polish — after CLI works)
```

### Parallel Opportunities
- T-001 and T-002: parallel
- T-003 and T-004: parallel
- T-009/T-010 and T-011/T-012: parallel (different methods, same file but different sections)
- T-018: parallel with T-015/T-016/T-017
