'use client';
const API_URL = process.env.NEXT_PUBLIC_API_URL;



import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, confirmPassword: string) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check if user is authenticated on initial load
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = () => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      // Decode token to get user info (or make an API call to get user info)
      try {
        const payload = JSON.parse(atob(storedToken.split('.')[1]));
        const currentTime = Date.now() / 1000;
        if (payload.exp && payload.exp > currentTime) {
          // Token is still valid
          // We'll fetch user details from the API to ensure it's accurate
          fetchUserDetails(storedToken);
        } else {
          // Token expired
          logout();
        }
      } catch (error) {
        console.error('Error decoding token:', error);
        logout();
      }
    } else {
      setLoading(false);
    }
  };

  const fetchUserDetails = async (token: string) => {
    try {
     const response = await fetch(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        // If fetching user details fails, it might mean the token is invalid/expired
        const errorData = await response.json().catch(() => ({}));
        console.error('Failed to fetch user details:', errorData);
        logout();
        return;
      }

      const userData = await response.json();
      setUser({
        id: userData.id,
        username: userData.username,
        email: userData.email,
      });
    } catch (error) {
      console.error('Error fetching user details:', error);
      // Check if it's a network error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.error('Network error when fetching user details');
      }
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
     const response = await fetch(`${API_URL}/api/auth/login`, {

        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      // Handle network errors
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));

        if (response.status === 401) {
          throw new Error(data.detail || 'Invalid username or password');
        } else if (response.status >= 500) {
          throw new Error('Server error. Please try again later.');
        } else {
          throw new Error(data.detail || `Login failed: ${response.status}`);
        }
      }

      const data = await response.json();
      const { access_token, user: userData } = data;

      // Save token to localStorage
      localStorage.setItem('token', access_token);
      setToken(access_token);

      // Set user data
      setUser({
        id: userData.id,
        username: userData.username,
        email: userData.email,
      });

      // Redirect to dashboard after successful login
      router.push('/dashboard');
    } catch (error: any) {
      console.error('Login error:', error);
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check if the backend is running.');
      }
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username: string, email: string, password: string, confirmPassword: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {

        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          confirm_password: confirmPassword,
        }),
      });

      // Handle network errors
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));

        if (response.status === 400) {
          throw new Error(data.detail || 'Invalid input data');
        } else if (response.status === 409) {
          throw new Error('Username or email already exists');
        } else if (response.status >= 500) {
          throw new Error('Server error. Please try again later.');
        } else {
          throw new Error(data.detail || `Registration failed: ${response.status}`);
        }
      }

      const data = await response.json();

      // Auto-login after successful registration
      await login(username, password);
    } catch (error: any) {
      console.error('Registration error:', error);
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check if the backend is running.');
      }
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // Clear token and user data
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);

    // Redirect to login page
    router.push('/login');
  };

  const value = {
    user,
    token,
    isAuthenticated: !!user,
    loading,
    login,
    register,
    logout,
    checkAuthStatus,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};