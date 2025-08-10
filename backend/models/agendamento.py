# Código para: backend/models/agendamento.py
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_id = Column(String(36), ForeignKey("clientes.id"), nullable=False, index=True)
    servico_id = Column(String(36), ForeignKey("servicos.id"), nullable=False, index=True)
    data_hora_inicio = Column(DateTime(timezone=True), nullable=False, index=True)
    data_hora_fim = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="confirmado", index=True)
    observacoes = Column(String, nullable=True)

    # Usando strings para quebrar o ciclo de importação
    cliente = relationship("Cliente", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    pagamentos = relationship("Pagamento", back_populates="agendamento", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_agendamentos_data_hora_inicio', 'data_hora_inicio'),
    )
