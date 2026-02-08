"""
OpenAI Agent Integration for Todo Management

This module integrates the OpenAI Agents SDK to process natural language
queries and manage todos using MCP tools.
"""

import os
from typing import Dict, Any, List
from openai import OpenAI
from ..mcp.server import get_mcp_server


class TodoAgent:
    """AI Agent for managing todos through natural language using OpenAI function calling."""
    
    def __init__(self):
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Get the MCP server instance
        self.mcp_server = get_mcp_server()
    
    def _get_mcp_tools(self):
        """Get the function definitions for the agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "status": {"type": "string", "description": "Filter by status: all, pending, completed", "enum": ["all", "pending", "completed"]}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "integer", "description": "Task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "integer", "description": "Task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "integer", "description": "Task ID to update"},
                            "title": {"type": "string", "description": "New task title"},
                            "description": {"type": "string", "description": "New task description"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]
    
    async def process_query(
        self, 
        user_id: str, 
        query: str, 
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Process a natural language query and return the AI response.
        
        Args:
            user_id: The ID of the user making the request
            query: The natural language query
            conversation_history: History of the conversation
            
        Returns:
            Dictionary containing the response and any tool calls made
        """
        # Prepare the messages for the agent
        messages = []
        
        # Add system message
        messages.append({
            "role": "system",
            "content": "You are a helpful assistant for managing todos. Use the provided functions to manage tasks for the user."
        })
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add the current query
        messages.append({"role": "user", "content": query})
        
        try:
            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self._get_mcp_tools(),
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # If the model wants to call functions, process them
            if tool_calls:
                # In a real implementation, we would execute the tool calls
                # For now, we'll return the tool calls for the calling function to handle
                return {
                    "response": response_message.content or "Processing your request...",
                    "tool_calls": [{"name": tc.function.name, "arguments": tc.function.arguments} for tc in tool_calls],
                    "final_state": response
                }
            else:
                # If no tool calls were made, return the response directly
                return {
                    "response": response_message.content or "I processed your request.",
                    "tool_calls": [],
                    "final_state": response
                }
                
        except Exception as e:
            return {
                "response": f"Error processing query: {str(e)}",
                "tool_calls": [],
                "final_state": {}
            }


# Global agent instance
todo_agent = None


def get_todo_agent():
    """Get the global todo agent instance."""
    global todo_agent
    if todo_agent is None:
        todo_agent = TodoAgent()
    return todo_agent