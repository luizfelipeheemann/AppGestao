# Código para o arquivo: backend/schemas/pacote.py
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
# Importa o schema de Serviço para usar na resposta
from .servicos import ServicoOut as ServicoSchema

class PacoteServicoBase(BaseModel):
    nome: str
    quantidade_sessoes: int = Field(..., gt=0)
    validade_dias: int = Field(..., gt=0)
    preco: float

class PacoteServicoCreate(PacoteServicoBase):
    servicos_ids: List[UUID]

class PacoteServicoUpdate(BaseModel):
    nome: Optional[str] = None
    quantidade_sessoes: Optional[int] = Field(None, gt=0)
    validade_dias: Optional[int] = Field(None, gt=0)
    preco: Optional[float] = None
    servicos_ids: Optional[List[UUID]] = None

class PacoteServicoOut(PacoteServicoBase):
    id: UUID
    servicos: List[ServicoSchema] # Usa o schema de serviço para a saída

    class Config:
        # Renomeado de 'orm_mode' para 'from_attributes' para Pydantic V2
        from_attributes = True
