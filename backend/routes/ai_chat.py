"""
AI Chat Endpoint for Todo Management

This module implements the chat endpoint that processes natural language
queries and manages todos through the AI agent and MCP tools.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..auth import get_current_active_user
from ..models import User
from ..mcp.server import initialize_mcp_server
from ..services.ai_chat import process_natural_language_query


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: list = []


router = APIRouter(prefix="/ai", tags=["ai"])


def get_db_session():
    """Dependency to get database session."""
    from ..db import get_engine
    with Session(get_engine()) as session:
        yield session


# Global variable to store the initialized MCP server
_initialized_mcp = False

@router.on_event("startup")
async def startup_event():
    """Initialize the MCP server on startup."""
    global _initialized_mcp
    if _initialized_mcp:
        return  # Prevent multiple initializations
    
    # Note: We can't initialize with a session here because sessions are request-scoped
    # The session will be set per-request in the handler
    _initialized_mcp = True


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Process natural language input and return AI response.
    
    This endpoint:
    1. Gets or creates a conversation
    2. Retrieves conversation history
    3. Stores the user's message
    4. Determines if task operation is needed or general conversation
    5. Uses appropriate AI model (GEMINI for general, agent for tasks)
    6. Stores the AI's response
    7. Returns the response
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden: Cannot access another user's chat")
    
    try:
        # Set the database session for MCP tools
        from ..mcp.server import set_db_session_and_service
        set_db_session_and_service(db, None)  # Pass None for task_service as we're using direct imports
        
        # Process the natural language query
        result = await process_natural_language_query(
            user_id=current_user.id,
            query=request.message,
            conversation_id=request.conversation_id,
            db_session=db
        )
        
        # Return the response
        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """Retrieve conversation history."""
    from ..services.conversations import get_conversation_history
    
    history = await get_conversation_history(conversation_id, current_user.id, db)
    return {"conversation_id": conversation_id, "history": history}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """Delete a conversation."""
    from ..services.conversations import delete_conversation as delete_conv
    
    success = await delete_conv(conversation_id, current_user.id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {"message": "Conversation deleted successfully"}