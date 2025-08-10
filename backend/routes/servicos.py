from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

# --- Importações Corrigidas ---
from backend.core.database import get_db
from backend.services.servicos import criar_servico_srv, listar_servicos_srv, atualizar_servico_srv, excluir_servico_srv
# A linha abaixo foi alterada de 'servico' para 'servicos'
from backend.schemas.servicos import ServicoOut, ServicoCreate, ServicoUpdate
from utils.exception_handler import safe_route
# --- Fim das Importações Corrigidas ---

router = APIRouter() # O prefixo e as tags já são definidos no __init__.py das rotas

@router.post("", response_model=ServicoOut, status_code=status.HTTP_201_CREATED)
@safe_route("criar_servico")
def criar_servico(servico_data: ServicoCreate, db: Session = Depends(get_db)):
    return criar_servico_srv(db=db, servico_data=servico_data)

@router.get("", response_model=List[ServicoOut])
@safe_route("listar_servicos")
def listar_servicos(db: Session = Depends(get_db)):
    return listar_servicos_srv(db=db)

@router.put("/{servico_id}", response_model=ServicoOut)
@safe_route("atualizar_servico")
def atualizar_servico(servico_id: UUID, servico_data: ServicoUpdate, db: Session = Depends(get_db)):
    return atualizar_servico_srv(db=db, servico_id=servico_id, servico_data=servico_data)

@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
@safe_route("excluir_servico")
def excluir_servico(servico_id: UUID, db: Session = Depends(get_db)):
    excluir_servico_srv(db=db, servico_id=servico_id)
    return None
