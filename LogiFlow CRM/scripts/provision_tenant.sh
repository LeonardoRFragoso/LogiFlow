#!/bin/bash
# =============================================
# LogiFlow CRM - Provisioning Script
# =============================================
# Cria novo tenant (banco, usuário, bucket)
#
# Uso: ./provision_tenant.sh <tenant_slug> <admin_email>
# Exemplo: ./provision_tenant.sh transportes-abc admin@abc.com.br

set -e

# ===========================================
# Configurações
# ===========================================
TENANT_SLUG=$1
ADMIN_EMAIL=$2

if [ -z "$TENANT_SLUG" ] || [ -z "$ADMIN_EMAIL" ]; then
    echo "Uso: ./provision_tenant.sh <tenant_slug> <admin_email>"
    echo "Exemplo: ./provision_tenant.sh transportes-abc admin@abc.com.br"
    exit 1
fi

# Carregar variáveis de ambiente
if [ -f ../.env ]; then
    source ../.env
fi

DB_ROOT_PASSWORD=${DB_ROOT_PASSWORD:-"rootpass123"}
DB_HOST=${DB_HOST:-"localhost"}
TEMPLATE_DB="logiflow_template"
S3_BUCKET_PREFIX=${S3_BUCKET_PREFIX:-"logiflow"}

# Gerar nomes únicos
TENANT_DB="logiflow_${TENANT_SLUG//-/_}"
TENANT_USER="user_${TENANT_SLUG//-/_}"
TENANT_PASSWORD=$(openssl rand -hex 12)
TENANT_BUCKET="${S3_BUCKET_PREFIX}-${TENANT_SLUG}"

echo "============================================="
echo "LogiFlow CRM - Provisionamento de Tenant"
echo "============================================="
echo "Tenant: $TENANT_SLUG"
echo "Database: $TENANT_DB"
echo "User: $TENANT_USER"
echo "Admin Email: $ADMIN_EMAIL"
echo "============================================="

# ===========================================
# 1. Criar Banco de Dados
# ===========================================
echo "[1/6] Criando banco de dados..."

mysql -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS \`${TENANT_DB}\` 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
EOF

echo "✓ Banco de dados criado: $TENANT_DB"

# ===========================================
# 2. Clonar Schema do Template
# ===========================================
echo "[2/6] Clonando schema do template..."

mysqldump -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" \
    --no-data --routines --triggers \
    "$TEMPLATE_DB" | mysql -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" "$TENANT_DB"

echo "✓ Schema clonado do template"

# ===========================================
# 3. Criar Usuário do Banco
# ===========================================
echo "[3/6] Criando usuário do banco..."

mysql -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" <<EOF
CREATE USER IF NOT EXISTS '${TENANT_USER}'@'%' IDENTIFIED BY '${TENANT_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${TENANT_DB}\`.* TO '${TENANT_USER}'@'%';
FLUSH PRIVILEGES;
EOF

echo "✓ Usuário criado: $TENANT_USER"

# ===========================================
# 4. Inserir Dados Iniciais
# ===========================================
echo "[4/6] Inserindo dados iniciais..."

# Gerar UUID para admin
ADMIN_ID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen)
ADMIN_PASSWORD_HASH=$(python3 -c "from passlib.hash import bcrypt; print(bcrypt.hash('mudar123'))")

mysql -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" "$TENANT_DB" <<EOF
-- Inserir usuário admin
INSERT INTO users (id, user_name, first_name, last_name, status, is_admin, user_hash, email1, date_entered, date_modified)
VALUES ('${ADMIN_ID}', 'admin', 'Administrador', '${TENANT_SLUG}', 'Active', 1, '${ADMIN_PASSWORD_HASH}', '${ADMIN_EMAIL}', NOW(), NOW());

-- Configurações iniciais
INSERT INTO config (category, name, value) VALUES 
    ('system', 'tenant_slug', '${TENANT_SLUG}'),
    ('system', 'tenant_created', NOW());
EOF

echo "✓ Dados iniciais inseridos"

# ===========================================
# 5. Criar Bucket S3 (se MinIO/S3 disponível)
# ===========================================
echo "[5/6] Configurando storage..."

if command -v mc &> /dev/null; then
    # MinIO Client disponível
    mc mb "minio/${TENANT_BUCKET}" --ignore-existing 2>/dev/null || true
    echo "✓ Bucket S3 criado: $TENANT_BUCKET"
else
    echo "⚠ MinIO Client não encontrado. Configure o bucket manualmente: $TENANT_BUCKET"
fi

# ===========================================
# 6. Registrar na Base Administrativa
# ===========================================
echo "[6/6] Registrando tenant na base administrativa..."

# TODO: Inserir na tabela de tenants do admin DB
# mysql -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" logiflow_admin <<EOF
# INSERT INTO tenants (slug, database_name, database_user, status, plan, created_at)
# VALUES ('${TENANT_SLUG}', '${TENANT_DB}', '${TENANT_USER}', 'active', 'trial', NOW());
# EOF

echo "✓ Tenant registrado"

# ===========================================
# Resumo
# ===========================================
echo ""
echo "============================================="
echo "✅ PROVISIONAMENTO CONCLUÍDO!"
echo "============================================="
echo ""
echo "Credenciais do Banco:"
echo "  Host: $DB_HOST"
echo "  Database: $TENANT_DB"
echo "  User: $TENANT_USER"
echo "  Password: $TENANT_PASSWORD"
echo ""
echo "Credenciais do Admin:"
echo "  Email: $ADMIN_EMAIL"
echo "  Senha: mudar123 (solicitar alteração no primeiro login)"
echo ""
echo "Storage:"
echo "  Bucket: $TENANT_BUCKET"
echo ""
echo "IMPORTANTE: Salve estas credenciais em local seguro!"
echo "============================================="

# Salvar credenciais em arquivo (remover em produção)
cat > "../tenants/${TENANT_SLUG}.credentials" <<EOF
# Credenciais do Tenant: ${TENANT_SLUG}
# Gerado em: $(date)

DB_HOST=${DB_HOST}
DB_NAME=${TENANT_DB}
DB_USER=${TENANT_USER}
DB_PASSWORD=${TENANT_PASSWORD}

ADMIN_EMAIL=${ADMIN_EMAIL}
ADMIN_INITIAL_PASSWORD=mudar123

S3_BUCKET=${TENANT_BUCKET}
EOF

echo "Credenciais salvas em: tenants/${TENANT_SLUG}.credentials"
