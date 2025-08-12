from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

# ===== ADICIONADO: Schema para cadastro de usuário =====
class UsuarioRegister(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    confirmar_senha: str
# ===== FIM DA ADIÇÃO =====

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

class UsuarioOut(BaseModel):
    user_id: UUID
    email: EmailStr
    nome: Optional[str]

# ===== ADICIONADO: Schema para resposta de cadastro =====
class UsuarioCreated(BaseModel):
    id: str
    nome: str
    email: EmailStr
    message: str = "Usuário criado com sucesso"
# ===== FIM DA ADIÇÃO =====
