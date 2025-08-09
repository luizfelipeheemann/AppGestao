from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from logging_config import get_logger
import uuid
from functools import lru_cache

# Logger para este módulo
logger = get_logger("auth")

# Contexto para hashing de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança para obter o token Bearer do cabeçalho Authorization
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto plano."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(datetime.utcnow().timestamp()),
        "type": "access",
        "jti": str(uuid.uuid4()),
    })
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    logger.info("Token de acesso criado", user_email=data.get("sub"), expires_at=expire.isoformat())
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Cria um token JWT de refresh."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(datetime.utcnow().timestamp()),
        "type": "refresh",
        "jti": str(uuid.uuid4()),
    })
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    logger.info("Token de refresh criado", user_email=data.get("sub"), expires_at=expire.isoformat())
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verifica e decodifica o token JWT, validando tipo e expiração."""
    try:
        logger.debug(f"Verificando token: {token[:10]}... (truncado para log)")
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        logger.debug(f"Token decodificado: {payload}")
        if payload.get("type") != token_type:
            logger.warning(f"Tipo de token inválido: esperado={token_type}, recebido={payload.get('type')}")
            return None
        exp = payload.get("exp")
        if exp is None or datetime.utcnow().timestamp() > exp:
            logger.warning(f"Token expirado: exp={exp}, atual={datetime.utcnow().timestamp()}")
            return None
        return payload
    except JWTError as e:
        logger.error(f"Falha na verificação do JWT: {str(e)}")
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependência FastAPI para obter o usuário atual a partir do token JWT.
    Valida o token e extrai as informações do usuário.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token, "access")
    
    if payload is None:
        logger.warning("Token inválido ou expirado fornecido para autenticação.")
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        logger.warning("Token não contém o 'subject' (email).")
        raise credentials_exception
        
    logger.info("Usuário autenticado via token", user_email=email)
    return {"email": email, "user_id": payload.get("user_id")}

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """
    Verifica se o usuário está ativo. Pode ser estendido para checar no banco de dados.
    """
    return current_user

# Geração de hash automática para demo-user (para DEV)
@lru_cache()
def get_demo_password_hash():
    if settings.is_production:
        raise RuntimeError("Usuário demo não permitido em produção")
    return get_password_hash("123456")

def authenticate_user(email: str, password: str) -> Union[dict, bool]:
    """
    Autentica um usuário com email e senha.
    Esta função simula a busca de um usuário no banco de dados.
    """
    if settings.is_production:
        logger.warning("Tentativa de autenticação com usuário demo em produção")
        return False
    
    demo_users = {
        "joao@exemplo.com": {
            "email": "joao@exemplo.com",
            "hashed_password": get_demo_password_hash(),
            "nome": "João Silva",
            "ativo": True,
            "user_id": "demo-user-id"
        }
    }
    user = demo_users.get(email)
    if not user:
        logger.warning("Tentativa de login para usuário não encontrado", email=email)
        return False

    if not verify_password(password, user["hashed_password"]):
        logger.warning("Senha inválida para o usuário", email=email)
        return False

    if not user.get("ativo", True):
        logger.warning("Usuário inativo tentou login", email=email)
        return False

    logger.info("Usuário autenticado com sucesso via senha", email=email)
    return user

# Implementação básica de rate limiter para autenticação
class AuthRateLimiter:
    """Limita o número de tentativas de login para um identificador."""
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        self.attempts = {}
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes

    def is_rate_limited(self, identifier: str) -> bool:
        """Verifica se o identificador excedeu o limite de tentativas."""
        now = datetime.utcnow()
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        cutoff = now - timedelta(minutes=self.window_minutes)
        self.attempts[identifier] = [attempt for attempt in self.attempts[identifier] if attempt > cutoff]
        
        return len(self.attempts[identifier]) >= self.max_attempts

    def record_attempt(self, identifier: str):
        """Registra uma nova tentativa de login."""
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        self.attempts[identifier].append(datetime.utcnow())

# Instância global para limitar tentativas de autenticação
auth_rate_limiter = AuthRateLimiter()