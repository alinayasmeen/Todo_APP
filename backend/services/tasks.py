"""
Services for managing tasks, used by the MCP server.
"""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from ..models import Task, TaskCreate, TaskUpdate, User


async def create_task(task_create: TaskCreate, user_id: str, db: Session) -> Task:
    """Create a new task for a user."""
    task = Task(
        **task_create.model_dump(),
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


async def get_task(task_id: int, user_id: str, db: Session) -> Optional[Task]:
    """Get a specific task for a user."""
    task = db.exec(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    ).first()
    return task


async def get_tasks(user_id: str, status: Optional[str] = None, db: Session) -> List[Task]:
    """Get all tasks for a user with optional status filter."""
    query = select(Task).where(Task.user_id == user_id)
    
    if status:
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)
    
    tasks = db.exec(query.order_by(Task.created_at.desc())).all()
    return tasks


async def update_task(task_id: int, task_update: dict, user_id: str, db: Session) -> Task:
    """Update a specific task for a user."""
    task = await get_task(task_id, user_id, db)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found for user {user_id}")
    
    # Update task fields
    for key, value in task_update.items():
        setattr(task, key, value)
    
    task.updated_at = datetime.now()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


async def delete_task(task_id: int, user_id: str, db: Session) -> bool:
    """Delete a specific task for a user."""
    task = await get_task(task_id, user_id, db)
    if not task:
        return False
    
    db.delete(task)
    db.commit()
    return True