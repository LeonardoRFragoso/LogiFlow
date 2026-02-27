#!/bin/bash
# Script para executar migrations no Railway

set -e

echo "🚀 Iniciando execução de migrations..."
echo "📍 Diretório: $(pwd)"

# Verificar se alembic está instalado
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic não encontrado. Instalando..."
    pip install alembic
fi

# Executar migrations
echo "📊 Executando: alembic upgrade head"
alembic upgrade head

echo "✅ Migrations executadas com sucesso!"
echo ""
echo "📋 Resumo das mudanças:"
echo "  - Adicionado tenant_id em: clientes, motoristas, veiculos, pedidos, entregas"
echo "  - Removidos constraints UNIQUE que conflitam com multi-tenancy"
echo "  - Criados índices para performance"
echo ""
echo "🎉 Banco de dados atualizado!"
