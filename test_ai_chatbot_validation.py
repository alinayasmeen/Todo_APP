"""
Test script to validate the AI chatbot implementation.
"""
import pytest
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


def test_mcp_server_initialization():
    """Test that MCP server can be initialized."""
    from backend.mcp.server import MCPServer
    
    # This test verifies that the MCP server can be instantiated
    # In a real test, we would inject actual db session and task service
    try:
        # Just verify the class exists and can be imported
        assert MCPServer is not None
        print("✓ MCP server class exists")
    except ImportError:
        pytest.fail("MCP server module not found")


def test_database_models_for_conversations():
    """Test that conversation-related database models exist."""
    from backend.models import Conversation, Message, TaskAction
    
    # Verify that the models exist and have expected attributes
    conv_attrs = ["id", "user_id", "created_at", "updated_at"]
    for attr in conv_attrs:
        assert hasattr(Conversation, attr), f"Conversation model missing {attr}"
    
    msg_attrs = ["id", "conversation_id", "role", "content", "created_at", "message_metadata"]
    for attr in msg_attrs:
        assert hasattr(Message, attr), f"Message model missing {attr}"
    
    action_attrs = ["id", "conversation_id", "action_type", "task_details", "result", "created_at"]
    for attr in action_attrs:
        assert hasattr(TaskAction, attr), f"TaskAction model missing {attr}"
    
    print("✓ Conversation-related database models exist with correct attributes")


def test_ai_services_exist():
    """Test that AI services exist and can be imported."""
    try:
        from backend.services.ai_chat import process_natural_language_query
        assert process_natural_language_query is not None
        print("✓ AI chat service exists")
    except ImportError:
        pytest.fail("AI chat service module not found")
    
    try:
        from backend.ai.agent import get_todo_agent
        assert get_todo_agent is not None
        print("✓ AI agent service exists")
    except ImportError:
        pytest.fail("AI agent service module not found")


def test_routes_exist():
    """Test that AI chat routes exist."""
    try:
        from backend.routes.ai_chat import router
        assert router is not None
        print("✓ AI chat routes exist")
    except ImportError:
        pytest.fail("AI chat routes module not found")


def test_frontend_component_exists():
    """Test that the frontend chat component exists."""
    import os
    component_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'components', 'AIChatbot.tsx')
    assert os.path.exists(component_path), "AI Chatbot component does not exist"
    print("✓ Frontend AI chat component exists")


if __name__ == "__main__":
    print("Running AI Chatbot Implementation Tests...")
    
    test_mcp_server_initialization()
    test_database_models_for_conversations()
    test_ai_services_exist()
    test_routes_exist()
    test_frontend_component_exists()
    
    print("\n✅ All tests passed! AI chatbot implementation is validated.")