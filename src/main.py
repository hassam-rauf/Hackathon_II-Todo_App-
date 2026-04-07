# Task: T-015, T-016, T-017 | Spec: specs/phase1-console/spec.md §FR-009, FR-010
"""Todo App — Phase I: Interactive CLI interface."""

from src.task_manager import TaskManager

MENU = """
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
"""


def get_task_id(prompt: str = "Enter task ID: ") -> int | None:
    """Prompt for a task ID. Returns None if input is invalid."""
    raw = input(prompt).strip()
    if not raw:
        print("Please enter a task ID.")
        return None
    try:
        task_id = int(raw)
    except ValueError:
        print("Please enter a valid number.")
        return None
    if task_id <= 0:
        print("Please enter a valid task ID.")
        return None
    return task_id


def handle_add(manager: TaskManager) -> None:
    """Prompt user to add a new task."""
    title = input("Enter task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    description = input("Enter description (or press Enter to skip): ").strip()
    description = description if description else None

    try:
        task = manager.add_task(title, description)
        print(f"Task {task.id} created: {task.title}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_view(manager: TaskManager) -> None:
    """Display all tasks with status indicators."""
    tasks = manager.list_tasks()
    if not tasks:
        print("No tasks found. Add a task to get started!")
        return

    print()
    for task in tasks:
        desc = f" - {task.description}" if task.description else ""
        print(f"  {task}{desc}")

    completed = sum(1 for t in tasks if t.completed)
    pending = len(tasks) - completed
    print(f"\nTotal: {len(tasks)} tasks ({completed} completed, {pending} pending)")


def handle_update(manager: TaskManager) -> None:
    """Prompt user to update a task."""
    task_id = get_task_id()
    if task_id is None:
        return

    print("Leave blank to keep current value.")
    new_title = input("New title: ").strip()
    new_desc = input("New description: ").strip()

    try:
        result = manager.update_task(
            task_id,
            title=new_title if new_title else None,
            description=new_desc if new_desc else None,
        )
        if result is None:
            print(f"Task with ID {task_id} not found.")
        else:
            print(f"Task {task_id} updated: {result.title}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete(manager: TaskManager) -> None:
    """Prompt user to delete a task."""
    task_id = get_task_id()
    if task_id is None:
        return

    if manager.delete_task(task_id):
        print(f"Task {task_id} deleted.")
    else:
        print(f"Task with ID {task_id} not found.")


def handle_toggle(manager: TaskManager) -> None:
    """Prompt user to toggle a task's completion status."""
    task_id = get_task_id()
    if task_id is None:
        return

    result = manager.toggle_complete(task_id)
    if result is None:
        print(f"Task with ID {task_id} not found.")
    elif result.completed:
        print(f"Task {task_id} marked as complete.")
    else:
        print(f"Task {task_id} marked as incomplete.")


def main() -> None:
    """Run the interactive todo app."""
    manager = TaskManager()
    print("Welcome to Todo App! Type a number to get started.")

    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()

        match choice:
            case "1":
                handle_add(manager)
            case "2":
                handle_view(manager)
            case "3":
                handle_update(manager)
            case "4":
                handle_delete(manager)
            case "5":
                handle_toggle(manager)
            case "6":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
