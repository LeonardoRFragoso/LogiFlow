#!/bin/bash
# =============================================
# LogiFlow CRM - Backup de Tenant
# =============================================
# Faz backup do banco e arquivos de um tenant
#
# Uso: ./backup_tenant.sh <tenant_slug>

set -e

TENANT_SLUG=$1
BACKUP_DIR="../backups"
DATE=$(date +%Y%m%d_%H%M%S)

if [ -z "$TENANT_SLUG" ]; then
    echo "Uso: ./backup_tenant.sh <tenant_slug>"
    exit 1
fi

# Carregar variáveis
source ../.env 2>/dev/null || true

DB_HOST=${DB_HOST:-"localhost"}
DB_ROOT_PASSWORD=${DB_ROOT_PASSWORD:-"rootpass123"}
TENANT_DB="logiflow_${TENANT_SLUG//-/_}"
BACKUP_FILE="${BACKUP_DIR}/${TENANT_SLUG}_${DATE}.sql.gz"

echo "============================================="
echo "LogiFlow CRM - Backup de Tenant"
echo "============================================="
echo "Tenant: $TENANT_SLUG"
echo "Database: $TENANT_DB"
echo "Backup: $BACKUP_FILE"
echo "============================================="

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# Backup do banco
echo "[1/3] Fazendo backup do banco de dados..."
mysqldump -h"$DB_HOST" -uroot -p"$DB_ROOT_PASSWORD" \
    --single-transaction \
    --routines \
    --triggers \
    "$TENANT_DB" | gzip > "$BACKUP_FILE"

BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "✓ Backup do banco concluído: $BACKUP_SIZE"

# Backup de arquivos (uploads)
echo "[2/3] Fazendo backup de arquivos..."
UPLOAD_DIR="../suitecrm/upload"
if [ -d "$UPLOAD_DIR" ]; then
    tar -czf "${BACKUP_DIR}/${TENANT_SLUG}_${DATE}_files.tar.gz" \
        -C "$UPLOAD_DIR" . 2>/dev/null || true
    echo "✓ Backup de arquivos concluído"
else
    echo "⚠ Diretório de uploads não encontrado"
fi

# Upload para S3 (opcional)
echo "[3/3] Enviando para storage remoto..."
if command -v aws &> /dev/null && [ -n "$S3_BACKUP_BUCKET" ]; then
    aws s3 cp "$BACKUP_FILE" "s3://${S3_BACKUP_BUCKET}/backups/${TENANT_SLUG}/"
    echo "✓ Backup enviado para S3"
else
    echo "⚠ AWS CLI não configurado. Backup apenas local."
fi

echo ""
echo "============================================="
echo "✅ BACKUP CONCLUÍDO!"
echo "============================================="
echo "Arquivo: $BACKUP_FILE"
echo "Tamanho: $BACKUP_SIZE"
echo "============================================="

# Limpar backups antigos (manter últimos 30 dias)
echo "Limpando backups antigos..."
find "$BACKUP_DIR" -name "${TENANT_SLUG}_*.sql.gz" -mtime +30 -delete 2>/dev/null || true
echo "✓ Backups antigos removidos"
