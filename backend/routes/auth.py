from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Any
from auth import authenticate_user, create_access_token, create_refresh_token, get_current_user, auth_rate_limiter
from schemas.usuario import UsuarioLogin, Token
from utils.exception_handler import safe_route

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
@safe_route("login")
async def login(user_credentials: UsuarioLogin, request: Request) -> Any:
    client_ip = request.client.host
    if auth_rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts."
        )
    user = authenticate_user(user_credentials.email, user_credentials.senha)
    if not user:
        auth_rate_limiter.record_attempt(client_ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")
    access_token = create_access_token(data={"sub": user["email"], "user_id": user["user_id"]})
    refresh_token = create_refresh_token(data={"sub": user["email"], "user_id": user["user_id"]})
    return Token(access_token=access_token, refresh_token=refresh_token, expires_in=access_token.expires_in if hasattr(access_token, 'expires_in') else 0)

@router.get("/me", response_model=dict)
@safe_route("me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user
