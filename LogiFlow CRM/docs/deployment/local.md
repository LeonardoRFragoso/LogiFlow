# LogiFlow CRM - Local Development Setup

> Guia para configurar o ambiente de desenvolvimento local

## Pré-requisitos

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Node.js** 18+ (para frontend)
- **Python** 3.11+ (para desenvolvimento backend)
- **Git**

## Quick Start (Docker)

```bash
# 1. Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd "LogiFlow CRM"

# 2. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 3. Suba os containers
docker-compose up -d

# 4. Verifique os serviços
docker-compose ps

# 5. Acesse a aplicação
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Swagger: http://localhost:8000/api/v1/docs
# Adminer: http://localhost:8080
```

## Setup Manual (Sem Docker)

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco
# Certifique-se que PostgreSQL e Redis estão rodando

# Rodar migrations
alembic upgrade head

# Iniciar servidor
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar ambiente
cp .env.example .env.local

# Iniciar dev server
npm run dev
```

## Variáveis de Ambiente

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://logiflow:logiflow123@localhost:5432/logiflow

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis123

# JWT
SECRET_KEY=dev-secret-key-change-in-production

# Debug
DEBUG=true

# API
API_PREFIX=/api
API_VERSION=v1
```

### Frontend (.env.local)

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

## Comandos Úteis

### Docker

```bash
# Ver logs
docker-compose logs -f api
docker-compose logs -f frontend

# Reiniciar serviço específico
docker-compose restart api

# Rebuild após mudanças
docker-compose up -d --build

# Limpar tudo
docker-compose down -v
```

### Backend

```bash
# Rodar testes
pytest

# Testes com coverage
pytest --cov=. --cov-report=html

# Lint
ruff check .

# Criar migration
alembic revision --autogenerate -m "descrição"

# Aplicar migrations
alembic upgrade head
```

### Frontend

```bash
# Lint
npm run lint

# Build
npm run build

# Preview build
npm run preview
```

## Troubleshooting

### Erro de conexão com banco

```bash
# Verificar se PostgreSQL está rodando
docker-compose ps db

# Ver logs do banco
docker-compose logs db

# Recriar banco
docker-compose down -v
docker-compose up -d db
```

### Erro de conexão com Redis

```bash
# Verificar Redis
docker-compose ps redis
docker-compose logs redis
```

### Porta já em uso

```bash
# Encontrar processo na porta
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000

# Matar processo ou mudar porta no docker-compose.yml
```

## Seed de Dados (Opcional)

```bash
# Criar dados de exemplo
python scripts/seed_data.py
```

## Estrutura de Serviços

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| api | 8000 | Backend FastAPI |
| frontend | 3000 | Frontend Vue.js |
| db | 5432 | PostgreSQL |
| redis | 6379 | Redis Cache |
| adminer | 8080 | DB Admin UI |
| celery_worker | - | Background tasks |
| celery_beat | - | Scheduled tasks |
