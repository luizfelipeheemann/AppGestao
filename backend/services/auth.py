from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional
import jwt

# --- Importações Corrigidas ---
from config import settings
from backend.models.usuario import Usuario as UsuarioDB
# ===== ADICIONADO: Import do schema de registro =====
from backend.schemas.auth import UsuarioRegister
# ===== FIM DA ADIÇÃO =====
# --- Fim das Importações Corrigidas ---

# As constantes agora usam os nomes padronizados do nosso config.py
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

def authenticate_user(db: Session, email: str, senha: str) -> Optional[UsuarioDB]:
    """
    Busca um usuário no banco de dados pelo email e verifica sua senha.
    Retorna o objeto do usuário se for bem-sucedido, caso contrário, None.
    """
    user = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    # Verifica se o usuário existe e se a senha está correta
    if not user or not user.verify_password(senha):
        return None
    return user

# ===== ADICIONADO: Função para criar usuário =====
def create_user(db: Session, user_data: UsuarioRegister) -> UsuarioDB:
    """
    Cria um novo usuário no banco de dados.
    """
    # Criar hash da senha
    senha_hash = UsuarioDB.get_password_hash(user_data.senha)
    
    # Criar objeto do usuário
    db_user = UsuarioDB(
        nome=user_data.nome,
        email=user_data.email,
        senha_hash=senha_hash,
        ativo=True
    )
    
    # Salvar no banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
# ===== FIM DA ADIÇÃO =====

def create_access_token(data: dict) -> str:
    """Cria um novo token de acesso."""
    to_encode = data.copy()
    # Usa timezone.utc para garantir que o tempo seja timezone-aware
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Cria um novo refresh token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """Verifica um token e retorna o payload se for válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # Trata ambos os erros de token inválido ou expirado da mesma forma
        return None
