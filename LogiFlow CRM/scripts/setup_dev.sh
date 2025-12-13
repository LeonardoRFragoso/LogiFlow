#!/bin/bash
# =============================================
# LogiFlow CRM - Setup Development Environment
# =============================================

set -e

echo "============================================="
echo "LogiFlow CRM - Setup do Ambiente de Desenvolvimento"
echo "============================================="

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker primeiro."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não encontrado."
    exit 1
fi

echo "✓ Docker encontrado"

# Criar diretórios necessários
echo "[1/5] Criando diretórios..."
mkdir -p suitecrm
mkdir -p backend/logs
mkdir -p docker/nginx/ssl
mkdir -p docker/mysql/init
mkdir -p tenants
mkdir -p backups

echo "✓ Diretórios criados"

# Copiar .env se não existir
echo "[2/5] Configurando variáveis de ambiente..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Arquivo .env criado a partir do .env.example"
    echo "⚠ IMPORTANTE: Edite o arquivo .env com suas configurações!"
else
    echo "✓ Arquivo .env já existe"
fi

# Gerar certificados SSL auto-assinados para dev
echo "[3/5] Gerando certificados SSL para desenvolvimento..."
if [ ! -f docker/nginx/ssl/localhost.crt ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout docker/nginx/ssl/localhost.key \
        -out docker/nginx/ssl/localhost.crt \
        -subj "/C=BR/ST=SP/L=SaoPaulo/O=LogiFlow/CN=localhost" \
        2>/dev/null || echo "⚠ OpenSSL não encontrado. SSL não configurado."
    echo "✓ Certificados SSL gerados"
else
    echo "✓ Certificados SSL já existem"
fi

# Build das imagens
echo "[4/5] Construindo imagens Docker..."
docker compose build --no-cache

echo "✓ Imagens construídas"

# Iniciar containers
echo "[5/5] Iniciando containers..."
docker compose up -d

echo ""
echo "============================================="
echo "✅ AMBIENTE DE DESENVOLVIMENTO PRONTO!"
echo "============================================="
echo ""
echo "Serviços disponíveis:"
echo "  - SuiteCRM: http://localhost"
echo "  - API (FastAPI): http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Adminer (DB): http://localhost:8080"
echo ""
echo "Próximos passos:"
echo "  1. Acesse http://localhost para completar instalação do SuiteCRM"
echo "  2. Configure as credenciais OAuth2 no SuiteCRM"
echo "  3. Atualize SUITECRM_CLIENT_ID e SUITECRM_CLIENT_SECRET no .env"
echo "  4. Reinicie os containers: docker compose restart"
echo ""
echo "Comandos úteis:"
echo "  docker compose logs -f        # Ver logs"
echo "  docker compose down            # Parar containers"
echo "  docker compose restart         # Reiniciar"
echo "============================================="
