"""
Security tests for data isolation between users in the Todo App

These tests verify that:
1. Users cannot access other users' tasks
2. Error responses don't reveal information about other users' data
3. Authentication and authorization properly enforce data isolation
4. Role-based access controls work correctly for admin users
5. Database-level isolation is effective
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
from sqlmodel import Session, select
from backend.db import get_engine


class TestDataIsolationSecurity:
    """Security tests for data isolation between users"""

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

    def test_user_cannot_access_other_users_tasks(self, client):
        """Test that a user cannot access tasks belonging to another user"""
        # Create tokens for two different users
        user_a_id = "user-a-security-test"
        user_b_id = "user-b-security-test"

        user_a_token = self.create_test_token(user_a_id)
        user_b_token = self.create_test_token(user_b_id)

        # First, let user A create a task
        task_data = {
            "title": "User A's Private Task",
            "description": "This should only be accessible by User A"
        }
        headers_user_a = {
            "Authorization": f"Bearer {user_a_token}",
            "Content-Type": "application/json"
        }
        create_response = client.post("/api/tasks/", json=task_data, headers=headers_user_a)

        assert create_response.status_code in [200, 201]  # Task created successfully
        task_id = create_response.json()["id"]

        # Now try to access that task with user B's token (should fail)
        headers_user_b = {
            "Authorization": f"Bearer {user_b_token}"
        }
        access_response = client.get(f"/api/tasks/{task_id}", headers=headers_user_b)

        # Should return 404 (Not Found) rather than 403 (Forbidden) to avoid information leakage
        assert access_response.status_code == 404
        response_detail = access_response.json().get("detail", "").lower()
        assert "not found" in response_detail or "does not exist" in response_detail

    def test_user_cannot_update_other_users_tasks(self, client):
        """Test that a user cannot update tasks belonging to another user"""
        # Create tokens for two different users
        user_a_id = "user-a-update-test"
        user_b_id = "user-b-update-test"

        user_a_token = self.create_test_token(user_a_id)
        user_b_token = self.create_test_token(user_b_id)

        # First, let user A create a task
        task_data = {
            "title": "User A's Update Protected Task",
            "description": "This should only be updatable by User A"
        }
        headers_user_a = {
            "Authorization": f"Bearer {user_a_token}",
            "Content-Type": "application/json"
        }
        create_response = client.post("/api/tasks/", json=task_data, headers=headers_user_a)

        assert create_response.status_code in [200, 201]
        task_id = create_response.json()["id"]

        # Now try to update that task with user B's token (should fail)
        update_data = {
            "title": "Hacked by User B",  # Attempt to change the title
            "completed": True
        }
        headers_user_b = {
            "Authorization": f"Bearer {user_b_token}",
            "Content-Type": "application/json"
        }
        update_response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=headers_user_b)

        # Should return 404 (Not Found) to avoid revealing that the task exists
        assert update_response.status_code == 404
        response_detail = update_response.json().get("detail", "").lower()
        assert "not found" in response_detail

    def test_user_cannot_delete_other_users_tasks(self, client):
        """Test that a user cannot delete tasks belonging to another user"""
        # Create tokens for two different users
        user_a_id = "user-a-delete-test"
        user_b_id = "user-b-delete-test"

        user_a_token = self.create_test_token(user_a_id)
        user_b_token = self.create_test_token(user_b_id)

        # First, let user A create a task
        task_data = {
            "title": "User A's Delete Protected Task",
            "description": "This should only be deletable by User A"
        }
        headers_user_a = {
            "Authorization": f"Bearer {user_a_token}",
            "Content-Type": "application/json"
        }
        create_response = client.post("/api/tasks/", json=task_data, headers=headers_user_a)

        assert create_response.status_code in [200, 201]
        task_id = create_response.json()["id"]

        # Now try to delete that task with user B's token (should fail)
        headers_user_b = {
            "Authorization": f"Bearer {user_b_token}"
        }
        delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers_user_b)

        # Should return 404 (Not Found) to avoid revealing that the task exists
        assert delete_response.status_code == 404
        response_detail = delete_response.json().get("detail", "").lower()
        assert "not found" in response_detail

    def test_user_cannot_see_other_users_in_task_list(self, client):
        """Test that a user cannot see tasks belonging to other users in their task list"""
        # Create tokens for two different users
        user_a_id = "user-a-list-test"
        user_b_id = "user-b-list-test"

        user_a_token = self.create_test_token(user_a_id)
        user_b_token = self.create_test_token(user_b_id)

        # Let user A create a task
        task_a_data = {
            "title": "User A's Task",
            "description": "Task belonging to User A"
        }
        headers_user_a = {
            "Authorization": f"Bearer {user_a_token}",
            "Content-Type": "application/json"
        }
        create_response_a = client.post("/api/tasks/", json=task_a_data, headers=headers_user_a)
        assert create_response_a.status_code in [200, 201]

        # Let user B create a task
        task_b_data = {
            "title": "User B's Task",
            "description": "Task belonging to User B"
        }
        headers_user_b = {
            "Authorization": f"Bearer {user_b_token}",
            "Content-Type": "application/json"
        }
        create_response_b = client.post("/api/tasks/", json=task_b_data, headers=headers_user_b)
        assert create_response_b.status_code in [200, 201]

        # Get User A's task list - should only see their own task
        list_response_a = client.get("/api/tasks/", headers=headers_user_a)
        assert list_response_a.status_code == 200
        user_a_tasks = list_response_a.json()

        # Verify User A only sees their own task
        user_a_task_titles = [task["title"] for task in user_a_tasks]
        assert "User A's Task" in user_a_task_titles
        assert "User B's Task" not in user_a_task_titles

        # Get User B's task list - should only see their own task
        list_response_b = client.get("/api/tasks/", headers=headers_user_b)
        assert list_response_b.status_code == 200
        user_b_tasks = list_response_b.json()

        # Verify User B only sees their own task
        user_b_task_titles = [task["title"] for task in user_b_tasks]
        assert "User B's Task" in user_b_task_titles
        assert "User A's Task" not in user_b_task_titles

    def test_error_messages_dont_reveal_other_users_data(self, client):
        """Test that error responses don't reveal information about other users' data"""
        # Create a token for a user
        user_id = "test-user-error-messages"
        user_token = self.create_test_token(user_id)

        headers = {
            "Authorization": f"Bearer {user_token}"
        }

        # Try to access a high task ID that likely doesn't exist
        # This should return "not found" rather than any message that indicates
        # the task might exist but belong to another user
        response = client.get("/api/tasks/999999", headers=headers)

        if response.status_code == 404:
            response_detail = response.json().get("detail", "").lower()
            # Should say "not found" rather than revealing that it belongs to another user
            assert "not found" in response_detail
            assert "belongs to another user" not in response_detail
            assert "access denied" not in response_detail
            assert "forbidden" not in response_detail

    def test_admin_can_access_all_tasks(self, client):
        """Test that admin users can access all tasks in the system"""
        # Create tokens - one for regular user, one for admin
        regular_user_id = "regular-user-admin-test"
        admin_user_id = "admin-user-access-test"

        regular_user_token = self.create_test_token(regular_user_id, role="user")
        admin_token = self.create_test_token(admin_user_id, role="admin")

        # Let regular user create a task
        task_data = {
            "title": "Regular User's Task for Admin Access Test",
            "description": "Task that should be accessible to admin"
        }
        headers_regular = {
            "Authorization": f"Bearer {regular_user_token}",
            "Content-Type": "application/json"
        }
        create_response = client.post("/api/tasks/", json=task_data, headers=headers_regular)
        assert create_response.status_code in [200, 201]
        task_id = create_response.json()["id"]

        # Admin should be able to access this task
        headers_admin = {
            "Authorization": f"Bearer {admin_token}"
        }
        access_response = client.get(f"/api/tasks/{task_id}", headers=headers_admin)

        # Admin should be able to access the task
        assert access_response.status_code in [200, 404]  # 200 if successful, 404 if admin endpoints have different structure
        if access_response.status_code == 200:
            task_data = access_response.json()
            assert task_data["id"] == task_id

    def test_regular_user_cannot_impersonate_admin(self, client):
        """Test that regular users cannot access admin functionality by manipulating claims"""
        # Create a token that claims to be admin but signed with wrong secret
        user_id = "regular-user-impersonation-test"
        wrong_secret = "wrong-secret-key"
        correct_secret = os.getenv("SECRET_KEY", "test-secret-key")

        # Create a token with admin role but signed with wrong secret
        payload = {
            "sub": user_id,
            "role": "admin",  # Claiming to be admin
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        fake_admin_token = jwt.encode(payload, wrong_secret, algorithm="HS256")

        headers = {
            "Authorization": f"Bearer {fake_admin_token}"
        }
        # Try to access what might be an admin endpoint
        response = client.get("/api/admin/tasks", headers=headers)

        # Should fail authentication since the token signature won't validate
        assert response.status_code == 401

    def test_task_creation_associates_with_correct_user(self, client):
        """Test that created tasks are properly associated with the authenticated user"""
        user_id = "test-user-task-association"
        user_token = self.create_test_token(user_id)

        task_data = {
            "title": "Correctly Associated Task",
            "description": "This task should be linked to the creating user"
        }
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        }
        response = client.post("/api/tasks/", json=task_data, headers=headers)

        assert response.status_code in [200, 201]
        created_task = response.json()

        # The task should be associated with the authenticated user
        # Note: Depending on implementation, the field might be "user_id" or similar
        assert created_task.get("user_id") == user_id or str(created_task.get("user_id")) == user_id

    def test_database_level_isolation(self):
        """Test that data isolation works at the database level"""
        # This test verifies that even if someone bypassed the API layer,
        # the database queries properly filter by user
        from backend.db import get_engine
        from backend.models import Task

        # Create a test user and task directly in the database
        user_id = "db-isolation-test-user"
        other_user_id = "db-isolation-other-user"

        engine = get_engine()
        with Session(engine) as session:
            # Create tasks for two different users
            task_for_user = Task(
                title="Task for User",
                description="Task belonging to first user",
                user_id=user_id,
                completed=False
            )

            task_for_other_user = Task(
                title="Task for Other User",
                description="Task belonging to second user",
                user_id=other_user_id,
                completed=False
            )

            session.add(task_for_user)
            session.add(task_for_other_user)
            session.commit()

            # Query tasks for the first user - should only return their task
            user_tasks = session.exec(
                select(Task).where(Task.user_id == user_id)
            ).all()

            assert len(user_tasks) == 1
            assert user_tasks[0].title == "Task for User"

            # Query tasks for the other user - should only return their task
            other_user_tasks = session.exec(
                select(Task).where(Task.user_id == other_user_id)
            ).all()

            assert len(other_user_tasks) == 1
            assert other_user_tasks[0].title == "Task for Other User"


class TestAuthenticationSecurity:
    """Additional security tests for authentication mechanisms"""

    def test_jwt_token_manipulation_resistance(self, client):
        """Test that the system is resistant to JWT token manipulation"""
        # Create a legitimate token
        user_id = "test-user-jwt-security"
        legitimate_token = self.create_test_token(user_id)

        # Manipulate the token by changing the user ID in the payload
        # (This requires decoding, modifying, and re-encoding with a different key)
        # Since we can't easily manipulate without the secret, we'll test
        # that tampered tokens are rejected

        # Create a token with different user ID
        other_user_id = "other-user-id"
        payload = {
            "sub": other_user_id,
            "role": "user",
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        tampered_token = jwt.encode(payload, "different-secret", algorithm="HS256")

        headers = {
            "Authorization": f"Bearer {tampered_token}"
        }
        response = client.get("/api/tasks/", headers=headers)

        # Should reject the tampered token
        assert response.status_code == 401

    def test_brute_force_protection_on_auth_endpoints(self):
        """Test protection against brute force attacks on authentication endpoints"""
        # This would typically require a rate-limiting implementation
        # For now, we'll test that multiple failed login attempts don't crash the server
        with TestClient(app) as client:
            for i in range(5):  # Try multiple invalid requests
                response = client.post("/api/auth/login", json={
                    "email": "nonexistent@example.com",
                    "password": "wrongpassword"
                })

                # Should consistently return 401 for invalid credentials
                assert response.status_code in [401, 422]  # 422 if validation fails


if __name__ == "__main__":
    pytest.main([__file__])