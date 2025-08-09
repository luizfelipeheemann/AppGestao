import { useAuth } from "../contexts/AuthContext";
import { Navigate } from "react-router-dom";
import LoadingSpinner from "./LoadingSpinner";

export function RequireAuth({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <LoadingSpinner />;
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}
