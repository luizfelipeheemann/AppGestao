from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Any

# --- Importações Corrigidas ---
# Todas as importações agora são absolutas a partir da raiz do projeto.
from backend.services.auth import authenticate_user, create_access_token, create_refresh_token
from backend.auth.security import get_current_user # Assumindo que get_current_user está em auth/security.py
from backend.auth.rate_limiter import auth_rate_limiter # Assumindo que o rate limiter está em auth/rate_limiter.py
from backend.schemas.usuario import UsuarioLogin, Token
from utils.exception_handler import safe_route
from backend.core.database import get_db # Importa o get_db
from sqlalchemy.orm import Session # Importa a Session
# --- Fim das Importações Corrigidas ---

router = APIRouter() # O prefixo e as tags já são definidos no __init__.py das rotas

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
@safe_route("login")
async def login(
    user_credentials: UsuarioLogin, 
    request: Request,
    db: Session = Depends(get_db) # Injeta a dependência do banco de dados
) -> Any:
    client_ip = request.client.host
    if auth_rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Tente novamente mais tarde."
        )
    
    # A função de serviço agora recebe a sessão 'db'
    user = authenticate_user(db=db, email=user_credentials.email, senha=user_credentials.senha)
    
    if not user:
        auth_rate_limiter.record_attempt(client_ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")
    
    # O 'user' retornado pelo serviço é um objeto SQLAlchemy, então acessamos os atributos com '.'
    access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": user.email, "user_id": str(user.id)})
    
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=dict)
@safe_route("me")
async def me(current_user: dict = Depends(get_current_user)):
    # Esta rota provavelmente precisará de ajustes dependendo do que get_current_user retorna
    return current_user
