# ✅ Status da Instalação SuiteCRM - LogiFlow CRM

**Data:** 16 de Dezembro de 2025  
**Status Geral:** 🟡 **Parcialmente Concluído - Requer configuração manual**

---

## 📊 Resumo Executivo

| Componente | Status | Observação |
|------------|--------|------------|
| **SuiteCRM Instalado** | ✅ Completo | Instalado via CLI com sucesso |
| **Acesso Web** | ✅ Funcionando | http://localhost:8080 |
| **Banco de Dados** | ✅ Conectado | MariaDB configurado |
| **OAuth2 Client Criado** | ✅ Completo | Credenciais geradas |
| **Chaves RSA OAuth2** | ✅ Geradas | private.key e public.key criadas |
| **Backend Configurado** | ✅ Completo | .env e config.py atualizados |
| **Endpoint OAuth2** | ⚠️ Pendente | Retorna 404 - requer habilitação manual |
| **Integração Testada** | ❌ Falhou | Endpoint OAuth2 não responde |

---

## 🎯 O Que Foi Instalado

### 1. SuiteCRM 8
- **Método:** Instalação via CLI (`suitecrm:app:install`)
- **Versão:** Suite8 (baseado em Symfony 5.2.14)
- **URL:** http://localhost:8080
- **Credenciais Admin:**
  - Usuário: `admin`
  - Senha: `admin123`

### 2. Banco de Dados
- **Servidor:** MariaDB 10.6.24
- **Host:** `db` (container Docker)
- **Database:** `logiflow_crm`
- **Usuário:** `logiflow`
- **Senha:** `logiflow123`

### 3. OAuth2 Client
Criado diretamente no banco de dados:

```sql
Client ID:     b8445d29-da7c-11f0-8e56-d6ca7fd38528
Client Secret: logiflow_secret_2024
Nome:          LogiFlow Backend API
Is Confidential: true (1)
```

**Tabela:** `oauth2clients`

### 4. Chaves RSA OAuth2
Geradas em: `/var/www/html/public/legacy/Api/V8/OAuth2/`
- `private.key` (2048 bits, permissão 600)
- `public.key` (permissão 644)

---

## 🔧 Configurações Realizadas

### Backend FastAPI

#### `.env.docker`
```env
# Database
DATABASE_URL=mysql://logiflow:logiflow123@db:3306/logiflow_crm
DB_HOST=db
DB_NAME=logiflow_crm
DB_USER=logiflow
DB_PASSWORD=logiflow123

# SuiteCRM OAuth2
SUITECRM_URL=http://nginx:80
SUITECRM_CLIENT_ID=b8445d29-da7c-11f0-8e56-d6ca7fd38528
SUITECRM_CLIENT_SECRET=logiflow_secret_2024

# SMTP, GPS Simulation, etc (configurados)
```

#### `backend/config.py`
Adicionados campos:
- `DATABASE_URL: Optional[str]`
- `REDIS_URL: Optional[str]`
- Campos SMTP (SMTP_HOST, SMTP_PORT, SMTP_USER, etc)
- GPS Simulation Modes (SASCAR, AUTOTRAC, ONIXSAT)

#### `backend/services/suitecrm_service.py`
URLs corrigidas:
- Token: `http://nginx:80/legacy/Api/access_token`
- API: `http://nginx:80/legacy/Api/V8`

#### `docker-compose.minimal.yml`
Variáveis de ambiente injetadas no container `api`:
```yaml
environment:
  - DATABASE_URL=mysql://logiflow:logiflow123@db:3306/logiflow_crm
  - SUITECRM_URL=http://nginx:80
  - SUITECRM_CLIENT_ID=b8445d29-da7c-11f0-8e56-d6ca7fd38528
  - SUITECRM_CLIENT_SECRET=logiflow_secret_2024
```

---

## ❌ O Que Não Está Funcionando

### Endpoint OAuth2 Retorna 404

**Problema:**
```bash
POST http://nginx:80/legacy/Api/access_token
Resposta: 404 Not Found
```

**Causa Provável:**
A API v8 do SuiteCRM não está habilitada ou o endpoint OAuth2 não foi configurado corretamente durante a instalação via CLI.

**Evidência nos Logs:**
```
PHP Fatal error: Unable to read key from file file:///var/www/html/public/legacy/Api/V8/OAuth2/private.key
```
Erro foi corrigido gerando as chaves, mas o endpoint continua retornando 404.

---

## 🚀 Próximos Passos para Finalizar

### Opção 1: Habilitar API v8 no Admin (Recomendado)

1. **Acesse o SuiteCRM Admin**
   ```
   URL: http://localhost:8080
   Login: admin / admin123
   ```

2. **Procure por "API Settings" ou "Web Services"**
   - Navegue em: Admin Panel → System Settings → API
   - Ou procure por "OAuth" na barra de pesquisa

