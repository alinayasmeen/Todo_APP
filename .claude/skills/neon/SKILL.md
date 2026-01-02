---
name: neon
description: Guides the use of Neon, a cloud-hosted PostgreSQL platform, for database creation, management, and integration with applications.
---

# Neon

## Instructions

1. Set up and configure Neon projects and branches for development, staging, and production.
2. Create databases, tables, and relationships using PostgreSQL standards.
3. Use SQL queries for CRUD operations, indexing, and data retrieval.
4. Optimize performance using indexes, query tuning, and proper schema design.
5. Implement backup, restore, and branching strategies provided by Neon.
6. Connect Neon databases with backend frameworks or ORMs for seamless integration.
7. Ensure security with proper authentication, roles, and access control.
8. Document Neon database configurations, schemas, and query patterns.

## Examples

- Creating a table in Neon:

  ```sql
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(50) UNIQUE NOT NULL,
      email VARCHAR(100) UNIQUE NOT NULL,
      created_at TIMESTAMP DEFAULT NOW()
  );

Querying data:

sql
Copy code
SELECT * FROM users WHERE username='alina';
Creating an index for performance:

sql
Copy code
CREATE INDEX idx_username ON users(username);
Using branches for testing:

css
Copy code
neon branch create staging --from main
