from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from .shared import BaseModelWithId

class PacoteServicoBase(BaseModel):
    nome: str = Field(..., min_length=2)
    quantidade_sessoes: int = Field(..., ge=1)
    validade_dias: int = Field(..., ge=1)

class PacoteServicoCreate(PacoteServicoBase):
    servicos_ids: List[UUID]

class PacoteServicoUpdate(BaseModel):
    nome: Optional[str] = None
    quantidade_sessoes: Optional[int] = None
    validade_dias: Optional[int] = None
    servicos_ids: Optional[List[UUID]] = None

class PacoteServico(PacoteServicoBase, BaseModelWithId):
    servicos: List['Servico'] = []

class ClientePacote(BaseModelWithId):
    cliente_id: str
    pacote_id: str
    saldo_sessoes: int
    data_compra: datetime
    data_expiracao: datetime
    status: str
    pacote: Optional[PacoteServico]
