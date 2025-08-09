# Sistema de Gestão para Profissional Liberal

Um sistema completo e seguro para gestão de clientes, agendamentos e serviços para profissionais liberais.

## 🚀 Características Principais

### ✅ Melhorias Implementadas

- **🔒 Segurança Robusta**
  - Autenticação JWT com refresh tokens
  - Hash seguro de senhas com bcrypt
  - Rate limiting para endpoints de autenticação
  - Validação rigorosa de dados com Pydantic
  - Configuração segura de CORS
  - Headers de segurança implementados

- **🧪 Testes Automatizados**
  - Cobertura de testes > 80%
  - Testes unitários e de integração
  - Fixtures para facilitar testes
  - Relatórios de cobertura em HTML

- **📊 Logging e Observabilidade**
  - Logging estruturado com structlog
  - Logs em formato JSON para análise
  - Rastreamento de requests e performance
  - Health checks implementados

- **🗃️ Gerenciamento de Banco de Dados**
  - Migrations com Alembic
  - Modelos SQLAlchemy otimizados
  - Suporte a SQLite (dev) e PostgreSQL (prod)
  - Índices para performance

- **🐳 Containerização Completa**
  - Dockerfile otimizado
  - Docker Compose para desenvolvimento
  - Nginx como reverse proxy
  - Configuração para produção

- **⚙️ DevOps e Automação**
  - Scripts de setup automatizado
  - Makefile com comandos úteis
  - Configuração de CI/CD pronta
  - Ambientes separados (dev/prod)

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **Alembic** - Migrations de banco de dados
- **Pydantic** - Validação de dados
- **JWT** - Autenticação segura
- **bcrypt** - Hash de senhas
- **structlog** - Logging estruturado
- **pytest** - Framework de testes

### Infraestrutura
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Nginx** - Reverse proxy e load balancer
- **PostgreSQL** - Banco de dados (produção)
- **Redis** - Cache e sessões

## 🚀 Início Rápido

### Pré-requisitos
- Docker e Docker Compose
- Git

### Setup Automático
```bash
# Clone o repositório
git clone <repository-url>
cd professional_management_improved

# Setup completo do ambiente de desenvolvimento
make quick-start
```

### Setup Manual
```bash
# 1. Copie o arquivo de ambiente
cp .env.example .env

# 2. Configure as variáveis no .env
nano .env

# 3. Execute o setup
make setup

# 4. Inicie o ambiente de desenvolvimento
make dev
```

## 📋 Comandos Disponíveis

### Desenvolvimento
```bash
make dev          # Iniciar ambiente de desenvolvimento
make stop         # Parar todos os serviços
make restart      # Reiniciar serviços
make logs         # Ver logs de todos os serviços
make logs-api     # Ver logs apenas da API
```

### Testes
```bash
make test         # Executar todos os testes
make test-unit    # Executar testes unitários
make test-integration # Executar testes de integração
make test-docker  # Executar testes no Docker
```

### Banco de Dados
```bash
make migrate      # Executar migrations
make migrate-create # Criar nova migration
make db-reset     # Resetar banco (CUIDADO!)
```

### Produção
```bash
make build        # Build das imagens de produção
make deploy       # Deploy para produção
make prod-logs    # Ver logs de produção
```

### Manutenção
```bash
make clean        # Limpar containers e volumes
make clean-all    # Limpar tudo incluindo imagens
make health       # Verificar saúde dos serviços
```

## 🌐 Endpoints da API

### Autenticação
- `POST /auth/login` - Login do usuário
- `GET /auth/me` - Informações do usuário atual

### Clientes
- `GET /clientes` - Listar clientes
- `POST /clientes` - Criar cliente
- `GET /clientes/{id}` - Obter cliente específico
- `PUT /clientes/{id}` - Atualizar cliente
- `DELETE /clientes/{id}` - Remover cliente
- `GET /clientes/etiquetas` - Listar etiquetas

### Sistema
- `GET /health` - Health check
- `GET /` - Informações da API
- `GET /docs` - Documentação Swagger (apenas desenvolvimento)

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Ambiente
ENVIRONMENT=development

