from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Any

# --- Importações Corrigidas ---
# Todas as importações agora são absolutas a partir da raiz do projeto.
from backend.services.auth import authenticate_user, create_access_token, create_refresh_token
# ===== ADICIONADO: Import da função de criação de usuário =====
from backend.services.auth import create_user
# ===== FIM DA ADIÇÃO =====
from backend.auth.security import get_current_user # Assumindo que get_current_user está em auth/security.py
from backend.auth.rate_limiter import auth_rate_limiter # Assumindo que o rate limiter está em auth/rate_limiter.py
# ===== MODIFICADO: Importar novos schemas =====
from backend.schemas.auth import UsuarioLogin, UsuarioRegister, Token, UsuarioCreated
# ===== FIM DA MODIFICAÇÃO =====
from utils.exception_handler import safe_route
from backend.core.database import get_db # Importa o get_db
from sqlalchemy.orm import Session # Importa a Session
# ===== ADICIONADO: Import do modelo de usuário =====
from backend.models.usuario import Usuario as UsuarioDB
# ===== FIM DA ADIÇÃO =====
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

# ===== ADICIONADO: Endpoint de cadastro =====
@router.post("/register", response_model=UsuarioCreated, status_code=status.HTTP_201_CREATED)
@safe_route("register")
async def register(
    user_data: UsuarioRegister,
    db: Session = Depends(get_db)
) -> Any:
    # Validar se as senhas coincidem
    if user_data.senha != user_data.confirmar_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="As senhas não coincidem"
        )
    
    # Verificar se o email já existe
    existing_user = db.query(UsuarioDB).filter(UsuarioDB.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar o usuário
    new_user = create_user(db=db, user_data=user_data)
    
    return UsuarioCreated(
        id=str(new_user.id),
        nome=new_user.nome,
        email=new_user.email
    )
# ===== FIM DA ADIÇÃO =====

@router.get("/me", response_model=dict)
@safe_route("me")
async def me(current_user: dict = Depends(get_current_user)):
    # Esta rota provavelmente precisará de ajustes dependendo do que get_current_user retorna
    return current_user
