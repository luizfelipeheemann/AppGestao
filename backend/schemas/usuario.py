# Código para: backend/schemas/usuario.py
from pydantic import BaseModel, EmailStr

# Schema para os dados de login que a API recebe
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

# Schema para o token que a API retorna
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer" # Adicionado para seguir o padrão OAuth2

# Schema para os dados do token decodificado
class TokenData(BaseModel):
    email: str | None = None
    user_id: str | None = None
