# 🏢 SuiteCRM - Guia de Instalação e Configuração

## Visão Geral

O LogiFlow CRM integra o SuiteCRM 8.6.1 para gerenciamento avançado de relacionamento com clientes. Este guia aborda a instalação completa, configuração OAuth2 e integração com a API FastAPI.

---

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Portas 8080 (HTTP) e 3306 (MySQL) disponíveis
- Mínimo 4GB RAM para o ambiente completo

---

## 🚀 Instalação Passo a Passo

### 1. Iniciar Containers

```bash
# Iniciar todos os serviços
docker-compose up -d

# Verificar status
docker-compose ps

# Acompanhar logs do SuiteCRM
docker-compose logs -f suitecrm
```

### 2. Aguardar Inicialização

O container `logiflow_suitecrm` executa automaticamente:
- Download do SuiteCRM 8.6.1 (se necessário)
- Instalação de dependências Composer
- Configuração de permissões
- Geração de chaves OAuth2
- Conexão com banco de dados

**Tempo estimado**: 3-5 minutos na primeira execução.

### 3. Acessar Instalador Web

Após a inicialização, acesse:

```
http://localhost:8080/install.php
```

### 4. Assistente de Instalação

#### Passo 1: Licença
- Aceite os termos da licença AGPLv3
- Clique em **Next**

#### Passo 2: Verificação do Sistema
- O instalador verifica requisitos PHP e extensões
- Todas as verificações devem estar **verdes** ✅
- Se houver erros, revise os logs: `docker-compose logs suitecrm`

#### Passo 3: Configuração do Banco de Dados

Use as credenciais definidas no `.env` ou docker-compose:

```
Database Type: MySQL
Host Name: db
Database Name: logiflow_crm
User Name: logiflow
Password: logiflow123

Database Port: 3306
```

**Importante**: Não use `localhost` - use `db` (nome do serviço Docker).

#### Passo 4: Conta de Administrador

Crie o usuário admin do SuiteCRM:

```
Admin User Name: admin
Admin Password: [Escolha uma senha forte]
Admin Email: admin@logiflow.local
```

**Dica**: Anote as credenciais - você precisará delas!

#### Passo 5: Configurações Locais

```
Site URL: http://localhost:8080
Session Directory: (deixe padrão)
Timezone: America/Sao_Paulo
Currency: BRL - Real Brasileiro
Date Format: dd/mm/yyyy
Time Format: H:i
```

#### Passo 6: Temas e Idioma

```
System Language: pt_BR (Português)
Default Theme: SuiteP
```

#### Passo 7: Confirmação

- Revise todas as configurações
- Clique em **Install**
- Aguarde a conclusão (2-3 minutos)

### 5. Primeiro Acesso

Após instalação bem-sucedida:

1. Acesse: `http://localhost:8080`
2. Login: `admin` / `[sua senha]`
3. Você verá o dashboard do SuiteCRM

---

## 🔐 Configuração OAuth2

### 1. Gerar Credenciais OAuth2

As chaves OAuth2 foram geradas automaticamente pelo script de instalação:

```bash
# Verificar chaves geradas
docker exec logiflow_suitecrm ls -l /var/www/html/Api/V8/OAuth2/

# Deve exibir:
# private.key (600)
# public.key (644)
```

### 2. Criar Cliente OAuth2

Acesse o SuiteCRM como admin e execute via Admin > System Console:

```bash
# Entrar no container
docker exec -it logiflow_suitecrm bash

# Navegar para o diretório
cd /var/www/html

# Criar cliente OAuth2 para o LogiFlow
php bin/console suitecrm:app:create-oauth-client \
  --name="LogiFlow API" \
  --redirect-uri="http://localhost:8000/auth/callback" \
  --grant-types="password,refresh_token,client_credentials" \
  --scope="read,write"
```

**Saída esperada**:
```
Client created successfully:
Client ID: logiflow_123abc
Client Secret: secret_xyz789
```

**⚠️ IMPORTANTE**: Anote o `Client ID` e `Client Secret` - você precisará configurá-los no backend!

### 3. Configurar Backend FastAPI

Adicione as credenciais ao arquivo `.env` do backend:

