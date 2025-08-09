from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Union
from datetime import datetime, date
from enum import Enum
import re


# Enums para melhor segurança de tipos
class StatusEnum(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class StatusPagamentoEnum(str, Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"
    ESTORNADO = "estornado"


class StatusAgendamentoEnum(str, Enum):
    CONFIRMADO = "confirmado"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    REAGENDADO = "reagendado"


class MetodoPagamentoEnum(str, Enum):
    DINHEIRO = "dinheiro"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    TRANSFERENCIA = "transferencia"
    BOLETO = "boleto"


# Modelos Base
class BaseModelWithId(BaseModel):
    id: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos de Usuário
class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('senha')
    @classmethod
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v): raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', v): raise ValueError('Senha deve conter pelo menos uma letra minúscula')
        if not re.search(r'\d', v): raise ValueError('Senha deve conter pelo menos um número')
        return v


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class Usuario(UsuarioBase, BaseModelWithId):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# Modelos de Cliente
class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    observacoes: Optional[str] = Field(None, max_length=1000)
    etiquetas: List[str] = Field(default_factory=list)

    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, v):
        digits_only = re.sub(r'\D', '', v)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Telefone deve ter entre 10 e 15 dígitos')
        return v
    
    @field_validator('etiquetas', mode='before')
    @classmethod
    def split_etiquetas(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(',') if tag.strip()]
        return v

class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    telefone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    observacoes: Optional[str] = Field(None, max_length=1000)
    etiquetas: Optional[List[str]] = None
    
    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, v):
        if v is not None:
            digits_only = re.sub(r'\D', '', v)
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError('Telefone deve ter entre 10 e 15 dígitos')
        return v


class Cliente(ClienteBase, BaseModelWithId):
    class Config:
        from_attributes = True


# Modelos de Serviço
class ServicoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: float = Field(..., gt=0, le=999999.99)
    duracao_minutos: Optional[int] = Field(None, gt=0, le=1440)
    ativo: bool = True


class ServicoCreate(ServicoBase):
    pass


class ServicoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Optional[float] = Field(None, gt=0, le=999999.99)
    duracao_minutos: Optional[int] = Field(None, gt=0, le=1440)
    ativo: Optional[bool] = None


class Servico(ServicoBase, BaseModelWithId):
    pass


# Modelos de Agendamento
class AgendamentoBase(BaseModel):
    cliente_id: str
    servico_id: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: StatusAgendamentoEnum = StatusAgendamentoEnum.CONFIRMADO
    observacoes: Optional[str] = Field(None, max_length=500)
    
    @field_validator('data_hora_fim')
    @classmethod
    def validate_data_fim(cls, v, info):
        if 'data_hora_inicio' in info.data and v <= info.data['data_hora_inicio']:
            raise ValueError('Data/hora fim deve ser posterior ao início')
        return v
    
    @field_validator('data_hora_inicio')
    @classmethod
    def validate_data_inicio(cls, v):
        if v < datetime.utcnow() - timedelta(days=1):
            raise ValueError('Data/hora início não pode estar no passado')
        return v


class AgendamentoCreate(AgendamentoBase):
    pass


class AgendamentoUpdate(BaseModel):
    cliente_id: Optional[str] = None
    servico_id: Optional[str] = None
    data_hora_inicio: Optional[datetime] = None
    data_hora_fim: Optional[datetime] = None
    status: Optional[StatusAgendamentoEnum] = None
    observacoes: Optional[str] = Field(None, max_length=500)


class Agendamento(AgendamentoBase, BaseModelWithId):
    cliente: Cliente
    servico: Servico


# Modelos de Pagamento
class PagamentoBase(BaseModel):
    agendamento_id: str
    valor: float = Field(..., gt=0, le=999999.99)
    metodo_pagamento: MetodoPagamentoEnum
    status: StatusPagamentoEnum = StatusPagamentoEnum.PENDENTE
    descricao: Optional[str] = Field(None, max_length=500)
    link_pagamento: Optional[str] = None


class PagamentoCreate(PagamentoBase):
    pass


class PagamentoUpdate(BaseModel):
    valor: Optional[float] = Field(None, gt=0, le=999999.99)
    metodo_pagamento: Optional[MetodoPagamentoEnum] = None
    status: Optional[StatusPagamentoEnum] = None
    descricao: Optional[str] = Field(None, max_length=500)
    link_pagamento: Optional[str] = None


class Pagamento(PagamentoBase, BaseModelWithId):
    pass


# Modelos de Pacotes de Serviço
class PacoteServicoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: float = Field(..., gt=0)
    quantidade_sessoes: int = Field(..., gt=0)
    validade_dias: int = Field(..., gt=0)
    servicos_ids: List[str] = Field(..., min_length=1)
    ativo: bool = True


class PacoteServicoCreate(PacoteServicoBase):
    pass


class PacoteServicoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Optional[float] = Field(None, gt=0)
    quantidade_sessoes: Optional[int] = Field(None, gt=0)
    validade_dias: Optional[int] = Field(None, gt=0)
    servicos_ids: Optional[List[str]] = Field(None, min_length=1)
    ativo: Optional[bool] = None


class PacoteServico(PacoteServicoBase, BaseModelWithId):
    servicos: List[Servico] = []


# Modelos de Gestão de Pacotes do Cliente
class ClientePacoteBase(BaseModel):
    cliente_id: str
    pacote_id: str
    data_compra: datetime
    data_expiracao: datetime
    saldo_sessoes: int
    status: str


class ClientePacote(ClientePacoteBase, BaseModelWithId):
    pacote: PacoteServico


class VendaPacoteCreate(BaseModel):
    pacote_id: str


# Modelos de Preço Personalizado
class PrecoPersonalizadoBase(BaseModel):
    cliente_id: str
    servico_id: str
    preco_personalizado: float = Field(..., gt=0, le=999999.99)
    observacoes: Optional[str] = Field(None, max_length=500)
    ativo: bool = True


class PrecoPersonalizadoCreate(PrecoPersonalizadoBase):
    pass


class PrecoPersonalizadoUpdate(BaseModel):
    preco_personalizado: Optional[float] = Field(None, gt=0, le=999999.99)
    observacoes: Optional[str] = Field(None, max_length=500)
    ativo: Optional[bool] = None


class PrecoPersonalizado(PrecoPersonalizadoBase, BaseModelWithId):
    pass


# Modelos para o Relatório de Consumo
class RelatorioConsumoItem(BaseModel):
    data_uso: datetime
    servico_nome: str


class RelatorioConsumoPacote(BaseModel):
    cliente_nome: str
    pacote_nome: str
    data_compra: datetime
    data_expiracao: datetime
    sessoes_total: int
    sessoes_saldo: int
    status: str
    consumo: List[RelatorioConsumoItem]


# Modelos de Resposta Genérica
class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    message: str
    detail: Optional[str] = None
    success: bool = False