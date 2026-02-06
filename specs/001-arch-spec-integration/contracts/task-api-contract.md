# Task Management API Contract

## Base URL
`https://api.todoapp.com/api` (production)
`http://localhost:8000/api` (development)

## Authentication
All endpoints require JWT token in Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Role-Based Access Control
- **User Role**: Can only access their own tasks
- **Admin Role**: Can access all tasks in the system with additional administrative endpoints

## Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

**Responses:**
- `201`: User created successfully
- `400`: Invalid input data
- `409`: Email already exists

#### POST /auth/login
Authenticate user and return JWT token.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Responses:**
- `200`: Authentication successful, returns JWT token
- `401`: Invalid credentials

### User Task Management Endpoints (User Role)

#### GET /users/me/tasks
Retrieve all tasks for the authenticated user.

**Query Parameters:**
- `status` (optional): Filter by status ("all", "pending", "completed")
- `sort` (optional): Sort by ("created", "title")

**Responses:**
- `200`: Array of user's tasks
- `401`: Unauthorized (invalid/expired token)

#### POST /users/me/tasks
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, <=1000 chars)"
}
```

**Responses:**
- `201`: Task created successfully
- `400`: Invalid input data
- `401`: Unauthorized (invalid/expired token)

#### GET /users/me/tasks/{id}
Retrieve a specific task for the authenticated user.

**Path Parameters:**
- `id`: Task ID

**Responses:**
- `200`: Task data
- `401`: Unauthorized (invalid/expired token)
- `403`: Access denied (trying to access another user's task)
- `404`: Task not found

#### PUT /users/me/tasks/{id}
Update a specific task for the authenticated user.

**Path Parameters:**
- `id`: Task ID

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Responses:**
- `200`: Task updated successfully
- `400`: Invalid input data
- `401`: Unauthorized (invalid/expired token)
- `403`: Access denied (trying to access another user's task)
- `404`: Task not found

#### PATCH /users/me/tasks/{id}/complete
Toggle completion status of a task for the authenticated user.

**Path Parameters:**
- `id`: Task ID

**Responses:**
- `200`: Task completion status toggled
- `401`: Unauthorized (invalid/expired token)
- `403`: Access denied (trying to access another user's task)
- `404`: Task not found

#### DELETE /users/me/tasks/{id}
Delete a specific task for the authenticated user.

**Path Parameters:**
- `id`: Task ID

**Responses:**
- `200`: Task deleted successfully
- `401`: Unauthorized (invalid/expired token)
- `403`: Access denied (trying to access another user's task)
- `404`: Task not found

### Administrative Task Management Endpoints (Admin Role)

#### GET /admin/tasks
Retrieve all tasks in the system (admin only).

**Query Parameters:**
- `limit` (optional): Number of tasks to return (default: 50, max: 1000)
- `offset` (optional): Number of tasks to skip (default: 0)
- `status` (optional): Filter by status ("all", "pending", "completed")
- `user_id` (optional): Filter by specific user

**Responses:**
- `200`: Array of all tasks in the system
- `401`: Unauthorized (invalid/expired token)
- `403`: Access denied (user does not have admin role)

#### GET /admin/users/{user_id}/tasks
Retrieve all tasks for a specific user (admin only).

**Path Parameters:**
- `user_id`: User ID to retrieve tasks for

**Query Parameters:**
- `status` (optional): Filter by status ("all", "pending", "completed")
- `sort` (optional): Sort by ("created", "title")

**Responses:**
- `200`: Array of user's tasks
- `401`: Unauthorized (invalid/expired token)
- `403`: Access denied (user does not have admin role)
- `404`: User not found

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "Human-readable error message"
}
```

## Common Error Codes
- `400 Bad Request`: Invalid request parameters or body
- `401 Unauthorized`: Missing, invalid, or expired JWT token
- `403 Forbidden`: User lacks permission for requested resource
- `404 Not Found`: Requested resource does not exist
- `500 Internal Server Error`: Unexpected server error