# Banco de Dados
DATABASE_URL=sqlite:///./data/professional_management.db

# Segurança
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=INFO
```

## 🧪 Testes

O sistema possui cobertura completa de testes:

### Estrutura de Testes
```
tests/
├── conftest.py           # Fixtures compartilhadas
├── unit/                 # Testes unitários
│   ├── test_models.py    # Testes dos modelos Pydantic
│   └── test_auth.py      # Testes de autenticação
└── integration/          # Testes de integração
    └── test_api.py       # Testes das APIs
```

### Executar Testes
```bash
# Todos os testes com cobertura
make test

# Apenas testes unitários
make test-unit

# Apenas testes de integração
make test-integration

# Testes no Docker
make test-docker
```

## 📊 Monitoramento

### Health Checks
- **API**: `GET /health`
- **Docker**: Health checks configurados nos containers
- **Nginx**: Rate limiting e logs de acesso

### Logs
- **Formato**: JSON estruturado
- **Localização**: `./logs/`
- **Rotação**: Configurada no Docker

### Métricas
- Tempo de resposta das requisições
- Status codes e erros
- Rate limiting por IP

## 🔒 Segurança

### Implementações de Segurança
- ✅ Autenticação JWT com refresh tokens
- ✅ Hash seguro de senhas (bcrypt)
- ✅ Rate limiting por IP
- ✅ Validação rigorosa de entrada
- ✅ Headers de segurança (HSTS, CSP, etc.)
- ✅ CORS configurado adequadamente
- ✅ Secrets em variáveis de ambiente
- ✅ Container não-root

### Configuração de Produção
```bash
# Use HTTPS sempre
ENVIRONMENT=production

# Chave secreta forte
SECRET_KEY=<generate-strong-secret>

# Tokens com expiração curta
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=1

# CORS restritivo
ALLOWED_ORIGINS=https://yourdomain.com
```

## 🚀 Deploy em Produção

### 1. Preparação
```bash
# Configure variáveis de produção
cp .env.example .env.production
nano .env.production

# Build das imagens
make build
```

### 2. Deploy
```bash
# Deploy com Docker Compose
docker-compose -f docker-compose.yml up -d

# Ou usando o Makefile
make deploy
```

### 3. Configuração SSL
```bash
# Coloque os certificados SSL em:
./ssl/cert.pem
./ssl/key.pem
```

## 📁 Estrutura do Projeto

```
professional_management_improved/
├── alembic/              # Migrations do banco
├── data/                 # Dados do SQLite
├── logs/                 # Arquivos de log
├── scripts/              # Scripts de automação
├── ssl/                  # Certificados SSL
├── tests/                # Testes automatizados
├── auth.py               # Sistema de autenticação
├── config.py             # Configurações
├── database.py           # Modelos e conexão DB
├── logging_config.py     # Configuração de logs
├── main.py               # Aplicação FastAPI
├── models.py             # Modelos Pydantic
├── docker-compose.yml    # Produção
├── docker-compose.dev.yml # Desenvolvimento
├── Dockerfile            # Imagem Docker
├── Makefile              # Comandos úteis
├── nginx.conf            # Configuração Nginx
├── pytest.ini            # Configuração testes
└── requirements.txt      # Dependências Python
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- Use `black` para formatação
- Use `isort` para imports
- Mantenha cobertura de testes > 80%
- Documente funções públicas

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🆘 Suporte

### Problemas Comuns

**Erro de permissão no Docker:**
```bash
sudo chown -R $USER:$USER data logs
```

**Porta já em uso:**
```bash
# Pare outros serviços na porta 8000
sudo lsof -ti:8000 | xargs kill -9
```

**Banco de dados corrompido:**
```bash
make db-reset
```

### Logs de Debug
```bash
# Ver logs detalhados
make logs

# Ver logs apenas da API
make logs-api

# Acessar container para debug
make shell
```

## 📞 Contato

Para dúvidas ou suporte, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para profissionais liberais**

