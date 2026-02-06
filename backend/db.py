from sqlmodel import SQLModel, create_engine
from .models import User, Task
import os
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.pool import Pool

load_dotenv()

def get_database_url():
    """Get database URL from environment or use default for Neon PostgreSQL"""
    # Prioritize NEON_DATABASE_URL for Neon PostgreSQL, fall back to DATABASE_URL
    database_url = os.getenv("NEON_DATABASE_URL", os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/todo_app"))
    return database_url


def create_db_and_tables():
    """Create database tables for User and Task models."""
    database_url = get_database_url()

    # Create engine with connection pooling settings for production
    engine = create_engine(
        database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before use
        echo=False  # Set to True for SQL query logging during development
    )

    # Create all tables defined in the models
    SQLModel.metadata.create_all(engine)

    return engine


# Optional: Add connection event listeners for debugging
@event.listens_for(Pool, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance (only applicable for SQLite)."""
    if dbapi_connection.__class__.__module__ == "sqlite3":
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")  # Enable foreign key constraints
        cursor.close()


# Global engine instance that can be imported by other modules
# Initialize only when needed to avoid startup connection issues
def get_engine():
    """Get the database engine, creating it if it doesn't exist."""
    return create_db_and_tables()