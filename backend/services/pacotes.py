from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

# --- Importações Corrigidas ---
from backend.models.pacote import PacoteServico as PacoteDB
from backend.models.servico import Servico as ServicoDB
from backend.schemas.pacote import PacoteServicoCreate, PacoteServicoUpdate
# --- Fim das Importações Corrigidas ---

def criar_pacote_srv(db: Session, pacote_data: PacoteServicoCreate) -> PacoteDB:
    """Cria um novo pacote de serviços."""
    # Primeiro, busca os objetos de serviço com base nos IDs fornecidos
    servicos = db.query(ServicoDB).filter(ServicoDB.id.in_([str(sid) for sid in pacote_data.servicos_ids])).all()
    if len(servicos) != len(pacote_data.servicos_ids):
        raise HTTPException(status_code=404, detail="Um ou mais IDs de serviço não foram encontrados.")

    # Cria o objeto do pacote, excluindo o campo 'servicos_ids'
    db_pacote = PacoteDB(**pacote_data.model_dump(exclude={"servicos_ids"}))
    
    # Associa os objetos de serviço encontrados ao novo pacote
    db_pacote.servicos = servicos
    
    db.add(db_pacote)
    db.commit()
    db.refresh(db_pacote)
    return db_pacote

def listar_pacotes_srv(db: Session) -> List[PacoteDB]:
    """Lista todos os pacotes de serviço."""
    return db.query(PacoteDB).order_by(PacoteDB.nome).all()

def atualizar_pacote_srv(db: Session, pacote_id: UUID, pacote_data: PacoteServicoUpdate) -> PacoteDB:
    """Atualiza um pacote de serviço existente."""
    db_pacote = db.query(PacoteDB).filter(PacoteDB.id == str(pacote_id)).first()
    if not db_pacote:
        raise HTTPException(status_code=404, detail="Pacote não encontrado")

    update_data = pacote_data.model_dump(exclude_unset=True)
    
    # Se a lista de serviços for atualizada, precisamos tratar a relação
    if "servicos_ids" in update_data:
        servicos_ids = update_data.pop("servicos_ids")
        servicos = db.query(ServicoDB).filter(ServicoDB.id.in_([str(sid) for sid in servicos_ids])).all()
        if len(servicos) != len(servicos_ids):
            raise HTTPException(status_code=404, detail="Um ou mais IDs de serviço para atualização não foram encontrados.")
        db_pacote.servicos = servicos

    for key, value in update_data.items():
        setattr(db_pacote, key, value)
        
    db.commit()
    db.refresh(db_pacote)
    return db_pacote

def excluir_pacote_srv(db: Session, pacote_id: UUID) -> None:
    """Exclui um pacote de serviço."""
    db_pacote = db.query(PacoteDB).filter(PacoteDB.id == str(pacote_id)).first()
    if not db_pacote:
        raise HTTPException(status_code=404, detail="Pacote não encontrado")
        
    db.delete(db_pacote)
    db.commit()
