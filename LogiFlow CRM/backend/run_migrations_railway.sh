#!/bin/bash
# Script para executar migrations no Railway

set -e

echo "🔄 Executando migrations no Railway..."

# Verificar se DATABASE_URL está configurada
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL não está configurada"
    exit 1
fi

echo "📍 Conectando ao banco de dados..."
echo "🗄️  Database: $DATABASE_URL"

# Executar migrations
alembic upgrade head

echo "✅ Migrations executadas com sucesso!"
