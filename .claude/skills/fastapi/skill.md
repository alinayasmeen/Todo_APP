---
name: fastapi
description: Guides the creation of RESTful APIs using FastAPI, including routing, validation, and integration with databases or AI services.
---

# FastAPI

## Instructions

1. Set up a FastAPI project and define the main application entry point.
2. Create API routes with proper HTTP methods (GET, POST, PUT, DELETE) and path parameters.
3. Use Pydantic models for request validation and response formatting.
4. Integrate with databases (PostgreSQL, Neo4j, etc.) or external services like AI APIs.
5. Implement authentication and authorization where required.
6. Include error handling, logging, and middleware for enhanced functionality.
7. Test endpoints to ensure correctness and efficiency.
8. Document APIs using FastAPI’s built-in OpenAPI and Swagger UI.

## Examples

- Basic FastAPI endpoint:
  
  ```python
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/hello")
  async def say_hello():
      return {"message": "Hello, World!"}

Endpoint with request validation:

from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

@app.post("/users")
async def create_user(user: User):
    return {"username": user.username, "email": user.email}

Connecting to PostgreSQL with SQLAlchemy:
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:password@localhost/dbname")
