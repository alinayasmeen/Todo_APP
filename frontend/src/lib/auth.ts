/**
 * Authentication Utilities
 *
 * This file provides functions for authentication in the frontend application.
 * It handles token management and authenticated API requests for the Todo App.
 */

// Export functions for authentication
export const useSession = () => {
  // In a real implementation, this would come from Better Auth
  // For now, we'll simulate the session
  const token = typeof window !== 'undefined' ? localStorage.getItem('authToken') : null;
  return {
    data: token ? { user: { name: 'Demo User', email: 'demo@example.com' } } : null,
    isLoading: false
  };
};

export const signIn = async (provider: string, credentials: any) => {
  try {
    // Simulate signing in with credentials
    if (provider === 'credentials') {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        const data = await response.json();
        // Store token in localStorage (in a real app, use secure storage)
        if (typeof window !== 'undefined') {
          localStorage.setItem('authToken', data.token || 'demo-token');
        }
        return { error: null };
      } else {
        const errorData = await response.json();
        return { error: errorData.detail || 'Login failed' };
      }
    }
    return { error: 'Unsupported provider' };
  } catch (error) {
    return { error: 'Network error' };
  }
};

export const signOut = async () => {
  // Remove token from localStorage
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
  }
};

// Export a function to get the auth token for API requests
export const getAuthToken = async (): Promise<string | null> => {
  try {
    // Get the token from localStorage (in a real app, use secure storage)
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken') || null;
    }
    return null;
  } catch (error) {
    console.error('Failed to get auth token:', error);
    return null;
  }
};

// Export a function to make authenticated API requests
export const makeAuthenticatedRequest = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  const token = await getAuthToken();

  // Add authorization header to the request
  const authenticatedOptions: RequestInit = {
    ...options,
    headers: {
      ...options.headers,
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      'Content-Type': 'application/json',
    },
  };

  // Make the authenticated request
  return fetch(url, authenticatedOptions);
};