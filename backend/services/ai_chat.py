"""
GEMINI Integration Service for AI Chatbot

This module handles the integration with GEMINI API through the OpenAI-compatible interface.
"""

import os
import json
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv
from sqlmodel import Session
from ..models import User
from ..mcp.conversation_manager import ConversationStateManager
from ..mcp.server import get_mcp_server
from ..ai.agent import get_todo_agent


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_gemini_client():
    """Initialize and return the GEMINI client."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it before running the application.")
    
    return OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


async def process_natural_language_query(
    user_id: str,
    query: str,
    conversation_id: Optional[int],
    db_session: Session
):
    """
    Process a natural language query using GEMINI and return an appropriate response.
    
    This function will:
    1. Determine if the query requires task operations
    2. Use the AI agent with MCP tools if needed
    3. Otherwise, use GEMINI for general conversation
    """
    # Initialize conversation state manager
    state_manager = ConversationStateManager(db_session)
    
    # Get conversation context
    actual_conversation_id, conversation_history = await state_manager.get_conversation_context(
        user_id=user_id,
        conversation_id=conversation_id
    )
    
    # Store the user's message
    await state_manager.store_user_message(
        conversation_id=actual_conversation_id,
        content=query
    )
    
    # Use the AI agent with MCP tools for all queries
    agent = get_todo_agent()
    result = await agent.process_query(
        user_id=user_id,
        query=query,
        conversation_history=conversation_history
    )
    
    # Execute any tool calls that were generated
    if result.get("tool_calls"):
        # In this implementation, the tools are executed directly by the MCP server
        # when the agent makes the function calls, so we just record the results
        for tool_call in result["tool_calls"]:
            tool_name = tool_call["name"]
            arguments = json.loads(tool_call["arguments"])
            
            # Add user_id to arguments if not present
            if "user_id" not in arguments:
                arguments["user_id"] = user_id
            
            # Note: In the current implementation, the tools are executed when the OpenAI API
            # processes the function call, so we're just recording what happened
            tool_result = f"{tool_name} executed with args: {arguments}"
            
            # Add the tool result to the conversation
            await state_manager.add_tool_call_result(
                conversation_id=actual_conversation_id,
                tool_name=tool_name,
                tool_input=arguments,
                tool_output={"status": "executed", "result": tool_result}
            )
    
    # Store the AI's response
    await state_manager.store_assistant_message(
        conversation_id=actual_conversation_id,
        content=result["response"]
    )
    
    return {
        "conversation_id": actual_conversation_id,
        "response": result["response"],
        "tool_calls": result.get("tool_calls", []),
        "is_task_action": len(result.get("tool_calls", [])) > 0
    }