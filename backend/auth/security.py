from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

# --- Importações Corrigidas ---
from backend.core.database import get_db
from backend.services.auth import verify_token
from backend.schemas.usuario import TokenData
from backend.models.usuario import Usuario as UsuarioDB
# --- Fim das Importações Corrigidas ---

# Esta linha cria o "esquema" de segurança. 
# O FastAPI usará o 'tokenUrl' para mostrar um botão "Authorize" na documentação /docs.
# Ele espera que o token seja enviado no cabeçalho "Authorization: Bearer <seu_token>".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> UsuarioDB:
    """
    Dependência do FastAPI para obter o usuário atual a partir de um token JWT.
    1. Extrai o token da requisição.
    2. Verifica se o token é válido.
    3. Busca o usuário no banco de dados.
    4. Retorna o objeto do usuário ou lança uma exceção HTTP.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
        
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
        
    # Valida o payload com o schema Pydantic
    token_data = TokenData(user_id=user_id)
    
    user = db.query(UsuarioDB).filter(UsuarioDB.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_active_user(
    current_user: UsuarioDB = Depends(get_current_user)
) -> UsuarioDB:
    """
    Dependência que verifica se o usuário obtido de get_current_user está ativo.
    """
    if not current_user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user
