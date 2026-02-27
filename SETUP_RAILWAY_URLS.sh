#!/bin/bash

# Script para atualizar URLs do backend em todos os frontends
# Uso: ./SETUP_RAILWAY_URLS.sh <URL_DO_BACKEND_RAILWAY>
# Exemplo: ./SETUP_RAILWAY_URLS.sh https://logiflow-api.railway.app

if [ -z "$1" ]; then
    echo "❌ Erro: URL do backend não fornecida"
    echo "Uso: ./SETUP_RAILWAY_URLS.sh <URL_DO_BACKEND_RAILWAY>"
    echo "Exemplo: ./SETUP_RAILWAY_URLS.sh https://logiflow-api.railway.app"
    exit 1
fi

BACKEND_URL="$1"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/LogiFlow CRM"

echo "🚀 Atualizando URLs do backend para: $BACKEND_URL"
echo ""

# Função para atualizar vercel.json
update_vercel_json() {
    local file="$1"
    local app_name="$2"
    
    if [ ! -f "$file" ]; then
        echo "⚠️  Arquivo não encontrado: $file"
        return 1
    fi
    
    # Usar sed para substituir a URL (compatível com macOS e Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|https://logiflow-api.onrender.com|$BACKEND_URL|g" "$file"
    else
        # Linux
        sed -i "s|https://logiflow-api.onrender.com|$BACKEND_URL|g" "$file"
    fi
    
    echo "✅ Atualizado: $app_name"
}

# Atualizar frontend principal
update_vercel_json "$PROJECT_DIR/frontend/vercel.json" "Frontend Principal"

# Atualizar app motorista
update_vercel_json "$PROJECT_DIR/app-motorista/vercel.json" "App Motorista"

# Atualizar portal cliente
update_vercel_json "$PROJECT_DIR/portal-cliente/vercel.json" "Portal Cliente"

echo ""
echo "✨ Atualização concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Revisar os arquivos vercel.json para confirmar as mudanças"
echo "2. Fazer commit das alterações: git add . && git commit -m 'chore: atualizar URLs do backend para Railway'"
echo "3. Fazer push: git push origin main"
echo "4. Vercel fará deploy automático dos frontends"
echo ""
echo "🔍 Verificar mudanças:"
echo "   grep -r 'destination.*railway' \"$PROJECT_DIR\""
