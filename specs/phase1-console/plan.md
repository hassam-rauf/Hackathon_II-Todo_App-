# Implementation Plan: Todo In-Memory Python Console App

**Branch**: `phase1-console-app` | **Date**: 2026-03-29 | **Spec**: `specs/phase1-console/spec.md`
**Input**: Feature specification from `/specs/phase1-console/spec.md`

## Summary

Build a Python CLI todo application with 5 CRUD operations (add, view, update, delete, toggle complete). Tasks stored in-memory using a Python dict keyed by auto-incremented integer ID. Interactive menu loop for user interaction. UV as package manager. pytest for testing.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only — dataclasses, datetime)
**Storage**: In-memory Python dict (no external database)
**Testing**: pytest
**Target Platform**: Linux CLI (WSL2 compatible)
**Project Type**: Single Python project
**Performance Goals**: Instant CLI response (no I/O bottleneck — all in-memory)
**Constraints**: Data lost on exit (in-memory only, by design for Phase I)
**Scale/Scope**: Single user, local console, <1000 tasks expected

## Constitution Check

| Principle | Status | Notes |
|-----------|:------:|-------|
| Spec-Driven Development | PASS | Spec written, plan in progress |
| Tech Stack | PASS | Python 3.13+ with UV |
| Code Quality | PASS | Type hints, single responsibility, <50 line functions |
| Testing | PASS | pytest, 80%+ coverage target |
| Security | N/A | No secrets, no network, no auth (Phase I) |
| Architecture | PASS | Simple single-project structure |

## Component Design

### Component 1: Task Model (`src/models.py`)

**Responsibility**: Define the Task data structure.

```
@dataclass
class Task:
    id: int
    title: str                    # Required, 1-200 chars
    description: str | None       # Optional, max 1000 chars
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}. {self.title}"
```

### Component 2: Task Manager (`src/task_manager.py`)

**Responsibility**: All CRUD operations on the in-memory task collection.

```
class TaskManager:
    _tasks: dict[int, Task]       # Storage: dict keyed by task ID
    _next_id: int                 # Auto-increment counter, starts at 1

    + add_task(title, description?) -> Task
    + get_task(task_id) -> Task | None
    + list_tasks() -> list[Task]
    + update_task(task_id, title?, description?) -> Task | None
    + delete_task(task_id) -> bool
    + toggle_complete(task_id) -> Task | None
```

**Design Decisions:**
- Dict over list: O(1) lookup by ID vs O(n) search
- Auto-increment ID: simple, predictable, never reuses deleted IDs
- Returns Task object or None for not-found cases (caller decides error message)

### Component 3: CLI Interface (`src/main.py`)

**Responsibility**: Interactive menu, user input handling, display formatting.

```
Menu:
  1. Add Task
  2. View All Tasks
  3. Update Task
  4. Delete Task
  5. Toggle Complete
  6. Exit

Flow:
  while True:
    show_menu()
    choice = get_input()
    match choice:
      case "1": handle_add()
      case "2": handle_view()
      case "3": handle_update()
      case "4": handle_delete()
      case "5": handle_toggle()
      case "6": exit gracefully
      case _: show error
```

**Input Validation:**
- Title: strip whitespace, reject empty, enforce max 200 chars
- Description: strip whitespace, allow empty (None), enforce max 1000 chars
- Task ID: must be positive integer, must exist in TaskManager
- Menu choice: must be 1-6

**Display Formatting:**
```
=== Todo App ===
[ ] 1. Buy groceries (2026-03-29)
[x] 2. Call mom (2026-03-29)
[ ] 3. Write report (2026-03-29)
---
Total: 3 tasks (1 completed, 2 pending)
```

## Data Flow

```
User Input → main.py (validate + parse) → TaskManager (execute) → Task (data)
                                               ↓
User Screen ← main.py (format + display) ← result/error
```

## Project Structure

```text
Todo_App/
├── src/
│   ├── __init__.py          # Package marker
│   ├── main.py              # CLI entry point + menu + input handling
│   ├── models.py            # Task dataclass
│   └── task_manager.py      # TaskManager class with CRUD methods
├── tests/
│   └── phase1/
│       ├── __init__.py
│       ├── test_models.py       # Task model tests
│       └── test_task_manager.py # TaskManager CRUD tests
├── pyproject.toml           # UV project config
└── specs/phase1-console/
    ├── spec.md              # This feature's spec
    ├── plan.md              # This file
    └── tasks.md             # Task breakdown (next step)
```

**Structure Decision**: Single project layout chosen. Phase I is a standalone CLI app — no frontend/backend split needed. The src/ directory will be upgraded to backend/ in Phase II.

## Complexity Tracking

No constitution violations. All components are minimal and justified.
