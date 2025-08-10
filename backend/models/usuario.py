# Código para: backend/models/usuario.py
import uuid
from sqlalchemy import Column, String, Boolean, Index
from backend.core.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)

    __table_args__ = (
        Index('ix_usuarios_email', 'email'),
    )

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.senha_hash)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
