from pydantic import BaseModel, EmailStr, Field

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
