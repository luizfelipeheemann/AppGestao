import pytest
from pydantic import ValidationError
from models import (
    ClienteCreate, ClienteUpdate, ServicoCreate, ServicoUpdate,
    UsuarioCreate, AgendamentoCreate, PagamentoCreate,
    StatusEnum, StatusPagamentoEnum, MetodoPagamentoEnum
)
from datetime import datetime, timedelta


class TestClienteModels:
    """Test client models validation"""
    
    def test_cliente_create_valid(self):
        """Test valid client creation"""
        cliente_data = {
            "nome": "João Silva",
            "telefone": "+5511999999999",
            "email": "joao@teste.com",
            "observacoes": "Cliente teste",
            "etiquetas": ["novo", "vip"]
        }
        cliente = ClienteCreate(**cliente_data)
        assert cliente.nome == "João Silva"
        assert cliente.telefone == "+5511999999999"
        assert cliente.email == "joao@teste.com"
        assert len(cliente.etiquetas) == 2
    
    def test_cliente_create_invalid_nome(self):
        """Test client creation with invalid name"""
        with pytest.raises(ValidationError) as exc_info:
            ClienteCreate(
                nome="A",  # Too short
                telefone="+5511999999999",
                email="joao@teste.com"
            )
        assert "at least 2 characters" in str(exc_info.value)
    
    def test_cliente_create_invalid_telefone(self):
        """Test client creation with invalid phone"""
        with pytest.raises(ValidationError) as exc_info:
            ClienteCreate(
                nome="João Silva",
                telefone="1234567890123456789",  # Too long (19 digits)
                email="joao@teste.com"
            )
        assert "Telefone deve ter entre 10 e 15 dígitos" in str(exc_info.value)
    
    def test_cliente_create_invalid_email(self):
        """Test client creation with invalid email"""
        with pytest.raises(ValidationError) as exc_info:
            ClienteCreate(
                nome="João Silva",
                telefone="+5511999999999",
                email="invalid-email"
            )
        assert "value is not a valid email address" in str(exc_info.value)
    
    def test_cliente_create_too_many_etiquetas(self):
        """Test client creation with too many tags"""
        with pytest.raises(ValidationError) as exc_info:
            ClienteCreate(
                nome="João Silva",
                telefone="+5511999999999",
                email="joao@teste.com",
                etiquetas=[f"tag{i}" for i in range(15)]  # Too many tags
            )
        assert "Máximo de 10 etiquetas permitidas" in str(exc_info.value)
    
    def test_cliente_update_partial(self):
        """Test partial client update"""
        update_data = {"nome": "João Santos"}
        cliente_update = ClienteUpdate(**update_data)
        assert cliente_update.nome == "João Santos"
        assert cliente_update.telefone is None
        assert cliente_update.email is None


class TestServicoModels:
    """Test service models validation"""
    
    def test_servico_create_valid(self):
        """Test valid service creation"""
        servico_data = {
            "nome": "Consulta Psicológica",
            "descricao": "Sessão de terapia",
            "preco": 150.0,
            "duracao_minutos": 60,
            "ativo": True
        }
        servico = ServicoCreate(**servico_data)
        assert servico.nome == "Consulta Psicológica"
        assert servico.preco == 150.0
        assert servico.duracao_minutos == 60
        assert servico.ativo is True
    
    def test_servico_create_invalid_preco(self):
        """Test service creation with invalid price"""
        with pytest.raises(ValidationError) as exc_info:
            ServicoCreate(
                nome="Consulta",
                preco=-10.0,  # Negative price
                duracao_minutos=60
            )
        assert "Input should be greater than 0" in str(exc_info.value)
    
    def test_servico_create_invalid_duracao(self):
        """Test service creation with invalid duration"""
        with pytest.raises(ValidationError) as exc_info:
            ServicoCreate(
                nome="Consulta",
                preco=100.0,
                duracao_minutos=2000  # Too long (more than 24 hours)
            )
        assert "Input should be less than or equal to 1440" in str(exc_info.value)


