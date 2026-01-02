---

name: db-design
description: Helps design efficient and scalable database schemas for relational and graph databases, ensuring data integrity and optimized queries
---

# DB Design

- Instructions:

1. Analyze the requirements of the system or feature.
2. Identify entities, relationships, and data types.
3. Design tables for relational databases (e.g., PostgreSQL) including primary keys, foreign keys, indexes, and constraints.
4. Design nodes and relationships for graph databases (e.g., Neo4j) including labels, properties, and connections.
5. Optimize schema for query performance and storage efficiency.
6. Document the schema clearly with diagrams or tables.

-- Examples:

- Creating a PostgreSQL schema for a user management system:
CREATE TABLE users (
user_id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
created_at TIMESTAMP DEFAULT NOW()
);

css
Copy code

- Designing a Neo4j graph schema for a social network:
(:User {id, name, email})-[:FRIEND_WITH]->(:User)
(:User)-[:POSTED]->(:Post {id, content, timestamp})
