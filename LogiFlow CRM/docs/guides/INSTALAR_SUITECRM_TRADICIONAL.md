# 🚀 Instalar SuiteCRM Tradicional - Passo a Passo (30 min)

## ✅ PRÉ-REQUISITOS

Você já tem:
- ✅ MariaDB rodando no Docker (porta 3306)
- ✅ Backend FastAPI pronto para integrar

Você precisa:
- 🔧 XAMPP, WAMP ou servidor PHP local
- 📥 Download do SuiteCRM 8.4.0

---

## 📥 PASSO 1: Download (5 min)

### Opção A: Download Direto (Recomendado)

**Link oficial:**
```
https://github.com/salesagility/SuiteCRM-Core/releases/download/v8.4.0/SuiteCRM-8.4.0.zip
```

### Opção B: Site Oficial
```
https://suitecrm.com/download/
```

**Baixe:** `SuiteCRM-8.4.0.zip` (~150MB)

---

## 🔧 PASSO 2: Instalar Servidor Web (10 min)

### Opção A: XAMPP (Recomendado para Windows)

**1. Download XAMPP:**
```
https://www.apachefriends.org/download.html
```

**2. Instalar:**
- Execute o instalador
- Selecione: Apache + MySQL + PHP
- Instale em: `C:\xampp`

**3. Iniciar:**
- Abra XAMPP Control Panel
- Inicie Apache

**4. Testar:**
```
http://localhost → Deve mostrar página do XAMPP
```

### Opção B: Usar PHP Embutido (Rápido)

Se já tem PHP instalado:

```powershell
# Verificar PHP
php -v

# Se versão >= 8.1, pode usar servidor embutido
```

---

## 📁 PASSO 3: Extrair SuiteCRM (2 min)

**Windows:**
```powershell
# 1. Extrair ZIP
# Descompactar SuiteCRM-8.4.0.zip

# 2. Mover para pasta web
# XAMPP: C:\xampp\htdocs\suitecrm
# OU qualquer pasta para usar servidor PHP
```

**Estrutura esperada:**
```
C:\xampp\htdocs\suitecrm\
├── public/
│   ├── index.php
│   ├── install.php
│   └── ...
├── vendor/
├── config/
├── composer.json
└── ...
```

---

## 🗄️ PASSO 4: Configurar Banco de Dados (3 min)

### Usar MariaDB do Docker (Recomendado)

**Banco já está rodando!** Só precisa criar database específico para SuiteCRM.

```powershell
# Conectar ao MariaDB do Docker
docker exec -it logiflow_db mysql -u root -prootpass123

# Criar database
CREATE DATABASE suitecrm_ui CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'suitecrm_ui'@'%' IDENTIFIED BY 'suitecrm123';
GRANT ALL PRIVILEGES ON suitecrm_ui.* TO 'suitecrm_ui'@'%';
FLUSH PRIVILEGES;
EXIT;
```

**Credenciais:**
- Host: `localhost` (ou `127.0.0.1`)
- Port: `3306`
- Database: `suitecrm_ui`
- User: `suitecrm_ui`
- Password: `suitecrm123`

---

## 🌐 PASSO 5: Acessar Instalador Web (5 min)

### Opção A: XAMPP

```
http://localhost/suitecrm/public/install.php
```

### Opção B: PHP Servidor Embutido

```powershell
# Na pasta do SuiteCRM
cd C:\caminho\para\suitecrm\public
php -S localhost:8888

# Acessar
http://localhost:8888/install.php
```

---

## 📋 PASSO 6: Preencher Instalador (5 min)

### Tela 1: Verificação de Sistema

- ✅ PHP 8.1+
- ✅ Extensões necessárias
- **Clique:** Next

### Tela 2: Licença

- **Aceite** a licença
- **Clique:** Next

### Tela 3: Configuração do Banco

| Campo | Valor |
|-------|-------|
| Database Type | `MySQL` |
| Database Host | `localhost` |
| Database Port | `3306` |
| Database Name | `suitecrm_ui` |
| Database User | `suitecrm_ui` |
| Database Password | `suitecrm123` |

**Clique:** Next

### Tela 4: Conta Admin

| Campo | Valor |
|-------|-------|
| Admin Username | `admin` |
| Admin Password | `admin123` |
| Admin Email | `admin@logiflow.com` |
| First Name | `Admin` |
| Last Name | `LogiFlow` |

**Clique:** Next

### Tela 5: Configurações do Site

| Campo | Valor |
|-------|-------|
| Site URL | `http://localhost/suitecrm` (ou porta usada) |
| Session Directory | (deixar padrão) |
| Log Directory | (deixar padrão) |

**Clique:** Next

