import { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { Toaster } from "sonner";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { ApiProvider } from "./contexts/ApiContext";

// --- IMPORTAÇÕES CORRIGIDAS ---
// O caminho agora aponta para a subpasta correta dentro de 'pages'
import LoginPage from "./pages/auth/LoginPage";
import Dashboard from "./pages/dashboard/Dashboard";
import ClientesPage from "./pages/clientes/ClientesPage";
import ServicosPage from "./pages/servicos/ServicosPage";
import AgendamentosPage from "./pages/agendamentos/AgendamentosPage";
import PacotesPage from "./pages/pacotes/PacotesPage";
import RelatoriosPage from "./pages/relatorios/RelatoriosPage";
// --- FIM DAS IMPORTAÇÕES CORRIGIDAS ---

import Layout from "./components/Layout";
import LoadingSpinner from "./components/LoadingSpinner";
import "./App.css";

// Componente de Rota Protegida
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

// Componente de Rota Pública (redireciona se autenticado)
function PublicRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  return !isAuthenticated ? children : <Navigate to="/dashboard" replace />;
}

function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/login"
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        }
      />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="clientes" element={<ClientesPage />} />
        <Route path="servicos" element={<ServicosPage />} />
        <Route path="agendamentos" element={<AgendamentosPage />} />
        <Route path="pacotes" element={<PacotesPage />} />
        <Route path="relatorios" element={<RelatoriosPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <ApiProvider>
          <div className="min-h-screen bg-background">
            <AppRoutes />
            <Toaster
              position="bottom-right"
              theme="unstyled"
              toastOptions={{
                success: {
                  className:
                    "bg-green-100 text-green-800 border border-green-200 shadow-lg",
                  iconTheme: {
                    primary: "#22c55e",
                    secondary: "#fff",
                  },
                },
                error: {
                  className:
                    "bg-red-100 text-red-800 border border-red-200 shadow-lg",
                  iconTheme: {
                    primary: "#ef4444",
                    secondary: "#fff",
                  },
                },
              }}
            />
          </div>
        </ApiProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
