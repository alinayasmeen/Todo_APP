# Data Model: Todo App Authentication Integration

## User Entity

### Attributes
- **id**: String (Primary identifier from Better Auth system)
- **email**: String (Unique email address for login)
- **name**: String (User's display name)
- **role**: String (User role: "user" or "admin", default: "user")
- **created_at**: DateTime (Account creation timestamp)
- **updated_at**: DateTime (Last account update timestamp)

### Relationships
- **Tasks**: One-to-many relationship (one user to many tasks)

## Task Entity

### Attributes
- **id**: Integer (Auto-incrementing primary key)
- **user_id**: String (Foreign key referencing User.id)
- **title**: String (Required, min length: 1, max length: 200)
- **description**: String (Optional, max length: 1000)
- **completed**: Boolean (Default: false)
- **created_at**: DateTime (Task creation timestamp)
- **updated_at**: DateTime (Last task update timestamp)

### Relationships
- **User**: Many-to-one relationship (many tasks to one user)

### Validation Rules
- Title must be 1-200 characters
- Description, if provided, must be ≤1000 characters
- All tasks must be associated with a valid user_id
- Completed status defaults to false
- Only task owner or admin can modify task

### State Transitions
- **Creation**: `status = "pending"` (completed = false)
- **Completion**: `status = "completed"` (completed = true)
- **Reopening**: `status = "pending"` (completed = false)

## API Data Contracts

### Task Creation Request
```json
{
  "title": "String (required, 1-200 chars)",
  "description": "String (optional, <=1000 chars)"
}
```

### Task Response
```json
{
  "id": "Integer",
  "user_id": "String",
  "title": "String",
  "description": "String (nullable)",
  "completed": "Boolean",
  "created_at": "ISO 8601 DateTime",
  "updated_at": "ISO 8601 DateTime"
}
```

### Task Update Request
```json
{
  "title": "String (optional, 1-200 chars)",
  "description": "String (optional, <=1000 chars)",
  "completed": "Boolean (optional)"
}
```

## Database Schema

### Users Table
```
users (
  id VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  role VARCHAR(20) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tasks Table
```
tasks (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Query Patterns

### User's Tasks Query
```sql
SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC
```

### Specific Task Query
```sql
SELECT * FROM tasks WHERE id = $1 AND user_id = $2
```

### Admin Tasks Query (for admin users only)
```sql
SELECT t.*, u.name as owner_name FROM tasks t JOIN users u ON t.user_id = u.id
ORDER BY t.created_at DESC
LIMIT $1 OFFSET $2
```

### Filtered Tasks Query
```sql
SELECT * FROM tasks
WHERE user_id = $1
AND ($2 IS NULL OR completed = $2)
ORDER BY CASE WHEN $3 = 'title' THEN title ELSE created_at END
```

## Access Control Rules

### Role-Based Permissions
- **User Role**:
  - Read/write access to their own tasks
  - Cannot access other users' tasks
  - Limited to personal task management operations

- **Admin Role**:
  - Read/write access to all tasks in the system
  - Can view aggregated task statistics
  - Can perform administrative operations on any task
  - Can manage user accounts and roles (future extension)