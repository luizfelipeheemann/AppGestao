from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

# --- Importações Corrigidas ---
from backend.core.database import get_db
from backend.services.clientes_pacotes import vender_pacote_srv, listar_pacotes_do_cliente_srv
from backend.schemas.cliente_pacote import VendaPacoteCreate, ClientePacoteOut
from utils.exception_handler import safe_route
# --- Fim das Importações Corrigidas ---

router = APIRouter(prefix="/clientes/{cliente_id}/pacotes", tags=["Clientes Pacotes"])

@router.post("", response_model=ClientePacoteOut, status_code=status.HTTP_201_CREATED)
@safe_route("vender_pacote_para_cliente")
def vender_pacote(cliente_id: UUID, venda: VendaPacoteCreate, db: Session = Depends(get_db)):
    # A lógica agora está na camada de serviço
    return vender_pacote_srv(db=db, cliente_id=cliente_id, venda_data=venda)

@router.get("", response_model=List[ClientePacoteOut])
@safe_route("listar_pacotes_do_cliente")
def listar_pacotes(cliente_id: UUID, db: Session = Depends(get_db)):
    # A lógica agora está na camada de serviço
    return listar_pacotes_do_cliente_srv(db=db, cliente_id=cliente_id)
