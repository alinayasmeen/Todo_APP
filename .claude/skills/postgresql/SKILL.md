---
name: postgresql
description: Guides the use, management, and optimization of PostgreSQL relational databases for applications.
---

# PostgreSQL

## Instructions

1. Design and create databases, tables, and relationships using SQL.
2. Write efficient queries for inserting, updating, deleting, and retrieving data.
3. Implement indexes, constraints, and foreign keys for data integrity and performance.
4. Use transactions, views, and stored procedures where needed.
5. Monitor database performance and optimize queries to reduce latency.
6. Ensure proper backup, restore, and security configurations.
7. Integrate PostgreSQL with backend frameworks and ORMs.
8. Document database schemas, queries, and optimization strategies.

## Examples

- Creating a table:

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
Updating a record:

sql
Copy code
UPDATE users SET email='<alina@example.com>' WHERE username='alina';
Indexing for performance:

sql
Copy code
CREATE INDEX idx_username ON users(username);
