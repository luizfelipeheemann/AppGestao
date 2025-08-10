# Código para o arquivo: backend/schemas/clientes_pacotes.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# Schema para criar uma nova "venda" de pacote para um cliente
class VendaPacoteCreate(BaseModel):
    pacote_id: UUID
    cliente_id: UUID # Adicionei o cliente_id que estava faltando

# Schema para retornar os dados da compra de um pacote
class ClientePacoteOut(BaseModel):
    id: UUID
    cliente_id: UUID
    pacote_id: UUID
    saldo_sessoes: int
    status: str
    data_compra: datetime
    data_expiracao: datetime
    
    # Estes campos podem ser preenchidos na lógica de serviço
    cliente_nome: Optional[str] = None
    pacote_nome: Optional[str] = None

    class Config:
        orm_mode = True
