from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class VendaPacoteCreate(BaseModel):
    pacote_id: UUID

class ClientePacoteOut(BaseModel):
    id: UUID
    cliente_id: UUID
    pacote_id: UUID
    saldo_sessoes: int
    status: str
    data_compra: datetime
    data_expiracao: datetime
    cliente_nome: Optional[str] = None
    pacote_nome: Optional[str] = None

    class Config:
        orm_mode = True
