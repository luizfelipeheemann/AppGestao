from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

# --- Importações Corrigidas ---
from backend.models.cliente import Cliente as ClienteDB
from backend.schemas.cliente import ClienteCreate, ClienteUpdate
# --- Fim das Importações Corrigidas ---

# As funções de serviço agora recebem a sessão 'db' como parâmetro.

def listar_clientes_srv(
    db: Session, 
    limit: Optional[int] = None, 
    sort: Optional[str] = None
) -> List[ClienteDB]:
    """Lista todos os clientes com opções de limite e ordenação."""
    query = db.query(ClienteDB)
    
    if sort:
        if sort.lower() == "desc":
            query = query.order_by(ClienteDB.nome.desc())
        else:
            query = query.order_by(ClienteDB.nome.asc())
    else:
        query = query.order_by(ClienteDB.nome)
        
    if limit:
        query = query.limit(limit)
        
    return query.all()

def criar_cliente_srv(db: Session, cliente_data: ClienteCreate) -> ClienteDB:
    """Cria um novo cliente no banco de dados."""
    # Usando .model_dump() para compatibilidade com Pydantic V2
    db_cliente = ClienteDB(**cliente_data.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def atualizar_cliente_srv(db: Session, cliente_id: UUID, cliente_data: ClienteUpdate) -> ClienteDB:
    """Atualiza um cliente existente."""
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == str(cliente_id)).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Usando .model_dump() para compatibilidade com Pydantic V2
    update_data = cliente_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
        
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def excluir_cliente_srv(db: Session, cliente_id: UUID) -> None:
    """Exclui um cliente do banco de dados."""
    db_cliente = db.query(ClienteDB).filter(ClienteDB.id == str(cliente_id)).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
    db.delete(db_cliente)
    db.commit()
