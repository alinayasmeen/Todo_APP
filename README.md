# Todo Application - In-Memory Console App

A command-line todo application that stores tasks in memory, built as part of the Hackathon Phase I.

## Project Overview

This project implements a simple console-based todo application with the following features:
- Add tasks with title and description
- List all tasks with status indicators
- Update task details
- Delete tasks by ID
- Mark tasks as complete/incomplete

## Technology Stack

- Python 3.13+
- UV for package management
- Claude Code for development

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Setup Instructions

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd todo-app
   ```

2. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

3. **Install project dependencies**:
   ```bash
   uv sync
   ```

4. **Run the application**:
   ```bash
   uv run src/todo_app/__init__.py
   ```

   Or if you've installed the package:
   ```bash
   uv run todo-app
   ```

## Usage

Once the application is running, you'll see a menu with the following options:

1. **Add Task**: Create a new todo task with a title and optional description
2. **List Tasks**: View all tasks with their completion status
3. **Update Task**: Modify an existing task's title, description, or completion status
4. **Delete Task**: Remove a task by its ID
5. **Mark Task Complete**: Change a task's status to completed
6. **Mark Task Incomplete**: Change a task's status to incomplete
7. **Exit**: Quit the application

## Project Structure

```
todo-app/
├── src/                    # Source code files
│   └── todo_app/          # Main application package
│       └── __init__.py    # Main application code
├── specs/history/         # Specification history files
│   └── phase1_spec.md     # Phase I specification
├── constitution.md        # Project constitution file
├── pyproject.toml         # Project configuration and dependencies
├── README.md             # This file
└── CLAUDE.md             # Claude Code instructions
```

## Features

### Add Task
- Creates a new task with a unique ID
- Requires a title (description is optional)
- Task is stored in memory

### List Tasks
- Displays all tasks in a formatted table
- Shows ID, status (✓ for complete, ○ for incomplete), title, and description
- Truncates long titles and descriptions for better readability

### Update Task
- Modifies existing task properties
- Supports partial updates (only specified fields are changed)
- Updates the task's modification timestamp

### Delete Task
- Removes a task by its ID
- Validates that the task exists before deletion

### Mark Complete/Incomplete
- Changes the completion status of a task
- Provides separate options for marking complete or incomplete

## Development

This project was developed using Claude Code following the agentic development workflow:
1. Write specification
2. Generate implementation plan
3. Break implementation into tasks
4. Implement via Claude Code
5. Test and validate
6. Document and review

## Phase Requirements Met

✓ All 5 Basic Level features implemented (Add, Delete, Update, View, Mark Complete)
✓ Spec-driven development with Claude Code and Spec-Kit Plus
✓ Clean code principles and proper Python project structure
✓ In-memory storage as required
✓ Console-based user interface

## License

[Specify license if applicable]