```bash
# LogiFlow CRM/backend/.env

# SuiteCRM OAuth2
SUITECRM_URL=http://suitecrm:80
SUITECRM_CLIENT_ID=logiflow_123abc
SUITECRM_CLIENT_SECRET=secret_xyz789
SUITECRM_USERNAME=admin
SUITECRM_PASSWORD=[senha do admin]
```

### 4. Testar Conexão OAuth2

```bash
# Script de teste (criar em backend/)
python -c "
from integrations.suitecrm import SuiteCRMClient
from config import settings

client = SuiteCRMClient(
    base_url=settings.SUITECRM_URL,
    client_id=settings.SUITECRM_CLIENT_ID,
    client_secret=settings.SUITECRM_CLIENT_SECRET
)

token = client.authenticate(
    username=settings.SUITECRM_USERNAME,
    password=settings.SUITECRM_PASSWORD
)

print('Token obtido:', token[:20] + '...')
"
```

**Saída esperada**:
```
Token obtido: eyJ0eXAiOiJKV1QiLCJhb...
```

---

## 🔗 Integração com LogiFlow API

### Endpoints Disponíveis

A API FastAPI expõe endpoints para sincronização bidirecional:

#### 1. Sincronizar Cliente para SuiteCRM

```bash
POST http://localhost:8000/api/v1/suitecrm/sync-account
Content-Type: application/json

{
  "nome": "Transportadora Exemplo",
  "cnpj": "12.345.678/0001-90",
  "telefone": "(11) 3456-7890",
  "email": "contato@exemplo.com.br",
  "cidade": "São Paulo",
  "uf": "SP"
}
```

**Resposta**:
```json
{
  "success": true,
  "suitecrm_id": "abc123-def456",
  "message": "Cliente sincronizado com sucesso"
}
```

#### 2. Buscar Contas do SuiteCRM

```bash
GET http://localhost:8000/api/v1/suitecrm/accounts?limit=50
```

#### 3. Sincronizar Pedido para SuiteCRM

```bash
POST http://localhost:8000/api/v1/suitecrm/sync-order
Content-Type: application/json

{
  "numero_pedido": "PED-2024-001",
  "cliente_id": "abc123-def456",
  "valor_total": 5000.00,
  "status": "aprovado"
}
```

### Sincronização Automática

O LogiFlow sincroniza automaticamente:

- ✅ **Clientes** → SuiteCRM Accounts
- ✅ **Pedidos** → SuiteCRM Opportunities
- ✅ **Cotações** → SuiteCRM Quotes
- ✅ **Contatos** → SuiteCRM Contacts

Configure o intervalo no `backend/config.py`:

```python
# Sincronização a cada 15 minutos
SUITECRM_SYNC_INTERVAL = 900  # segundos
```

---

## 🔧 Módulos Personalizados

O LogiFlow instala módulos customizados no SuiteCRM:

### Módulos Disponíveis

1. **Cotacoes** - Cotações de frete
2. **PedidosFrete** - Pedidos de transporte
3. **Entregas** - Acompanhamento de entregas
4. **Motoristas** - Cadastro de motoristas
5. **Veiculos** - Frota de veículos
6. **Ocorrencias** - Registro de ocorrências

### Instalar Módulos

```bash
# Entrar no container
docker exec -it logiflow_suitecrm bash

cd /var/www/html

# Executar Repair & Rebuild
php bin/console cache:clear
php bin/console suitecrm:app:update-app-metadata
```

### Acessar Módulos

No SuiteCRM, vá para:
- **Admin** → **Module Loader**
- Verifique se os módulos estão ativos
- Configure relacionamentos em **Admin** → **Studio**

---

## 🐛 Troubleshooting

### Erro: "Cannot connect to database"

**Solução**:
```bash
# Verificar se o banco está rodando
docker-compose ps db

# Ver logs do banco
docker-compose logs db

# Reiniciar banco se necessário
docker-compose restart db
```

### Erro: "Permission denied" durante instalação

**Solução**:
```bash
# Corrigir permissões
docker exec logiflow_suitecrm chown -R www:www /var/www/html
docker exec logiflow_suitecrm chmod -R 775 /var/www/html/cache
docker exec logiflow_suitecrm chmod -R 775 /var/www/html/custom
```

### Erro OAuth2: "Invalid client credentials"

**Solução**:
1. Verifique se as chaves OAuth2 existem:
   ```bash
   docker exec logiflow_suitecrm ls /var/www/html/Api/V8/OAuth2/
   ```

