import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
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
import LoadingSpinner from "../../components/LoadingSpinner";
import { toast } from "sonner";
import { useApi } from "../../contexts/ApiContext";

export default function NovoAgendamento({
  initialData = null,
  onClose = () => {},
  onSaved = () => {},
}) {
  const api = useApi();
  const [clientes, setClientes] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [form, setForm] = useState(
    initialData || {
      cliente_id: "",
      servico_id: "",
      data_hora_inicio: "",
      data_hora_fim: "",
      status: "confirmado",
      observacoes: "",
    }
  );
  const [loading, setLoading] = useState(true);
  const [erros, setErros] = useState({});

  useEffect(() => {
    async function load() {
      try {
        const [c, s] = await Promise.all([
          api.clientes.getAll(),
          api.servicos.getAll(),
        ]);
        setClientes(c);
        setServicos(s);
      } catch {
        toast.error("Erro ao carregar dados.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [api]);

  const handleChange = (name, value) => {
    const novo = { ...form, [name]: value };
    if (
      (name === "servico_id" || name === "data_hora_inicio") &&
      novo.servico_id &&
      novo.data_hora_inicio
    ) {
      const sel = servicos.find((s) => s.id === novo.servico_id);
      if (sel) {
        const inicio = new Date(novo.data_hora_inicio);
        novo.data_hora_fim = new Date(
          inicio.getTime() + sel.duracao_minutos * 60000
        )
          .toISOString()
          .slice(0, 16);
      }
    }
    setForm(novo);
  };

  const validar = () => {
    const e = {};
    if (!form.cliente_id) e.cliente_id = "Selecione cliente.";
    if (!form.servico_id) e.servico_id = "Selecione serviço.";
    if (!form.data_hora_inicio)
      e.data_hora_inicio = "Data/hora de início é obrigatória.";
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
        data_hora_inicio: new Date(form.data_hora_inicio).toISOString(),
        data_hora_fim: new Date(form.data_hora_fim).toISOString(),
      };
      if (initialData) {
        await api.agendamentos.update(initialData.id, payload);
      } else {
        await api.agendamentos.create(payload);
      }
      toast.success("Agendamento salvo!");
      onSaved();
      onClose();
    } catch (err) {
      toast.error(err.detail || "Erro ao salvar agendamento.");
      setLoading(false);
    }
  };

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {initialData ? "Editar Agendamento" : "Novo Agendamento"}
          </DialogTitle>
        </DialogHeader>
        {loading ? (
          <LoadingSpinner text="Carregando..." />
        ) : (
          <form className="space-y-4 pt-4" onSubmit={salvar}>
            <div>
              <Select
                value={form.cliente_id}
                onValueChange={(v) => handleChange("cliente_id", v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Cliente" />
                </SelectTrigger>
                <SelectContent>
                  {clientes.map((c) => (
                    <SelectItem key={c.id} value={c.id}>
                      {c.nome}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {erros.cliente_id && (
                <p className="text-xs text-red-600">{erros.cliente_id}</p>
              )}
            </div>
            <div>
              <Select
                value={form.servico_id}
                onValueChange={(v) => handleChange("servico_id", v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Serviço" />
                </SelectTrigger>
                <SelectContent>
                  {servicos.map((s) => (
                    <SelectItem key={s.id} value={s.id}>
                      {s.nome} – R$ {s.preco.toFixed(2)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {erros.servico_id && (
                <p className="text-xs text-red-600">{erros.servico_id}</p>
              )}
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label>Início</label>
                <Input
                  type="datetime-local"
                  value={form.data_hora_inicio}
                  onChange={(e) =>
                    handleChange("data_hora_inicio", e.target.value)
                  }
                />
                {erros.data_hora_inicio && (
                  <p className="text-xs text-red-600">
                    {erros.data_hora_inicio}
                  </p>
                )}
              </div>
              <div>
                <label>Fim (automático)</label>
                <Input
                  type="datetime-local"
                  value={form.data_hora_fim}
                  readOnly
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
            <DialogFooter>
              <Button variant="outline" onClick={onClose}>
                Cancelar
              </Button>
              <Button type="submit">
                {initialData ? "Atualizar" : "Criar"}
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog>
  );
}
