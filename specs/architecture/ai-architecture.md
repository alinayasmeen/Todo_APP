# AI Architecture for Todo App

## Overview

This document outlines the AI architecture for transforming the console-based Todo app into a modern multi-user web application with persistent storage, authentication, and potential AI capabilities.

## Current State Analysis

### Existing Components

- **Backend**: FastAPI server with task CRUD operations
- **Database**: PostgreSQL (Neon) with SQLModel ORM
- **Frontend**: Planned Next.js 14 application (currently empty)
- **Authentication**: Better Auth integration planned

### Architecture Requirements

- Multi-user support with proper data isolation
- JWT-based authentication between frontend and backend
- Persistent storage using Neon Serverless PostgreSQL
- Responsive web interface using Next.js

## Proposed AI Architecture

### 1. System Architecture

```

┌─────────────────┐    ┌──────────────────────────────────────────────┐    ┌─────────────────┐
│                 │    │                                              │    │                 │
│   Browser       │    │              FastAPI Server                  │    │   Neon          │
│   (Next.js)     │◄──►│  ┌────────────────────────────────────────┐  │    │   PostgreSQL    │
│                 │    │  │           Authentication             │  │    │                 │
│                 │    │  │  ┌──────────────────────────────────┐  │  │    │                 │
│  Better Auth    │    │  │  │    JWT Middleware & User         │  │  │    │                 │
│  (Sessions)     │    │  │  │    Verification                │  │  │    │                 │
│                 │    │  │  └───────────────┬──────────────────┘  │  │    │                 │
│                 │    │  │                  │                   │  │    │                 │
│                 │    │  │                  ▼                   │  │    │                 │
│                 │    │  │  ┌──────────────────────────────────┐  │  │    │                 │
│                 │    │  │  │        API Endpoints           │  │  │    │                 │
│                 │    │  │  │ GET /api/tasks                 │  │  │    │                 │
│                 │    │  │  │ POST /api/tasks                │  │  │    │                 │
│                 │    │  │  │ PUT /api/tasks/{id}            │  │  │    │                 │
│                 │    │  │  │ PATCH /api/tasks/{id}/complete │  │  │    │                 │
│                 │    │  │  │ DELETE /api/tasks/{id}         │  │  │    │                 │
│                 │    │  │  └───────────────┬──────────────────┘  │  │    │                 │
│                 │    │  │                  │                   │  │    │                 │
│                 │    │  │                  ▼                   │  │    │                 │
│                 │    │  │  ┌──────────────────────────────────┐  │  │    │                 │
│                 │    │  │  │         Business Logic         │  │  │    │                 │
│                 │    │  │  │    (Task CRUD Operations)      │  │  │    │                 │
│                 │    │  │  └───────────────┬──────────────────┘  │  │    │                 │
│                 │    │  │                  │                   │  │    │                 │
│                 │    │  │                  ▼                   │  │    │                 │
│                 │    │  │  ┌──────────────────────────────────┐  │  │    │                 │
│                 │    │  │  │         Database Layer         │  │  │    │                 │
│                 │    │  │  │        (SQLModel/PostgreSQL)   │  │  │    │                 │
│                 │    │  │  └──────────────────────────────────┘  │  │    │                 │
│                 │    │  └────────────────────────────────────────┘  │    │                 │
└─────────────────┘    └──────────────────────────────────────────────┘    └─────────────────┘
```

### 2. Authentication Flow with JWT

#### Frontend (Next.js) Configuration

```
Better Auth Client
├── Sign Up/Login
├── JWT Token Generation
└── Automatic Header Injection
    └── Authorization: Bearer <token>
```

#### Backend (FastAPI) Configuration

```
JWT Middleware
├── Token Extraction (Authorization: Bearer <token>)
├── Token Verification (using shared secret)
├── User Identification (decode user ID from JWT)
└── Request Context (attach user info to request)
```

### 3. API Layer Design

#### Current Endpoints (Need Modification for Multi-user)

```
GET    /api/tasks          → GET /api/users/{user_id}/tasks
POST   /api/tasks          → POST /api/users/{user_id}/tasks
GET    /api/tasks/{id}     → GET /api/users/{user_id}/tasks/{id}
PUT    /api/tasks/{id}     → PUT /api/users/{user_id}/tasks/{id}
DELETE /api/tasks/{id}     → DELETE /api/users/{user_id}/tasks/{id}
```

#### Enhanced Endpoint Structure

```
Authentication Endpoints:
POST   /api/auth/signup
POST   /api/auth/login
POST   /api/auth/logout

User-Specific Task Endpoints:
GET    /api/users/me/tasks        (Authenticated user's tasks)
POST   /api/users/me/tasks        (Create task for authenticated user)
GET    /api/users/me/tasks/{id}   (Get specific task)
PUT    /api/users/me/tasks/{id}   (Update specific task)
DELETE /api/users/me/tasks/{id}   (Delete specific task)
PATCH  /api/users/me/tasks/{id}/complete  (Toggle completion)
```

### 4. Data Model Enhancements

#### Current Task Model

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")  # This references Better Auth's user table
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### 5. Authentication Implementation Plan

#### Frontend (Next.js) - Better Auth Setup

```typescript
// lib/auth.ts
import { createAuthClient } from "better-auth/client";
import { jwtPlugin } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    jwtPlugin({
      secret: process.env.BETTER_AUTH_SECRET || "",
    }),
  ],
});
```

#### Backend (FastAPI) - JWT Middleware

