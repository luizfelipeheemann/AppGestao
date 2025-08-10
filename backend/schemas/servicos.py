from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class ServicoBase(BaseModel):
    nome: str = Field(..., min_length=2)
    duracao_minutos: int = Field(..., gt=0)
    preco: float = Field(..., ge=0.0)
    ativo: bool = True

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    duracao_minutos: Optional[int] = Field(None, gt=0)
    preco: Optional[float] = Field(None, ge=0.0)
    ativo: Optional[bool] = None

# Renomeado de 'Servico' para 'ServicoOut' para padronização
class ServicoOut(ServicoBase):
    id: UUID

    class Config:
        # Renomeado de 'orm_mode' para 'from_attributes' para Pydantic V2
        from_attributes = True
