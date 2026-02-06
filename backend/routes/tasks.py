from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from ..models import Task, TaskCreate, TaskUpdate, TaskRead, User
from ..auth import get_current_active_user
from ..services.ai import integrate_ai_suggestions, get_productivity_insights
from datetime import datetime

router = APIRouter()


def get_session():
    from ..db import get_engine
    with Session(get_engine()) as session:
        yield session


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task: Task creation data
        current_user: The authenticated user creating the task
        session: Database session

    Returns:
        TaskRead: The created task
    """
    # Create task with authenticated user's ID
    db_task = Task.model_validate(task)
    db_task.user_id = current_user.id
    db_task.created_at = datetime.now()
    db_task.updated_at = datetime.now()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    sort: Optional[str] = Query("created", description="Sort by: created, title"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of results (1-100)"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user with filtering, sorting, and pagination.

    Args:
        status: Filter by status (all, pending, completed)
        sort: Sort by (created, title)
        limit: Limit number of results (1-100)
        offset: Offset for pagination
        current_user: The authenticated user requesting tasks
        session: Database session

    Returns:
        List[TaskRead]: List of user's tasks
    """
    # Query tasks for the authenticated user only
    query = select(Task).where(Task.user_id == current_user.id)

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

    # Apply pagination
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)

    tasks = session.exec(query).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task for the authenticated user.

    Args:
        task_id: ID of the task to retrieve
        current_user: The authenticated user requesting the task
        session: Database session

    Returns:
        TaskRead: The requested task

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Task does not belong to current user"
        )

    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.

    Args:
        task_id: ID of the task to update
        task_update: Task update data
        current_user: The authenticated user updating the task
        session: Database session

    Returns:
        TaskRead: The updated task

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Task does not belong to current user"
        )

    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.now()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/{task_id}/complete")
def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.

    Args:
        task_id: ID of the task to update
        current_user: The authenticated user updating the task
        session: Database session

    Returns:
        TaskRead: The updated task

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Task does not belong to current user"
        )

    # Toggle completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.now()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.

    Args:
        task_id: ID of the task to delete
        current_user: The authenticated user deleting the task
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to user
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: Task does not belong to current user"
        )

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}


@router.get("/ai/suggestions")
async def get_ai_task_suggestions(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get AI-generated task suggestions for the authenticated user.

    Args:
        current_user: The authenticated user requesting suggestions
        session: Database session

    Returns:
        List[AITaskSuggestion]: List of AI-generated task suggestions
    """
    # Get user's existing tasks for context
    user_tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()

    # Prepare context for AI service
    context = {
        "existing_tasks_count": len(user_tasks),
        "completed_tasks_count": sum(1 for task in user_tasks if task.completed),
        "recent_tasks": [task.title for task in user_tasks[-5:]],  # Last 5 tasks
        "user_preferences": {}  # Placeholder for future user preferences
    }

    # Get AI suggestions
    suggestions = await integrate_ai_suggestions(current_user, context)
    return suggestions


@router.get("/ai/insights")
async def get_productivity_insights(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get AI-generated productivity insights for the authenticated user.

    Args:
        current_user: The authenticated user requesting insights
        session: Database session

    Returns:
        List[AIInsight]: List of AI-generated productivity insights
    """
    # Get user's tasks for analysis
    user_tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()

    # Get AI insights
    insights = await get_productivity_insights(current_user, user_tasks)
    return insights