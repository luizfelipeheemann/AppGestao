from datetime import datetime
from typing import List
from pydantic import BaseModel

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
    status: str  # idealmente substituir por Enum
    consumo: List[RelatorioConsumoItem]

    class Config:
        orm_mode = True
