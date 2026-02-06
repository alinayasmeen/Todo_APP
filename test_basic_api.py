"""
Basic tests to verify the Todo App API functionality.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo App API"}

def test_docs_endpoint():
    """Test the API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_routes_exist():
    """Test that the main route prefixes exist."""
    # Test that auth routes are available
    auth_response = client.get("/api/auth")
    # This should return 422 (validation error) rather than 404 (not found)
    assert auth_response.status_code != 404

    # Test that tasks routes are available
    tasks_response = client.get("/api/tasks")
    # This should return 401 (unauthorized) rather than 404 (not found)
    assert tasks_response.status_code != 404