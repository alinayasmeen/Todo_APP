"""
Test script to verify the create task feature implementation.
This tests the acceptance criteria from specs/features/task-crud.md
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models import TaskCreate, UserCreate
from sqlmodel import Session, select
from backend.db import get_engine
import uuid


def test_create_task_feature():
    """Test the create task feature implementation."""
    client = TestClient(app)
    
    print("Testing Create Task Feature...")
    
    # First, register a user
    print("\n0. Registering test user...")
    import time
    unique_email = f"test_{int(time.time())}@example.com"
    user_data = {
        "email": unique_email,
        "name": "Test User",
        "password": "securepassword123"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    print(f"Registration response status: {response.status_code}")
    
    if response.status_code == 200:
        registration_result = response.json()
        token = registration_result["access_token"]
        user_info = registration_result["user"]
        user_id = user_info["id"]
        print(f"✓ User registered successfully with ID: {user_id}")
    else:
        # If user already exists, try to log in with the default test user
        print("User might already exist, trying to log in...")
        login_data = {
            "email": "test@example.com",
            "password": "securepassword123"
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result["access_token"]
            user_info = login_result["user"]
            user_id = user_info["id"]
            print(f"✓ User logged in successfully with ID: {user_id}")
        else:
            print(f"✗ Failed to register or log in user. Status: {login_response.status_code}, Response: {login_response.json()}")
            return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Create a valid task with title and description
    print("\n1. Testing valid task creation...")
    task_data = {
        "title": "Test Task",
        "description": "This is a test task description"
    }
    
    response = client.post("/api/tasks/", json=task_data, headers=headers)
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response data: {response.json()}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task description"
    assert data["completed"] == False
    assert data["user_id"] == user_id
    print("✓ Valid task creation works")
    
    # Test 2: Create a task with only title (description optional)
    print("\n2. Testing task creation with only title...")
    task_data_minimal = {
        "title": "Minimal Task"
    }
    
    response = client.post("/api/tasks/", json=task_data_minimal, headers=headers)
    print(f"Response status: {response.status_code}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert "id" in data
    assert data["title"] == "Minimal Task"
    assert data["description"] is None
    assert data["user_id"] == user_id
    print("✓ Task creation with only title works")
    
    # Test 3: Title length validation (1-200 characters)
    print("\n3. Testing title length validation...")
    
    # Test with empty title (should fail)
    task_data_empty = {
        "title": "",
        "description": "Description for empty title test"
    }
    
    response = client.post("/api/tasks/", json=task_data_empty, headers=headers)
    print(f"Empty title response status: {response.status_code}")
    assert response.status_code in [422, 400], f"Expected validation error, got {response.status_code}: {response.text}"
    print("✓ Empty title validation works")
    
    # Test with long title (should fail if > 200 chars)
    long_title = "a" * 201
    task_data_long = {
        "title": long_title,
        "description": "Description for long title test"
    }
    
    response = client.post("/api/tasks/", json=task_data_long, headers=headers)
    print(f"Long title response status: {response.status_code}")
    assert response.status_code in [422, 400], f"Expected validation error for long title, got {response.status_code}: {response.text}"
    print("✓ Long title validation works")
    
    # Test 4: Description length validation (max 1000 characters)
    print("\n4. Testing description length validation...")
    
    long_description = "a" * 1001  # More than 1000 chars
    task_data_long_desc = {
        "title": "Task with long description",
        "description": long_description
    }
    
    response = client.post("/api/tasks/", json=task_data_long_desc, headers=headers)
    print(f"Long description response status: {response.status_code}")
    assert response.status_code in [422, 400], f"Expected validation error for long description, got {response.status_code}: {response.text}"
    print("✓ Long description validation works")
    
    # Test 5: Task is associated with logged-in user
    print("\n5. Testing user association...")
    task_data_user_assoc = {
        "title": "User Association Test",
        "description": "Task should be associated with the logged-in user"
    }
    
    response = client.post("/api/tasks/", json=task_data_user_assoc, headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert data["user_id"] == user_id, f"Task should be associated with user {user_id}, but got {data['user_id']}"
    print("✓ Task is properly associated with logged-in user")
    
    print("\n✅ All create task feature tests passed!")
    print("\nSummary of implemented features:")
    print("- Title is required (1-200 characters) ✓")
    print("- Description is optional (max 1000 characters) ✓")
    print("- Task is associated with logged-in user ✓")
    print("- Proper validation and error handling ✓")


if __name__ == "__main__":
    test_create_task_feature()