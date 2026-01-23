from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from backend.models import Task, TaskCreate, TaskUpdate, TaskRead
from backend.db import engine
from datetime import datetime

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    # In a real app, user_id would come from authentication
    # For now, using a placeholder
    db_task = Task.model_validate(task)
    db_task.user_id = "placeholder_user_id"  # This would come from auth
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
    session: Session = Depends(get_session)
):
    query = select(Task)

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


@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.now()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}