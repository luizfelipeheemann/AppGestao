import { useState, useEffect } from "react";
import { useApi } from "../../contexts/ApiContext";
import { toast } from "sonner";
import LoadingSpinner from "../../components/LoadingSpinner";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Calendar } from "lucide-react";

export default function AgendamentoInteligente() {
  const api = useApi();
  const [clientes, setClientes] = useState([]);
  const [clienteId, setClienteId] = useState("");
  const [data, setData] = useState("");
  const [sugestoes, setSugestoes] = useState([]);
  const [duracao, setDuracao] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.clientes
      .getAll()
      .then(setClientes)
      .catch(() => toast.error("Erro ao carregar clientes."));
  }, [api.clientes]);

  const buscarSugestoes = async () => {
    if (!clienteId || !data) {
      return toast.error("Selecione cliente e data.");
    }
    setLoading(true);
    try {
      const resp = await api.agendamentoInteligente.sugerir(clienteId, data);
      setSugestoes(resp.horarios);
      setDuracao(resp.duracao_minutos);
    } catch (err) {
      toast.error(err.message || "Erro ao buscar sugestões.");
      setSugestoes([]);
      setDuracao(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Agendamento Inteligente</h1>
      <div className="flex gap-2 items-center">
        <Select onValueChange={setClienteId} value={clienteId}>
          <SelectTrigger>
            <SelectValue placeholder="Selecione cliente" />
          </SelectTrigger>
          <SelectContent>
            {clientes.map((c) => (
              <SelectItem key={c.id} value={c.id}>
                {c.nome}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <input
          type="date"
          value={data}
          onChange={(e) => setData(e.target.value)}
          className="p-2 border rounded"
        />
        <Button onClick={buscarSugestoes}>Buscar Horários</Button>
      </div>

      {loading && <LoadingSpinner text="Buscando horários..." />}

      {sugestoes.length > 0 && (
        <div>
          <h2>Horários disponíveis (duração: {duracao} min)</h2>
          <ul className="space-y-2">
            {sugestoes.map((h) => (
              <li
                key={h}
                className="flex items-center justify-between p-2 border rounded"
              >
                <div className="flex items-center gap-2">
                  <Calendar />
                  {new Intl.DateTimeFormat("pt-BR", {
                    day: "2-digit",
                    month: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                  }).format(new Date(h))}
                </div>
                <Button
                  variant="secondary"
                  onClick={() =>
                    api.navigate(
                      `/agendamentos?cliente=${clienteId}&inicio=${h}`
                    )
                  }
                >
                  Agendar
                </Button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {sugestoes.length === 0 && !loading && (
        <p>Nenhuma sugestão encontrada.</p>
      )}
    </div>
  );
}
