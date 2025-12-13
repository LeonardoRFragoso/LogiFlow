#!/bin/bash
# =============================================
# LogiFlow CRM - SuiteCRM Installation Script
# =============================================

set -e

SUITECRM_VERSION="${SUITECRM_VERSION:-8.4.0}"
INSTALL_DIR="/var/www/html"

echo "============================================="
echo "LogiFlow CRM - SuiteCRM Installation"
echo "Version: ${SUITECRM_VERSION}"
echo "============================================="

# Verificar se já está instalado
if [ -f "${INSTALL_DIR}/public/index.php" ]; then
    echo "SuiteCRM já está instalado. Pulando download..."
else
    echo "Baixando SuiteCRM ${SUITECRM_VERSION}..."
    
    cd /tmp
    
    # Download do SuiteCRM
    curl -L -o suitecrm.zip "https://suitecrm.com/download/${SUITECRM_VERSION}/SuiteCRM-${SUITECRM_VERSION}.zip"
    
    # Extrair
    unzip -q suitecrm.zip -d suitecrm_temp
    
    # Mover para diretório de instalação
    mv suitecrm_temp/SuiteCRM-${SUITECRM_VERSION}/* ${INSTALL_DIR}/
    
    # Limpar
    rm -rf suitecrm.zip suitecrm_temp
    
    echo "Download concluído!"
fi

# Configurar permissões
echo "Configurando permissões..."
chown -R www:www ${INSTALL_DIR}
chmod -R 755 ${INSTALL_DIR}
chmod -R 775 ${INSTALL_DIR}/cache
chmod -R 775 ${INSTALL_DIR}/custom
chmod -R 775 ${INSTALL_DIR}/modules
chmod -R 775 ${INSTALL_DIR}/upload
chmod -R 775 ${INSTALL_DIR}/public/legacy/cache
chmod 775 ${INSTALL_DIR}/config.php 2>/dev/null || true
chmod 775 ${INSTALL_DIR}/.env.local 2>/dev/null || true

# Criar diretórios necessários
mkdir -p ${INSTALL_DIR}/cache
mkdir -p ${INSTALL_DIR}/upload
mkdir -p ${INSTALL_DIR}/custom/modules
mkdir -p ${INSTALL_DIR}/custom/themes
mkdir -p ${INSTALL_DIR}/custom/Extension

# Verificar variáveis de ambiente
if [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
    echo "AVISO: Variáveis de banco de dados não configuradas"
    echo "Configure: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
fi

# Aguardar banco de dados
echo "Aguardando conexão com banco de dados..."
max_tries=30
counter=0
until mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &> /dev/null; do
    counter=$((counter+1))
    if [ $counter -gt $max_tries ]; then
        echo "ERRO: Não foi possível conectar ao banco de dados após ${max_tries} tentativas"
        exit 1
    fi
    echo "Tentativa ${counter}/${max_tries}..."
    sleep 2
done

echo "Conexão com banco de dados estabelecida!"

# Verificar se precisa rodar instalação
if [ ! -f "${INSTALL_DIR}/.installed" ]; then
    echo "Executando instalação silenciosa do SuiteCRM..."
    
    cd ${INSTALL_DIR}
    
    # Instalar dependências via Composer
    if [ -f "composer.json" ]; then
        echo "Instalando dependências do Composer..."
        composer install --no-dev --optimize-autoloader --no-interaction
    fi
    
    # Criar arquivo de configuração do banco
    cat > ${INSTALL_DIR}/.env.local << EOF
DATABASE_URL=mysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:3306/${DB_NAME}
EOF
    
    # Marcar como instalado (instalação web ainda necessária na primeira vez)
    touch ${INSTALL_DIR}/.installed
    
    echo "Arquivos preparados. Complete a instalação via web em /install.php"
else
    echo "SuiteCRM já configurado."
fi

# Configurar OAuth2 para API V8
echo "Verificando configuração OAuth2..."
if [ -d "${INSTALL_DIR}/Api" ]; then
    # Gerar chaves OAuth2 se não existirem
    if [ ! -f "${INSTALL_DIR}/Api/V8/OAuth2/private.key" ]; then
        echo "Gerando chaves OAuth2..."
        mkdir -p ${INSTALL_DIR}/Api/V8/OAuth2
        openssl genrsa -out ${INSTALL_DIR}/Api/V8/OAuth2/private.key 2048
        openssl rsa -in ${INSTALL_DIR}/Api/V8/OAuth2/private.key -pubout -out ${INSTALL_DIR}/Api/V8/OAuth2/public.key
        chmod 600 ${INSTALL_DIR}/Api/V8/OAuth2/private.key
        chmod 644 ${INSTALL_DIR}/Api/V8/OAuth2/public.key
        chown www:www ${INSTALL_DIR}/Api/V8/OAuth2/*.key
    fi
fi

echo "============================================="
echo "Instalação do SuiteCRM concluída!"
echo "============================================="
