import { useState, useEffect } from "react";
// CORRIGIDO
import { useApi } from "../../contexts/ApiContext";
import { toast } from "sonner";
// CORRIGIDO
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
import { useNavigate } from "react-router-dom"; // Importar useNavigate

export default function AgendamentoInteligente() {
  const api = useApi();
  const navigate = useNavigate(); // Instanciar useNavigate
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
      toast.error(err.detail || "Erro ao buscar sugestões.");
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
        <Select onValueChange={(val) => setClienteId(val)} value={clienteId}>
          <SelectTrigger>
            <SelectValue placeholder="Selecione cliente" />
          </SelectTrigger>
          <SelectContent>
            {clientes.map((c) => (
              <SelectItem key={c.id} value={String(c.id)}>
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

      {sugestoes.length > 0 && !loading && (
        <div>
          <h2 className="font-semibold mt-4 mb-2">
            Horários disponíveis (duração: {duracao} min)
          </h2>
          <ul className="space-y-2">
            {sugestoes.map((h) => (
              <li
                key={h}
                className="flex items-center justify-between p-2 border rounded"
              >
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
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
                    navigate(
                      `/agendamentos/novo?clienteId=${clienteId}&dataHoraInicio=${h}`
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

      {sugestoes.length === 0 && !loading && data && (
        <p className="mt-4">
          Nenhuma sugestão encontrada para a data selecionada.
        </p>
      )}
    </div>
  );
}
