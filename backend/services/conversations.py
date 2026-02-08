"""
Services for managing conversations and messages for the AI chatbot.
"""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from ..models import Conversation, Message, ConversationRead, MessageRead


async def create_conversation(user_id: str, db: Session) -> Conversation:
    """Create a new conversation."""
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


async def get_conversation(conversation_id: int, user_id: str, db: Session) -> Optional[Conversation]:
    """Get a specific conversation for a user."""
    conversation = db.exec(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == user_id)
    ).first()
    return conversation


async def get_or_create_conversation(user_id: str, conversation_id: Optional[int], db: Session) -> Conversation:
    """Get an existing conversation or create a new one."""
    if conversation_id:
        conversation = await get_conversation(conversation_id, user_id, db)
        if conversation:
            return conversation
    
    # Create a new conversation
    return await create_conversation(user_id, db)


async def add_message(conversation_id: int, role: str, content: str, db: Session, message_metadata: Optional[str] = None) -> Message:
    """Add a message to a conversation."""
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        message_metadata=message_metadata
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


async def get_messages(conversation_id: int, db: Session, limit: int = 50) -> List[Message]:
    """Get messages for a conversation."""
    messages = db.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .limit(limit)
    ).all()
    return messages


async def get_conversation_history(conversation_id: int, user_id: str, db: Session) -> List[dict]:
    """Get the full conversation history as a list of dictionaries."""
    # First verify the conversation belongs to the user
    conversation = await get_conversation(conversation_id, user_id, db)
    if not conversation:
        return []
    
    # Get all messages in the conversation
    messages = await get_messages(conversation_id, db)
    
    # Format messages for the AI agent
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg.role,
            "content": msg.content
        })
    
    return formatted_messages


async def delete_conversation(conversation_id: int, user_id: str, db: Session) -> bool:
    """Delete a conversation and all its messages."""
    conversation = await get_conversation(conversation_id, user_id, db)
    if not conversation:
        return False
    
    # Delete all messages in the conversation first
    messages = await get_messages(conversation_id, db)
    for message in messages:
        db.delete(message)
    
    # Delete the conversation
    db.delete(conversation)
    db.commit()
    return True