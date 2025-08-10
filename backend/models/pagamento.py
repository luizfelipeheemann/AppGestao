# Código para: backend/models/pagamento.py
import uuid
from sqlalchemy import Column, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agendamento_id = Column(String(36), ForeignKey("agendamentos.id"), nullable=False, index=True)
    valor = Column(Float, nullable=False)
    metodo_pagamento = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default="pendente", index=True)
    descricao = Column(Text, nullable=True)
    link_pagamento = Column(String(500), nullable=True)

    # CORREÇÃO: Usando "Agendamento" como string
    agendamento = relationship("Agendamento", back_populates="pagamentos")
