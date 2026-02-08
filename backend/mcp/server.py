"""
Official MCP (Model Context Protocol) Server for Todo Management

This module implements an official MCP server that exposes task operations as tools
for AI agents to use in managing todos through natural language.
"""

from mcp.server import Server
from mcp.types import Tool, Result as ToolResult
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from sqlmodel import Session
import asyncio
import json


class AddTaskInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: str = Field(None, description="Task description", max_length=1000)


class ListTasksInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    status: str = Field("all", description="Filter by task status: all, pending, completed")


class CompleteTaskInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    task_id: int = Field(..., description="Task ID to complete")


class DeleteTaskInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    task_id: int = Field(..., description="Task ID to delete")


class UpdateTaskInput(BaseModel):
    user_id: str = Field(..., description="User ID")
    task_id: int = Field(..., description="Task ID to update")
    title: str = Field(None, description="New task title", min_length=1, max_length=200)
    description: str = Field(None, description="New task description", max_length=1000)


# Global MCP server instance
mcp_server = Server("todo-manager")


# Need to store the session and services for use in tools
_db_session = None
_task_service = None

def set_db_session_and_service(db_session, task_service):
    """Set the database session and task service for the MCP tools."""
    global _db_session, _task_service
    _db_session = db_session
    _task_service = task_service


@mcp_server.tool(
    "add_task",
    "Create a new task",
    AddTaskInput.model_json_schema()
)
async def add_task_tool(input: Dict[str, Any]) -> Result:
    """MCP tool to create a new task."""
    try:
        from ..services.tasks import create_task
        from ..models import TaskCreate
        
        # Parse input
        parsed_input = AddTaskInput(**input)
        
        # Create task using the existing service
        task_create = TaskCreate(
            title=parsed_input.title,
            description=parsed_input.description
        )
        
        # Use the stored session to create the task
        if _db_session is None:
            raise Exception("Database session not initialized")
        
        task = await create_task(task_create, parsed_input.user_id, _db_session)
        
        result = {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }
        
        return Result(output=json.dumps(result))
    except Exception as e:
        return Result(error=str(e))


@mcp_server.tool(
    "list_tasks",
    "Retrieve tasks with optional filtering",
    ListTasksInput.model_json_schema()
)
async def list_tasks_tool(input: Dict[str, Any]) -> Result:
    """MCP tool to retrieve tasks with optional filtering."""
    try:
        from ..services.tasks import get_tasks
        
        # Parse input
        parsed_input = ListTasksInput(**input)
        
        # Use the stored session to get tasks
        if _db_session is None:
            raise Exception("Database session not initialized")
        
        tasks = await get_tasks(
            user_id=parsed_input.user_id,
            status=parsed_input.status,
            db=_db_session
        )
        
        # Convert tasks to a serializable format
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            })
        
        return Result(output=json.dumps(tasks_data))
    except Exception as e:
        return Result(error=str(e))


@mcp_server.tool(
    "complete_task",
    "Mark a task as complete",
    CompleteTaskInput.model_json_schema()
)
async def complete_task_tool(input: Dict[str, Any]) -> Result:
    """MCP tool to mark a task as complete."""
    try:
        from ..services.tasks import update_task
        
        # Parse input
        parsed_input = CompleteTaskInput(**input)
        
        # Use the stored session to update the task
        if _db_session is None:
            raise Exception("Database session not initialized")
        
        updated_task = await update_task(
            task_id=parsed_input.task_id,
            task_update={"completed": True},
            user_id=parsed_input.user_id,
            db=_db_session
        )
        
        result = {
            "task_id": parsed_input.task_id,
            "status": "completed",
            "title": updated_task.title
        }
        
        return Result(output=json.dumps(result))
    except Exception as e:
        return Result(error=str(e))


@mcp_server.tool(
    "delete_task",
    "Remove a task",
    DeleteTaskInput.model_json_schema()
)
async def delete_task_tool(input: Dict[str, Any]) -> Result:
    """MCP tool to remove a task."""
    try:
        from ..services.tasks import delete_task
        
        # Parse input
        parsed_input = DeleteTaskInput(**input)
        
        # Use the stored session to delete the task
        if _db_session is None:
            raise Exception("Database session not initialized")
        
        success = await delete_task(parsed_input.task_id, parsed_input.user_id, _db_session)
        
        if not success:
            raise Exception(f"Failed to delete task {parsed_input.task_id}")
        
        result = {
            "task_id": parsed_input.task_id,
            "status": "deleted",
            "title": "Deleted task"  # In a real implementation, we'd get the title before deletion
        }
        
        return Result(output=json.dumps(result))
    except Exception as e:
        return Result(error=str(e))


@mcp_server.tool(
    "update_task",
    "Update a task's title or description",
    UpdateTaskInput.model_json_schema()
)
async def update_task_tool(input: Dict[str, Any]) -> Result:
    """MCP tool to update a task's title or description."""
    try:
        from ..services.tasks import update_task
        
        # Parse input
        parsed_input = UpdateTaskInput(**input)
        
        # Prepare update data
        update_data = {}
        if parsed_input.title is not None:
            update_data["title"] = parsed_input.title
        if parsed_input.description is not None:
            update_data["description"] = parsed_input.description
        
        # Use the stored session to update the task
        if _db_session is None:
            raise Exception("Database session not initialized")
        
        updated_task = await update_task(
            task_id=parsed_input.task_id,
            task_update=update_data,
            user_id=parsed_input.user_id,
            db=_db_session
        )
        
        result = {
            "task_id": parsed_input.task_id,
            "status": "updated",
            "title": updated_task.title
        }
        
        return Result(output=json.dumps(result))
    except Exception as e:
        return Result(error=str(e))


def get_mcp_server():
    """Get the global MCP server instance."""
    return mcp_server