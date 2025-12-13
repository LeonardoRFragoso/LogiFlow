# =============================================
# LogiFlow CRM - FastAPI Backend Dockerfile
# =============================================
FROM python:3.11-slim

LABEL maintainer="LogiFlow CRM <contato@logiflow.com.br>"
LABEL description="FastAPI backend for LogiFlow CRM"

# Argumentos
ARG DEBIAN_FRONTEND=noninteractive

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -g 1000 appgroup \
    && useradd -u 1000 -g appgroup -ms /bin/bash appuser

# Diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache de camadas)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiar código da aplicação
COPY . .

# Ajustar permissões
RUN chown -R appuser:appgroup /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
