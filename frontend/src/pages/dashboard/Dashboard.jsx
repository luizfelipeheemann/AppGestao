import { useState, useEffect } from "react";
import {
  Users,
  Calendar,
  Briefcase,
  DollarSign,
  TrendingUp,
} from "lucide-react";
import StatCard from "@/components/dashboard/StatCard";
import ClientesRecentes from "@/components/dashboard/ClientesRecentes";
import AgendamentosProximos from "@/components/dashboard/AgendamentosProximos";
import LoadingSpinner from "../components/LoadingSpinner";
import { useNavigate } from "react-router-dom";
import { useApi } from "../contexts/ApiContext";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [recentClientes, setRecentClientes] = useState([]);
  const [proximosAgendamentos, setProximosAgendamentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const api = useApi();

  const loadDashboardData = async () => {
    try {
      const [s, clientes, ags] = await Promise.all([
        api.dashboard.getStats(),
        api.clientes.getAll({ limit: 5, sort: "desc" }),
        api.agendamentos.getProximos(),
      ]);
      setStats(s);
      setRecentClientes(clientes);
      setProximosAgendamentos(ags);
    } catch {
      toast.error("Não foi possível carregar os dados do dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(loadDashboardData, []);

  const formatCurrency = (v) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(v || 0);
  const formatDate = (dateString) =>
    new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(dateString));
  const getStatusBadgeVariant = (status) =>
    ({ confirmado: "default", concluido: "success", cancelado: "destructive" }[
      status
    ] || "secondary");

  if (loading) return <LoadingSpinner text="Carregando dashboard..." />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between pt-4 pb-2">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-gray-700 dark:text-gray-300 text-base font-medium">
            Bem-vindo ao seu sistema de gestão
          </p>
        </div>
        <Button onClick={() => navigate("/agendamentos")}>
          Novo Agendamento
        </Button>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total de Clientes"
          value={stats.totalClientes}
          icon={Users}
          description={`+${stats.clientesNoMes} este mês`}
        />
        <StatCard
          title="Agendamentos Hoje"
          value={stats.agendamentosHoje}
          icon={Calendar}
        />
        <StatCard
          title="Serviços Ativos"
          value={stats.servicosAtivos}
          icon={Briefcase}
        />
        <StatCard
          title="Receita do Mês"
          value={formatCurrency(stats.receitaMes)}
          icon={DollarSign}
          description="+8% que o mês passado"
        />
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <StatCard title="Clientes Recentes" value="" icon={Users} />
        <div className="space-y-6">
          <div>
            <h2 className="text-lg font-medium">Clientes Recentes</h2>
            <ClientesRecentes clientes={recentClientes} />
          </div>
          <div>
            <h2 className="text-lg font-medium">Próximos Agendamentos</h2>
            <AgendamentosProximos
              agendamentos={proximosAgendamentos}
              formatDate={formatDate}
              getStatusBadgeVariant={getStatusBadgeVariant}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
