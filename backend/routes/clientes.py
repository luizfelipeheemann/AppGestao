from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from services.clientes import listar_clientes_srv, criar_cliente_srv, atualizar_cliente_srv, excluir_cliente_srv
from schemas.cliente import Cliente, ClienteCreate, ClienteUpdate
from utils.exception_handler import safe_route
from database import get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("", response_model=List[Cliente])
@safe_route("listar_clientes")
def listar_clientes(limit: int = None, sort: str = None, db: Session = Depends(get_db)):
    return listar_clientes_srv(limit, sort, db)

@router.post("", response_model=Cliente, status_code=status.HTTP_201_CREATED)
@safe_route("criar_cliente")
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return criar_cliente_srv(cliente, db)

@router.put("/{cliente_id}", response_model=Cliente)
@safe_route("atualizar_cliente")
def atualizar_cliente(cliente_id: UUID, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    return atualizar_cliente_srv(cliente_id, cliente, db)

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
@safe_route("excluir_cliente")
def excluir_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    excluir_cliente_srv(cliente_id, db)
