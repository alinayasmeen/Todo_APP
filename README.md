# Todo App with Authentication and RBAC

A full-stack web application that transforms a console-based todo application into a multi-user web application with secure authentication, role-based access control, and AI-ready architecture.

## Features

- **Multi-user support**: Each user has their own account and tasks
- **Secure authentication**: JWT-based authentication with registration and login
- **Role-based access control**: Different permissions for regular users and admins
- **Task management**: Full CRUD operations for tasks with data isolation
- **AI-ready architecture**: Extensible design for future AI integration
- **Structured logging**: Comprehensive logging for observability
- **Neon PostgreSQL**: Serverless PostgreSQL database with built-in backup/restore

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLModel, JWT authentication
- **Frontend**: Next.js 14, TypeScript, React
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Security**: Role-based access control, data isolation
- **AI Integration**: Pluggable AI service interface

## Prerequisites

- Node.js 18+
- Python 3.12+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Git

## Setup Instructions

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd todo-app
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp ../.env.example .env
# Edit .env with your database URL and authentication settings
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with your API and auth settings
```

### 4. Environment Configuration

#### Backend (.env)

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_app?sslmode=require
SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env.local)

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running the Application

### Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Run the backend server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
# From the frontend directory
npm run dev
# or
yarn dev
```

## API Usage

### Authentication Flow

1. Register a new user: `POST /api/auth/register`
2. Login to get JWT token: `POST /api/auth/login`
3. Use token in headers for protected endpoints:

   ```
   Authorization: Bearer <jwt_token>
   ```

### Task Operations

Once authenticated, you can perform these operations:

**Get all tasks:**

```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/tasks
```

**Create a task:**

```bash
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample task", "description": "Sample description"}' \
     http://localhost:8000/api/tasks
```

### Administrative Operations (Admin Role Only)

Admin users have access to additional endpoints:

**Get all tasks in the system:**

```bash
curl -H "Authorization: Bearer <admin-token>" \
     http://localhost:8000/api/admin
```

**Get tasks for a specific user:**

```bash
curl -H "Authorization: Bearer <admin-token>" \
     http://localhost:8000/api/admin/users/{user-id}/tasks
```

## Role-Based Access Control

- **User Role**: Default role for registered users, can only access their own tasks
- **Admin Role**: Special role with elevated privileges to access all tasks in the system
- Role assignment is managed by system administrators

## Database Migration

To create database tables:

```bash
# From the backend directory
python migrate.py create
```

Other migration commands:

- `python migrate.py drop` - Drop all tables
- `python migrate.py reset` - Reset the database

## Development Commands

### Backend

```bash
# Run tests
pytest

# Run with auto-reload
uvicorn main:app --reload

# Format code
black .

# Check types
mypy .
```

### Frontend

```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint
```

## API Endpoints

### Authentication Endpoints (`/api/auth`)

- `POST /register` - Register a new user
- `POST /login` - Authenticate user and return JWT token
- `GET /profile` - Get current user's profile
- `POST /refresh` - Refresh JWT token

### Task Management Endpoints (`/api/tasks`)

- `GET /` - Get all tasks for authenticated user
- `POST /` - Create a new task for authenticated user
- `GET /{task_id}` - Get a specific task
- `PUT /{task_id}` - Update a specific task
- `PATCH /{task_id}/complete` - Toggle task completion status
- `DELETE /{task_id}` - Delete a specific task
- `GET /ai/suggestions` - Get AI-generated task suggestions
- `GET /ai/insights` - Get AI-generated productivity insights

### Administrative Endpoints (`/api/admin`)

- `GET /` - Get all tasks in the system
- `GET /users/{user_id}/tasks` - Get tasks for a specific user
- `PATCH /users/{user_id}/role` - Update user's role
- `GET /users/{user_id}` - Get user information
- `GET /stats` - Get system statistics

## Security Features

- JWT token validation on all protected endpoints
- Data isolation - users can only access their own data
- Password hashing with bcrypt
- Rate limiting on authentication endpoints
- Proper error handling without information leakage

## AI Integration

The application is designed with AI capabilities in mind:

- AI service interface for easy integration of AI providers
- AI-ready data models with metadata fields
- AI endpoints for task suggestions and productivity insights
- Pluggable architecture for swapping AI implementations

## Troubleshooting

### Common Issues

- **Database Connection**: Ensure PostgreSQL is running and credentials are correct
- **Authentication**: Verify JWT secret is the same in both backend and frontend
- **CORS**: Check that frontend origin is allowed in backend CORS settings
- **Environment Variables**: Ensure all required environment variables are set
- **Role Access**: Verify user has appropriate role for accessing protected endpoints

### Reset Database

```bash
# In backend directory
python -c "from db import create_db_and_tables; create_db_and_tables()"
```

## Architecture Overview

The application follows a layered architecture:

- **Presentation Layer**: Next.js frontend with React components
- **API Layer**: FastAPI backend with REST endpoints
- **Service Layer**: Business logic and AI integration services
- **Data Layer**: SQLModel ORM with Neon PostgreSQL database
- **Security Layer**: JWT authentication and RBAC middleware

This architecture ensures separation of concerns, scalability, and maintainability while preparing for future AI integration.
