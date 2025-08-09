import { Badge } from "@/components/ui/badge";
import { Calendar } from "lucide-react";

export default function AgendamentosProximos({
  agendamentos,
  formatDate,
  getStatusBadgeVariant,
}) {
  if (!agendamentos.length) {
    return (
      <p className="text-sm text-muted-foreground text-center py-4">
        Nenhum agendamento próximo.
      </p>
    );
  }
  return (
    <div className="space-y-4">
      {agendamentos.map((ag) => (
        <div key={ag.id} className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
              <Calendar className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="text-sm font-medium">{ag.cliente.nome}</p>
              <p className="text-xs text-muted-foreground">{ag.servico.nome}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm font-medium">
              {formatDate(ag.data_hora_inicio)}
            </p>
            <Badge variant={getStatusBadgeVariant(ag.status)} className="mt-1">
              {ag.status}
            </Badge>
          </div>
        </div>
      ))}
    </div>
  );
}
