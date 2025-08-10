from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

# --- Importações Corrigidas ---
from backend.models.servico import Servico as ServicoDB
# A linha abaixo foi alterada de 'servico' para 'servicos'
from backend.schemas.servicos import ServicoCreate, ServicoUpdate
# --- Fim das Importações Corrigidas ---

def criar_servico_srv(db: Session, servico_data: ServicoCreate) -> ServicoDB:
    """Cria um novo serviço no banco de dados."""
    # Usando .model_dump() para compatibilidade com Pydantic V2
    db_servico = ServicoDB(**servico_data.model_dump())
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

def listar_servicos_srv(db: Session) -> List[ServicoDB]:
    """Lista todos os serviços."""
    return db.query(ServicoDB).order_by(ServicoDB.nome).all()

def atualizar_servico_srv(db: Session, servico_id: UUID, servico_data: ServicoUpdate) -> ServicoDB:
    """Atualiza um serviço existente."""
    db_servico = db.query(ServicoDB).filter(ServicoDB.id == str(servico_id)).first()
    if not db_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    # Usando .model_dump() para compatibilidade com Pydantic V2
    update_data = servico_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_servico, key, value)
        
    db.commit()
    db.refresh(db_servico)
    return db_servico

def excluir_servico_srv(db: Session, servico_id: UUID) -> None:
    """Exclui um serviço do banco de dados."""
    db_servico = db.query(ServicoDB).filter(ServicoDB.id == str(servico_id)).first()
    if not db_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
        
    db.delete(db_servico)
    db.commit()
