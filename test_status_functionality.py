#!/usr/bin/env python3
"""
Test script specifically for status completion functionality.
"""

from src.todo_app import TodoManager


def test_status_functionality():
    """Test the status completion functionality specifically."""
    print("Testing status completion functionality...")

    # Create a todo manager
    todo_manager = TodoManager()

    # Add a task
    task = todo_manager.add_task("Test Task", "Test Description")
    print(f"Added task: ID={task.task_id}, Title='{task.title}', Completed={task.completed}")

    # Verify it starts as incomplete
    assert task.completed == False, f"Expected task to start as incomplete, but got {task.completed}"
    print("PASS: Task starts as incomplete")

    # Mark as complete
    result = todo_manager.mark_complete(task.task_id, True)
    print(f"Mark complete result: {result}")

    # Verify it's now complete
    updated_task = todo_manager.get_task(task.task_id)
    assert updated_task.completed == True, f"Expected task to be complete, but got {updated_task.completed}"
    print(f"✓ Task marked as complete: Completed={updated_task.completed}")

    # Mark as incomplete
    result = todo_manager.mark_complete(task.task_id, False)
    print(f"Mark incomplete result: {result}")

    # Verify it's now incomplete
    updated_task = todo_manager.get_task(task.task_id)
    assert updated_task.completed == False, f"Expected task to be incomplete, but got {updated_task.completed}"
    print(f"✓ Task marked as incomplete: Completed={updated_task.completed}")

    # Test the shorthand methods (without specifying True/False)
    # Mark as complete using default (should be True)
    result = todo_manager.mark_complete(task.task_id)
    updated_task = todo_manager.get_task(task.task_id)
    assert updated_task.completed == True, f"Expected task to be complete using default, but got {updated_task.completed}"
    print(f"✓ Task marked as complete using default: Completed={updated_task.completed}")

    print("\nAll status functionality tests passed!")


def test_edge_cases():
    """Test edge cases for status functionality."""
    print("\nTesting edge cases...")

    todo_manager = TodoManager()

    # Try to mark a non-existent task
    result = todo_manager.mark_complete(999, True)
    assert result == False, f"Expected False for non-existent task, but got {result}"
    print("✓ Properly handles non-existent task IDs")

    # Add a task and test toggling
    task = todo_manager.add_task("Toggle Test", "Testing toggle functionality")
    original_status = task.completed
    print(f"Original status: {original_status}")

    # Toggle multiple times
    for i, status in enumerate([True, False, True, False]):
        todo_manager.mark_complete(task.task_id, status)
        updated_task = todo_manager.get_task(task.task_id)
        assert updated_task.completed == status, f"Iteration {i}: Expected {status}, got {updated_task.completed}"
        print(f"✓ Set status to {status} successfully")


if __name__ == "__main__":
    print("Testing status completion functionality...\n")

    try:
        test_status_functionality()
        test_edge_cases()
        print("\n🎉 All status functionality tests passed!")
    except Exception as e:
        print(f"\n❌ Status functionality test failed: {e}")
        import traceback
        traceback.print_exc()