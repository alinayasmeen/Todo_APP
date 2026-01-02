---
name: better-auth
description: Guides implementing secure authentication and authorization for applications.
---

# Better Auth

## Instructions
1. Implement authentication mechanisms such as JWT, OAuth2, and multi-factor authentication.
2. Design and enforce role-based access control (RBAC) or permission systems.
3. Secure password storage using hashing and salting techniques.
4. Integrate authentication with backend services and APIs.
5. Monitor and log authentication attempts and suspicious activities.
6. Ensure session management is secure and efficient.
7. Document authentication workflows, endpoints, and security practices.
8. Follow best practices to protect against vulnerabilities such as XSS, CSRF, and brute-force attacks.

## Examples
- Creating a JWT token:
  ```python
  import jwt
  token = jwt.encode({"user_id":1}, "SECRET_KEY", algorithm="HS256")
  ```

- Verifying a JWT token:
  ```python
  payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
  user_id = payload["user_id"]
  ```

- Implementing RBAC:
  ```python
  roles = {"admin": ["read", "write", "delete"], "user": ["read"]}
  ```