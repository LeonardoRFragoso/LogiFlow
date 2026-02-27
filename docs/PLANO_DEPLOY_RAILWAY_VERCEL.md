# 🚀 Plano de Deploy: Backend Railway + Frontends Vercel

## 📊 Status Atual

**Backend:**
- Localização: `/LogiFlow CRM/backend`
- Framework: FastAPI (Python 3.11.7)
- Banco de dados: PostgreSQL
- Cache: Redis
- Status: Pronto para deploy no Railway

**Frontends (Vercel):**
- `frontend/` - Dashboard principal
- `app-motorista/` - App para motoristas
- `portal-cliente/` - Portal do cliente
- `site-divulgacao/` - Site de divulgação
- Status: Apontando para `https://logiflow-api.onrender.com` (DESATUALIZADO)

---

## 🎯 Objetivo

Fazer o deploy do backend no Railway e conectar todos os frontends do Vercel para usar a nova URL do backend no Railway.

---

## 📋 Passo a Passo

### FASE 1: Deploy do Backend no Railway

#### 1.1 Criar Novo Serviço no Railway

1. Acesse [railway.app](https://railway.app)
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Escolha o repositório **`LeonardoRFragoso/LogiFlow`**

#### 1.2 Configurar Root Directory (CRÍTICO)

Após o serviço ser criado:

1. Clique no serviço para abrir
2. Vá em **Settings** (ícone de engrenagem)
3. Role até **Service Settings**
4. Configure **Root Directory**: `LogiFlow CRM/backend`
5. Clique em **Deploy**

**Por quê?** O código está em `LogiFlow CRM/backend/`, não na raiz.

#### 1.3 Adicionar Banco de Dados PostgreSQL

1. No projeto Railway, clique em **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway criará automaticamente:
   - `DATABASE_URL`
   - `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`

#### 1.4 Adicionar Redis (Cache)

1. Clique em **"New"** → **"Database"** → **"Add Redis"**
2. Railway criará automaticamente:
   - `REDIS_URL`
   - `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`

#### 1.5 Configurar Variáveis de Ambiente

No Railway Dashboard, vá em **Settings** → **Variables** e adicione:

**Obrigatórias:**
```
DEBUG=False
SECRET_KEY=<gere-uma-chave-secreta-forte>
API_PREFIX=/api
API_VERSION=v1
ALLOWED_ORIGINS=https://logi-flow-blush.vercel.app,https://logi-flow-app-motorista.vercel.app,https://logi-flow-z315.vercel.app,https://logi-flow-wuhp.vercel.app,https://logiflow.com.br
```

**Integrações (conforme necessário):**
```
GOOGLE_MAPS_API_KEY=<sua-chave>
MERCADOPAGO_ACCESS_TOKEN=<seu-token>
FOCUSNFE_TOKEN=<seu-token>
EVOLUTION_API_URL=<url-da-sua-api>
EVOLUTION_API_KEY=<sua-chave>
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<seu-email>
SMTP_PASSWORD=<senha-de-app>
```

**Dica:** Use o arquivo `.env.railway` como referência.

#### 1.6 Executar Migrações do Banco

Após o primeiro deploy bem-sucedido:

**Via Railway CLI:**
```bash
npm i -g @railway/cli
railway login
railway link
railway run alembic upgrade head
```

#### 1.7 Obter URL do Backend

Após o deploy:
1. Vá em **Settings** → **Networking**
2. Clique em **"Generate Domain"** para obter um domínio `.railway.app`
3. Anote a URL: `https://seu-backend.railway.app`

**Verificar saúde da API:**
```
https://seu-backend.railway.app/health
https://seu-backend.railway.app/api/v1/docs
```

---

### FASE 2: Atualizar Frontends no Vercel

Todos os frontends estão apontando para `https://logiflow-api.onrender.com`. Precisamos atualizar para a URL do Railway.

#### 2.1 Frontend Principal (`frontend/`)

**Arquivo:** `vercel.json`

Alterar:
```json
"destination": "https://logiflow-api.onrender.com/api/:path*"
```

Para:
```json
"destination": "https://seu-backend.railway.app/api/:path*"
```

Também atualizar:
```json
"destination": "https://logiflow-api.onrender.com/auth/:path*"
```

Para:
```json
"destination": "https://seu-backend.railway.app/auth/:path*"
```

#### 2.2 App Motorista (`app-motorista/`)

**Arquivo:** `vercel.json`

Alterar:
```json
"destination": "https://logiflow-api.onrender.com/api/:path*"
```

Para:
```json
"destination": "https://seu-backend.railway.app/api/:path*"
```

**Arquivo:** `src/services/api.js`

Verificar se o `baseURL` está configurado corretamente. Atualmente está vazio, o que significa que usa URLs relativas. Isso é correto com o rewrite do Vercel.

#### 2.3 Portal Cliente (`portal-cliente/`)

**Arquivo:** `vercel.json`

Alterar:
```json
"destination": "https://logiflow-api.onrender.com/api/:path*"
```

Para:
```json
"destination": "https://seu-backend.railway.app/api/:path*"
```

#### 2.4 Site de Divulgação (`site-divulgacao/`)

**Arquivo:** `vercel.json`

Este não tem rewrites para API, então não precisa alterar.

---

### FASE 3: Validar Integração

#### 3.1 Testar Endpoints de Saúde

```bash
# Verificar se o backend está respondendo
curl https://seu-backend.railway.app/health

# Verificar documentação da API
curl https://seu-backend.railway.app/api/v1/docs
```

#### 3.2 Testar CORS

Acessar um dos frontends e verificar no console do navegador se há erros de CORS.

#### 3.3 Testar Autenticação

1. Fazer login em um dos frontends
2. Verificar se as requisições de API estão funcionando
3. Verificar nos logs do Railway se há erros

#### 3.4 Testar Banco de Dados

```bash
# Via Railway CLI
railway run python -c "from database import get_engine; print(get_engine().connect())"
```

---

## 🔧 Checklist de Configuração

### Backend Railway
- [ ] Root Directory configurado: `LogiFlow CRM/backend`
- [ ] PostgreSQL adicionado
- [ ] Redis adicionado
- [ ] Variáveis de ambiente configuradas
- [ ] Migrações executadas (`alembic upgrade head`)
- [ ] Healthcheck respondendo em `/health`
- [ ] URL do backend obtida (ex: `https://seu-backend.railway.app`)

### Frontends Vercel
- [ ] `frontend/vercel.json` atualizado com URL do Railway
- [ ] `app-motorista/vercel.json` atualizado com URL do Railway
- [ ] `portal-cliente/vercel.json` atualizado com URL do Railway
- [ ] Todos os frontends fazem deploy automático após push
- [ ] CORS configurado no backend para domínios do Vercel

### Validação
- [ ] Backend respondendo em `/health`
- [ ] Documentação da API acessível em `/api/v1/docs`
- [ ] Frontends conseguem fazer requisições para o backend
- [ ] Autenticação funcionando
- [ ] Banco de dados conectado e migrações executadas

---

## 🚨 Problemas Comuns

### Erro de CORS
**Causa:** `ALLOWED_ORIGINS` não inclui os domínios do Vercel

**Solução:** Adicionar todos os domínios do Vercel em `ALLOWED_ORIGINS`:
```
ALLOWED_ORIGINS=https://logiflow-frontend.vercel.app,https://logiflow-motorista.vercel.app,https://logiflow-cliente.vercel.app,https://logiflow-site.vercel.app
```

### Erro de Conexão com Banco de Dados
**Causa:** `DATABASE_URL` não configurada ou PostgreSQL não adicionado

**Solução:** 
1. Adicionar PostgreSQL no Railway
2. Verificar se `DATABASE_URL` está em **Variables**

### Erro de Conexão com Redis
**Causa:** `REDIS_URL` não configurada ou Redis não adicionado

**Solução:**
1. Adicionar Redis no Railway
2. Verificar se `REDIS_URL` está em **Variables**

### Migrações Falhando
**Causa:** Banco de dados não inicializado

**Solução:**
```bash
railway run alembic upgrade head
```

---

## 📚 Referências

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)
- [Redis on Railway](https://docs.railway.app/databases/redis)
- [Vercel Rewrites](https://vercel.com/docs/edge-network/rewrites)

---

## 🔐 Segurança

**Antes de colocar em produção:**
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` forte e única
- [ ] Variáveis sensíveis como secrets
- [ ] CORS configurado apenas para domínios permitidos
- [ ] HTTPS habilitado (Railway fornece automaticamente)
- [ ] Backups do banco configurados

---

## 📞 Próximos Passos

1. **Fazer deploy do backend no Railway** seguindo a FASE 1
2. **Obter URL do backend** após deploy bem-sucedido
3. **Atualizar todos os frontends** com a nova URL (FASE 2)
4. **Fazer push dos frontends** para o Vercel
5. **Validar integração** (FASE 3)

---

**Data de Criação:** 27 de Fevereiro de 2026
**Status:** Pronto para implementação
