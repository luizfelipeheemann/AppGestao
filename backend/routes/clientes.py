from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

# --- Importações Corrigidas ---
from backend.services.clientes import listar_clientes_srv, criar_cliente_srv, atualizar_cliente_srv, excluir_cliente_srv
# Renomeei o schema de saída para ClienteOut para evitar conflito com o nome do modelo
from backend.schemas.cliente import Cliente as ClienteOut, ClienteCreate, ClienteUpdate
from utils.exception_handler import safe_route
from backend.core.database import get_db
# --- Fim das Importações Corrigidas ---

router = APIRouter() # O prefixo e as tags já são definidos no __init__.py das rotas

@router.get("", response_model=List[ClienteOut])
@safe_route("listar_clientes")
def listar_clientes(
    db: Session = Depends(get_db),
    limit: Optional[int] = None, 
    sort: Optional[str] = None
):
    return listar_clientes_srv(db=db, limit=limit, sort=sort)

@router.post("", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
@safe_route("criar_cliente")
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return criar_cliente_srv(db=db, cliente_data=cliente)

@router.put("/{cliente_id}", response_model=ClienteOut)
@safe_route("atualizar_cliente")
def atualizar_cliente(cliente_id: UUID, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    return atualizar_cliente_srv(db=db, cliente_id=cliente_id, cliente_data=cliente)

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
@safe_route("excluir_cliente")
def excluir_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    excluir_cliente_srv(db=db, cliente_id=cliente_id)
    # Retorna None, pois o status é 204 No Content
    return None
