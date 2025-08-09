import { createContext, useContext } from "react";
import { useAuth } from "./AuthContext";
import { toast } from "sonner";

// Cria o contexto de API
const ApiContext = createContext({});

// Hook para acessar a API
export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error("useApi deve ser usado dentro de um ApiProvider");
  }
  return context;
};

// Provider do contexto de API
export const ApiProvider = ({ children }) => {
  const { makeAuthenticatedRequest } = useAuth();

  // Handler de erro centralizado para exibir detalhes do backend
  const handleApiError = async (error, customMessage) => {
    let errorMessage = customMessage || "Ocorreu um erro na API.";
    if (error instanceof Response) {
      try {
        const data = await error.json();
        console.log("Resposta do erro do servidor:", data); // Adicionar log
        const detail = data.detail || JSON.stringify(data);
        errorMessage = `${customMessage}: ${detail}`;
      } catch {
        errorMessage = `${customMessage}: ${
          error.statusText || "Erro de rede."
        }`;
      }
    } else {
      errorMessage = `${customMessage}: ${
        error?.message || "Erro desconhecido."
      }`;
    }
    toast.error(errorMessage);
    console.error("API Error:", error);
    throw error;
  };

  // Função genérica para todas as requisições, centralizando a lógica
  const apiRequest = async (url, options = {}, errorMessage) => {
    try {
      // Adiciona o header Content-Type se houver um body
      if (options.body) {
        options.headers = {
          ...options.headers,
          "Content-Type": "application/json",
        };
      }
      const response = await makeAuthenticatedRequest(url, options);
      if (response.ok) {
        // Retorna true para status 204 No Content (DELETE)
        if (response.status === 204) return true;
        return await response.json();
      } else {
        throw response;
      }
    } catch (error) {
      await handleApiError(error, errorMessage);
      throw error;
    }
  };

  // ================== CLIENTES ==================
  const clientes = {
    getAll: (params = {}) =>
      apiRequest(
        `/clientes?${new URLSearchParams(params)}`,
        {},
        "Erro ao carregar clientes"
      ),
    getById: (id) =>
      apiRequest(`/clientes/${id}`, {}, "Erro ao carregar cliente"),
    create: (data) =>
      apiRequest(
        "/clientes",
        { method: "POST", body: JSON.stringify(data) },
        "Erro ao criar cliente"
      ),
    update: (id, data) =>
      apiRequest(
        `/clientes/${id}`,
        { method: "PUT", body: JSON.stringify(data) },
        "Erro ao atualizar cliente"
      ),
    delete: (id) =>
      apiRequest(
        `/clientes/${id}`,
        { method: "DELETE" },
        "Erro ao remover cliente"
      ),
    // Métodos de pacotes do cliente
    getPacotes: (clienteId) =>
      apiRequest(
        `/clientes/${clienteId}/pacotes`,
        {},
        "Erro ao buscar pacotes do cliente"
      ),
    venderPacote: (clienteId, data) =>
      apiRequest(
        `/clientes/${clienteId}/pacotes`,
        { method: "POST", body: JSON.stringify(data) },
        "Erro ao vender pacote"
      ),
  };

  // ================== SERVIÇOS ==================
  const servicos = {
    getAll: (params = {}) =>
      apiRequest(
        `/servicos?${new URLSearchParams(params)}`,
        {},
        "Erro ao carregar serviços"
      ),
    create: (data) =>
      apiRequest(
        "/servicos",
        { method: "POST", body: JSON.stringify(data) },
        "Erro ao criar serviço"
      ),
    update: (id, data) =>
      apiRequest(
        `/servicos/${id}`,
        { method: "PUT", body: JSON.stringify(data) },
        "Erro ao atualizar serviço"
      ),
    delete: (id) =>
      apiRequest(
        `/servicos/${id}`,
        { method: "DELETE" },
        "Erro ao remover serviço"
      ),
  };

  // ================== AGENDAMENTOS ==================
  const agendamentos = {
    getAll: (params = {}) =>
      apiRequest(
        `/agendamentos?${new URLSearchParams(params)}`,
        {},
        "Erro ao carregar agendamentos"
      ),
    create: (data) =>
      apiRequest(
        "/agendamentos",
        { method: "POST", body: JSON.stringify(data) },
        "Erro ao criar agendamento"
      ),
    update: (id, data) =>
      apiRequest(
        `/agendamentos/${id}`,
        { method: "PUT", body: JSON.stringify(data) },
        "Erro ao atualizar agendamento"
      ),
    concluir: (id) =>
      apiRequest(
        `/agendamentos/${id}/concluir`,
        { method: "PATCH" },
        "Erro ao concluir agendamento"
      ),
    getProximos: () =>
      apiRequest(
        "/agendamentos/proximos",
        {},
        "Erro ao buscar próximos agendamentos"
      ),
  };

  // ================== PACOTES ==================
  const pacotes = {
    getAll: (params = {}) =>
      apiRequest(
        `/pacotes?${new URLSearchParams(params)}`,
        {},
        "Erro ao carregar pacotes"
      ),
    create: (data) =>
      apiRequest(
        "/pacotes",
        { method: "POST", body: JSON.stringify(data) },
        "Erro ao criar pacote"
      ),
    update: (id, data) =>
      apiRequest(
        `/pacotes/${id}`,
        { method: "PUT", body: JSON.stringify(data) },
        "Erro ao atualizar pacote"
      ),
    delete: (id) =>
      apiRequest(
        `/pacotes/${id}`,
        { method: "DELETE" },
        "Erro ao remover pacote"
      ),
  };

  // ================== DASHBOARD ==================
  const dashboard = {
    getStats: () =>
      apiRequest("/dashboard/stats", {}, "Erro ao carregar estatísticas"),
  };

  // ================== RELATÓRIOS ==================
  const relatorios = {
    getConsumoPacotes: (params = {}) =>
      apiRequest(
        `/relatorios/consumo-pacotes?${new URLSearchParams(params)}`,
        {},
        "Erro ao gerar relatório"
      ),
  };

  // Valor final do contexto que será disponibilizado para toda a aplicação
  const value = {
    clientes,
    servicos,
    agendamentos,
    pacotes,
    dashboard,
    relatorios,
  };

  return <ApiContext.Provider value={value}>{children}</ApiContext.Provider>;
};
