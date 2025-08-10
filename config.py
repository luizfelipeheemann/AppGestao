# Código para: config.py
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    # Configuração do banco de dados
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Segurança
    SECRET_KEY: str = "dev-secret-key-change-in-production-12345678901234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
    
    # Ambiente
    ENVIRONMENT: str = "development"
    
    # Log (CORRIGIDO de LOG_LEVEL para log_level )
    log_level: str = "INFO"
    
    # OpenTelemetry
    OTEL_SERVICE_NAME: str = "professional-management-api"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    
    @property
    def allowed_origins_list(self ) -> List[str]:
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return self.ALLOWED_ORIGINS
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    def validate_secret_key(self):
        if self.is_production and self.SECRET_KEY == "dev-secret-key-change-in-production-12345678901234567890":
            raise ValueError("Secret key padrão não permitido em produção")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instância global das configurações
settings = Settings()
settings.validate_secret_key()
