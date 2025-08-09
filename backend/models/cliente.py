from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
import re
from .shared import BaseModelWithId

class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    observacoes: Optional[str] = Field(None, max_length=1000)
    etiquetas: Optional[List[str]] = []

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    telefone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    observacoes: Optional[str] = Field(None, max_length=1000)
    etiquetas: Optional[List[str]] = None

    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, v):
        if v is not None:
            digits_only = re.sub(r'\D', '', v)
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError('Telefone deve ter entre 10 e 15 dígitos')
        return v

class Cliente(ClienteBase, BaseModelWithId):
    pass