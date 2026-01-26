# LogiFlow CRM - Docker Guide

> Guia de containerização e uso do Docker

## Estrutura de Containers

```
┌─────────────────────────────────────────────────────────────┐
│                     docker-compose.yml                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │   api   │  │frontend │  │   db    │  │  redis  │        │
│  │ :8000   │  │ :3000   │  │ :5432   │  │ :6379   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ celery  │  │  beat   │  │ adminer │                     │
│  │ worker  │  │         │  │ :8080   │                     │
│  └─────────┘  └─────────┘  └─────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Comandos Essenciais

### Iniciar Ambiente

```bash
# Subir todos os serviços
docker-compose up -d

# Subir serviços específicos
docker-compose up -d api db redis

# Subir com rebuild
docker-compose up -d --build
```

### Gerenciar Serviços

```bash
# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f api
docker-compose logs -f --tail=100 api

# Reiniciar serviço
docker-compose restart api

# Parar tudo
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

### Executar Comandos

```bash
# Shell no container
docker-compose exec api bash

# Rodar migrations
docker-compose exec api alembic upgrade head

# Rodar testes
docker-compose exec api pytest

# Python REPL
docker-compose exec api python
```

## Dockerfile (Backend)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (cache de layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: logiflow
      POSTGRES_USER: logiflow
      POSTGRES_PASSWORD: ${DB_PASSWORD:-logiflow123}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U logiflow"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD:-redis123}
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://logiflow:${DB_PASSWORD:-logiflow123}@db:5432/logiflow
      REDIS_HOST: redis
      REDIS_PASSWORD: ${REDIS_PASSWORD:-redis123}
      SECRET_KEY: ${SECRET_KEY:-dev-secret}
      DEBUG: ${DEBUG:-true}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app  # Hot reload em dev

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://localhost:8000/api/v1
    depends_on:
      - api

  celery_worker:
    build: ./backend
    command: celery -A tasks worker -l info
    environment:
      DATABASE_URL: postgresql://logiflow:${DB_PASSWORD:-logiflow123}@db:5432/logiflow
      REDIS_HOST: redis
      REDIS_PASSWORD: ${REDIS_PASSWORD:-redis123}
    depends_on:
      - db
      - redis

  celery_beat:
    build: ./backend
    command: celery -A tasks beat -l info
    depends_on:
      - celery_worker

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
  redis_data:
```

## Otimizações para Produção

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .dockerignore

```
.git
.gitignore
__pycache__
*.pyc
*.pyo
.env
.env.*
venv/
.venv/
node_modules/
dist/
build/
*.md
tests/
.pytest_cache/
.coverage
htmlcov/
```

## Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker-compose logs api

# Verificar se imagem foi construída
docker images | grep logiflow

# Rebuild forçado
docker-compose build --no-cache api
```

### Banco não conecta

```bash
# Verificar se db está healthy
docker-compose ps db

# Testar conexão
docker-compose exec db psql -U logiflow -d logiflow

# Ver logs do banco
docker-compose logs db
```

### Espaço em disco

```bash
# Limpar containers parados
docker container prune

# Limpar imagens não utilizadas
docker image prune

# Limpar tudo (CUIDADO!)
docker system prune -a --volumes
```
