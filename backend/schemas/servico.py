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
    nome: Optional[str]
    duracao_minutos: Optional[int] = Field(None, gt=0)
    preco: Optional[float] = Field(None, ge=0.0)
    ativo: Optional[bool]

class Servico(ServicoBase):
    id: UUID

    class Config:
        orm_mode = True