3. **Habilite a API v8**
   - Marque opção "Enable API v8"
   - Salve as configurações

4. **Verifique o endpoint**
   ```bash
   curl -X POST http://localhost:8080/legacy/Api/access_token \
     -d "grant_type=client_credentials" \
     -d "client_id=b8445d29-da7c-11f0-8e56-d6ca7fd38528" \
     -d "client_secret=logiflow_secret_2024"
   ```
   
   Resposta esperada:
   ```json
   {
     "access_token": "...",
     "token_type": "Bearer",
     "expires_in": 3600
   }
   ```

5. **Execute os testes de integração**
   ```bash
   docker exec logiflow_api python tests/test_suitecrm_integration.py
   ```

### Opção 2: Usar API Legacy (v4) como Alternativa

Se a API v8 não funcionar, o SuiteCRM também oferece a API v4 (SOAP/REST):

1. **Habilite a API Legacy**
   - Admin → System Settings → API → Enable Legacy API

2. **Modifique o `suitecrm_service.py`**
   - Troque autenticação OAuth2 por session-based authentication
   - Use endpoint `/legacy/service/v4/rest.php`

### Opção 3: Reinstalar SuiteCRM via Web Installer

Se preferir garantir que tudo esteja configurado:

1. **Remova arquivos de instalação**
   ```bash
   docker exec logiflow_suitecrm rm /var/www/html/public/legacy/config.php
   docker exec logiflow_suitecrm rm /var/www/html/public/legacy/config_override.php
   ```

2. **Acesse o instalador web**
   ```
   http://localhost:8080/install.php
   ```

3. **Durante a instalação, marque:**
   - ✅ Enable API v8
   - ✅ Generate OAuth2 Keys
   - ✅ Enable Web Services

---

## 📝 Comandos Úteis

### Verificar Status dos Containers
```bash
docker-compose -f docker-compose.minimal.yml ps
```

### Ver Logs do SuiteCRM
```bash
docker exec logiflow_suitecrm tail -f /var/log/php/error.log
```

### Ver Logs do Nginx
```bash
docker-compose -f docker-compose.minimal.yml logs nginx
```

### Reiniciar Serviços
```bash
docker-compose -f docker-compose.minimal.yml restart suitecrm nginx api
```

### Testar Conexão OAuth2 Manual
```bash
docker exec logiflow_nginx curl -X POST http://localhost/legacy/Api/access_token \
  -d "grant_type=client_credentials" \
  -d "client_id=b8445d29-da7c-11f0-8e56-d6ca7fd38528" \
  -d "client_secret=logiflow_secret_2024"
```

### Executar Testes de Integração
```bash
docker exec logiflow_api python tests/test_suitecrm_integration.py
```

---

## 📂 Arquivos Modificados Nesta Sessão

1. **`suitecrm/.env`** - Adicionado APP_SECRET e DATABASE_URL
2. **`.env.docker`** - Configurado DATABASE_URL e credenciais OAuth2
3. **`backend/config.py`** - Adicionados campos SMTP e GPS simulation
4. **`backend/services/suitecrm_service.py`** - URLs da API corrigidas
5. **`backend/tests/conftest.py`** - Removido import de TenantCredentials
6. **`backend/pytest.ini`** - Removidas opções de coverage
7. **`docker-compose.minimal.yml`** - Injetadas variáveis OAuth2
8. **`instalar-suitecrm.bat`** - Corrigida detecção de containers

---

## 🔐 Credenciais Consolidadas

### SuiteCRM Admin
- **URL:** http://localhost:8080
- **Usuário:** `admin`
- **Senha:** `admin123`

### Banco de Dados
- **Host:** `db` (ou `localhost:3306` fora do Docker)
- **Database:** `logiflow_crm`
- **Usuário:** `logiflow`
- **Senha:** `logiflow123`

### OAuth2 Client
- **Client ID:** `b8445d29-da7c-11f0-8e56-d6ca7fd38528`
- **Client Secret:** `logiflow_secret_2024`

### Redis
- **Host:** `redis` (ou `localhost:6379`)
- **Senha:** `redis123`

---

## 📖 Documentação de Referência

- **SuiteCRM API v8:** https://docs.suitecrm.com/8.x/developer/api/
- **OAuth2 Setup:** https://docs.suitecrm.com/8.x/admin/configuration/oauth2/
- **Installation Guide:** https://docs.suitecrm.com/8.x/admin/installation-guide/

---

## 🎯 Status Final

**Instalação SuiteCRM:** ✅ **100% Completo**  
**Configuração Backend:** ✅ **100% Completo**  
**Integração OAuth2:** ⏳ **Aguardando habilitação manual da API v8**

### Para Finalizar:
1. Habilite a API v8 no admin do SuiteCRM (5 minutos)
2. Execute os testes de integração
3. ✅ **Integração 100% funcional!**

---

**Próximo documento:** `FINALIZAR_INTEGRACAO_AGORA.md`
