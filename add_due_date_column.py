"""
Migration script to add due_date column to the task table.
"""
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel
from backend.models import Task
from backend.db import get_database_url


def migrate():
    """Add due_date column to the task table."""
    database_url = get_database_url()
    
    # Connect to the database
    engine = create_engine(database_url)
    
    # Add the due_date column to the existing task table
    with engine.connect() as conn:
        # Check if the column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'due_date'
        """))
        
        if result.fetchone() is None:
            # Column doesn't exist, add it
            conn.execute(text("ALTER TABLE task ADD COLUMN due_date TIMESTAMP;"))
            conn.commit()
            print("Added due_date column to task table")
        else:
            print("due_date column already exists in task table")


if __name__ == "__main__":
    migrate()