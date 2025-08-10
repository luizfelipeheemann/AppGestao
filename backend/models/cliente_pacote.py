# Código para o arquivo: backend/models/cliente_pacote.py
import uuid
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class ClientePacote(Base):
    __tablename__ = "cliente_pacotes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False, index=True)
    pacote_id = Column(String(36), ForeignKey("pacotes_servicos.id"), nullable=False, index=True)
    data_compra = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_expiracao = Column(DateTime(timezone=True), nullable=False)
    saldo_sessoes = Column(Integer, nullable=False)
    status = Column(String(20), default="ativo", index=True)

    cliente = relationship("Cliente", back_populates="pacotes_adquiridos")
    pacote = relationship("PacoteServico", back_populates="compras")
