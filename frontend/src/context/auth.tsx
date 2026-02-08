import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/router';
import { signIn as betterSignIn, signUp as betterSignUp, signOut as betterSignOut, getSession } from '../lib/better-auth-client';

interface AuthContextType {
  user: any;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (name: string, email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('authToken');
    if (token) {
      // In a real app, you'd validate the token with an API call
      // For now, we'll just set a dummy user based on the token
      try {
        // Decode the token to get user info (simplified)
        const base64Payload = token.split('.')[1];
        const payload = JSON.parse(atob(base64Payload));
        setUser({ id: payload.sub, email: payload.email });
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('authToken');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const result = await betterSignIn('credentials', { email, password });
      
      if (result.success) {
        // Get updated session info
        const session = getSession();
        setUser(session?.user || { email });
        router.push('/dashboard');
      } else {
        throw new Error(result.error || 'Login failed');
      }
    } catch (error: any) {
      throw new Error(error.message || 'Login failed');
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      const result = await betterSignUp({ name, email, password });
      
      if (result.success) {
        // Get updated session info
        const session = getSession();
        setUser(session?.user || { email });
        router.push('/dashboard');
      } else {
        throw new Error(result.error || 'Registration failed');
      }
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed');
    }
  };

  const logout = async () => {
    try {
      await betterSignOut();
      setUser(null);
      router.push('/');
    } catch (error) {
      console.error('Logout failed:', error);
      // Still clear local state even if backend logout failed
      localStorage.removeItem('authToken');
      setUser(null);
      router.push('/');
    }
  };

  const value = {
    user,
    loading,
    login,
    logout,
    register
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};