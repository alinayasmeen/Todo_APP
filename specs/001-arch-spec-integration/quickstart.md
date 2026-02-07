# Quickstart Guide: Todo App with Authentication and RBAC

## Prerequisites
- Node.js 18+ for frontend
- Python 3.12+ for backend
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
cp .env.example .env
# Edit .env with your database URL and Better Auth settings
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
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
BETTER_AUTH_URL=http://localhost:4000
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=https://todo-app-lpxv.onrender.com/api
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:4000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
```

### 5. Running the Application

#### Backend
```bash
# Activate virtual environment
source venv/bin/activate

# Run the backend server
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
# From the frontend directory
npm run dev
# or
yarn dev
```

## API Usage

### Authentication Flow
1. Register a new user: `POST /auth/register`
2. Login to get JWT token: `POST /auth/login`
3. Use token in headers for protected endpoints:
   ```
   Authorization: Bearer <jwt_token>
   ```

### Task Operations
Once authenticated, you can perform these operations:

**Get all tasks:**
```bash
curl -H "Authorization: Bearer <token>" \
     https://todo-app-lpxv.onrender.com/api/users/me/tasks
```

**Create a task:**
```bash
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample task", "description": "Sample description"}' \
     https://todo-app-lpxv.onrender.com/api/users/me/tasks
```

### Administrative Operations (Admin Role Only)
Admin users have access to additional endpoints:

**Get all tasks in the system:**
```bash
curl -H "Authorization: Bearer <admin-token>" \
     https://todo-app-lpxv.onrender.com/api/admin/tasks
```

**Get tasks for a specific user:**
```bash
curl -H "Authorization: Bearer <admin-token>" \
     https://todo-app-lpxv.onrender.com/api/admin/users/{user-id}/tasks
```

## Role-Based Access Control
- **User Role**: Default role for registered users, can only access their own tasks
- **Admin Role**: Special role with elevated privileges to access all tasks in the system
- Role assignment is managed by system administrators

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