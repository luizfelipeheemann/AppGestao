from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from schemas.usuario import UsuarioLogin, TokenData
from core.database import get_db
from models import Usuario
from config import settings
from auth.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authenticate_user(email: str, senha: str, db: Session):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verify_password(senha, usuario.senha):
        return None
    return {"email": usuario.email, "user_id": str(usuario.id)}

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "sub": data["email"]})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "sub": data["email"]})
    return jwt.encode(to_encode, settings.refresh_secret, algorithm=settings.algorithm)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return {"email": payload.get("sub"), "user_id": payload.get("user_id")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
