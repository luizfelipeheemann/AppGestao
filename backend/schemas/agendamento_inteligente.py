from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class AgendamentoSugestao(BaseModel):
    horarios: List[datetime]
    duracao_minutos: int
    ultimo_servico_id: Optional[str] = None

class RepetirAgendamentoRequest(BaseModel):
    cliente_id: UUID
    data: datetime

class ErroAgendamento(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)
