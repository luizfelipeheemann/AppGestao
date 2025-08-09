from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

class UsuarioOut(BaseModel):
    user_id: UUID
    email: EmailStr
    nome: Optional[str]
