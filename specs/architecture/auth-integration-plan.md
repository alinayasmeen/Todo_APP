# Authentication Integration Plan

## Overview

This document outlines the implementation plan for integrating Better Auth with JWT tokens into the Todo App, enabling secure multi-user functionality.

## Goals

1. Implement user authentication (signup/login)
2. Secure all API endpoints with JWT tokens
3. Ensure proper user data isolation
4. Maintain compatibility with existing task CRUD operations

## Implementation Steps

### Phase 1: Backend Authentication Setup

#### 1.1 Update Requirements

- Verify Better Auth is properly configured in backend requirements
- Add JWT libraries if needed (though Better Auth handles this)

#### 1.2 Create User Model Integration

Although Better Auth manages users, we need to ensure our task model properly references the user system:

```python
# Updated models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # Will be populated from JWT token
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
```

#### 1.3 Implement JWT Authentication Middleware

```python
# backend/auth.py
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime
import os
from typing import Optional

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify JWT token and return user ID
    """
    token = credentials.credentials

    # Get the secret from environment variables
    secret = os.getenv("BETTER_AUTH_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server configuration error: missing auth secret")

    try:
        # Decode the JWT token - Better Auth JWT structure
        payload = jwt.decode(token, secret, algorithms=["HS256"])

        # Extract user ID from the payload
        user_id = payload.get("userId") or payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

#### 1.4 Update Task Routes with Authentication

```python
# Updated routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from ..models import Task, TaskCreate, TaskUpdate, TaskRead
from ..db import engine
from ..auth import verify_jwt_token
from datetime import datetime

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user_id: str = Security(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """Create a task for the authenticated user"""
    db_task = Task.model_validate(task)
    db_task.user_id = current_user_id  # Use authenticated user ID
    db_task.created_at = datetime.now()
    db_task.updated_at = datetime.now()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    current_user_id: str = Security(verify_jwt_token),
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    sort: Optional[str] = Query("created", description="Sort by: created, title"),
    session: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user"""
    query = select(Task).where(Task.user_id == current_user_id)

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
def read_task(
    task_id: int,
    current_user_id: str = Security(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """Get a specific task for the authenticated user"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if task.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Security(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """Update a task for the authenticated user"""
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if db_task.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.now()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user_id: str = Security(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """Delete a task for the authenticated user"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the current user
    if task.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
```

### Phase 2: Frontend Authentication Setup

#### 2.1 Install Better Auth Client

```bash
cd frontend
npm install better-auth better-auth/client
```

#### 2.2 Configure Better Auth Client

```typescript
// frontend/lib/auth.ts
import { createAuthClient } from "better-auth/react";
import { jwtPlugin } from "better-auth/client/plugins";

export const auth = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:4000",
  plugins: [
    jwtPlugin({
      secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET || "",
    }),
  ],
});
```

#### 2.3 Create API Client with Authentication

```typescript
// frontend/lib/api.ts
import { auth } from './auth';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskCreateData {
  title: string;
  description?: string;
}

interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
}

class TodoApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-app-lpxv.onrender.com/api';

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    // Get JWT token from Better Auth
    const token = await auth.getJWT();

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Redirect to login if unauthorized
        window.location.href = '/login';
        return Promise.reject(new Error('Unauthorized'));
      }
      const errorText = await response.text();
      throw new Error(errorText || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getTasks(): Promise<Task[]> {
    return this.request<Task[]>('/users/me/tasks');
  }

  async createTask(taskData: TaskCreateData): Promise<Task> {
    return this.request<Task>('/users/me/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: number, taskData: TaskUpdateData): Promise<Task> {
    return this.request<Task>(`/users/me/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: number): Promise<void> {
    await this.request(`/users/me/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: number): Promise<Task> {
    return this.request<Task>(`/users/me/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }
}

export const todoApi = new TodoApiClient();
```

### Phase 3: Environment Configuration

#### 3.1 Backend Environment Variables

```bash
# backend/.env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_URL=http://localhost:4000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
BETTER_AUTH_TRUST_HOST=true
```

#### 3.2 Frontend Environment Variables

```bash
# frontend/.env.local
NEXT_PUBLIC_API_BASE_URL=https://todo-app-lpxv.onrender.com/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:4000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
```

### Phase 4: Better Auth Server Setup

#### 4.1 Create Better Auth Configuration

```typescript
// backend/auth_server.ts
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-super-secret-jwt-key-here-make-it-long-and-random",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:4000",
  trustHost: true,
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET || "your-super-secret-jwt-key-here-make-it-long-and-random",
    }),
  ],
  socialProviders: {
    // Add social providers as needed
  },
});
```

#### 4.2 Update Main Application to Include Auth

```typescript
// backend/main.ts (or update existing main.py if using different approach)
import { auth } from "./auth_server";
import { Hono } from "hono";

const app = new Hono();

// Mount Better Auth routes
app.route("/auth", auth.hono);

export default app;
```

### Phase 5: Testing Strategy

#### 5.1 Unit Tests for Authentication

- Test JWT token verification
- Test user data isolation
- Test error handling for invalid tokens

#### 5.2 Integration Tests

- Test complete authentication flow
- Test API endpoints with valid/invalid tokens
- Test data isolation between users

This plan provides a comprehensive approach to implementing secure authentication in the Todo App while maintaining the existing functionality and ensuring proper user data isolation.
