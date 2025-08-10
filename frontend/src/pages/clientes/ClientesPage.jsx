import { useState, useEffect } from "react";
import {
  Plus,
  Search,
  Edit,
  Trash2,
  Phone,
  Mail,
  Package,
  ShoppingBag,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
// CORRIGIDO
import { useApi } from "../../contexts/ApiContext";
import { toast } from "sonner";
// CORRIGIDO
import LoadingSpinner from "../../components/LoadingSpinner";

// Funções utilitárias
function formatarTelefone(valor) {
  let tel = (valor || "").replace(/\D/g, "").slice(0, 11);
  if (tel.length <= 10) {
    return tel.replace(
      /(\d{2})(\d{4})(\d{0,4})/,
      (_, ddd, p1, p2) => `(${ddd}) ${p1}${p2 ? "-" + p2 : ""}`
    );
  }
  return tel.replace(
    /(\d{2})(\d{5})(\d{0,4})/,
    (_, ddd, p1, p2) => `(${ddd}) ${p1}${p2 ? "-" + p2 : ""}`
  );
}

function validarEmail(email) {
  if (!email) return true; // E-mail é opcional
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function normalize(str) {
  return (str || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

const ClientesPage = () => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState(null);
  const [form, setForm] = useState({
    nome: "",
    telefone: "",
    email: "",
    etiquetas: "",
    observacoes: "",
  });
  const [erros, setErros] = useState({});
  const api = useApi();

  // Estados para o modal de pacotes
  const [pacotesModalOpen, setPacotesModalOpen] = useState(false);
  const [venderPacoteModalOpen, setVenderPacoteModalOpen] = useState(false);
  const [clienteSelecionado, setClienteSelecionado] = useState(null);
  const [pacotesDoCliente, setPacotesDoCliente] = useState([]);
  const [pacotesDisponiveis, setPacotesDisponiveis] = useState([]);
  const [pacoteParaVenderId, setPacoteParaVenderId] = useState("");
  const [loadingPacotes, setLoadingPacotes] = useState(false);

  useEffect(() => {
    loadClientes();
  }, []);

  const loadClientes = async () => {
    try {
      setLoading(true);
      const data = await api.clientes.getAll();
      setClientes(data);
    } catch (error) {
      toast.error("Erro ao carregar clientes. Verifique a conexão com a API.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const abrirNovo = () => {
    setEditando(null);
    setForm({
      nome: "",
      telefone: "",
      email: "",
      etiquetas: "",
      observacoes: "",
    });
    setErros({});
    setModalOpen(true);
  };

  const abrirEditar = (cliente) => {
    setEditando(cliente);
    setForm({
      nome: cliente.nome || "",
      telefone: cliente.telefone || "",
      email: cliente.email || "",
      etiquetas: (cliente.etiquetas || []).join(", "),
      observacoes: cliente.observacoes || "",
    });
    setErros({});
    setModalOpen(true);
  };

  const validar = () => {
    let novoErros = {};
    if (!form.nome.trim()) novoErros.nome = "Nome é obrigatório.";
    if (
      !form.telefone.replace(/\D/g, "") ||
      form.telefone.replace(/\D/g, "").length < 10
    )
      novoErros.telefone = "Telefone deve ter pelo menos 10 dígitos.";
    if (!validarEmail(form.email)) novoErros.email = "E-mail inválido.";
    setErros(novoErros);
    return Object.keys(novoErros).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: name === "telefone" ? formatarTelefone(value) : value,
    });
  };

  const salvar = async (e) => {
    e.preventDefault();
    if (!validar()) return;
    const payload = {
      nome: form.nome.trim(),
      telefone: form.telefone.trim(),
      email: form.email.trim() || null,
      observacoes: form.observacoes?.trim() || "",
      etiquetas: (form.etiquetas || "")
        .split(",")
        .map((et) => et.trim())
        .filter((et) => et),
    };

    try {
      if (editando) {
        await api.clientes.update(editando.id, payload);
        toast.success("Cliente atualizado com sucesso!");
      } else {
        await api.clientes.create(payload);
        toast.success("Cliente criado com sucesso!");
      }
      setModalOpen(false);
      loadClientes();
    } catch (error) {
      toast.error(error?.detail || "Erro ao salvar cliente.");
    }
  };

  const excluir = async (cliente) => {
    if (
      !window.confirm(`Deseja realmente remover o cliente "${cliente.nome}"?`)
    )
      return;
    try {
      await api.clientes.delete(cliente.id);
      toast.success("Cliente removido com sucesso!");
      loadClientes();
    } catch (error) {
      toast.error(error?.detail || "Erro ao remover cliente.");
    }
  };

  // Funções para Pacotes conectadas ao Backend
  const abrirModalPacotes = async (cliente) => {
    setClienteSelecionado(cliente);
    setLoadingPacotes(true);
    setPacotesModalOpen(true);
    try {
      // Assumindo que você criará esses métodos no seu ApiContext
      const [pacotesCliente, pacotesTodos] = await Promise.all([
        api.clientes.getPacotes(cliente.id),
        api.pacotes.getAll(),
      ]);
      setPacotesDoCliente(pacotesCliente);
      setPacotesDisponiveis(pacotesTodos);
    } catch (error) {
      toast.error("Erro ao carregar informações de pacotes.");
      setPacotesModalOpen(false);
    } finally {
      setLoadingPacotes(false);
    }
  };

  const handleVenderPacote = async () => {
    if (!pacoteParaVenderId || !clienteSelecionado) {
      toast.warning("Selecione um pacote para vender.");
      return;
    }
    try {
      // O payload deve corresponder ao schema VendaPacoteCreate do backend
      const payload = { pacote_id: parseInt(pacoteParaVenderId) }; // Garante que o ID é um número
      await api.clientes.venderPacote(clienteSelecionado.id, payload);
      toast.success("Pacote vendido com sucesso!");
      setVenderPacoteModalOpen(false);
      setPacoteParaVenderId(""); // Limpa a seleção
      abrirModalPacotes(clienteSelecionado); // Recarrega os pacotes do cliente
    } catch (error) {
      toast.error(error?.detail || "Erro ao vender pacote.");
    }
  };

  const filteredClientes = clientes.filter((c) =>
    normalize(c.nome).includes(normalize(searchTerm))
  );

  if (loading) return <LoadingSpinner text="Carregando clientes..." />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Clientes
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Gerencie seus clientes e informações de contato
          </p>
        </div>
        <Button onClick={abrirNovo}>
          <Plus className="mr-2 h-4 w-4" /> Novo Cliente
        </Button>
      </div>

      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Buscar clientes..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredClientes.map((cliente) => (
          <Card key={cliente.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{cliente.nome}</CardTitle>
                <div className="flex space-x-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => abrirModalPacotes(cliente)}
                    title="Gerenciar Pacotes"
                  >
                    <Package className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => abrirEditar(cliente)}
                    title="Editar Cliente"
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => excluir(cliente)}
                    title="Excluir Cliente"
                  >
                    <Trash2 className="h-4 w-4 text-red-500" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{cliente.telefone}</span>
                </div>
                {cliente.email && (
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{cliente.email}</span>
                  </div>
                )}
                {cliente.etiquetas && cliente.etiquetas.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {cliente.etiquetas.map((tag, i) => (
                      <Badge key={i} variant="secondary">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredClientes.length === 0 && !loading && (
        <div className="text-center py-12">
          <p className="text-gray-500">Nenhum cliente encontrado.</p>
        </div>
      )}

      {/* Modal de Cadastro/Edição de Cliente */}
      <Dialog open={modalOpen} onOpenChange={setModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editando ? "Editar Cliente" : "Novo Cliente"}
            </DialogTitle>
            <DialogDescription>
              Preencha os campos abaixo para {editando ? "editar" : "cadastrar"}{" "}
              o cliente.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={salvar} className="space-y-4 pt-4" autoComplete="off">
            <Input
              placeholder="Nome"
              name="nome"
              value={form.nome}
              onChange={handleChange}
            />
            {erros.nome && <p className="text-xs text-red-600">{erros.nome}</p>}
            <Input
              placeholder="Telefone"
              name="telefone"
              value={form.telefone}
              onChange={handleChange}
              maxLength={15}
            />
            {erros.telefone && (
              <p className="text-xs text-red-600">{erros.telefone}</p>
            )}
            <Input
              placeholder="E-mail (opcional)"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
            />
            {erros.email && (
              <p className="text-xs text-red-600">{erros.email}</p>
            )}
            <Input
              placeholder="Etiquetas (separadas por vírgula)"
              name="etiquetas"
              value={form.etiquetas}
              onChange={handleChange}
            />
            <Input
              placeholder="Observações"
              name="observacoes"
              value={form.observacoes}
              onChange={handleChange}
            />
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setModalOpen(false)}
              >
                Cancelar
              </Button>
              <Button type="submit">Salvar</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Modal para visualizar pacotes do cliente */}
      <Dialog open={pacotesModalOpen} onOpenChange={setPacotesModalOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Pacotes de {clienteSelecionado?.nome}</DialogTitle>
            <DialogDescription>
              Gerencie os pacotes adquiridos pelo cliente.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4 max-h-[60vh] overflow-y-auto">
            {loadingPacotes ? (
              <LoadingSpinner text="Carregando pacotes..." />
            ) : pacotesDoCliente.length > 0 ? (
              pacotesDoCliente.map((p) => (
                <div
                  key={p.id}
                  className="p-3 border rounded-md bg-slate-50 dark:bg-slate-800"
                >
                  <p className="font-semibold">{p.pacote.nome}</p>
                  <div className="flex justify-between items-center mt-2 text-sm text-muted-foreground">
                    <span>
                      Saldo:{" "}
                      <span className="font-bold text-primary">
                        {p.saldo_sessoes}
                      </span>{" "}
                      de {p.pacote.quantidade_sessoes} sessões
                    </span>
                    <span>
                      Expira em:{" "}
                      {new Date(p.data_expiracao).toLocaleDateString("pt-BR")}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-center text-muted-foreground py-8">
                Este cliente não possui pacotes ativos.
              </p>
            )}
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setPacotesModalOpen(false)}
            >
              Fechar
            </Button>
            <Button
              onClick={() => {
                setPacotesModalOpen(false);
                setVenderPacoteModalOpen(true);
              }}
            >
              <ShoppingBag className="mr-2 h-4 w-4" /> Vender Novo Pacote
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Modal para vender um novo pacote */}
      <Dialog
        open={venderPacoteModalOpen}
        onOpenChange={setVenderPacoteModalOpen}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              Vender Pacote para {clienteSelecionado?.nome}
            </DialogTitle>
            <DialogDescription>
              Selecione o pacote que deseja vender.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <label
              htmlFor="pacote-select"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Selecione o Pacote
            </label>
            <select
              id="pacote-select"
              className="w-full p-2 border rounded-md bg-white dark:bg-gray-700"
              onChange={(e) => setPacoteParaVenderId(e.target.value)}
              value={pacoteParaVenderId}
            >
              <option value="">-- Escolha um pacote --</option>
              {pacotesDisponiveis.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nome} -{" "}
                  {Intl.NumberFormat("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  }).format(p.preco)}
                </option>
              ))}
            </select>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setVenderPacoteModalOpen(false)}
            >
              Cancelar
            </Button>
            <Button onClick={handleVenderPacote}>Confirmar Venda</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ClientesPage;
