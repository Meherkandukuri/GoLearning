import React, { createContext, useContext, useState, useEffect } from "react";
import { authApi } from "../services/api";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem("admin_token");
      if (token) {
        // Verify token with backend
        const response = await authApi.verifyToken();
        if (response.data.valid) {
          setUser(response.data.user);
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem("admin_token");
        }
      }
    } catch (error) {
      console.error("Auth check failed:", error);
      localStorage.removeItem("admin_token");
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      const response = await authApi.login(credentials);
      const { token, user } = response.data;

      localStorage.setItem("admin_token", token);
      setUser(user);
      setIsAuthenticated(true);

      return { success: true };
    } catch (error) {
      console.error("Login failed:", error);
      return {
        success: false,
        error: error.response?.data?.detail || "Login failed",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("admin_token");
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
