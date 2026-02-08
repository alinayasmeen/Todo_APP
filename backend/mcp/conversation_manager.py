"""
Conversation State Manager for the AI Chatbot

This module manages conversation state, storing and retrieving conversation history
to provide context for the AI agent.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlmodel import Session
from ..models import Message
from ..services.conversations import (
    get_or_create_conversation,
    add_message,
    get_conversation_history
)


class ConversationStateManager:
    """Manages conversation state for the AI chatbot."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def get_conversation_context(
        self, 
        user_id: str, 
        conversation_id: Optional[int] = None
    ) -> tuple[int, List[Dict[str, str]]]:
        """
        Get conversation context for the AI agent.
        
        Args:
            user_id: The ID of the user
            conversation_id: Optional conversation ID (creates new if not provided)
            
        Returns:
            Tuple of (conversation_id, list of messages in OpenAI format)
        """
        # Get or create conversation
        conversation = await get_or_create_conversation(user_id, conversation_id, self.db_session)
        
        # Get conversation history
        history = await get_conversation_history(conversation.id, user_id, self.db_session)
        
        return conversation.id, history
    
    async def store_user_message(
        self, 
        conversation_id: int, 
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """Store a user message in the conversation."""
        metadata_str = None
        if metadata:
            import json
            metadata_str = json.dumps(metadata)
        
        message = await add_message(
            conversation_id=conversation_id,
            role="user",
            content=content,
            db=self.db_session,
            message_metadata=metadata_str
        )
        return message
    
    async def store_assistant_message(
        self, 
        conversation_id: int, 
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """Store an assistant message in the conversation."""
        metadata_str = None
        if metadata:
            import json
            metadata_str = json.dumps(metadata)
        
        message = await add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            db=self.db_session,
            message_metadata=metadata_str
        )
        return message
    
    async def add_tool_call_result(
        self,
        conversation_id: int,
        tool_name: str,
        tool_input: Dict[str, Any],
        tool_output: Dict[str, Any]
    ) -> Message:
        """Add a tool call result to the conversation."""
        content = f"Tool '{tool_name}' called with input {tool_input}. Result: {tool_output}"
        
        return await self.store_assistant_message(
            conversation_id=conversation_id,
            content=content,
            metadata={
                "tool_call": {
                    "name": tool_name,
                    "input": tool_input,
                    "output": tool_output
                }
            }
        )