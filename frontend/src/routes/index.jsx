import React, { useContext } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import LoginPage from "../pages/Auth/LoginPage";
import ListaClientes from "../pages/Clientes/ListaClientes";
import Dashboard from "../pages/Dashboard/Dashboard";
import ListaAgendamentos from "../pages/Agendamentos/ListaAgendamentos";
import NovoAgendamento from "../pages/Agendamentos/NovoAgendamento";
import AgendamentoInteligente from "../pages/Agendamentos/AgendamentoInteligente";
import ListaPacotes from "../pages/Pacotes/ListaPacotes";
import ListaServicos from "../pages/Servicos/ListaServicos";

function PrivateRoute({ children }) {
  const { user } = useContext(AuthContext);
  return user ? children : <Navigate to="/login" />;
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />
      <Route
        path="/clientes"
        element={
          <PrivateRoute>
            <ListaClientes />
          </PrivateRoute>
        }
      />
      <Route
        path="/servicos"
        element={
          <PrivateRoute>
            <ListaServicos />
          </PrivateRoute>
        }
      />
      <Route
        path="/pacotes"
        element={
          <PrivateRoute>
            <ListaPacotes />
          </PrivateRoute>
        }
      />
      <Route
        path="/agendamentos"
        element={
          <PrivateRoute>
            <ListaAgendamentos />
          </PrivateRoute>
        }
      />
      <Route
        path="/agendamentos/novo"
        element={
          <PrivateRoute>
            <NovoAgendamento />
          </PrivateRoute>
        }
      />
      <Route
        path="/agendamentos/inteligente"
        element={
          <PrivateRoute>
            <AgendamentoInteligente />
          </PrivateRoute>
        }
      />
    </Routes>
  );
}
