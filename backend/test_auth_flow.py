"""
Test script for user registration and login flow with specific scenarios
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"

def test_registration_flow():
    """Test registration with valid credentials succeeds"""
    print("Testing registration with valid credentials...")

    # Register a new user
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

    if response.status_code == 200 or response.status_code == 201:
        print("✅ Registration with valid credentials succeeds")
        return True
    else:
        print(f"❌ Registration failed with status {response.status_code}: {response.text}")
        return False


def test_login_flow():
    """Test login with valid credentials returns JWT token"""
    print("Testing login with valid credentials...")

    # Login with the registered user
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    if response.status_code == 200:
        token_data = response.json()
        if "access_token" in token_data:
            print("✅ Login with valid credentials returns JWT token")
            return token_data["access_token"]
        else:
            print("❌ Login response does not contain access token")
            return None
    else:
        print(f"❌ Login failed with status {response.status_code}: {response.text}")
        return None


def test_dashboard_access():
    """Test that authentication protects dashboard access"""
    print("Testing authentication protects dashboard access...")

    # Try to access tasks without authentication (should fail)
    response = requests.get(f"{BASE_URL}/users/me/tasks")

    if response.status_code == 401:
        print("✅ Authentication protects dashboard access (unauthorized access denied)")
        return True
    else:
        print(f"❌ Authentication does not protect dashboard access: {response.status_code}")
        return False


def run_auth_tests():
    """Run all authentication flow tests"""
    print("Running authentication flow tests...\n")

    results = []

    # Test registration
    results.append(test_registration_flow())

    # Test login
    token = test_login_flow()
    if token:
        results.append(True)

        # Test dashboard access with valid token
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me/tasks", headers=headers)
        if response.status_code == 200:
            print("✅ Authenticated access to dashboard succeeds")
            results.append(True)
        else:
            print(f"❌ Authenticated access to dashboard failed: {response.status_code}")
            results.append(False)
    else:
        results.append(False)

    # Test dashboard access without auth (should fail)
    results.append(test_dashboard_access())

    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\nAuthentication flow tests: {passed}/{total} passed")

    if passed == total:
        print("🎉 All authentication flow tests passed!")
        return True
    else:
        print("⚠️ Some authentication flow tests failed.")
        return False


if __name__ == "__main__":
    run_auth_tests()