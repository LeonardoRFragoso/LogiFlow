#!/bin/bash
# =============================================
# LogiFlow CRM - SuiteCRM OAuth2 Setup Script
# =============================================

set -e

echo "============================================="
echo "LogiFlow CRM - Configuração OAuth2 SuiteCRM"
echo "============================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se o container está rodando
if ! docker ps | grep -q logiflow_suitecrm; then
    echo -e "${RED}ERRO: Container logiflow_suitecrm não está rodando${NC}"
    echo "Execute: docker compose -f docker/docker-compose.yml up -d suitecrm"
    exit 1
fi

echo -e "${GREEN}✓${NC} Container SuiteCRM está rodando"

# Verificar se o SuiteCRM está instalado
if ! docker exec logiflow_suitecrm test -f /var/www/html/.installed; then
    echo -e "${YELLOW}AVISO: SuiteCRM ainda não foi instalado via web${NC}"
    echo "Acesse http://localhost:8080/install.php para completar a instalação"
    exit 1
fi

echo -e "${GREEN}✓${NC} SuiteCRM está instalado"

# Verificar/gerar chaves OAuth2
echo ""
echo "Verificando chaves OAuth2..."

if docker exec logiflow_suitecrm test -f /var/www/html/Api/V8/OAuth2/private.key; then
    echo -e "${GREEN}✓${NC} Chaves OAuth2 já existem"
else
    echo -e "${YELLOW}→${NC} Gerando novas chaves OAuth2..."
    
    docker exec logiflow_suitecrm bash -c "
        mkdir -p /var/www/html/Api/V8/OAuth2
        openssl genrsa -out /var/www/html/Api/V8/OAuth2/private.key 2048 2>/dev/null
        openssl rsa -in /var/www/html/Api/V8/OAuth2/private.key -pubout -out /var/www/html/Api/V8/OAuth2/public.key 2>/dev/null
        chmod 600 /var/www/html/Api/V8/OAuth2/private.key
        chmod 644 /var/www/html/Api/V8/OAuth2/public.key
        chown www:www /var/www/html/Api/V8/OAuth2/*.key
    "
    
    echo -e "${GREEN}✓${NC} Chaves OAuth2 geradas"
fi

# Informações sobre criação de cliente OAuth2
echo ""
echo "============================================="
echo "PRÓXIMOS PASSOS - Criação de Cliente OAuth2"
echo "============================================="
echo ""
echo "Execute o seguinte comando para criar um cliente OAuth2:"
echo ""
echo -e "${YELLOW}docker exec -it logiflow_suitecrm bash -c \"cd /var/www/html && php bin/console suitecrm:app:create-oauth-client --name='LogiFlow API' --redirect-uri='http://localhost:8000/auth/callback' --grant-types='password,refresh_token,client_credentials' --scope='read,write'\"${NC}"
echo ""
echo "Ou crie manualmente via interface:"
echo "  1. Acesse: http://localhost:8080"
echo "  2. Login como admin"
echo "  3. Admin → OAuth2 Clients → Create"
echo ""
echo "Após criar o cliente, copie:"
echo "  - Client ID"
echo "  - Client Secret"
echo ""
echo "E adicione ao backend/.env:"
echo ""
echo "SUITECRM_URL=http://suitecrm:80"
echo "SUITECRM_CLIENT_ID=[seu_client_id]"
echo "SUITECRM_CLIENT_SECRET=[seu_client_secret]"
echo "SUITECRM_USERNAME=admin"
echo "SUITECRM_PASSWORD=[senha_admin]"
echo ""
echo "============================================="
echo ""

# Verificar se o arquivo .env existe
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} Arquivo backend/.env encontrado"
    
    if grep -q "SUITECRM_CLIENT_ID" backend/.env; then
        echo -e "${GREEN}✓${NC} Configuração OAuth2 encontrada no .env"
        
        # Oferecer teste de conexão
        echo ""
        read -p "Deseja testar a conexão OAuth2? (s/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            echo ""
            echo "Testando conexão OAuth2..."
            
            # Verificar se o container backend está rodando
            if docker ps | grep -q logiflow_api; then
                docker exec logiflow_api python -c "
from integrations.suitecrm import SuiteCRMClient
from config import settings

try:
    client = SuiteCRMClient(
        base_url=settings.SUITECRM_URL,
        client_id=settings.SUITECRM_CLIENT_ID,
        client_secret=settings.SUITECRM_CLIENT_SECRET
    )
    
    token = client.authenticate(
        username=settings.SUITECRM_USERNAME,
        password=settings.SUITECRM_PASSWORD
    )
    
    print('✓ Conexão OAuth2 bem-sucedida!')
    print('Token:', token[:30] + '...')
except Exception as e:
    print('✗ Erro na conexão:', str(e))
" 2>/dev/null || echo -e "${RED}Erro ao testar conexão. Verifique as credenciais no .env${NC}"
            else
                echo -e "${YELLOW}Container backend não está rodando. Execute: docker compose -f docker/docker-compose.yml up -d api${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}⚠${NC}  Credenciais OAuth2 não encontradas no .env"
        echo "    Adicione as configurações após criar o cliente OAuth2"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Arquivo backend/.env não encontrado"
    echo "    Copie de backend/.env.example e configure"
fi

echo ""
echo "============================================="
echo "Configuração concluída!"
echo "============================================="

