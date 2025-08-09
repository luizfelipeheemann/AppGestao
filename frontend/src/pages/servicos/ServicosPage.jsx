import { useState, useEffect } from "react";
import { Plus, Clock, DollarSign, Edit, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { useApi } from "../contexts/ApiContext";
import LoadingSpinner from "../components/LoadingSpinner";

const ServicosPage = () => {
  const [servicos, setServicos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState(null);
  const [form, setForm] = useState({
    nome: "",
    descricao: "",
    preco: "",
    duracao_minutos: "",
    ativo: true,
  });
  const [erros, setErros] = useState({});
  const [servicoParaExcluir, setServicoParaExcluir] = useState(null);

  const api = useApi();

  useEffect(() => {
    loadServicos();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadServicos = async () => {
    setLoading(true);
    try {
      // Assumindo que você criará api.servicos.getAll() no seu ApiContext
      const data = await api.servicos.getAll();
      setServicos(data);
    } catch (error) {
      toast.error("Erro ao carregar serviços. Verifique a conexão com a API.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setEditando(null);
    setForm({
      nome: "",
      descricao: "",
      preco: "",
      duracao_minutos: "",
      ativo: true,
    });
    setErros({});
  };

  const abrirNovo = () => {
    resetForm();
    setModalOpen(true);
  };

  const abrirEditar = (servico) => {
    setEditando(servico);
    setForm({
      nome: servico.nome,
      descricao: servico.descricao || "",
      preco: servico.preco,
      duracao_minutos: servico.duracao_minutos || "",
      ativo: servico.ativo,
    });
    setErros({});
    setModalOpen(true);
  };

  const pedirConfirmacaoExclusao = (servico) => {
    setServicoParaExcluir(servico);
  };

  const confirmarExclusao = async () => {
    if (!servicoParaExcluir) return;
    try {
      await api.servicos.delete(servicoParaExcluir.id);
      toast.success("Serviço excluído com sucesso!");
      setServicoParaExcluir(null);
      loadServicos(); // Recarrega a lista
    } catch (error) {
      toast.error(error?.detail || "Erro ao excluir serviço.");
    }
  };

  const validar = () => {
    let novoErros = {};
    if (!form.nome.trim()) novoErros.nome = "Nome é obrigatório.";
    if (!form.preco || isNaN(Number(form.preco)) || Number(form.preco) <= 0)
      novoErros.preco = "Preço válido e maior que zero é obrigatório.";
    if (
      !form.duracao_minutos ||
      isNaN(Number(form.duracao_minutos)) ||
      Number(form.duracao_minutos) <= 0
    )
      novoErros.duracao_minutos = "Duração em minutos válida é obrigatória.";

    setErros(novoErros);
    return Object.keys(novoErros).length === 0;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prevForm) => ({
      ...prevForm,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const salvar = async (e) => {
    e.preventDefault();
    if (!validar()) return;

    const payload = {
      ...form,
      preco: Number(form.preco),
      duracao_minutos: Number(form.duracao_minutos),
    };

    try {
      if (editando) {
        await api.servicos.update(editando.id, payload);
        toast.success("Serviço atualizado com sucesso!");
      } else {
        await api.servicos.create(payload);
        toast.success("Serviço criado com sucesso!");
      }
      setModalOpen(false);
      loadServicos();
    } catch (error) {
      toast.error(error?.detail || "Erro ao salvar o serviço.");
    }
  };

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);

  if (loading) {
    return <LoadingSpinner text="Carregando serviços..." />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Serviços
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Gerencie os serviços oferecidos
          </p>
        </div>
        <Button onClick={abrirNovo}>
          <Plus className="mr-2 h-4 w-4" />
          Novo Serviço
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {servicos.map((servico) => (
          <Card key={servico.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{servico.nome}</CardTitle>
                <div className="flex gap-1 items-center">
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => abrirEditar(servico)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => pedirConfirmacaoExclusao(servico)}
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </div>
              <Badge
                className={
                  servico.ativo
                    ? "bg-green-100 text-green-700 w-fit"
                    : "bg-gray-200 text-gray-700 w-fit"
                }
              >
                {servico.ativo ? "Ativo" : "Inativo"}
              </Badge>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <p className="text-sm text-muted-foreground h-10 overflow-hidden">
                  {servico.descricao}
                </p>
                <div className="flex items-center justify-between pt-3 border-t">
                  <div className="flex items-center space-x-2 font-medium text-primary">
                    <DollarSign className="h-4 w-4" />
                    <span>{formatCurrency(servico.preco)}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-muted-foreground">
                    <Clock className="h-4 w-4" />
                    <span className="text-sm">
                      {servico.duracao_minutos} min
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {servicos.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500">Nenhum serviço cadastrado ainda.</p>
        </div>
      )}

      {/* Modal de confirmação de exclusão */}
      <Dialog
        open={!!servicoParaExcluir}
        onOpenChange={() => setServicoParaExcluir(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Excluir Serviço</DialogTitle>
            <DialogDescription>
              Tem certeza que deseja excluir o serviço{" "}
              <span className="font-bold">{servicoParaExcluir?.nome}</span>?
              Esta ação não pode ser desfeita.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="gap-2 sm:justify-end">
            <Button
              variant="outline"
              onClick={() => setServicoParaExcluir(null)}
            >
              Cancelar
            </Button>
            <Button variant="destructive" onClick={confirmarExclusao}>
              Excluir
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Modal para adicionar/editar serviço */}
      <Dialog open={modalOpen} onOpenChange={setModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editando ? "Editar Serviço" : "Novo Serviço"}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={salvar} className="space-y-4 pt-4">
            <Input
              placeholder="Nome do Serviço"
              name="nome"
              value={form.nome}
              onChange={handleChange}
            />
            {erros.nome && <p className="text-xs text-red-600">{erros.nome}</p>}

            <Textarea
              placeholder="Descrição (opcional)"
              name="descricao"
              value={form.descricao}
              onChange={handleChange}
            />

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Input
                  placeholder="Preço (R$)"
                  name="preco"
                  value={form.preco}
                  onChange={handleChange}
                  type="number"
                  min="0"
                  step="0.01"
                />
                {erros.preco && (
                  <p className="text-xs text-red-600">{erros.preco}</p>
                )}
              </div>
              <div>
                <Input
                  placeholder="Duração (minutos)"
                  name="duracao_minutos"
                  value={form.duracao_minutos}
                  onChange={handleChange}
                  type="number"
                  min="1"
                />
                {erros.duracao_minutos && (
                  <p className="text-xs text-red-600">
                    {erros.duracao_minutos}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Checkbox
                id="ativo"
                name="ativo"
                checked={form.ativo}
                onCheckedChange={(checked) =>
                  setForm((f) => ({ ...f, ativo: checked }))
                }
              />
              <label htmlFor="ativo" className="text-sm">
                Serviço Ativo
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
              <Button type="submit">Salvar Serviço</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ServicosPage;
