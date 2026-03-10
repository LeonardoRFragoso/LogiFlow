#!/bin/bash
# Script para executar migration 010 no Railway
# Uso: bash run_migration_010.sh

echo "=========================================="
echo "🚀 Executando Migration 010 no Railway"
echo "=========================================="

# Verificar se estamos no diretório correto
if [ ! -f "alembic.ini" ]; then
    echo "❌ Erro: alembic.ini não encontrado"
    echo "Execute este script no diretório backend/"
    exit 1
fi

# Executar migration
echo ""
echo "📦 Aplicando migration 010_add_tenant_db_columns..."
alembic upgrade 010_add_tenant_db_columns

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Migration 010 aplicada com sucesso!"
    echo ""
    echo "📊 Verificando versão atual..."
    alembic current
else
    echo ""
    echo "❌ Erro ao aplicar migration"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Processo concluído!"
echo "=========================================="