2. Regenere as chaves se necessário:
   ```bash
   docker exec logiflow_suitecrm bash -c "
   cd /var/www/html
   openssl genrsa -out Api/V8/OAuth2/private.key 2048
   openssl rsa -in Api/V8/OAuth2/private.key -pubout -out Api/V8/OAuth2/public.key
   chmod 600 Api/V8/OAuth2/private.key
   chmod 644 Api/V8/OAuth2/public.key
   "
   ```

3. Recrie o cliente OAuth2 (seção 2 acima)

### SuiteCRM está lento

**Soluções**:

1. **Ativar OPcache**:
   Já está configurado no `php.ini` - verifique:
   ```bash
   docker exec logiflow_suitecrm php -i | grep opcache.enable
   ```

2. **Limpar cache**:
   ```bash
   docker exec logiflow_suitecrm php bin/console cache:clear --env=prod
   ```

3. **Aumentar recursos Docker**:
   No Docker Desktop, aumente RAM para 4GB+ e CPU para 2+ cores.

### Erro: "Call to undefined function openssl_pkey_new()"

**Solução**: A extensão OpenSSL está faltando - reconstrua o container:
```bash
docker-compose build suitecrm --no-cache
docker-compose up -d suitecrm
```

---

## 📊 Monitoramento

### Logs

```bash
# Logs do SuiteCRM
docker-compose logs -f suitecrm

# Logs do Nginx
docker-compose logs -f nginx

# Logs específicos do SuiteCRM (dentro do container)
docker exec logiflow_suitecrm tail -f /var/www/html/logs/prod/suitecrm.log
```

### Saúde do Sistema

```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats logiflow_suitecrm

# Espaço em disco
docker exec logiflow_suitecrm df -h
```

---

## 🔄 Backup e Restauração

### Backup

```bash
# Backup do banco de dados
docker exec logiflow_db mysqldump -u logiflow -plogiflow123 logiflow_crm > backup_$(date +%Y%m%d).sql

# Backup de arquivos customizados
docker cp logiflow_suitecrm:/var/www/html/custom ./backup_custom_$(date +%Y%m%d)/
docker cp logiflow_suitecrm:/var/www/html/upload ./backup_upload_$(date +%Y%m%d)/
```

### Restauração

```bash
# Restaurar banco
cat backup_20241215.sql | docker exec -i logiflow_db mysql -u logiflow -plogiflow123 logiflow_crm

# Restaurar arquivos
docker cp backup_custom_20241215/ logiflow_suitecrm:/var/www/html/custom
docker cp backup_upload_20241215/ logiflow_suitecrm:/var/www/html/upload

# Corrigir permissões
docker exec logiflow_suitecrm chown -R www:www /var/www/html/custom
docker exec logiflow_suitecrm chown -R www:www /var/www/html/upload
```

---

## 📚 Recursos Adicionais

- [Documentação Oficial SuiteCRM 8](https://docs.suitecrm.com/8.x/)
- [API V8 Reference](https://docs.suitecrm.com/8.x/developer/api/)
- [Forum SuiteCRM](https://suitecrm.com/suitecrm/forum/)
- [LogiFlow CRM - Arquitetura](./ARCHITECTURE.md)

---

## ✅ Checklist de Instalação

- [ ] Containers Docker iniciados (`docker-compose up -d`)
- [ ] Instalação web concluída (`/install.php`)
- [ ] Login admin funcionando
- [ ] Chaves OAuth2 geradas
- [ ] Cliente OAuth2 criado
- [ ] Credenciais configuradas no `.env` do backend
- [ ] Teste de autenticação OAuth2 bem-sucedido
- [ ] Módulos customizados instalados
- [ ] Sincronização automática configurada
- [ ] Backup inicial criado

---

## 🆘 Suporte

Para dúvidas ou problemas:

1. Consulte a seção [Troubleshooting](#-troubleshooting)
2. Revise os logs: `docker-compose logs`
3. Verifique o [FAQ do SuiteCRM](https://docs.suitecrm.com/8.x/)
4. Abra uma issue no repositório do projeto

---

**Última atualização**: 2024-12-15  
**Versão SuiteCRM**: 8.6.1  
**Versão LogiFlow**: 2.0.0
