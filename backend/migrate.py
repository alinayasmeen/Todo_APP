"""
Database Migration Script for Todo App

This script handles database setup and migrations for the Todo App.
It creates the necessary tables for users and tasks in the Neon PostgreSQL database.
"""

from sqlmodel import SQLModel
from backend.db import engine
from backend.models import User, Task  # Import models to register them
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_db_and_tables():
    """
    Create database tables for User and Task models.

    This function creates all necessary database tables based on the SQLModel models.
    It's safe to call multiple times as it will only create tables that don't exist.
    """
    logger.info("Creating database tables...")

    # Create all tables defined in the models
    SQLModel.metadata.create_all(engine)

    logger.info("Database tables created successfully!")


def drop_db_tables():
    """
    Drop all database tables (use with caution!).

    This function drops all tables defined in the SQLModel metadata.
    Use only in development environments.
    """
    logger.warning("Dropping all database tables...")

    # Drop all tables defined in the models
    SQLModel.metadata.drop_all(engine)

    logger.info("Database tables dropped successfully!")


def reset_db():
    """
    Reset the database by dropping and recreating all tables.

    This function drops all existing tables and recreates them.
    Use only in development environments.
    """
    logger.warning("Resetting database...")

    # Drop all tables
    SQLModel.metadata.drop_all(engine)

    # Recreate all tables
    SQLModel.metadata.create_all(engine)

    logger.info("Database reset successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1].lower()

        if action == "create":
            create_db_and_tables()
        elif action == "drop":
            drop_db_tables()
        elif action == "reset":
            reset_db()
        else:
            print(f"Unknown action: {action}")
            print("Usage: python migrate.py [create|drop|reset]")
    else:
        # Default action is to create tables
        create_db_and_tables()