class TestUsuarioModels:
    """Test user models validation"""
    
    def test_usuario_create_valid(self):
        """Test valid user creation"""
        user_data = {
            "nome": "João Silva",
            "email": "joao@teste.com",
            "senha": "MinhaSenh@123"
        }
        usuario = UsuarioCreate(**user_data)
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@teste.com"
        assert usuario.senha == "MinhaSenh@123"
    
    def test_usuario_create_weak_password(self):
        """Test user creation with weak password"""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(
                nome="João Silva",
                email="joao@teste.com",
                senha="12345678"  # 8 chars but no uppercase, no special chars
            )
        assert "Senha deve conter pelo menos uma letra maiúscula" in str(exc_info.value)
    
    def test_usuario_create_short_password(self):
        """Test user creation with short password"""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(
                nome="João Silva",
                email="joao@teste.com",
                senha="Abc1"  # Too short
            )
        assert "at least 8 characters" in str(exc_info.value)


class TestAgendamentoModels:
    """Test appointment models validation"""
    
    def test_agendamento_create_valid(self):
        """Test valid appointment creation"""
        inicio = datetime.now() + timedelta(hours=1)
        fim = inicio + timedelta(hours=1)
        
        agendamento_data = {
            "cliente_id": "cliente-123",
            "servico_id": "servico-456",
            "data_hora_inicio": inicio,
            "data_hora_fim": fim,
            "observacoes": "Primeira consulta"
        }
        agendamento = AgendamentoCreate(**agendamento_data)
        assert agendamento.cliente_id == "cliente-123"
        assert agendamento.servico_id == "servico-456"
        assert agendamento.data_hora_inicio == inicio
        assert agendamento.data_hora_fim == fim
    
    def test_agendamento_create_invalid_dates(self):
        """Test appointment creation with invalid dates"""
        inicio = datetime.now() + timedelta(hours=1)
        fim = inicio - timedelta(hours=1)  # End before start
        
        with pytest.raises(ValidationError) as exc_info:
            AgendamentoCreate(
                cliente_id="cliente-123",
                servico_id="servico-456",
                data_hora_inicio=inicio,
                data_hora_fim=fim
            )
        assert "Data/hora fim deve ser posterior ao início" in str(exc_info.value)


class TestPagamentoModels:
    """Test payment models validation"""
    
    def test_pagamento_create_valid(self):
        """Test valid payment creation"""
        pagamento_data = {
            "agendamento_id": "agendamento-123",
            "valor": 150.0,
            "metodo_pagamento": MetodoPagamentoEnum.PIX,
            "status": StatusPagamentoEnum.PENDENTE,
            "descricao": "Pagamento da consulta"
        }
        pagamento = PagamentoCreate(**pagamento_data)
        assert pagamento.agendamento_id == "agendamento-123"
        assert pagamento.valor == 150.0
        assert pagamento.metodo_pagamento == MetodoPagamentoEnum.PIX
        assert pagamento.status == StatusPagamentoEnum.PENDENTE
    
    def test_pagamento_create_invalid_valor(self):
        """Test payment creation with invalid value"""
        with pytest.raises(ValidationError) as exc_info:
            PagamentoCreate(
                agendamento_id="agendamento-123",
                valor=0.0,  # Zero value
                metodo_pagamento=MetodoPagamentoEnum.PIX
            )
        assert "Input should be greater than 0" in str(exc_info.value)


class TestEnums:
    """Test enum validations"""
    
    def test_status_enum_values(self):
        """Test status enum values"""
        assert StatusEnum.ATIVO == "ativo"
        assert StatusEnum.INATIVO == "inativo"
    
    def test_status_pagamento_enum_values(self):
        """Test payment status enum values"""
        assert StatusPagamentoEnum.PENDENTE == "pendente"
        assert StatusPagamentoEnum.PAGO == "pago"
        assert StatusPagamentoEnum.CANCELADO == "cancelado"
        assert StatusPagamentoEnum.ESTORNADO == "estornado"
    
    def test_metodo_pagamento_enum_values(self):
        """Test payment method enum values"""
        assert MetodoPagamentoEnum.PIX == "pix"
        assert MetodoPagamentoEnum.CARTAO_CREDITO == "cartao_credito"
        assert MetodoPagamentoEnum.DINHEIRO == "dinheiro"

