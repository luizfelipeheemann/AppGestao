from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from .shared import BaseModelWithId

class AgendamentoBase(BaseModel):
    cliente_id: UUID
    servico_id: UUID
    data_hora_inicio: datetime
    observacoes: Optional[str] = None
    status: Optional[str] = "confirmado"

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(BaseModel):
    cliente_id: Optional[UUID] = None
    servico_id: Optional[UUID] = None
    data_hora_inicio: Optional[datetime] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

class Agendamento(AgendamentoBase, BaseModelWithId):
    cliente: Optional['Cliente']
    servico: Optional['Servico']
