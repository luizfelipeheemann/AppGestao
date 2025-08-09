import { createContext, useContext, useState, useEffect } from "react";
import { toast } from "sonner";
import { API_BASE_URL } from "../config";

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context)
    throw new Error("useAuth deve ser usado dentro do AuthProvider");
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("access_token");
    if (savedToken) {
      setToken(savedToken);
      checkAuthStatus(savedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const checkAuthStatus = async (tokenToUse) => {
    if (!tokenToUse) {
      setUser(null);
      setIsAuthenticated(false);
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${tokenToUse}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        setIsAuthenticated(true);
      } else {
        logout();
      }
    } catch {
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, senha) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        setToken(data.access_token);
        toast.success("Login realizado com sucesso!");
        await checkAuthStatus(data.access_token);
        return { success: true };
      } else {
        toast.error(data.message || "Credenciais inválidas");
        logout();
        return { success: false, error: data.message };
      }
    } catch {
      toast.error("Erro de conexão");
      logout();
      return { success: false, error: "Erro de conexão" };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    setIsAuthenticated(false);
    setToken(null);
    toast.success("Logout realizado com sucesso.");
  };

  const refreshAccessToken = async () => {
    const refresh_token = localStorage.getItem("refresh_token");
    if (!refresh_token) return false;

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token }),
      });
      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        setToken(data.access_token);
        return true;
      }
    } catch {}
    return false;
  };

  const makeAuthenticatedRequest = async (url, options = {}) => {
    let tokenToUse = token || localStorage.getItem("access_token");
    if (!tokenToUse) throw new Error("Nenhum token de acesso disponível");

    let requestOptions = {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${tokenToUse}`,
        ...options.headers,
      },
    };

    let response = await fetch(`${API_BASE_URL}${url}`, requestOptions);

    if (response.status === 401) {
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        tokenToUse = localStorage.getItem("access_token");
        requestOptions.headers.Authorization = `Bearer ${tokenToUse}`;
        response = await fetch(`${API_BASE_URL}${url}`, requestOptions);
      } else {
        logout();
        throw new Error("Sessão expirada. Faça login novamente.");
      }
    }

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Erro na requisição");
    return data;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        login,
        logout,
        makeAuthenticatedRequest,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
