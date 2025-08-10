import { useState, useEffect, useMemo } from "react";
import {
  Plus,
  Edit,
  Trash2,
  Package,
  DollarSign,
  Hash,
  Calendar,
  ArrowRight,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "sonner";
// CORREÇÃO 1: Ajuste no caminho do context da API
import { useApi } from "../../contexts/ApiContext";
// CORREÇÃO 2: Ajuste no caminho do componente de loading
import LoadingSpinner from "../../components/LoadingSpinner";

const PacotesPage = () => {
  const [pacotes, setPacotes] = useState([]);
  const [allServices, setAllServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState(null);
  const [form, setForm] = useState({
    nome: "",
    descricao: "",
    preco: "",
    quantidade_sessoes: "",
    validade_dias: "",
    servicos_ids: [],
    ativo: true,
  });
  const [erros, setErros] = useState({});
  const [pacoteParaExcluir, setPacoteParaExcluir] = useState(null);

  // ESTADOS PARA FILTROS
  const [filtroStatus, setFiltroStatus] = useState("todos");
  const [filtroServicoId, setFiltroServicoId] = useState("todos");

  const api = useApi();

  useEffect(() => {
    const loadInitialData = async () => {
      setLoading(true);
      try {
        const [pacotesData, servicosData] = await Promise.all([
          api.pacotes.getAll(),
          api.servicos.getAll(),
        ]);
        setPacotes(pacotesData);
        setAllServices(servicosData.filter((s) => s.ativo));
      } catch (error) {
        toast.error("Erro ao carregar dados iniciais.");
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    loadInitialData();
  }, [api]);

  const resetForm = () => {
    setEditando(null);
    setForm({
      nome: "",
      descricao: "",
      preco: "",
      quantidade_sessoes: "",
      validade_dias: "",
      servicos_ids: [],
      ativo: true,
    });
    setErros({});
  };

  const abrirNovo = () => {
    resetForm();
    setModalOpen(true);
  };

  const abrirEditar = (pacote) => {
    setEditando(pacote);
    setForm({
      nome: pacote.nome,
      descricao: pacote.descricao,
      preco: pacote.preco,
      quantidade_sessoes: pacote.quantidade_sessoes,
      validade_dias: pacote.validade_dias,
      servicos_ids: pacote.servicos.map((s) => s.id),
      ativo: pacote.ativo,
    });
    setErros({});
    setModalOpen(true);
  };

  const pedirConfirmacaoExclusao = (pacote) => {
    setPacoteParaExcluir(pacote);
  };

  const confirmarExclusao = async () => {
    if (!pacoteParaExcluir) return;
    try {
      await api.pacotes.delete(pacoteParaExcluir.id);
      toast.success("Pacote excluído com sucesso!");
      setPacoteParaExcluir(null);
      const pacotesData = await api.pacotes.getAll();
      setPacotes(pacotesData);
    } catch (error) {
      toast.error(error?.detail || "Erro ao excluir pacote.");
    }
  };

  const validar = () => {
    let novoErros = {};
    if (!form.nome.trim()) novoErros.nome = "Nome é obrigatório.";
    if (!form.preco || isNaN(Number(form.preco)) || Number(form.preco) <= 0)
      novoErros.preco = "Preço válido e maior que zero é obrigatório.";
    if (
      !form.quantidade_sessoes ||
      isNaN(Number(form.quantidade_sessoes)) ||
      Number(form.quantidade_sessoes) <= 0
    )
      novoErros.quantidade_sessoes =
        "Quantidade de sessões válida é obrigatória.";
    if (
      !form.validade_dias ||
      isNaN(Number(form.validade_dias)) ||
      Number(form.validade_dias) <= 0
    )
      novoErros.validade_dias = "Validade em dias válida é obrigatória.";
    if (form.servicos_ids.length === 0)
      novoErros.servicos_ids = "Selecione pelo menos um serviço para o pacote.";

    setErros(novoErros);
    return Object.keys(novoErros).length === 0;
  };

  const handleFormChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prevForm) => ({
      ...prevForm,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleServiceCheckboxChange = (serviceId) => {
    setForm((prevForm) => {
      const newServicosIds = prevForm.servicos_ids.includes(serviceId)
        ? prevForm.servicos_ids.filter((id) => id !== serviceId)
        : [...prevForm.servicos_ids, serviceId];
      return { ...prevForm, servicos_ids: newServicosIds };
    });
  };

  const salvar = async (e) => {
    e.preventDefault();
    if (!validar()) return;
    const payload = {
      ...form,
      preco: Number(form.preco),
      quantidade_sessoes: Number(form.quantidade_sessoes),
      validade_dias: Number(form.validade_dias),
    };
    try {
      if (editando) {
        await api.pacotes.update(editando.id, payload);
        toast.success("Pacote atualizado com sucesso!");
      } else {
        await api.pacotes.create(payload);
        toast.success("Pacote criado com sucesso!");
      }
      setModalOpen(false);
      const pacotesData = await api.pacotes.getAll();
      setPacotes(pacotesData);
    } catch (error) {
      toast.error(error?.detail || "Erro ao salvar o pacote.");
    }
  };

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);

  // FILTRO
  const pacotesFiltrados = useMemo(() => {
    return pacotes.filter((p) => {
      const statusCond =
        filtroStatus === "todos" ||
        (filtroStatus === "ativos" && p.ativo) ||
        (filtroStatus === "inativos" && !p.ativo);

      const servicoCond =
        filtroServicoId === "todos" ||
        p.servicos.some((s) => s.id === parseInt(filtroServicoId)); // Adicionado parseInt para garantir a comparação correta

      return statusCond && servicoCond;
    });
  }, [pacotes, filtroStatus, filtroServicoId]);

  // Hook para calcular o total e o desconto
  const { totalServicos, descontoValor, descontoPercentual } = useMemo(() => {
    const total = form.servicos_ids.reduce((acc, serviceId) => {
      const service = allServices.find((s) => s.id === serviceId);
      return acc + (service ? service.preco : 0);
    }, 0);

    const precoPacote = Number(form.preco) || 0;
    if (total > 0 && precoPacote > 0 && precoPacote < total) {
      const valorDesconto = total - precoPacote;
      const percentualDesconto = (valorDesconto / total) * 100;
      return {
        totalServicos: total,
        descontoValor: valorDesconto,
        descontoPercentual: percentualDesconto.toFixed(1),
      };
    }
    return { totalServicos: total, descontoValor: 0, descontoPercentual: 0 };
  }, [form.servicos_ids, form.preco, allServices]);

  if (loading) {
    return <LoadingSpinner text="Carregando pacotes..." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Pacotes de Serviços
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Crie combos de serviços com preços promocionais
          </p>
        </div>
        <Button onClick={abrirNovo}>
          <Plus className="mr-2 h-4 w-4" /> Novo Pacote
        </Button>
      </div>

      {/* FILTROS */}
      <div className="flex flex-wrap gap-4 items-center pb-2">
        <div>
          <label className="block text-sm font-medium mb-1">Status</label>
          <select
            value={filtroStatus}
            onChange={(e) => setFiltroStatus(e.target.value)}
            className="p-2 border rounded-md bg-white dark:bg-gray-800"
          >
            <option value="todos">Todos</option>
            <option value="ativos">Ativos</option>
            <option value="inativos">Inativos</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Serviço</label>
          <select
            value={filtroServicoId}
            onChange={(e) => setFiltroServicoId(e.target.value)}
            className="p-2 border rounded-md bg-white dark:bg-gray-800"
          >
            <option value="todos">Todos</option>
            {allServices.map((s) => (
              <option key={s.id} value={s.id}>
                {s.nome}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {pacotesFiltrados.map((pacote) => (
          <Card
            key={pacote.id}
            className="hover:shadow-lg transition-shadow flex flex-col"
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Package className="h-5 w-5 text-primary" />
                  {pacote.nome}
                </CardTitle>
                <div className="flex gap-1 items-center">
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => abrirEditar(pacote)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => pedirConfirmacaoExclusao(pacote)}
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </div>
              <Badge
                className={
                  pacote.ativo
                    ? "bg-green-100 text-green-700 w-fit"
                    : "bg-gray-200 text-gray-700 w-fit"
                }
              >
                {pacote.ativo ? "Ativo" : "Inativo"}
              </Badge>
            </CardHeader>
            <CardContent className="flex-grow flex flex-col justify-between">
              <div>
                <CardDescription className="mb-4">
                  {pacote.descricao}
                </CardDescription>
                <div className="mb-4">
                  <h4 className="text-sm font-semibold mb-2">
                    Serviços Inclusos:
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {pacote.servicos.map((s) => (
                      <Badge key={s.id} variant="outline">
                        {s.nome}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
              <div className="space-y-3 pt-4 border-t">
                <div className="flex items-center justify-between text-lg">
                  <div className="flex items-center space-x-2 font-bold text-primary">
                    <DollarSign className="h-5 w-5" />
                    <span>{formatCurrency(pacote.preco)}</span>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <Hash className="h-4 w-4 text-muted-foreground" />
                    <span>{pacote.quantidade_sessoes} sessões</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                    <span>Válido por {pacote.validade_dias} dias</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {pacotesFiltrados.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500">Nenhum pacote cadastrado ainda.</p>
        </div>
      )}

      <Dialog
        open={!!pacoteParaExcluir}
        onOpenChange={() => setPacoteParaExcluir(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Excluir Pacote</DialogTitle>
            <DialogDescription>
              Tem certeza que deseja excluir o pacote{" "}
              <span className="font-bold">{pacoteParaExcluir?.nome}</span>?
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="gap-2 sm:justify-end">
            <Button
              variant="outline"
              onClick={() => setPacoteParaExcluir(null)}
            >
              Cancelar
            </Button>
            <Button variant="destructive" onClick={confirmarExclusao}>
              Excluir
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={modalOpen} onOpenChange={setModalOpen}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>
              {editando ? "Editar Pacote" : "Novo Pacote"}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={salvar} className="space-y-4 pt-4">
            <Input
              placeholder="Nome do Pacote (ex: Combo Relax, Pacote Fitness Inicial)"
              name="nome"
              value={form.nome}
              onChange={handleFormChange}
            />
            {erros.nome && <p className="text-xs text-red-600">{erros.nome}</p>}
            <Textarea
              placeholder="Descrição do pacote"
              name="descricao"
              value={form.descricao}
              onChange={handleFormChange}
            />

            <div>
              <label className="text-sm font-medium">
                Serviços Inclusos no Combo
              </label>
              <div className="mt-2 p-4 border rounded-md max-h-48 overflow-y-auto grid grid-cols-1 sm:grid-cols-2 gap-4">
                {allServices.map((service) => (
                  <div
                    key={service.id}
                    className="flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <Checkbox
                        id={`service-${service.id}`}
                        checked={form.servicos_ids.includes(service.id)}
                        onCheckedChange={() =>
                          handleServiceCheckboxChange(service.id)
                        }
                      />
                      <label
                        htmlFor={`service-${service.id}`}
                        className="text-sm cursor-pointer"
                      >
                        {service.nome}
                      </label>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {formatCurrency(service.preco)}
                    </span>
                  </div>
                ))}
              </div>
              {erros.servicos_ids && (
                <p className="text-xs text-red-600 mt-1">
                  {erros.servicos_ids}
                </p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center p-4 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <div>
                <label className="text-sm font-medium">
                  Preço do Pacote (Promocional)
                </label>
                <Input
                  placeholder="Preço (R$)"
                  name="preco"
                  value={form.preco}
                  onChange={handleFormChange}
                  type="number"
                  min="0"
                  step="0.01"
                  className="mt-1"
                />
                {erros.preco && (
                  <p className="text-xs text-red-600 mt-1">{erros.preco}</p>
                )}
              </div>
              <div className="text-sm text-center md:text-left">
                <p>
                  Valor total dos serviços:{" "}
                  <span className="font-semibold">
                    {formatCurrency(totalServicos)}
                  </span>
                </p>
                {descontoValor > 0 && (
                  <p className="text-green-600 font-semibold flex items-center justify-center md:justify-start gap-1">
                    <Sparkles className="h-4 w-4" />
                    Desconto de {formatCurrency(descontoValor)} (
                    {descontoPercentual}%)
                  </p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Input
                  placeholder="Quantidade de Sessões"
                  name="quantidade_sessoes"
                  value={form.quantidade_sessoes}
                  onChange={handleFormChange}
                  type="number"
                  min="1"
                />
                {erros.quantidade_sessoes && (
                  <p className="text-xs text-red-600">
                    {erros.quantidade_sessoes}
                  </p>
                )}
              </div>
              <div>
                <Input
                  placeholder="Validade (em dias)"
                  name="validade_dias"
                  value={form.validade_dias}
                  onChange={handleFormChange}
                  type="number"
                  min="1"
                />
                {erros.validade_dias && (
                  <p className="text-xs text-red-600">{erros.validade_dias}</p>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Checkbox
                id="ativo-form"
                name="ativo"
                checked={form.ativo}
                onCheckedChange={(checked) =>
                  setForm((f) => ({ ...f, ativo: checked }))
                }
              />
              <label htmlFor="ativo-form" className="text-sm">
                Pacote Ativo
              </label>
            </div>

            <DialogFooter className="pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => setModalOpen(false)}
              >
                Cancelar
              </Button>
              <Button type="submit">Salvar Pacote</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PacotesPage;
