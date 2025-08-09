from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    # Configuração do banco de dados
    database_url: str = "sqlite:///./app.db"
    
    # Segurança
    secret_key: str = "dev-secret-key-change-in-production-12345678901234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS
    allowed_origins: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
    
    # Ambiente
    environment: str = "development"
    
    # Log
    log_level: str = "INFO"
    
    # OpenTelemetry
    otel_service_name: str = "professional-management-api"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        if isinstance(self.allowed_origins, str):
            return [origin.strip() for origin in self.allowed_origins.split(",")]
        return self.allowed_origins
    
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"
    
    def validate_secret_key(self):
        if self.is_production and self.secret_key == "dev-secret-key-change-in-production-12345678901234567890":
            raise ValueError("Secret key padrão não permitido em produção")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings()
settings.validate_secret_key()
print(f"SECRET_KEY carregada: {settings.secret_key}")