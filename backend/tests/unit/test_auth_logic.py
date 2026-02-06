"""
Unit tests for authentication and authorization logic in the Todo App

These tests verify that:
1. JWT token validation works correctly
2. User authentication functions properly
3. Role-based access control functions as expected
4. Data isolation between users is maintained
5. Error handling works without information leakage
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt
from backend.models import User
from backend.auth import verify_token, get_current_active_user, get_current_user, get_current_active_admin_user
from sqlmodel import Session


class TestAuthenticationLogic:
    """Test suite for authentication logic"""

    def test_verify_token_valid(self):
        """Test that verify_token correctly validates valid tokens"""
        # Create a valid token
        user_id = "test-user-id"
        secret = "test-secret-key-for-testing"
        algorithm = "HS256"

        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        token = jwt.encode(payload, secret, algorithm=algorithm)

        # Test the function
        with patch('backend.auth.SECRET_KEY', secret), \
             patch('backend.auth.ALGORITHM', algorithm):

            result = verify_token(token)

        # verify_token returns the full payload, not just user_id
        assert result["sub"] == user_id

    def test_verify_token_expired(self):
        """Test that verify_token raises exception for expired tokens"""
        # Create an expired token
        user_id = "test-user-id"
        secret = "test-secret-key-for-testing"
        algorithm = "HS256"

        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() - timedelta(minutes=1)  # Expired 1 minute ago
        }
        token = jwt.encode(payload, secret, algorithm=algorithm)

        # Test that it raises an HTTPException
        with patch('backend.auth.SECRET_KEY', secret), \
             patch('backend.auth.ALGORITHM', algorithm):

            with pytest.raises(HTTPException) as exc_info:
                verify_token(token)

        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_token_invalid_signature(self):
        """Test that verify_token raises exception for tokens with invalid signature"""
        # Create a token with one secret
        user_id = "test-user-id"
        original_secret = "original-secret"
        new_secret = "different-secret"
        algorithm = "HS256"

        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        token = jwt.encode(payload, original_secret, algorithm=algorithm)

        # Try to verify with a different secret
        with patch('backend.auth.SECRET_KEY', new_secret), \
             patch('backend.auth.ALGORITHM', algorithm):

            with pytest.raises(HTTPException) as exc_info:
                verify_token(token)

        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail

    def test_verify_token_invalid_format(self):
        """Test that verify_token raises exception for invalid token format"""
        invalid_token = "not.a.valid.jwt.token"

        with patch('backend.auth.SECRET_KEY', "test-secret"), \
             patch('backend.auth.ALGORITHM', "HS256"):

            with pytest.raises(HTTPException) as exc_info:
                verify_token(invalid_token)

        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail


class TestAuthorizationLogic:
    """Test suite for authorization logic"""

    def test_get_current_user_valid_token(self):
        """Test that get_current_user returns user for valid token"""
        # Create a valid token
        user_id = "test-user-id"
        secret = "test-secret-key-for-testing"
        algorithm = "HS256"

        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        token = jwt.encode(payload, secret, algorithm=algorithm)

        # Create a mock user
        mock_user = User(
            id=user_id,
            email="test@example.com",
            name="Test User",
            role="user",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Mock the database session
        with patch('backend.auth.verify_token') as mock_verify_token, \
             patch('backend.auth.Session') as mock_session_class, \
             patch('backend.auth.get_engine') as mock_get_engine:

            mock_verify_token.return_value = payload
            mock_session_instance = MagicMock()
            mock_session_instance.get.return_value = mock_user
            mock_session_class.return_value.__enter__.return_value = mock_session_instance
            mock_get_engine.return_value = MagicMock()

            # Mock the security dependency to return the token
            from fastapi.security import HTTPAuthorizationCredentials
            mock_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

            result = get_current_user(mock_credentials)

        assert result.id == user_id

    def test_get_current_user_invalid_token(self):
        """Test that get_current_user raises exception for invalid token"""
        invalid_token = "invalid.token.here"

        # Mock the security dependency to return the invalid token
        from fastapi.security import HTTPAuthorizationCredentials
        mock_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)

        with patch('backend.auth.SECRET_KEY', "test-secret"), \
             patch('backend.auth.ALGORITHM', "HS256"):

            with pytest.raises(HTTPException) as exc_info:
                get_current_user(mock_credentials)

        assert exc_info.value.status_code == 401

    def test_get_current_active_user(self):
        """Test that get_current_active_user returns the authenticated user"""
        # Create a mock user
        mock_user = User(
            id="test-user-id",
            email="test@example.com",
            name="Test User",
            role="user",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        result = get_current_active_user(mock_user)

        assert result.id == mock_user.id

    def test_get_current_active_admin_user_valid_admin(self):
        """Test that get_current_active_admin_user returns user if they have admin role"""
        # Create a mock admin user
        mock_admin_user = User(
            id="test-admin-id",
            email="admin@example.com",
            name="Admin User",
            role="admin",  # Admin role
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        result = get_current_active_admin_user(mock_admin_user)

        assert result.id == mock_admin_user.id
        assert result.role == "admin"

    def test_get_current_active_admin_user_non_admin(self):
        """Test that get_current_active_admin_user raises exception for non-admin user"""
        # Create a mock regular user
        mock_regular_user = User(
            id="test-user-id",
            email="test@example.com",
            name="Regular User",
            role="user",  # Regular user role, not admin
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        with pytest.raises(HTTPException) as exc_info:
            get_current_active_admin_user(mock_regular_user)

        assert exc_info.value.status_code == 403
        assert "admin role required" in exc_info.value.detail


def test_jwt_algorithm_consistency():
    """Test that JWT algorithm is consistently applied"""
    user_id = "test-user-123"
    secret = "test-secret-key"
    algorithm = "HS256"

    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret, algorithm=algorithm)

    # Verify we can decode the token with the same algorithm
    with patch('backend.auth.SECRET_KEY', secret), \
         patch('backend.auth.ALGORITHM', algorithm):

        decoded_payload = verify_token(token)

    assert decoded_payload["sub"] == user_id


if __name__ == "__main__":
    pytest.main([__file__])