from pydantic import BaseModel
from datetime import datetime
from typing import List

class RelatorioConsumoItem(BaseModel):
    data_uso: datetime
    servico_nome: str

class RelatorioConsumoPacote(BaseModel):
    cliente_nome: str
    pacote_nome: str
    data_compra: datetime
    data_expiracao: datetime
    sessoes_total: int
    sessoes_saldo: int
    status: str
    consumo: List[RelatorioConsumoItem]
