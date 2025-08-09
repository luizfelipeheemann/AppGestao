from pydantic import BaseModel
from typing import Optional

class DashboardStats(BaseModel):
    totalClientes: int
    clientesNoMes: int
    agendamentosHoje: int
    servicosAtivos: int
    receitaMes: float
