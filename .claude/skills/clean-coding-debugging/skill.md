---
name: clean-coding-debugging
description: Guides writing maintainable code and systematically debugging issues in applications.
---

# Clean Coding & Debugging

## Instructions
1. Write code that is readable, modular, and follows best practices.
2. Use descriptive names for variables, functions, and classes.
3. Implement consistent formatting, comments, and documentation.
4. Debug systematically using logs, breakpoints, and error messages.
5. Collaborate with other agents to trace and resolve issues.
6. Test fixes thoroughly to prevent regressions.
7. Maintain a repository of known bugs and solutions.
8. Optimize code performance while keeping readability.

## Examples
- Debugging a Python function:
  ```python
  def divide(a, b):
      try:
          return a / b
      except ZeroDivisionError:
          print("Cannot divide by zero")
          return None
  ```

- Refactoring code for readability:
  ```python
  # Before
  def calc(x,y): return x*y+10

  # After
  def calculate_total(price, quantity):
      return price * quantity + 10
  ```