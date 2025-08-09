from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import Dict
import jwt
from config import settings
from models import Usuario as UsuarioDB
from database import get_db
from schemas.usuario import Token, UsuarioLogin

SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_EXPIRE_MINUTES = settings.access_token_expire_minutes

def authenticate_user(email: str, senha: str) -> Dict:
    db = next(get_db())
    user = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    if not user or not user.verify_password(senha):
        return None
    return {"user_id": str(user.id), "email": user.email}

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
