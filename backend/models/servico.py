from pydantic import BaseModel, Field
from typing import Optional
from .shared import BaseModelWithId

class ServicoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=1000)
    preco: float = Field(..., gt=0)
    duracao: int = Field(..., gt=0)
    ativo: Optional[bool] = True

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    duracao: Optional[int] = None
    ativo: Optional[bool] = None

class Servico(ServicoBase, BaseModelWithId):
    pass