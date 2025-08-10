import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
// CORRIGIDO
import LoadingSpinner from "../../components/LoadingSpinner";
import { toast } from "sonner";
// CORRIGIDO
import { useApi } from "../../contexts/ApiContext";

export default function NovoAgendamentoPage() {
  const api = useApi();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [clientes, setClientes] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [form, setForm] = useState({
    cliente_id: "",
    servico_id: "",
    data_hora_inicio: "",
    data_hora_fim: "",
    status: "confirmado",
    observacoes: "",
  });
  const [loading, setLoading] = useState(true);
  const [erros, setErros] = useState({});

  // Função para converter data para o formato do input datetime-local
  const toLocalISOString = (date) => {
    const tzoffset = new Date().getTimezoneOffset() * 60000;
    const localISOTime = new Date(new Date(date) - tzoffset)
      .toISOString()
      .slice(0, -1);
    return localISOTime.slice(0, 16);
  };

  useEffect(() => {
    async function load() {
      try {
        const [c, s] = await Promise.all([
          api.clientes.getAll(),
          api.servicos.getAll(),
        ]);
        setClientes(c);
        setServicos(s.filter((serv) => serv.ativo));

        // Preencher formulário com dados da URL (vindo do agendamento inteligente)
        const clienteIdParam = searchParams.get("clienteId");
        const dataHoraInicioParam = searchParams.get("dataHoraInicio");

        if (clienteIdParam) {
          setForm((prev) => ({ ...prev, cliente_id: clienteIdParam }));
        }
        if (dataHoraInicioParam) {
          setForm((prev) => ({
            ...prev,
            data_hora_inicio: toLocalISOString(dataHoraInicioParam),
          }));
        }
      } catch {
        toast.error("Erro ao carregar dados para o agendamento.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [api, searchParams]);

  const handleChange = (name, value) => {
    const novoForm = { ...form, [name]: value };
    if (
      (name === "servico_id" || name === "data_hora_inicio") &&
      novoForm.servico_id &&
      novoForm.data_hora_inicio
    ) {
      const servicoSelecionado = servicos.find(
        (s) => s.id === parseInt(novoForm.servico_id)
      );
      if (servicoSelecionado) {
        const inicio = new Date(novoForm.data_hora_inicio);
        const fim = new Date(
          inicio.getTime() + servicoSelecionado.duracao_minutos * 60000
        );
        novoForm.data_hora_fim = toLocalISOString(fim);
      }
    }
    setForm(novoForm);
  };

  const validar = () => {
    const e = {};
    if (!form.cliente_id) e.cliente_id = "Selecione um cliente.";
    if (!form.servico_id) e.servico_id = "Selecione um serviço.";
    if (!form.data_hora_inicio)
      e.data_hora_inicio = "Data e hora de início são obrigatórios.";
    setErros(e);
    return Object.keys(e).length === 0;
  };

  const salvar = async (e) => {
    e.preventDefault();
    if (!validar()) return;
    setLoading(true);
    try {
      const payload = {
        ...form,
        cliente_id: parseInt(form.cliente_id),
        servico_id: parseInt(form.servico_id),
        data_hora_inicio: new Date(form.data_hora_inicio).toISOString(),
        data_hora_fim: new Date(form.data_hora_fim).toISOString(),
      };
      await api.agendamentos.create(payload);
      toast.success("Agendamento criado com sucesso!");
      navigate("/agendamentos");
    } catch (err) {
      toast.error(err.detail || "Erro ao salvar agendamento.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner text="Carregando formulário..." />;
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Novo Agendamento</CardTitle>
          <CardDescription>
            Preencha os detalhes abaixo para criar um novo agendamento.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={salvar}>
            <div>
              <Select
                value={form.cliente_id}
                onValueChange={(v) => handleChange("cliente_id", v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o Cliente" />
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
                value={form.servico_id}
                onValueChange={(v) => handleChange("servico_id", v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o Serviço" />
                </SelectTrigger>
                <SelectContent>
                  {servicos.map((s) => (
                    <SelectItem key={s.id} value={String(s.id)}>
                      {s.nome} – R$ {s.preco.toFixed(2)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {erros.servico_id && (
                <p className="text-xs text-red-600 mt-1">{erros.servico_id}</p>
              )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Início</label>
                <Input
                  type="datetime-local"
                  value={form.data_hora_inicio}
                  onChange={(e) =>
                    handleChange("data_hora_inicio", e.target.value)
                  }
                />
                {erros.data_hora_inicio && (
                  <p className="text-xs text-red-600 mt-1">
                    {erros.data_hora_inicio}
                  </p>
                )}
              </div>
              <div>
                <label className="text-sm font-medium">Fim (automático)</label>
                <Input
                  type="datetime-local"
                  value={form.data_hora_fim}
                  readOnly
                  className="bg-gray-100 dark:bg-gray-800"
                />
              </div>
            </div>
            <div>
              <Textarea
                placeholder="Observações (opcional)"
                value={form.observacoes}
                onChange={(e) => handleChange("observacoes", e.target.value)}
              />
            </div>
            <div className="flex justify-end gap-2 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(-1)}
              >
                Cancelar
              </Button>
              <Button type="submit" disabled={loading}>
                {loading ? "Salvando..." : "Criar Agendamento"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
