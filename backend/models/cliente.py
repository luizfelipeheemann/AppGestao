# Código para o arquivo: backend/models/cliente.py
import uuid
from sqlalchemy import Column, String, Text, Index
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True, index=True)
    observacoes = Column(Text, nullable=True)
    etiquetas = Column(Text, nullable=True)

    agendamentos = relationship("Agendamento", back_populates="cliente", cascade="all, delete-orphan")
    pacotes_adquiridos = relationship("ClientePacote", back_populates="cliente", cascade="all, delete-orphan")
