from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import create_db_and_tables
import logging

# Set up structured logging
from .logging_config import setup_structured_logging
setup_structured_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Todo App API"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "todo-app-api",
        "version": "0.1.0"
    }

# Import and include routes
from .routes import tasks
from .routes import auth
from .routes import admin
from .routes import ai_chat

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(ai_chat.router, prefix="/api", tags=["ai"])