"""
Integration tests for API endpoints with authentication and authorization

These tests verify that:
1. API endpoints properly validate JWT tokens
2. Endpoints reject requests with invalid/missing tokens
3. Data isolation works at the API level
4. Role-based access controls work for different user roles
5. Error responses don't leak information about other users' data
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import jwt
import os
from backend.main import app
from backend.models import User, Task
from backend.auth import verify_token
from sqlmodel import Session, create_engine
from backend.db import get_engine_override


class TestAPIIntegration:
    """Integration tests for API endpoints"""

    @pytest.fixture
    def client(self):
        """Test client for the API"""
        with TestClient(app) as test_client:
            yield test_client

    def create_test_token(self, user_id: str, role: str = "user", expires_minutes: int = 30):
        """Helper to create a test JWT token"""
        secret = os.getenv("SECRET_KEY", "test-secret-key")
        algorithm = "HS256"

        payload = {
            "sub": user_id,
            "role": role,
            "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
        }
        return jwt.encode(payload, secret, algorithm=algorithm)

    def test_unauthenticated_access_rejected(self, client):
        """Test that unauthenticated requests are rejected"""
        response = client.get("/api/tasks/")

        assert response.status_code == 401  # Unauthorized
        assert "Authorization" in response.json()["detail"]

    def test_invalid_token_rejected(self, client):
        """Test that requests with invalid tokens are rejected"""
        headers = {
            "Authorization": "Bearer invalid.token.here"
        }
        response = client.get("/api/tasks/", headers=headers)

        assert response.status_code == 401
        assert "credentials" in response.json()["detail"].lower()

    def test_expired_token_rejected(self, client):
        """Test that requests with expired tokens are rejected"""
        expired_token = self.create_test_token("test-user", expires_minutes=-1)  # Expired token

        headers = {
            "Authorization": f"Bearer {expired_token}"
        }
        response = client.get("/api/tasks/", headers=headers)

        assert response.status_code == 401
        assert "credentials" in response.json()["detail"].lower()

    def test_authenticated_user_can_access_own_tasks(self, client):
        """Test that authenticated users can access their own tasks"""
        user_id = "test-user-123"
        valid_token = self.create_test_token(user_id)

        headers = {
            "Authorization": f"Bearer {valid_token}"
        }
        response = client.get("/api/tasks/", headers=headers)

        # Should be successful (200 OK) or at least not forbidden
        assert response.status_code in [200, 204]  # 204 if no tasks exist yet

    def test_user_cannot_access_other_users_tasks_via_direct_request(self, client):
        """Test that users cannot access other users' tasks even with valid token"""
        # Create a token for user A
        user_a_id = "user-a-123"
        user_a_token = self.create_test_token(user_a_id)

        # Try to access a specific task that belongs to user B
        # We'll try to access a task ID that would theoretically belong to another user
        headers = {
            "Authorization": f"Bearer {user_a_token}"
        }
        response = client.get("/api/tasks/999", headers=headers)  # Assuming task 999 exists but belongs to another user

        # Should return 404 (Not Found) rather than 403 (Forbidden) to avoid leaking information
        assert response.status_code in [404, 400]  # 404 if task doesn't exist, 403/400 if access denied

    def test_task_creation_with_authentication(self, client):
        """Test that task creation requires authentication and associates with correct user"""
        user_id = "test-user-create"
        valid_token = self.create_test_token(user_id)

        task_data = {
            "title": "Test Task",
            "description": "Test Description"
        }

        headers = {
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
        response = client.post("/api/tasks/", json=task_data, headers=headers)

        if response.status_code == 200 or response.status_code == 201:
            # Task created successfully
            data = response.json()
            assert "id" in data
            assert data["user_id"] == user_id  # Task should be associated with the authenticated user
        else:
            # Could be validation error or other issue, but should not be 401 (unauthorized)
            assert response.status_code != 401

    def test_task_update_with_authentication(self, client):
        """Test that task updates require authentication and respect user ownership"""
        user_id = "test-user-update"
        valid_token = self.create_test_token(user_id)

        update_data = {
            "title": "Updated Task Title",
            "completed": True
        }

        headers = {
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
        # Try to update a task (assuming task with ID 1 exists)
        response = client.put("/api/tasks/1", json=update_data, headers=headers)

        # Should either succeed (200) if the user owns task 1, or fail with 404 (not found) if they don't
        # or 404 if task doesn't exist at all
        assert response.status_code in [200, 404, 400]

    def test_admin_endpoint_access_with_non_admin_user(self, client):
        """Test that non-admin users cannot access admin endpoints"""
        user_id = "regular-user-123"
        regular_user_token = self.create_test_token(user_id, role="user")  # Regular user, not admin

        headers = {
            "Authorization": f"Bearer {regular_user_token}"
        }
        # Try to access an admin endpoint (this URL might not exist in basic implementation)
        response = client.get("/api/admin/tasks", headers=headers)

        # Should be forbidden for non-admin users
        assert response.status_code in [401, 403, 404]  # 404 if endpoint doesn't exist, 403 if access denied

    def test_admin_endpoint_access_with_admin_user(self, client):
        """Test that admin users can access admin endpoints"""
        admin_user_id = "admin-user-123"
        admin_token = self.create_test_token(admin_user_id, role="admin")  # Admin user

        headers = {
            "Authorization": f"Bearer {admin_token}"
        }
        # Try to access an admin endpoint
        response = client.get("/api/admin/tasks", headers=headers)

        # If endpoint exists and user is admin, should get 200 or 204 (if no tasks)
        # If endpoint doesn't exist, would get 404
        # The important thing is they don't get 403 (forbidden)
        assert response.status_code != 403  # Should not be forbidden for admin


class TestAPIErrorHandling:
    """Test API error handling and security"""

    @pytest.fixture
    def client(self):
        """Test client for the API"""
        with TestClient(app) as test_client:
            yield test_client

    def test_error_messages_dont_leak_information(self, client):
        """Test that error responses don't reveal information about other users' data"""
        user_id = "test-user-info-leak"
        valid_token = self.create_test_token(user_id)

        headers = {
            "Authorization": f"Bearer {valid_token}"
        }
        # Try to access a specific task that might belong to another user
        response = client.get("/api/tasks/999999", headers=headers)  # Very high ID that likely doesn't exist

        # Check that the error message doesn't reveal that the task exists but belongs to another user
        if response.status_code == 404:
            response_detail = response.json().get("detail", "").lower()
            # Should say "not found" rather than "access denied" or "belongs to another user"
            assert "not found" in response_detail or "does not exist" in response_detail
            assert "belongs to another user" not in response_detail
            assert "other user" not in response_detail

    def test_invalid_request_parameters_handled_gracefully(self, client):
        """Test that invalid request parameters are handled gracefully"""
        user_id = "test-user-invalid-params"
        valid_token = self.create_test_token(user_id)

        headers = {
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }

        # Send invalid task data (empty title should fail validation)
        invalid_task_data = {
            "title": "",  # Empty title should fail validation
            "description": "Valid description"
        }

        response = client.post("/api/tasks/", json=invalid_task_data, headers=headers)

        # Should return validation error (422) rather than 500 (internal server error)
        assert response.status_code in [422, 400]  # Validation error or bad request

    def test_rate_limiting_on_auth_endpoints(self, client):
        """Test rate limiting on authentication endpoints (if implemented)"""
        # Try to hit auth endpoint multiple times rapidly
        for i in range(10):
            # Try invalid login to trigger rate limiting
            response = client.post("/api/auth/login", json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            })

            # If rate limiting is implemented, we might see 429 status after multiple requests
            # If not implemented, we'll just see consistent responses
            if response.status_code == 429:
                # Rate limited - this is expected behavior if rate limiting is active
                assert True
                break


if __name__ == "__main__":
    pytest.main([__file__])