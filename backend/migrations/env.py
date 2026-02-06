"""
Migration script for Todo App database schema

This script handles database migrations for the Todo App using Alembic with SQLModel.
It provides functions to create and manage database schema changes for both development
and production environments.
"""
from alembic.config import Config
from alembic import command
import os
from alembic import op
import sqlalchemy as sa
from sqlmodel import SQLModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Import models to register them with SQLAlchemy metadata
from backend.models import User, Task

def upgrade():
    """
    Upgrade the database schema to the latest version.

    Creates the users and tasks tables if they don't exist.
    """
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('role', sa.String(20), nullable=False, default='user'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better performance
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])


def downgrade():
    """
    Downgrade the database schema to the previous version.

    Drops the tasks and users tables.
    """
    op.drop_table('tasks')
    op.drop_table('users')


def create_db_and_tables():
    """
    Create database tables for User and Task models using SQLModel's metadata.
    This is an alternative to using Alembic migrations for initial setup.
    """
    from backend.db import engine
    from backend.models import User, Task

    # Create all tables defined in the models
    SQLModel.metadata.create_all(engine)

    print("Database tables created successfully!")


def initialize_migration_environment():
    """
    Initialize the migration environment with proper configuration.
    """
   

    # Create alembic.ini configuration
    alembic_ini_content = f"""[alembic]
script_location = migrations
sqlalchemy.url = {os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/todo_app')}

[post_write_hooks]
# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""

    with open('/mnt/d/Hackathon_Q4/Todo-App/backend/alembic.ini', 'w') as f:
        f.write(alembic_ini_content)

    print("Alembic configuration created!")


if __name__ == "__main__":
    # For initial setup, we'll use the SQLModel approach
    create_db_and_tables()