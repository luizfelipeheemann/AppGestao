import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Sistema de Gestão"
    is_production: bool = os.getenv("ENV") == "production"
    access_token_expire_minutes: int = 60 * 24  # 1 dia
    allowed_origins_list: list = ["http://localhost:5173"]
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
