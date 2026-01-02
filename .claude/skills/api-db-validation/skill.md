---
name: api-db-validation
description: Guides testing and validating APIs and database consistency to ensure reliability and correctness of system data.
---

# API Validation & DB Consistency

## Instructions
1. Test API endpoints for correct responses, status codes, and error handling.
2. Verify data returned by APIs matches database records.
3. Validate input/output data formats and enforce schema rules.
4. Perform automated and manual testing for edge cases.
5. Monitor and report inconsistencies between database and API responses.
6. Collaborate with Backend Developer and Database Manager Agents to resolve discrepancies.
7. Document test cases, results, and any issues found.
8. Ensure repeatable and maintainable testing procedures.

## Examples
- Testing a REST API endpoint with Python:
  ```python
  import requests

  response = requests.get("https://api.example.com/users/1")
  assert response.status_code == 200
  assert response.json()["username"] == "alina"
  ```

- Checking database consistency:
  ```python
  db_user = session.query(User).filter_by(id=1).first()
  api_user = response.json()
  assert db_user.username == api_user["username"]
  ```