```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from better_auth.client.plugins.jwt import JWTConfig
import jwt
from datetime import datetime

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        # Decode JWT token using Better Auth secret
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])
        user_id = payload.get("userId")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 6. API Route Protection

#### Protected Task Routes

```python
@router.get("/me/tasks", response_model=List[TaskRead])
def read_user_tasks(
    current_user_id: str = Security(verify_token),
    status: Optional[str] = Query(None, description="Filter by status"),
    session: Session = Depends(get_session)
):
    # Filter tasks by authenticated user's ID
    query = select(Task).where(Task.user_id == current_user_id)

    if status and status != "all":
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

    tasks = session.exec(query).all()
    return tasks

@router.post("/me/tasks", response_model=TaskRead)
def create_user_task(
    task: TaskCreate,
    current_user_id: str = Security(verify_token),
    session: Session = Depends(get_session)
):
    db_task = Task.model_validate(task)
    db_task.user_id = current_user_id  # Assign to authenticated user
    db_task.created_at = datetime.now()
    db_task.updated_at = datetime.now()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### 7. Frontend API Client

#### API Client with JWT Integration

```typescript
// lib/api.ts
import { authClient } from './auth';

class ApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  private async request(endpoint: string, options: RequestInit = {}) {
    // Get JWT token from Better Auth
    const session = await authClient.getSession();
    const token = session?.accessToken;

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
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getTasks() {
    return this.request('/api/users/me/tasks');
  }

  async createTask(taskData: { title: string; description?: string }) {
    return this.request('/api/users/me/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  // Additional methods for update, delete, etc.
}

export const api = new ApiClient();
```

### 8. Security Considerations

#### JWT Token Security

- Use strong secret key (BETTER_AUTH_SECRET)
- Set appropriate expiration times
- Implement token refresh mechanism
- Secure token storage (HttpOnly cookies or secure local storage)

#### Data Isolation

- Enforce user_id filtering at database level
- Validate user ownership on every request
- Implement proper error responses (don't leak information about other users' data)

#### Rate Limiting

- Implement rate limiting on authentication endpoints
- Consider per-user rate limits for API endpoints

### 9. Future AI Capabilities

#### Potential AI Integration Points

1. **Smart Task Suggestions**
   - Analyze user's task patterns
   - Suggest task titles or categories
   - Predict task completion times

2. **Natural Language Processing**
   - Parse natural language for task creation
   - Example: "Remind me to call John tomorrow at 3pm"

3. **Intelligent Prioritization**
   - Learn from user behavior to suggest priorities
   - Automatically categorize tasks

4. **Analytics Dashboard**
   - Visualize productivity patterns
   - Identify peak productivity times

#### AI Architecture Components

```
┌─────────────────┐    ┌──────────────────────────────────────────────┐
│                 │    │                                              │
│   Frontend      │    │              Backend Services                │
│   (Next.js)     │    │                                              │
│                 │    │  ┌────────────────────────────────────────┐  │
│                 │    │  │        FastAPI Server                │  │
│                 │    │  │                                      │  │
│                 │    │  │  ┌──────────────────────────────────┐  │  │
│                 │    │  │  │    Task CRUD API                 │  │  │
│                 │    │  │  └──────────────────────────────────┘  │  │
│                 │    │  │                                      │  │
│                 │    │  │  ┌──────────────────────────────────┐  │  │
│                 │    │  │  │    AI Services API               │  │  │
│                 │    │  │  │  (Optional Integration)          │  │  │
│                 │    │  │  └──────────────────────────────────┘  │  │
│                 │    │  └────────────────────────────────────────┘  │
│                 │    │                                              │
│                 │    │  ┌────────────────────────────────────────┐  │
│                 │    │  │        AI Service Layer              │  │
│                 │    │  │  ┌──────────────────────────────────┐  │  │
│                 │    │  │  │    NLP Processing                │  │  │
│                 │    │  │  │    (OpenAI/Custom Model)        │  │  │
│                 │    │  │  └──────────────────────────────────┘  │  │
│                 │    │  │                                      │  │
│                 │    │  │  ┌──────────────────────────────────┐  │  │
│                 │    │  │  │    Analytics Engine             │  │  │
│                 │    │  │  └──────────────────────────────────┘  │  │
│                 │    │  └────────────────────────────────────────┘  │
└─────────────────┘    └──────────────────────────────────────────────┘
```

### 10. Deployment Architecture

#### Containerized Deployment

```
Docker Compose Setup:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │    │   (FastAPI)     │    │   (PostgreSQL)  │
│   :3000         │    │   :8000         │    │   :5432         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Reverse Proxy │
                    │   (nginx/Caddy) │
                    │   :443/80       │
                    └─────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │      Load Balancer      │
                    │   (Cloudflare/Kubernetes)│
                    └─────────────────────────┘
```

### 11. Monitoring and Observability

#### Logging Strategy

- Structured logging for API requests
- Authentication event logging
- Performance metrics collection

#### Health Checks

- Database connectivity checks
- Authentication service availability
- API response time monitoring

### 12. Scalability Considerations

#### Horizontal Scaling

- Stateless API servers (JWT enables this)
- Database read replicas for query scaling
- CDN for static assets

#### Caching Strategy

- API response caching for common queries
- JWT token validation caching
- Database query result caching

This architecture provides a solid foundation for transforming the console app into a modern, scalable, multi-user web application with robust authentication and potential for AI capabilities.
