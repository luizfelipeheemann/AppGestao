from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from uuid import UUID

# --- Importações Corrigidas ---
from backend.core.database import get_db
from backend.services.relatorios import get_relatorio_consumo_pacotes_srv
from backend.schemas.relatorio import RelatorioConsumoPacote
from utils.exception_handler import safe_route
# --- Fim das Importações Corrigidas ---

router = APIRouter() # O prefixo e as tags já são definidos no __init__.py das rotas

@router.get("/consumo-pacotes", response_model=List[RelatorioConsumoPacote])
@safe_route("get_relatorio_consumo_pacotes")
def relatorio_consumo(
    db: Session = Depends(get_db),
    cliente_id: Optional[UUID] = None, 
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    return get_relatorio_consumo_pacotes_srv(
        db=db, 
        cliente_id=cliente_id, 
        data_inicio=data_inicio, 
        data_fim=data_fim
    )
