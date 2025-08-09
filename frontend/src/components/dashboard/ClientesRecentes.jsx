import { Badge } from "@/components/ui/badge";

export default function ClientesRecentes({ clientes }) {
  if (!clientes.length) {
    return (
      <p className="text-sm text-muted-foreground text-center py-4">
        Nenhum cliente cadastrado ainda.
      </p>
    );
  }
  return (
    <div className="space-y-4">
      {clientes.map((cliente) => (
        <div key={cliente.id} className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
              <span className="font-semibold text-primary">
                {cliente.nome.charAt(0)}
              </span>
            </div>
            <div>
              <p className="text-sm font-medium">{cliente.nome}</p>
              <p className="text-xs text-muted-foreground">
                {cliente.telefone}
              </p>
            </div>
          </div>
          <div className="flex space-x-1">
            {cliente.etiquetas?.map((tag, i) => (
              <Badge key={i} variant="secondary">
                {tag}
              </Badge>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
