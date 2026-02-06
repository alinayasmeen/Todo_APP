from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from ..models import Task, TaskRead, User
from ..auth import get_current_active_admin_user, get_current_active_user
from datetime import datetime

router = APIRouter()


def get_session():
    from ..db import get_engine
    with Session(get_engine()) as session:
        yield session


@router.get("/", response_model=List[TaskRead])
def get_all_tasks(
    limit: Optional[int] = Query(50, ge=1, le=1000, description="Number of tasks to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of tasks to skip"),
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    user_id: Optional[str] = Query(None, description="Filter by specific user ID"),
    current_user: User = Depends(get_current_active_admin_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks in the system (admin only).

    Args:
        limit: Maximum number of tasks to return (default: 50, max: 1000)
        offset: Number of tasks to skip
        status: Filter by status (all, pending, completed)
        user_id: Filter by specific user ID
        current_user: The authenticated admin user requesting tasks
        session: Database session

    Returns:
        List[TaskRead]: List of all tasks in the system
    """
    query = select(Task)

    # Apply filters
    if user_id:
        query = query.where(Task.user_id == user_id)

    if status and status != "all":
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

    # Apply pagination
    query = query.offset(offset).limit(limit).order_by(Task.created_at.desc())

    tasks = session.exec(query).all()
    return tasks


@router.get("/users/{target_user_id}/tasks", response_model=List[TaskRead])
def get_user_tasks(
    target_user_id: str,
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    sort: Optional[str] = Query("created", description="Sort by: created, title"),
    current_user: User = Depends(get_current_active_admin_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for a specific user (admin only).

    Args:
        target_user_id: ID of the user whose tasks to retrieve
        status: Filter by status (all, pending, completed)
        sort: Sort by (created, title)
        current_user: The authenticated admin user requesting tasks
        session: Database session

    Returns:
        List[TaskRead]: List of user's tasks

    Raises:
        HTTPException: If user doesn't exist
    """
    # Verify that the target user exists
    target_user = session.get(User, target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Query tasks for the specified user
    query = select(Task).where(Task.user_id == target_user_id)

    # Apply status filter
    if status and status != "all":
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

    # Apply sorting
    if sort == "title":
        query = query.order_by(Task.title)
    else:  # Default to created date
        query = query.order_by(Task.created_at.desc())

    tasks = session.exec(query).all()
    return tasks


@router.patch("/users/{target_user_id}/role")
def update_user_role(
    target_user_id: str,
    role: str = Query(..., description="New role for the user (user or admin)"),
    current_user: User = Depends(get_current_active_admin_user),
    session: Session = Depends(get_session)
):
    """
    Update a user's role (admin only).

    Args:
        target_user_id: ID of the user whose role to update
        role: New role for the user (must be 'user' or 'admin')
        current_user: The authenticated admin user updating the role
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If user doesn't exist or role is invalid
    """
    if role not in ["user", "admin"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Role must be 'user' or 'admin'"
        )

    # Get the target user
    target_user = session.get(User, target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's role
    target_user.role = role
    target_user.updated_at = datetime.now()

    session.add(target_user)
    session.commit()

    return {"message": f"User role updated to {role}"}


@router.get("/users/{target_user_id}", response_model=dict)
def get_user_info(
    target_user_id: str,
    current_user: User = Depends(get_current_active_admin_user),
    session: Session = Depends(get_session)
):
    """
    Get information about a specific user (admin only).

    Args:
        target_user_id: ID of the user to get information about
        current_user: The authenticated admin user requesting user info
        session: Database session

    Returns:
        dict: User information

    Raises:
        HTTPException: If user doesn't exist
    """
    target_user = session.get(User, target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": target_user.id,
        "email": target_user.email,
        "name": target_user.name,
        "role": target_user.role,
        "created_at": target_user.created_at,
        "updated_at": target_user.updated_at
    }


@router.get("/stats")
def get_system_stats(
    current_user: User = Depends(get_current_active_admin_user),
    session: Session = Depends(get_session)
):
    """
    Get system statistics (admin only).

    Args:
        current_user: The authenticated admin user requesting stats
        session: Database session

    Returns:
        dict: System statistics
    """
    # Count total users
    users_count = session.exec(select(User)).all()
    total_users = len(users_count)

    # Count total tasks
    tasks_count = session.exec(select(Task)).all()
    total_tasks = len(tasks_count)

    # Count completed tasks
    completed_tasks = session.exec(select(Task).where(Task.completed == True)).all()
    total_completed_tasks = len(completed_tasks)

    # Count pending tasks
    total_pending_tasks = total_tasks - total_completed_tasks

    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "completed_tasks": total_completed_tasks,
        "pending_tasks": total_pending_tasks,
        "admin_user_id": current_user.id
    }