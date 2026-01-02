#!/usr/bin/env python3
"""
Test script to verify all functionality of the Todo App.
This tests all required features without requiring interactive input.
"""

from src.todo_app import TodoManager, Task


def test_add_functionality():
    """Test adding tasks functionality."""
    print("Testing Add functionality...")
    todo_manager = TodoManager()

    # Test adding a task
    task = todo_manager.add_task("Test Task", "This is a test task")
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.completed == False
    assert task.task_id == 1
    print("PASS: Add functionality works correctly")


def test_list_functionality():
    """Test listing tasks functionality."""
    print("Testing List functionality...")
    todo_manager = TodoManager()

    # Add some tasks
    todo_manager.add_task("Task 1", "First task")
    todo_manager.add_task("Task 2", "Second task")

    # List tasks
    tasks = todo_manager.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    print("PASS: List functionality works correctly")


def test_update_functionality():
    """Test updating tasks functionality."""
    print("Testing Update functionality...")
    todo_manager = TodoManager()

    # Add a task
    task = todo_manager.add_task("Original Task", "Original description")
    original_id = task.task_id

    # Update the task
    success = todo_manager.update_task(original_id, "Updated Task", "Updated description")
    assert success == True

    # Verify the update
    updated_task = todo_manager.get_task(original_id)
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated description"
    print("PASS: Update functionality works correctly")


def test_delete_functionality():
    """Test deleting tasks functionality."""
    print("Testing Delete functionality...")
    todo_manager = TodoManager()

    # Add a task
    task = todo_manager.add_task("Task to Delete", "Description")
    task_id = task.task_id

    # Verify it exists
    assert todo_manager.get_task(task_id) is not None

    # Delete the task
    success = todo_manager.delete_task(task_id)
    assert success == True

    # Verify it's gone
    assert todo_manager.get_task(task_id) is None

    print("PASS: Delete functionality works correctly")


def test_mark_complete_functionality():
    """Test marking tasks as complete/incomplete functionality."""
    print("Testing Mark Complete/Incomplete functionality...")
    todo_manager = TodoManager()

    # Add a task
    task = todo_manager.add_task("Test Task", "Description")
    task_id = task.task_id

    # Verify it starts as incomplete
    assert todo_manager.get_task(task_id).completed == False

    # Mark as complete
    success = todo_manager.mark_complete(task_id, True)
    assert success == True
    assert todo_manager.get_task(task_id).completed == True

    # Mark as incomplete
    success = todo_manager.mark_complete(task_id, False)
    assert success == True
    assert todo_manager.get_task(task_id).completed == False

    print("PASS: Mark Complete/Incomplete functionality works correctly")


def test_unique_ids():
    """Test that unique IDs are generated."""
    print("Testing unique ID generation...")
    todo_manager = TodoManager()

    # Add multiple tasks
    task1 = todo_manager.add_task("Task 1", "Description 1")
    task2 = todo_manager.add_task("Task 2", "Description 2")
    task3 = todo_manager.add_task("Task 3", "Description 3")

    # Verify unique IDs
    ids = [task1.task_id, task2.task_id, task3.task_id]
    assert len(ids) == len(set(ids))  # All IDs should be unique
    assert ids == [1, 2, 3]  # Should be sequential starting from 1

    print("PASS: Unique ID generation works correctly")


def main():
    """Run all tests."""
    print("Running functionality tests for Todo App...\n")

    try:
        test_add_functionality()
        test_list_functionality()
        test_update_functionality()
        test_delete_functionality()
        test_mark_complete_functionality()
        test_unique_ids()

        print("\nALL TESTS PASSED!")
        print("PASS: Add Task - Implemented and working")
        print("PASS: List Tasks - Implemented and working")
        print("PASS: Update Task - Implemented and working")
        print("PASS: Delete Task - Implemented and working")
        print("PASS: Mark Complete/Incomplete - Implemented and working")
        print("PASS: Unique ID Generation - Implemented and working")

    except AssertionError as e:
        print(f"\nERROR: Test failed: {e}")
        return False
    except Exception as e:
        print(f"\nERROR: Error during testing: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\nSUCCESS: All required features for Phase I are implemented correctly!")
    else:
        print("\n❌ Some features need to be fixed.")