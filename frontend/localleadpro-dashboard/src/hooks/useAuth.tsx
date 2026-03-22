import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface User {
  id: number;
  email: string;
  is_superuser: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, user: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * Global authentication provider that manages user session state.
 * Handles token persistence in local storage and provides safe login/logout utilities.
 * 
 * @param children - React components that require access to the authentication context.
 */
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const savedToken = localStorage.getItem('llp_token');
    const savedUser = localStorage.getItem('llp_user');
    
    if (savedToken && savedUser) {
      const timer = setTimeout(() => {
        setToken(savedToken);
        setUser(JSON.parse(savedUser));
        setIsLoading(false);
      }, 0);
      return () => clearTimeout(timer);
    } else {
      setIsLoading(false);
    }
  }, []);

  /**
   * Persists authentication credentials and updates global state.
   */
  const login = (newToken: string, newUser: User) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem('llp_token', newToken);
    localStorage.setItem('llp_user', JSON.stringify(newUser));
  };

  /**
   * Clears session data and redirects the user to the login screen.
   */
  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('llp_token');
    localStorage.removeItem('llp_user');
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to access the current authentication state and actions.
 * Throws an error if used outside of an AuthProvider.
 */
// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
