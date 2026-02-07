/**
 * Better Auth Client Configuration
 * 
 * This file sets up the Better Auth client for the frontend application.
 * It provides authentication functions that integrate with the backend API.
 * Note: Since the backend uses a custom JWT system, this acts as a wrapper
 * to maintain compatibility with Better Auth patterns.
 */

// Mock Better Auth client functions to maintain interface compatibility
export const signIn = async (provider: string, credentials: any) => {
  if (provider === 'credentials' && credentials.email && credentials.password) {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Store the JWT token in localStorage
        if (typeof window !== 'undefined') {
          localStorage.setItem('authToken', data.access_token || data.token);
        }
        return { success: true, user: data.user, token: data.access_token || data.token, error: null };
      } else {
        const errorData = await response.json();
        return { success: false, user: null, token: null, error: errorData.detail || 'Login failed' };
      }
    } catch (error: any) {
      return { success: false, user: null, token: null, error: error.message || 'Network error' };
    }
  }
  return { success: false, user: null, token: null, error: 'Invalid credentials provided' };
};

export const signUp = async (credentials: any) => {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
        name: credentials.name,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      // Store the JWT token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', data.access_token || data.token);
      }
      return { success: true, user: data.user, token: data.access_token || data.token, error: null };
    } else {
      const errorData = await response.json();
      return { success: false, user: null, token: null, error: errorData.detail || 'Registration failed' };
    }
  } catch (error: any) {
    return { success: false, user: null, token: null, error: error.message || 'Network error' };
  }
};

export const signOut = async () => {
  // Clear the stored token
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
  }
  
  // Optionally call the backend logout endpoint
  const token = localStorage.getItem('authToken');
  if (token) {
    await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    }).catch(() => {
      // Ignore logout errors - still clear local state
    });
  }
};

// Create a separate function to get session
export const getSession = () => {
  // Get user info from the stored JWT token
  const token = localStorage.getItem('authToken');
  if (!token) return null;
  
  try {
    // Decode the JWT token to get user info
    const base64Payload = token.split('.')[1];
    const payload = JSON.parse(atob(base64Payload));
    return {
      user: {
        id: payload.sub,
        email: payload.email || payload.sub,
        name: payload.name || null
      },
      expiresAt: new Date(payload.exp * 1000)
    };
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

// Enhanced authentication functions that work with our API
export const authenticateUser = async (email: string, password: string) => {
  try {
    // Attempt to sign in using Better Auth
    const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();
      
      // Store the token in localStorage for API requests
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', data.access_token || data.token);
      }
      
      return { success: true, user: data.user, token: data.access_token || data.token };
    } else {
      const errorData = await response.json();
      return { success: false, error: errorData.detail || 'Login failed' };
    }
  } catch (error) {
    console.error('Authentication error:', error);
    return { success: false, error: 'Network error occurred' };
  }
};

export const registerUser = async (name: string, email: string, password: string) => {
  try {
    // Attempt to register using Better Auth
    const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email, password }),
    });

    if (response.ok) {
      const data = await response.json();
      
      // Store the token in localStorage for API requests
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', data.access_token || data.token);
      }
      
      return { success: true, user: data.user, token: data.access_token || data.token };
    } else {
      const errorData = await response.json();
      return { success: false, error: errorData.detail || 'Registration failed' };
    }
  } catch (error) {
    console.error('Registration error:', error);
    return { success: false, error: 'Network error occurred' };
  }
};

export const logoutUser = async () => {
  try {
    // Clear the stored token
    if (typeof window !== 'undefined') {
      localStorage.removeItem('authToken');
    }
    
    // Optionally call the backend logout endpoint
    const token = localStorage.getItem('authToken');
    if (token) {
      await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://todo-app-lpxv.onrender.com'}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
    }
    
    return { success: true };
  } catch (error) {
    console.error('Logout error:', error);
    return { success: false, error: 'Logout failed' };
  }
};