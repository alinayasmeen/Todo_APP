import React, { useState, useEffect } from 'react';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  onTaskUpdated: () => void;
}

const TaskList: React.FC<TaskListProps> = ({ onTaskUpdated }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'created' | 'title'>('created');

  useEffect(() => {
    loadTasks();
  }, [filter, sortBy]);

  const loadTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      // In a real implementation, we would fetch from the API
      // const response = await todoApi.getTasks(filter, sortBy);
      // setTasks(response);

      // Mock data for demonstration
      const mockTasks: Task[] = [
        {
          id: 1,
          user_id: 'user123',
          title: 'Sample Task 1',
          description: 'This is a sample task description',
          completed: false,
          created_at: '2026-01-25T10:00:00Z',
          updated_at: '2026-01-25T10:00:00Z'
        },
        {
          id: 2,
          user_id: 'user123',
          title: 'Sample Task 2',
          description: 'Another sample task',
          completed: true,
          created_at: '2026-01-25T09:00:00Z',
          updated_at: '2026-01-25T09:30:00Z'
        }
      ];

      // Apply filter
      let filteredTasks = mockTasks;
      if (filter === 'pending') {
        filteredTasks = mockTasks.filter(task => !task.completed);
      } else if (filter === 'completed') {
        filteredTasks = mockTasks.filter(task => task.completed);
      }

      // Apply sort
      const sortedTasks = [...filteredTasks].sort((a, b) => {
        if (sortBy === 'title') {
          return a.title.localeCompare(b.title);
        } else { // created date
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        }
      });

      setTasks(sortedTasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    try {
      // In a real implementation, we would call the API
      // await todoApi.toggleTaskCompletion(taskId);
      console.log(`Toggling completion for task ${taskId}`);

      // Update local state
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      );

      onTaskUpdated(); // Notify parent component that task was updated
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
      console.error('Error toggling task completion:', err);
    }
  };

  const deleteTask = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      // In a real implementation, we would call the API
      // await todoApi.deleteTask(taskId);
      console.log(`Deleting task ${taskId}`);

      // Update local state
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));

      onTaskUpdated(); // Notify parent component that task was deleted
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center">
        <h2 className="text-xl font-semibold">My Tasks</h2>
        <div className="flex space-x-4">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as 'all' | 'pending' | 'completed')}
            aria-label="Filter tasks by"
            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="all">All Tasks</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'created' | 'title')}
            aria-label="Sort tasks by"
            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="created">Sort by Date</option>
            <option value="title">Sort by Title</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 p-4">
          {error}
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="p-8 text-center text-gray-500">
          No tasks found. Create your first task!
        </div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {tasks.map((task) => (
            <li key={task.id} className="p-4 hover:bg-gray-50">
              <div className="flex items-start">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTaskCompletion(task.id)}
                  className="h-5 w-5 text-indigo-600 rounded mt-1 focus:ring-indigo-500"
                />
                <div className="ml-3 flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {task.title}
                    </h3>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => deleteTask(task.id)}
                        className="text-red-600 hover:text-red-900 text-sm font-medium"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                  {task.description && (
                    <p className={`text-sm ${task.completed ? 'line-through text-gray-500' : 'text-gray-500'} mt-1`}>
                      {task.description}
                    </p>
                  )}
                  <p className="text-xs text-gray-400 mt-2">
                    Created: {new Date(task.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;