import { useState, useEffect } from "react";
import {
  FileText,
  Filter,
  Calendar,
  User,
  Hash,
  Check,
  X,
  Clock,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useApi } from "../contexts/ApiContext";
import { toast } from "sonner";
import LoadingSpinner from "../components/LoadingSpinner";

const RelatoriosPage = () => {
  const [relatorio, setRelatorio] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    cliente_id: "",
    data_inicio: "",
    data_fim: "",
  });
  const api = useApi();

  useEffect(() => {
    // Carrega a lista de clientes para o filtro
    const loadClientes = async () => {
      try {
        const clientesData = await api.clientes.getAll();
        setClientes(clientesData);
      } catch (error) {
        toast.error("Erro ao carregar lista de clientes.");
      }
    };
    loadClientes();
  }, [api]);

  const handleFilterChange = (name, value) => {
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleGerarRelatorio = async () => {
    setLoading(true);
    setRelatorio([]);
    try {
      const data = await api.relatorios.getConsumoPacotes(filters);
      setRelatorio(data);
      if (data.length === 0) {
        toast.info("Nenhum dado encontrado para os filtros selecionados.");
      }
    } catch (error) {
      toast.error(error?.detail || "Erro ao gerar relatório.");
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadgeVariant = (status) => {
    const variants = {
      ativo: "success",
      esgotado: "secondary",
      expirado: "destructive",
    };
    return variants[status] || "default";
  };

  const formatDate = (dateString) =>
    new Intl.DateTimeFormat("pt-BR").format(new Date(dateString));
  const formatDateTime = (dateString) =>
    new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(dateString));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Relatórios
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Analise o consumo de pacotes e outros dados.
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" /> Filtros do Relatório de Consumo
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Select
            onValueChange={(value) => handleFilterChange("cliente_id", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Todos os Clientes" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">Todos os Clientes</SelectItem>
              {clientes.map((c) => (
                <SelectItem key={c.id} value={c.id}>
                  {c.nome}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <div>
            <label className="text-sm">Data de Início</label>
            <Input
              type="date"
              value={filters.data_inicio}
              onChange={(e) =>
                handleFilterChange("data_inicio", e.target.value)
              }
            />
          </div>
          <div>
            <label className="text-sm">Data de Fim</label>
            <Input
              type="date"
              value={filters.data_fim}
              onChange={(e) => handleFilterChange("data_fim", e.target.value)}
            />
          </div>
          <Button
            onClick={handleGerarRelatorio}
            className="self-end"
            disabled={loading}
          >
            {loading ? <LoadingSpinner size="small" /> : "Gerar Relatório"}
          </Button>
        </CardContent>
      </Card>

      {/* BLOCO DE TOTALIZADORES */}
      {relatorio.length > 0 && (
        <Card className="mb-4">
          <CardContent className="flex flex-wrap gap-4 py-4 justify-between">
            <div>
              <span className="text-lg font-bold">{relatorio.length}</span>
              <span className="text-gray-600 ml-2">pacotes encontrados</span>
            </div>
            <div>
              <span className="text-lg font-bold">
                {relatorio.reduce((acc, r) => acc + (r.sessoes_total || 0), 0)}
              </span>
              <span className="text-gray-600 ml-2">sessões totais</span>
            </div>
            <div>
              <span className="text-lg font-bold">
                {relatorio.reduce((acc, r) => acc + (r.sessoes_saldo || 0), 0)}
              </span>
              <span className="text-gray-600 ml-2">sessões em saldo</span>
            </div>
            <div>
              <span className="text-lg font-bold">
                {
                  Array.from(new Set(relatorio.map((r) => r.cliente_nome)))
                    .length
                }
              </span>
              <span className="text-gray-600 ml-2">clientes</span>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="space-y-4">
        {relatorio.map((item, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle>{item.pacote_nome}</CardTitle>
              <CardDescription>
                Cliente:{" "}
                <span className="font-semibold">{item.cliente_nome}</span>
              </CardDescription>
              <div className="flex flex-wrap gap-4 text-sm pt-2">
                <Badge variant={getStatusBadgeVariant(item.status)}>
                  {item.status}
                </Badge>
                <span className="flex items-center gap-1">
                  <User className="h-4 w-4" /> Saldo: {item.sessoes_saldo} de{" "}
                  {item.sessoes_total}
                </span>
                <span className="flex items-center gap-1">
                  <Calendar className="h-4 w-4" /> Comprado em:{" "}
                  {formatDate(item.data_compra)}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="h-4 w-4" /> Expira em:{" "}
                  {formatDate(item.data_expiracao)}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <h4 className="font-semibold mb-2">Histórico de Consumo:</h4>
              {item.consumo.length > 0 ? (
                <ul className="space-y-2">
                  {item.consumo.map((uso, idx) => (
                    <li
                      key={idx}
                      className="flex justify-between items-center p-2 bg-slate-50 dark:bg-slate-800 rounded-md"
                    >
                      <span className="text-sm">{uso.servico_nome}</span>
                      <span className="text-xs text-muted-foreground">
                        {formatDateTime(uso.data_uso)}
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground text-center py-4">
                  Nenhum uso registrado para este pacote.
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default RelatoriosPage;
