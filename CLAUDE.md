# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this Todo App - Phase I repository.

## Project Overview

This repository contains the Todo Application - In-Memory Console App for Hackathon Phase I. The project implements a command-line todo application that stores tasks in memory using Python and Claude Code.

## Architecture Overview

The Todo App Phase I is a simple console application with the following components:

- **Task Class**: Represents a single todo task with ID, title, description, and completion status
- **TodoManager Class**: Manages the collection of tasks in memory with CRUD operations
- **Console Interface**: Menu-driven interface for user interaction

## Technology Stack

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Development**: Claude Code with Spec-Kit Plus
- **Project Structure**: Standard Python package structure

## Development Commands

For Phase I development:

- Use `uv sync` to install dependencies
- Use `uv run src/todo_app/__init__.py` to run the application
- Use `uv run todo-app` to run the installed package

## Key Features

The application implements all 5 required basic level features:

1. **Add Task**: Add a new task with title and description
2. **Delete Task**: Delete a task by its ID
3. **Update Task**: Update task title, description, or completion status
4. **View/List Tasks**: Display all tasks with status indicators
5. **Mark Complete/Incomplete**: Change task completion status

## Development Workflow

1. Write specifications using Spec-Kit Plus
2. Generate implementation plans
3. Implement using Claude Code
4. Follow clean code principles
5. Test all functionality
6. Maintain proper Python project structure

## Project Structure

- `/src` - Contains Python source code in proper package structure
- `/specs/history` - Contains specification files
- `pyproject.toml` - Project configuration and dependencies
- `README.md` - Project documentation
- `CLAUDE.md` - Claude Code instructions (this file)
- `constitution.md` - Project constitution file

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write clean, readable, and maintainable code
- Implement proper error handling
- Follow single responsibility principle
