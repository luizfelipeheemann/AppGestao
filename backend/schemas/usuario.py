from pydantic import BaseModel, EmailStr

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
