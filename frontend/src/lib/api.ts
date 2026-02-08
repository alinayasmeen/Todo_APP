/**
 * API Client for Todo App
 *
 * This file provides functions to interact with the Todo App backend API.
 * It includes authentication and error handling.
 */
import { getAuthToken } from './auth';

// Base API URL from environment - when using rewrites, use relative paths
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';

// Generic function to make API requests
export const apiRequest = async (
  endpoint: string,
  options: RequestInit = {},
  includeAuth = true
): Promise<any> => {
  // Prepare the request options
  const requestOptions: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  // Construct the full URL
  const url = `${API_BASE_URL}${endpoint}`;

  // Add authentication header if required
  if (includeAuth) {
    const token = await getAuthToken();
    if (token) {
      requestOptions.headers = {
        ...requestOptions.headers,
        'Authorization': `Bearer ${token}`,
      };
    } else {
      console.error('Authentication required but no token available');
      throw new Error('Authentication required but no token available');
    }
  }

  // Make the API request
  const response = await fetch(url, requestOptions);

  // Handle different response statuses
  if (!response.ok) {
    // Try to get error details from response
    let errorMessage = `HTTP error! status: ${response.status}`;

    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (e) {
      // If response is not JSON, use status text
      errorMessage = response.statusText || errorMessage;
    }

    throw new Error(errorMessage);
  }

  // Return response data if available
  if (response.status !== 204) { // No content
    return response.json();
  }

  return {};
};

// Authentication API functions
export const authAPI = {
  // Register a new user
  register: async (userData: { email: string; password: string; name?: string }) => {
    // Remove auth requirement for registration
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      let errorMessage = `Registration failed: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  // Login a user
  login: async (credentials: { email: string; password: string }) => {
    // Remove auth requirement for login
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      let errorMessage = `Login failed: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }

    return response.json();
  },

  // Get user profile
  getProfile: () => apiRequest('/auth/profile', {}, true),

  // Refresh token
  refreshToken: () => apiRequest('/auth/refresh', { method: 'POST' }, true),
};

// Task API functions
export const tasksAPI = {
  // Get all tasks for the authenticated user
  getAll: (params?: { status?: string; sort?: string }) => {
    const queryParams = params ? new URLSearchParams(params).toString() : '';
    const queryString = queryParams ? `?${queryParams}` : '';
    return apiRequest(`/tasks${queryString}`, { method: 'GET' });
  },

  // Create a new task
  create: (taskData: { title: string; description?: string }) => {
    return apiRequest('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  // Get a specific task
  getById: (id: number) => apiRequest(`/tasks/${id}`, { method: 'GET' }),

  // Update a task
  update: (id: number, taskData: Partial<{ title: string; description?: string; completed?: boolean }>) => {
    return apiRequest(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  // Toggle task completion status
  toggleComplete: (id: number) => {
    return apiRequest(`/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  },

  // Delete a task
  delete: (id: number) => {
    return apiRequest(`/tasks/${id}`, {
      method: 'DELETE',
    });
  },

  // Get AI task suggestions
  getAISuggestions: () => {
    return apiRequest('/tasks/ai/suggestions', { method: 'GET' });
  },

  // Get AI productivity insights
  getAIInsights: () => {
    return apiRequest('/tasks/ai/insights', { method: 'GET' });
  },
};

// Admin API functions (require admin role)
export const adminAPI = {
  // Get all tasks in the system
  getAllTasks: (params?: { limit?: number; offset?: number; status?: string; user_id?: string }) => {
    if (params) {
      // Convert numeric values to strings for URLSearchParams
      const stringParams: Record<string, string> = {};
      if (params.limit !== undefined) stringParams.limit = String(params.limit);
      if (params.offset !== undefined) stringParams.offset = String(params.offset);
      if (params.status) stringParams.status = params.status;
      if (params.user_id) stringParams.user_id = params.user_id;

      const queryParams = new URLSearchParams(stringParams).toString();
      const queryString = queryParams ? `?${queryParams}` : '';
      return apiRequest(`/admin${queryString}`, { method: 'GET' });
    }
    return apiRequest('/admin', { method: 'GET' });
  },

  // Get tasks for a specific user
  getUserTasks: (userId: string, params?: { status?: string; sort?: string }) => {
    if (params) {
      const queryParams = new URLSearchParams(params).toString();
      const queryString = queryParams ? `?${queryParams}` : '';
      return apiRequest(`/admin/users/${userId}/tasks${queryString}`, { method: 'GET' });
    }
    return apiRequest(`/admin/users/${userId}/tasks`, { method: 'GET' });
  },

  // Update user role
  updateUserRole: (userId: string, role: string) => {
    return apiRequest(`/admin/users/${userId}/role?role=${role}`, {
      method: 'PATCH',
    });
  },

  // Get user information
  getUserInfo: (userId: string) => {
    return apiRequest(`/admin/users/${userId}`, { method: 'GET' });
  },

  // Get system statistics
  getSystemStats: () => {
    return apiRequest('/admin/stats', { method: 'GET' });
  },
};

// Health check
export const healthAPI = {
  check: () => fetch('/').then(res => res.json()),
};