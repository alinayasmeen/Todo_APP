#!/usr/bin/env python3
"""
Todo Application - In-Memory Console App
A command-line todo application that stores tasks in memory.
"""

import json
from datetime import datetime
from typing import List, Optional, Dict, Any


class Task:
    """Represents a single todo task."""

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, title: Optional[str] = None, description: Optional[str] = None,
               completed: Optional[bool] = None):
        """Update task properties."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self.updated_at = datetime.now()


class TodoManager:
    """Manages the collection of tasks in memory."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the list."""
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[i]
                return True
        return False

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """Update a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.update(title, description, completed)
                return True
        return False

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        return self.tasks

    def mark_complete(self, task_id: int, completed: bool = True) -> bool:
        """Mark a task as complete or incomplete."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.update(completed=completed)
                return True
        return False


def print_menu():
    """Print the application menu."""
    print("\n" + "="*50)
    print("TODO APPLICATION - IN-MEMORY CONSOLE APP")
    print("="*50)
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Incomplete")
    print("7. Exit")
    print("-"*50)


def print_tasks(tasks: List[Task]):
    """Print all tasks in a formatted way."""
    if not tasks:
        print("\nNo tasks found!")
        return

    print("\n" + "-"*80)
    print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description':<30}")
    print("-"*80)

    for task in tasks:
        status = "✓" if task.completed else "○"
        title = task.title[:28] + ".." if len(task.title) > 28 else task.title
        description = task.description[:28] + ".." if len(task.description) > 28 else task.description
        print(f"{task.task_id:<4} {status:<8} {title:<30} {description:<30}")
    print("-"*80)


def main():
    """Main application loop."""
    todo_manager = TodoManager()

    print("Welcome to the Todo Application!")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            # Add Task
            title = input("Enter task title: ").strip()
            if not title:
                print("Title cannot be empty!")
                continue
            description = input("Enter task description (optional): ").strip()
            task = todo_manager.add_task(title, description)
            print(f"Task added successfully! ID: {task.task_id}")

        elif choice == '2':
            # List Tasks
            tasks = todo_manager.list_tasks()
            print_tasks(tasks)

        elif choice == '3':
            # Update Task
            try:
                task_id = int(input("Enter task ID to update: "))
                task = todo_manager.get_task(task_id)
                if not task:
                    print("Task not found!")
                    continue

                print(f"Current task: {task.title}")
                new_title = input(f"Enter new title (current: '{task.title}'): ").strip()
                new_title = new_title if new_title else None

                print(f"Current description: {task.description}")
                new_description = input(f"Enter new description (current: '{task.description}'): ").strip()
                new_description = new_description if new_description else None

                if todo_manager.update_task(task_id, new_title, new_description):
                    print("Task updated successfully!")
                else:
                    print("Failed to update task!")

            except ValueError:
                print("Invalid task ID!")

        elif choice == '4':
            # Delete Task
            try:
                task_id = int(input("Enter task ID to delete: "))
                if todo_manager.delete_task(task_id):
                    print("Task deleted successfully!")
                else:
                    print("Task not found!")
            except ValueError:
                print("Invalid task ID!")

        elif choice == '5':
            # Mark Task Complete
            try:
                task_id = int(input("Enter task ID to mark complete: "))
                if todo_manager.mark_complete(task_id, True):
                    print("Task marked as complete!")
                else:
                    print("Task not found!")
            except ValueError:
                print("Invalid task ID!")

        elif choice == '6':
            # Mark Task Incomplete
            try:
                task_id = int(input("Enter task ID to mark incomplete: "))
                if todo_manager.mark_complete(task_id, False):
                    print("Task marked as incomplete!")
                else:
                    print("Task not found!")
            except ValueError:
                print("Invalid task ID!")

        elif choice == '7':
            # Exit
            print("Thank you for using the Todo Application!")
            break

        else:
            print("Invalid choice! Please enter a number between 1-7.")


if __name__ == "__main__":
    main()