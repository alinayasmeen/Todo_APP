/**
 * Dashboard Page
 *
 * This page serves as the main dashboard for authenticated users.
 * It displays their tasks and provides controls for managing them.
 */
import React, { useState, useEffect } from 'react';
import { tasksAPI } from '../lib/api';
import { signOut } from '../lib/auth';
import { useRouter } from 'next/router';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  ai_category?: string;
  ai_priority_score?: number;
  ai_estimated_duration?: number;
  ai_suggested_tags?: string;
  ai_processing_metadata?: string;
}

const Dashboard: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  // Load tasks when component mounts
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await tasksAPI.getAll();
      setTasks(tasksData);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const createdTask = await tasksAPI.create(newTask);
      setTasks([createdTask, ...tasks]);
      setNewTask({ title: '', description: '' });
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    try {
      // Update the task in the local state optimistically
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));

      // Update on server
      const updatedTask = await tasksAPI.toggleComplete(taskId);

      // In case the server response differs, update with actual server data
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      // Revert the optimistic update if the API call fails
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      await tasksAPI.delete(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    }
  };

  const handleLogout = async () => {
    await signOut();
    router.push('/');
  };

  if (loading) return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-pastel-blue"></div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-pastel-lavender to-pastel-green py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 bg-clip-text text-transparent bg-gradient-to-r from-pastel-blue to-pastel-purple">
            Task Dashboard
          </h1>
          <button
            onClick={handleLogout}
            className="bg-pastel-pink hover:bg-pink-300 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
          >
            Logout
          </button>
        </div>

        {error && (
          <div className="bg-pastel-pink text-red-800 p-3 rounded-lg mb-4 text-center animate-fade-in">
            {error}
          </div>
        )}

        {/* Task Creation Form */}
        <form onSubmit={handleCreateTask} className="bg-white bg-opacity-80 backdrop-blur-sm p-6 rounded-xl shadow-md mb-8 border border-pastel-green animate-slide-up">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Create New Task</h2>
          <div className="mb-4">
            <input
              type="text"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
              placeholder="Task title"
              required
              className="w-full p-3 border border-pastel-gray rounded-lg focus:outline-none focus:ring-2 focus:ring-pastel-blue focus:border-transparent"
            />
          </div>
          <div className="mb-4">
            <textarea
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              placeholder="Task description (optional)"
              rows={3}
              className="w-full p-3 border border-pastel-gray rounded-lg focus:outline-none focus:ring-2 focus:ring-pastel-blue focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            className="bg-pastel-blue hover:bg-blue-300 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
          >
            Add Task
          </button>
        </form>

        {/* Task List */}
        <div className="bg-white bg-opacity-80 backdrop-blur-sm p-6 rounded-xl shadow-md border border-pastel-blue animate-slide-up">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks ({tasks.length})</h2>

          {tasks.length === 0 ? (
            <div className="text-center py-8">
              <div className="text-5xl mb-4 text-pastel-blue">📋</div>
              <p className="text-gray-600">No tasks yet. Create your first task above!</p>
            </div>
          ) : (
            <ul className="space-y-4">
              {tasks.map((task) => (
                <li
                  key={task.id}
                  className={`flex flex-col sm:flex-row justify-between items-start p-4 rounded-lg border ${
                    task.completed
                      ? 'bg-pastel-lavender bg-opacity-50 border-pastel-gray'
                      : 'bg-white border-pastel-blue'
                  } animate-slide-up`}
                >
                  <div className="flex-1 mb-4 sm:mb-0">
                    <div className="flex items-center">
                      <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                        {task.title}
                      </h3>
                      {task.completed && (
                        <span className="ml-2 bg-pastel-green text-white text-xs px-2 py-1 rounded-full">Completed</span>
                      )}
                    </div>
                    {task.description && <p className="text-gray-600 mt-1">{task.description}</p>}

                    <div className="flex flex-wrap gap-2 mt-3">
                      {task.ai_category && (
                        <span className="bg-pastel-yellow text-gray-800 text-xs px-2 py-1 rounded-full">
                          Category: {task.ai_category}
                        </span>
                      )}
                      {task.ai_priority_score && (
                        <span className="bg-pastel-orange text-gray-800 text-xs px-2 py-1 rounded-full">
                          Priority: {(task.ai_priority_score * 100).toFixed(0)}%
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => toggleTaskCompletion(task.id)}
                      className={`font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-md ${
                        task.completed
                          ? 'bg-pastel-green hover:bg-green-300 text-white'
                          : 'bg-pastel-blue hover:bg-blue-300 text-white'
                      }`}
                    >
                      {task.completed ? 'Undo' : 'Complete'}
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="bg-pastel-pink hover:bg-pink-300 text-red-800 font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-md"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;