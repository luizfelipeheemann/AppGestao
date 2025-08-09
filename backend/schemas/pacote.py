from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from .servico import Servico  # certifique-se que este schema exista

class PacoteServicoBase(BaseModel):
    nome: str
    quantidade_sessoes: int = Field(..., gt=0)
    validade_dias: int = Field(..., gt=0)

class PacoteServicoCreate(PacoteServicoBase):
    servicos_ids: List[UUID]

class PacoteServicoUpdate(BaseModel):
    nome: Optional[str]
    quantidade_sessoes: Optional[int] = Field(None, gt=0)
    validade_dias: Optional[int] = Field(None, gt=0)
    servicos_ids: Optional[List[UUID]]

class PacoteServicoOut(PacoteServicoBase):
    id: UUID
    servicos: List[Servico]

    class Config:
        orm_mode = True
