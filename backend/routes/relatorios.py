from fastapi import APIRouter, Depends
from typing import List, Optional
from datetime import date
from services.relatorios import get_relatorio_consumo_pacotes_srv
from schemas.relatorio import RelatorioConsumoPacote
from utils.exception_handler import safe_route
from database import get_db

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/consumo-pacotes", response_model=List[RelatorioConsumoPacote])
@safe_route("get_relatorio_consumo_pacotes")
def relatorio_consumo(cliente_id: Optional[str] = None, data_inicio: Optional[date] = None,
                      data_fim: Optional[date] = None, db = Depends(get_db)):
    return get_relatorio_consumo_pacotes_srv(cliente_id, data_inicio, data_fim, db)
