from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

# Schemas padrão de Agendamento
class AgendamentoBase(BaseModel):
    cliente_id: UUID
    servico_id: UUID
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str = "confirmado"

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(BaseModel):
    cliente_id: Optional[UUID] = None
    servico_id: Optional[UUID] = None
    data_hora_inicio: Optional[datetime] = None
    data_hora_fim: Optional[datetime] = None
    status: Optional[str] = None

class Agendamento(AgendamentoBase):
    id: UUID
    class Config:
        orm_mode = True
