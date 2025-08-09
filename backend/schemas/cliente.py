from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID

class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    observacoes: Optional[str] = Field(None, max_length=1000)
    etiquetas: Optional[List[str]] = Field(default_factory=list)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str]
    telefone: Optional[str]
    email: Optional[EmailStr]
    observacoes: Optional[str]
    etiquetas: Optional[List[str]]

class Cliente(ClienteBase):
    id: UUID

    class Config:
        orm_mode = True
