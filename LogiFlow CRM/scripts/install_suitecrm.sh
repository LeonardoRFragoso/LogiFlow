#!/bin/bash
# Script de instalação do SuiteCRM 8.x para LogiFlow CRM

set -e

SUITECRM_VERSION="8.6.1"
SUITECRM_URL="https://github.com/salesagility/SuiteCRM-Core/releases/download/v${SUITECRM_VERSION}/SuiteCRM-${SUITECRM_VERSION}.zip"
INSTALL_DIR="./suitecrm"

echo "=========================================="
echo "LogiFlow CRM - Instalação SuiteCRM ${SUITECRM_VERSION}"
echo "=========================================="

# Verificar se o diretório já existe
if [ -d "$INSTALL_DIR" ] && [ "$(ls -A $INSTALL_DIR)" ]; then
    echo "⚠️  Diretório $INSTALL_DIR não está vazio!"
    read -p "Deseja continuar e sobrescrever? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Instalação cancelada."
        exit 1
    fi
fi

# Criar diretório temporário
TEMP_DIR=$(mktemp -d)
echo "📦 Baixando SuiteCRM ${SUITECRM_VERSION}..."
cd "$TEMP_DIR"

# Download do SuiteCRM
curl -L "$SUITECRM_URL" -o suitecrm.zip

echo "📂 Extraindo arquivos..."
unzip -q suitecrm.zip

# Mover para o diretório de instalação
echo "📁 Movendo arquivos para $INSTALL_DIR..."
cd -
rm -rf "$INSTALL_DIR"/*
mv "$TEMP_DIR"/SuiteCRM-*/* "$INSTALL_DIR/"

# Preservar customizações
echo "🔧 Configurando permissões..."
chmod -R 755 "$INSTALL_DIR"
chmod -R 775 "$INSTALL_DIR/cache"
chmod -R 775 "$INSTALL_DIR/custom"
chmod -R 775 "$INSTALL_DIR/modules"
chmod -R 775 "$INSTALL_DIR/themes"
chmod -R 775 "$INSTALL_DIR/upload"
chmod -R 775 "$INSTALL_DIR/public/legacy/cache"

# Criar arquivo de configuração
echo "⚙️  Criando arquivo de configuração..."
cat > "$INSTALL_DIR/.env.local" << 'EOF'
###> symfony/framework-bundle ###
APP_ENV=prod
APP_SECRET=change-this-to-random-string
###< symfony/framework-bundle ###

###> doctrine/doctrine-bundle ###
DATABASE_URL="mysql://logiflow:logiflow123@db:3306/logiflow_crm?serverVersion=10.6"
###< doctrine/doctrine-bundle ###

###> nelmio/cors-bundle ###
CORS_ALLOW_ORIGIN='^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$'
###< nelmio/cors-bundle ###

SITE_URL=http://localhost:8080
LEGACY_SESSION_NAME=LEGACYSESSID
APP_SECRET_KEY=change-this-secret-key
EOF

# Limpar temporários
rm -rf "$TEMP_DIR"

echo ""
echo "✅ SuiteCRM instalado com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Ajuste as variáveis no arquivo .env.local"
echo "2. Execute: docker compose -f docker/docker-compose.yml up -d"
echo "3. Acesse: http://localhost:8080/install.php"
echo "4. Complete a instalação via interface web"
echo "5. Configure OAuth2 em Admin > OAuth2 Clients"
echo ""
