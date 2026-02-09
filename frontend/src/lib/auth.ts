/**
 * Authentication Utilities
 *
 * This file provides functions for authentication in the frontend application.
 * It handles Better Auth integration and authenticated API requests for the Todo App.
 */

import { signIn as betterSignIn, signOut as betterSignOut, getSession } from './better-auth-client';

// Export functions for authentication
export const useSession = () => {
  // Get session from Better Auth
  const session = getSession();
  return {
    data: session,
    isLoading: false
  };
};

// Wrapper for Better Auth signIn
export const signIn = async (provider: string, credentials: any) => {
  if (provider === 'credentials') {
    // Use the Better Auth client to sign in
    const result = await betterSignIn(provider, credentials);
    return result;
  }
  return { error: 'Invalid provider', success: false, user: null, token: null };
};

// Wrapper for Better Auth signOut
export const signOut = async () => {
  try {
    // Call Better Auth's signOut which handles token cleanup
    await betterSignOut();
  } catch (error) {
    console.error('Sign out error:', error);
  }
};

// Export a function to get the auth token for API requests
export const getAuthToken = async (): Promise<string | null> => {
  try {
    // Get the token from localStorage
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('authToken');
      console.log('Retrieved token from localStorage:', token ? 'YES' : 'NO');
      
      // Validate the token format before returning
      if (token) {
        const tokenParts = token.split('.');
        if (tokenParts.length !== 3) {
          console.error('Invalid JWT token format');
          localStorage.removeItem('authToken'); // Remove invalid token
          return null;
        }
        
        // Try to decode the payload to ensure it's valid
        try {
          const base64Payload = tokenParts[1].replace(/-/g, '+').replace(/_/g, '/');
          const paddedBase64 = base64Payload.padEnd(base64Payload.length + (4 - base64Payload.length % 4) % 4, '=');
          const payload = JSON.parse(atob(paddedBase64));
          
          // Check if token is expired
          const currentTime = Math.floor(Date.now() / 1000);
          if (payload.exp && payload.exp < currentTime) {
            console.warn('Token has expired, removing from storage');
            localStorage.removeItem('authToken');
            return null;
          }
        } catch (decodeError) {
          console.error('Invalid JWT token payload:', decodeError);
          localStorage.removeItem('authToken'); // Remove invalid token
          return null;
        }
      }
      
      return token || null;
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