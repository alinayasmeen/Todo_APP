/**
 * Session management utilities for the Todo App
 * Handles JWT token storage, validation, and expiration
 */

import jwtDecode from 'jwt-decode';

// Constants for session management
const TOKEN_KEY = 'todo_app_jwt_token';
const REFRESH_TOKEN_KEY = 'todo_app_refresh_token';
const SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes (configurable)

/**
 * Stores the JWT token in localStorage
 */
export const storeToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Retrieves the stored JWT token
 */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Removes the stored JWT token
 */
export const removeToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * Stores the refresh token in localStorage
 */
export const storeRefreshToken = (refreshToken: string): void => {
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

/**
 * Retrieves the stored refresh token
 */
export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * Removes the stored refresh token
 */
export const removeRefreshToken = (): void => {
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * Checks if the token is expired
 */
export const isTokenExpired = (token: string): boolean => {
  try {
    const decoded = jwtDecode<{ exp: number }>(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
  } catch (error) {
    console.error('Error decoding JWT token:', error);
    return true; // If we can't decode, assume it's invalid/expired
  }
};

/**
 * Checks if the current session is valid
 */
export const isValidSession = (): boolean => {
  const token = getToken();
  if (!token) {
    return false;
  }

  return !isTokenExpired(token);
};

/**
 * Refreshes the session token if needed
 */
export const refreshSession = async (): Promise<boolean> => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return false;
  }

  try {
    // In a real implementation, you would make an API call to refresh the token
    // For now, returning false to indicate that a full re-authentication is needed
    return false;
  } catch (error) {
    console.error('Error refreshing session:', error);
    return false;
  }
};

/**
 * Initializes session state on application startup
 */
export const initializeSession = (): void => {
  // Any session initialization logic would go here
  // For example, setting up session timeout checks, auto-refresh, etc.
  console.log('Session management initialized');
};

/**
 * Cleans up the current session
 */
export const clearSession = (): void => {
  removeToken();
  removeRefreshToken();
  // Optionally dispatch a logout event to notify other parts of the app
  window.dispatchEvent(new Event('userLoggedOut'));
};