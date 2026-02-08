import React, { useState } from 'react';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskUpdateDeleteProps {
  task: Task;
  onTaskUpdated: (updatedTask: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}

const TaskUpdateDelete: React.FC<TaskUpdateDeleteProps> = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [completed, setCompleted] = useState(task.completed);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate inputs according to requirements (title 1-200 chars, description <=1000 chars)
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length < 1 || title.length > 200) {
      setError('Title must be between 1 and 200 characters');
      return;
    }

    if (description.length > 1000) {
      setError('Description must be less than 1000 characters');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // In a real implementation, we would call the API
      // const updatedTask = await todoApi.updateTask(task.id, { title: title.trim(), description, completed });
      // onTaskUpdated(updatedTask);

      // For demo purposes, update the task locally
      const updatedTask = {
        ...task,
        title: title.trim(),
        description: description || undefined,
        completed,
        updated_at: new Date().toISOString()
      };

      onTaskUpdated(updatedTask);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onTaskDeleted(task.id);
    }
  };

  const handleToggleComplete = async () => {
    setLoading(true);
    setError(null);

    try {
      // In a real implementation, we would call the API
      // const updatedTask = await todoApi.toggleTaskCompletion(task.id, !task.completed);
      // onTaskUpdated(updatedTask);

      // For demo purposes, update the task locally
      const updatedTask = { ...task, completed: !task.completed, updated_at: new Date().toISOString() };
      onTaskUpdated(updatedTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task completion');
      console.error('Error updating task completion:', err);
    } finally {
      setLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="p-4 bg-blue-50 rounded-md mb-2">
        <form onSubmit={handleUpdate}>
          <div className="mb-3">
            <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              id="edit-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              maxLength={200}
              disabled={loading}
            />
            <p className="mt-1 text-xs text-gray-500">Title must be between 1 and 200 characters</p>
          </div>

          <div className="mb-3">
            <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="edit-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              rows={3}
              maxLength={1000}
              disabled={loading}
            />
            <p className="mt-1 text-xs text-gray-500">Maximum 1000 characters</p>
          </div>

          <div className="mb-3">
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                checked={completed}
                onChange={(e) => setCompleted(e.target.checked)}
                className="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                disabled={loading}
              />
              <span className="ml-2 text-sm text-gray-700">Completed</span>
            </label>
          </div>

          {error && (
            <div className="mb-3 p-2 bg-red-100 text-red-700 rounded-md text-sm">
              {error}
            </div>
          )}

          <div className="flex space-x-2">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Updating...' : 'Save'}
            </button>
            <button
              type="button"
              onClick={() => {
                setIsEditing(false);
                setTitle(task.title);
                setDescription(task.description || '');
                setCompleted(task.completed);
                setError(null);
              }}
              className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-between p-3 border border-gray-200 rounded-md bg-white shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center">
        <input
  type="checkbox"
  checked={completed}
  onChange={handleToggleComplete}
  aria-label={completed ? "Mark task as incomplete" : "Mark task as complete"}
  className="h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
  disabled={loading}
/>

        <div className="ml-3 min-w-0">
          <h3 className={`text-sm font-medium ${completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {title}
          </h3>
          {description && (
            <p className={`text-sm ${completed ? 'line-through text-gray-500' : 'text-gray-500'} mt-1`}>
              {description}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-1">
            Updated: {new Date(task.updated_at).toLocaleDateString()}
          </p>
        </div>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={() => setIsEditing(true)}
          className="text-sm font-medium text-indigo-600 hover:text-indigo-900"
          disabled={loading}
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="text-sm font-medium text-red-600 hover:text-red-900"
          disabled={loading}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskUpdateDelete;