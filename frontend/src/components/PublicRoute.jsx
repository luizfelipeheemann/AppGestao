import { useAuth } from "../contexts/AuthContext";
import { Navigate } from "react-router-dom";
import LoadingSpinner from "./LoadingSpinner";

export function PublicRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <LoadingSpinner />;
  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
}
