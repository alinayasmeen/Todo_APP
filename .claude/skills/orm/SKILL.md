---
name: orm
description: Guides the use of Object-Relational Mapping (ORM) tools to interact with relational databases using code objects instead of raw SQL.
---

# ORM

## Instructions

1. Choose an ORM framework compatible with your language (e.g., SQLAlchemy for Python).
2. Define models that map database tables to code classes, including fields and relationships.
3. Perform CRUD operations using ORM methods instead of raw SQL queries.
4. Manage database migrations and schema changes through the ORM.
5. Optimize queries with indexing, lazy loading, and proper relationships.
6. Handle transactions, rollbacks, and exception management.
7. Integrate ORM with your backend framework (e.g., FastAPI) for seamless data access.
8. Document models, relationships, and query patterns for maintainers.

## Examples

- Defining a SQLAlchemy model:

  ```python
  from sqlalchemy import Column, Integer, String
  from sqlalchemy.ext.declarative import declarative_base

  Base = declarative_base()

  class User(Base):
      __tablename__ = 'users'
      id = Column(Integer, primary_key=True)
      username = Column(String, unique=True, nullable=False)
      email = Column(String, unique=True, nullable=False)

Querying data with ORM:

python
Copy code
user = session.query(User).filter_by(username="alina").first()
Creating a new record:

python
Copy code
new_user = User(username="ali", email="<ali@example.com>")
session.add(new_user)
session.commit()
