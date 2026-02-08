from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
import uuid


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    role: str = Field(default="user", max_length=20)  # For RBAC: 'user' or 'admin'
    hashed_password: Optional[str] = Field(default=None, max_length=255)  # Store hashed password
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)  # Optional due date for the task


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")  # References User.id (table name is 'user' in SQLModel)
    # AI-ready metadata fields
    ai_category: Optional[str] = Field(default=None, max_length=50)  # Category assigned by AI
    ai_priority_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)  # Priority score from AI (0-1)
    ai_estimated_duration: Optional[int] = Field(default=None, ge=1)  # Estimated duration in minutes from AI
    ai_suggested_tags: Optional[str] = Field(default=None, max_length=500)  # Comma-separated tags suggested by AI
    ai_processing_metadata: Optional[str] = Field(default=None, max_length=2000)  # JSON string for AI processing details
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Conversation(SQLModel, table=True):
    """Model for storing conversation state."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")  # References User.id
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Message(SQLModel, table=True):
    """Model for storing individual messages in a conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")  # References Conversation.id
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(max_length=5000)  # The message content
    created_at: datetime = Field(default_factory=datetime.now)
    # Metadata for tracking tool calls and responses
    message_metadata: Optional[str] = Field(default=None, max_length=2000)  # JSON string for additional metadata


class TaskAction(SQLModel, table=True):
    """Model for tracking AI actions performed on tasks."""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")  # References Conversation.id
    action_type: str = Field(max_length=50)  # Type of action (create, update, delete, complete)
    task_details: Optional[str] = Field(default=None, max_length=2000)  # JSON string with task details
    result: Optional[str] = Field(default=None, max_length=2000)  # Result of the action
    created_at: datetime = Field(default_factory=datetime.now)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None  # Optional due date for the task
    # AI-ready metadata fields
    ai_category: Optional[str] = None
    ai_priority_score: Optional[float] = None
    ai_estimated_duration: Optional[int] = None
    ai_suggested_tags: Optional[str] = None
    ai_processing_metadata: Optional[str] = None


class TaskRead(TaskBase):
    id: int
    user_id: str
    # AI-ready metadata fields
    ai_category: Optional[str] = None
    ai_priority_score: Optional[float] = None
    ai_estimated_duration: Optional[int] = None
    ai_suggested_tags: Optional[str] = None
    ai_processing_metadata: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None  # Optional due date for the task


class ConversationRead(SQLModel):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class MessageRead(SQLModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
    message_metadata: Optional[str] = None


class UserRead(SQLModel):
    id: str
    email: str
    name: Optional[str] = None
    role: str
    created_at: datetime
    updated_at: datetime


class UserCreate(SQLModel):
    email: str
    name: Optional[str] = None
    password: str  # Plain text password that will be hashed before saving


class UserUpdate(SQLModel):
    name: Optional[str] = None
    role: Optional[str] = None  # Allow role updates for admin purposes


class UserLogin(SQLModel):
    email: str
    password: str  # Plain text password for comparison with hash