### Tela 6: Instalação

- Aguarde processo (2-5 minutos)
- ✅ Instalação completa
- **Clique:** Finish

---

## ✅ PASSO 7: Primeiro Acesso

```
http://localhost/suitecrm
```

**Login:**
- Username: `admin`
- Password: `admin123`

**Deve abrir o dashboard do SuiteCRM! 🎉**

---

## 🔐 PASSO 8: Configurar OAuth2 (3 min)

### Criar OAuth2 Client para Backend

**1. No SuiteCRM:**
```
Admin (menu superior direito) 
→ OAuth2 Clients and Tokens
→ Create OAuth2 Client
```

**2. Preencher:**
```
Name: LogiFlow Backend API
Client Type: Confidential
Redirect URI: (deixar vazio)
```

**3. Salvar**

**4. COPIAR credenciais:**
```
Client ID: abc123-def456-...
Client Secret: xyz789-uvw012-...
```

⚠️ **IMPORTANTE:** Copie agora! O Secret não pode ser visto depois.

---

## 🔗 PASSO 9: Conectar Backend (2 min)

### Atualizar .env do Backend

**Arquivo:** `backend\.env`

```env
# SuiteCRM Configuration
SUITECRM_URL=http://localhost/suitecrm
SUITECRM_CLIENT_ID=abc123-def456-...
SUITECRM_CLIENT_SECRET=xyz789-uvw012-...
SUITECRM_USERNAME=admin
SUITECRM_PASSWORD=admin123
```

**Reiniciar Backend:**
```powershell
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml restart api
```

---

## ✅ PASSO 10: Validar Integração (2 min)

### Testar Conexão

```powershell
# Executar script de validação
.\validar-integracao.bat
```

**OU testar manualmente:**

```powershell
# Acessar API docs
http://localhost:8000/api/v1/docs

# Testar endpoint de teste SuiteCRM
GET /api/v1/suitecrm/test
```

**Resposta esperada:**
```json
{
  "status": "success",
  "suitecrm_version": "8.4.0",
  "connection": "ok"
}
```

---

## 🎉 INSTALAÇÃO COMPLETA!

### O Que Você Tem Agora

1. ✅ **SuiteCRM UI** rodando em `http://localhost/suitecrm`
2. ✅ **Backend FastAPI** em `http://localhost:8000`
3. ✅ **Integração OAuth2** funcionando
4. ✅ **Banco MariaDB** compartilhado

### Arquitetura Final

```
┌─────────────────────────┐
│   SuiteCRM UI (PHP)     │ ← http://localhost/suitecrm
│   XAMPP/PHP Server      │
└──────────┬──────────────┘
           │ OAuth2 API V8
           ▼
┌─────────────────────────┐
│  FastAPI Backend (Docker)│ ← http://localhost:8000
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│   MariaDB (Docker)      │ ← localhost:3306
│   2 databases:          │
│   - logiflow_crm       │ (backend)
│   - suitecrm_ui        │ (SuiteCRM)
└─────────────────────────┘
```

---

## 🔧 TROUBLESHOOTING

### Erro: "Cannot connect to database"

**Solução:**
```powershell
# Verificar se MariaDB está rodando
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml ps

# Testar conexão
mysql -h 127.0.0.1 -P 3306 -u suitecrm_ui -psuitecrm123 suitecrm_ui
```

### Erro: "Permissões negadas"

**Windows (XAMPP):**
```powershell
# Dar permissões de escrita
# Propriedades da pasta → Segurança → Modificar
```

### Erro: "Composer not found"

**Solução:**
```powershell
# Instalar Composer
https://getcomposer.org/download/

# OU dentro do SuiteCRM:
cd C:\xampp\htdocs\suitecrm
composer install --no-dev
```

---

## 📚 PRÓXIMOS PASSOS

### 1. Explorar SuiteCRM
- Criar Leads
- Criar Contas
- Configurar Workflows
- Customizar módulos

### 2. Testar Integração Backend
- Criar registro via API
- Ler dados via backend
- Sincronizar com frontends

### 3. Desenvolver Frontends
- Conectar Vue 3 apps ao backend
- Exibir dados do SuiteCRM
- Criar/editar registros

---

## ✅ CHECKLIST FINAL

- [ ] SuiteCRM instalado
- [ ] Login funcionando
- [ ] OAuth2 Client criado
- [ ] Backend configurado (.env)
- [ ] Integração validada
- [ ] Teste de criação de Lead
- [ ] Teste de leitura via API

---

**Tempo Total:** ~30 minutos  
**Status:** ✅ **PRONTO PARA USO**

**SuiteCRM + Backend + Docker = Sistema Completo! 🚀**
