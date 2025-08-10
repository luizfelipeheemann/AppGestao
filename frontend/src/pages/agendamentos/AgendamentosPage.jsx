import { useState, useEffect } from "react";
import { Plus, Calendar, User, Edit, CheckCircle, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
// CORRIGIDO
import { useApi } from "../../contexts/ApiContext";
import { toast } from "sonner";
// CORRIGIDO
import LoadingSpinner from "../../components/LoadingSpinner";
import { useNavigate } from "react-router-dom";

const AgendamentosPage = () => {
  const [agendamentos, setAgendamentos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState(null);
  const [agendamentoParaAcao, setAgendamentoParaAcao] = useState(null); // Para concluir ou cancelar
  const [acao, setAcao] = useState(""); // 'concluir' ou 'cancelar'
  const [form, setForm] = useState({
    cliente_id: "",
    servico_id: "",
    data_hora_inicio: "",
    data_hora_fim: "",
    status: "confirmado",
    observacoes: "",
  });
  const [erros, setErros] = useState({});
  const api = useApi();
  const navigate = useNavigate();

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [agendamentosData, clientesData, servicosData] = await Promise.all([
        api.agendamentos.getAll(),
        api.clientes.getAll(),
        api.servicos.getAll(),
      ]);
      setAgendamentos(agendamentosData);
      setClientes(clientesData);
      setServicos(servicosData.filter((s) => s.ativo));
    } catch (error) {
      toast.error("Erro ao carregar dados. Verifique a API.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const resetForm = () => {
    setEditando(null);
    setForm({
      cliente_id: "",
      servico_id: "",
      data_hora_inicio: "",
      data_hora_fim: "",
      status: "confirmado",
      observacoes: "",
    });
    setErros({});
  };

  const abrirNovo = () => {
    navigate("/agendamentos/novo");
  };

  const abrirEditar = (agendamento) => {
    setEditando(agendamento);
    // Ajuste para o fuso horário local no input datetime-local
    const toLocalISOString = (date) => {
      const tzoffset = new Date().getTimezoneOffset() * 60000; //offset in milliseconds
      const localISOTime = new Date(new Date(date) - tzoffset)
        .toISOString()
        .slice(0, -1);
      return localISOTime.slice(0, 16);
    };

    setForm({
      cliente_id: String(agendamento.cliente.id),
      servico_id: String(agendamento.servico.id),
      data_hora_inicio: toLocalISOString(agendamento.data_hora_inicio),
      data_hora_fim: toLocalISOString(agendamento.data_hora_fim),
      status: agendamento.status,
      observacoes: agendamento.observacoes || "",
    });
    setErros({});
    setModalOpen(true);
  };

  const handleFormChange = (name, value) => {
    const newForm = { ...form, [name]: value };

    if (
      (name === "servico_id" || name === "data_hora_inicio") &&
      newForm.servico_id &&
      newForm.data_hora_inicio
    ) {
      const servicoSelecionado = servicos.find(
        (s) => s.id === parseInt(newForm.servico_id)
      );
      if (servicoSelecionado?.duracao_minutos) {
        const dataInicio = new Date(newForm.data_hora_inicio);
        const dataFim = new Date(
          dataInicio.getTime() + servicoSelecionado.duracao_minutos * 60000
        );
        const toLocalISOString = (date) => {
          const tzoffset = new Date().getTimezoneOffset() * 60000;
          const localISOTime = new Date(date - tzoffset)
            .toISOString()
            .slice(0, -1);
          return localISOTime.slice(0, 16);
        };
        newForm.data_hora_fim = toLocalISOString(dataFim);
      }
    }
    setForm(newForm);
  };

  const validar = () => {
    let novoErros = {};
    if (!form.cliente_id) novoErros.cliente_id = "Selecione um cliente.";
    if (!form.servico_id) novoErros.servico_id = "Selecione um serviço.";
    if (!form.data_hora_inicio)
      novoErros.data_hora_inicio = "Data e hora de início são obrigatórios.";
    setErros(novoErros);
    return Object.keys(novoErros).length === 0;
  };

  const salvar = async (e) => {
    e.preventDefault();
    if (!validar()) return;

    const payload = {
      ...form,
      cliente_id: parseInt(form.cliente_id),
      servico_id: parseInt(form.servico_id),
      data_hora_inicio: new Date(form.data_hora_inicio).toISOString(),
      data_hora_fim: new Date(form.data_hora_fim).toISOString(),
    };

    try {
      await api.agendamentos.update(editando.id, payload);
      toast.success("Agendamento atualizado com sucesso!");
      setModalOpen(false);
      loadInitialData();
    } catch (error) {
      toast.error(error?.detail || "Erro ao salvar agendamento.");
    }
  };

  const pedirConfirmacaoAcao = (agendamento, tipoAcao) => {
    setAgendamentoParaAcao(agendamento);
    setAcao(tipoAcao);
  };

  const confirmarAcao = async () => {
    if (!agendamentoParaAcao || !acao) return;
    try {
      if (acao === "concluir") {
        await api.agendamentos.concluir(agendamentoParaAcao.id);
        toast.success("Agendamento concluído com sucesso!");
      } else if (acao === "cancelar") {
        await api.agendamentos.update(agendamentoParaAcao.id, {
          status: "cancelado",
        });
        toast.success("Agendamento cancelado!");
      }
      setAgendamentoParaAcao(null);
      setAcao("");
      loadInitialData();
    } catch (error) {
      toast.error(error?.detail || `Erro ao ${acao} agendamento.`);
    }
  };

  const formatDateTime = (dateString) =>
    new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(dateString));

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);

  const getStatusBadgeVariant = (status) =>
    ({
      confirmado: "default",
      concluido: "success",
      cancelado: "destructive",
    }[status] || "secondary");

  if (loading) return <LoadingSpinner text="Carregando agendamentos..." />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Agendamentos
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Gerencie seus agendamentos e consultas
          </p>
        </div>
        <Button onClick={abrirNovo}>
          <Plus className="mr-2 h-4 w-4" /> Novo Agendamento
        </Button>
      </div>

      <div className="space-y-4">
        {agendamentos.map((ag) => (
          <Card key={ag.id} className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                  <User className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{ag.cliente.nome}</h3>
                  <p className="text-muted-foreground">{ag.servico.nome}</p>
                </div>
              </div>
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-6 w-full sm:w-auto">
                <div className="text-left sm:text-center">
                  <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                    <Calendar className="h-4 w-4" />
                    <span>{formatDateTime(ag.data_hora_inicio)}</span>
                  </div>
                  <p className="font-semibold text-base mt-1">
                    {formatCurrency(ag.servico.preco)}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={getStatusBadgeVariant(ag.status)}>
                    {ag.status}
                  </Badge>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => abrirEditar(ag)}
                    title="Editar"
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  {ag.status === "confirmado" && (
                    <Button
                      variant="ghost"
                      size="icon"
                      title="Marcar como Concluído"
                      onClick={() => pedirConfirmacaoAcao(ag, "concluir")}
                    >
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    </Button>
                  )}
                  {ag.status !== "cancelado" && ag.status !== "concluido" && (
                    <Button
                      variant="ghost"
                      size="icon"
                      title="Cancelar Agendamento"
                      onClick={() => pedirConfirmacaoAcao(ag, "cancelar")}
                    >
                      <XCircle className="h-5 w-5 text-red-600" />
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {agendamentos.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">
            Nenhum agendamento encontrado.
          </p>
        </div>
      )}

      {/* Modal para editar agendamento */}
      <Dialog open={modalOpen} onOpenChange={setModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Editar Agendamento</DialogTitle>
          </DialogHeader>
          <form onSubmit={salvar} className="space-y-4 pt-4">
            <div>
              <Select
                onValueChange={(value) => handleFormChange("cliente_id", value)}
                value={form.cliente_id}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um cliente" />
                </SelectTrigger>
                <SelectContent>
                  {clientes.map((c) => (
                    <SelectItem key={c.id} value={String(c.id)}>
                      {c.nome}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {erros.cliente_id && (
                <p className="text-xs text-red-600 mt-1">{erros.cliente_id}</p>
              )}
            </div>
            <div>
              <Select
                onValueChange={(value) => handleFormChange("servico_id", value)}
                value={form.servico_id}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um serviço" />
                </SelectTrigger>
                <SelectContent>
                  {servicos.map((s) => (
                    <SelectItem key={s.id} value={String(s.id)}>
                      {s.nome} - {formatCurrency(s.preco)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {erros.servico_id && (
                <p className="text-xs text-red-600 mt-1">{erros.servico_id}</p>
              )}
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-sm">Início</label>
                <Input
                  type="datetime-local"
                  name="data_hora_inicio"
                  value={form.data_hora_inicio}
                  onChange={(e) =>
                    handleFormChange("data_hora_inicio", e.target.value)
                  }
                />
                {erros.data_hora_inicio && (
                  <p className="text-xs text-red-600 mt-1">
                    {erros.data_hora_inicio}
                  </p>
                )}
              </div>
              <div>
                <label className="text-sm">Fim (automático)</label>
                <Input
                  type="datetime-local"
                  name="data_hora_fim"
                  value={form.data_hora_fim}
                  readOnly
                  className="bg-gray-100 dark:bg-gray-800"
                />
              </div>
            </div>
            <div>
              <Textarea
                placeholder="Observações (opcional)"
                name="observacoes"
                value={form.observacoes}
                onChange={(e) =>
                  handleFormChange("observacoes", e.target.value)
                }
              />
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setModalOpen(false)}
              >
                Cancelar
              </Button>
              <Button type="submit">Salvar Alterações</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Modal de confirmação para concluir/cancelar */}
      <Dialog
        open={!!agendamentoParaAcao}
        onOpenChange={() => setAgendamentoParaAcao(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {acao === "concluir"
                ? "Concluir Atendimento"
                : "Cancelar Agendamento"}
            </DialogTitle>
            <DialogDescription>
              {acao === "concluir" ? (
                <>
                  Você confirma a conclusão do atendimento para{" "}
                  <span className="font-bold">
                    {agendamentoParaAcao?.cliente.nome}
                  </span>
                  ? Esta ação irá debitar o saldo de pacotes ou gerar cobrança.
                </>
              ) : (
                <>
                  Tem certeza que deseja cancelar o agendamento de{" "}
                  <span className="font-bold">
                    {agendamentoParaAcao?.cliente.nome}
                  </span>
                  ?
                </>
              )}
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setAgendamentoParaAcao(null)}
            >
              Voltar
            </Button>
            <Button
              variant={acao === "cancelar" ? "destructive" : "default"}
              onClick={confirmarAcao}
            >
              Confirmar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AgendamentosPage;
