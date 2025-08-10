from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

# --- Importações Corrigidas ---
from backend.core.database import get_db
from backend.services.pacotes import criar_pacote_srv, listar_pacotes_srv, atualizar_pacote_srv, excluir_pacote_srv
# Renomeei o schema de saída para PacoteServicoOut para consistência
from backend.schemas.pacote import PacoteServicoOut, PacoteServicoCreate, PacoteServicoUpdate
from utils.exception_handler import safe_route
# --- Fim das Importações Corrigidas ---

router = APIRouter() # O prefixo e as tags já são definidos no __init__.py das rotas

@router.post("", response_model=PacoteServicoOut, status_code=status.HTTP_201_CREATED)
@safe_route("criar_pacote")
def criar_pacote(pacote_data: PacoteServicoCreate, db: Session = Depends(get_db)):
    return criar_pacote_srv(db=db, pacote_data=pacote_data)

@router.get("", response_model=List[PacoteServicoOut])
@safe_route("listar_pacotes")
def listar_pacotes(db: Session = Depends(get_db)):
    return listar_pacotes_srv(db=db)

@router.put("/{pacote_id}", response_model=PacoteServicoOut)
@safe_route("atualizar_pacote")
def atualizar_pacote(pacote_id: UUID, pacote_data: PacoteServicoUpdate, db: Session = Depends(get_db)):
    return atualizar_pacote_srv(db=db, pacote_id=pacote_id, pacote_data=pacote_data)

@router.delete("/{pacote_id}", status_code=status.HTTP_204_NO_CONTENT)
@safe_route("excluir_pacote")
def excluir_pacote(pacote_id: UUID, db: Session = Depends(get_db)):
    excluir_pacote_srv(db=db, pacote_id=pacote_id)
    return None
