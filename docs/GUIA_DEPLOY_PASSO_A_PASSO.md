# 📖 Guia de Deploy Passo a Passo: Railway + Vercel

## 🎯 Objetivo Final

Fazer o deploy do backend no Railway e conectar todos os frontends do Vercel para usar a nova URL.

---

## ⏱️ Tempo Estimado

- **Fase 1 (Railway):** 15-20 minutos
- **Fase 2 (Vercel):** 5-10 minutos
- **Fase 3 (Validação):** 5-10 minutos
- **Total:** ~30-40 minutos

---

## 🚀 FASE 1: Deploy do Backend no Railway

### Passo 1.1: Criar Novo Projeto no Railway

1. Acesse [railway.app](https://railway.app)
2. Faça login com sua conta
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório **`LeonardoRFragoso/LogiFlow`**
6. Aguarde o Railway criar o serviço inicial

### Passo 1.2: Configurar Root Directory (CRÍTICO)

**⚠️ Este passo é essencial para o deploy funcionar!**

1. Clique no serviço criado para abrir
2. Vá em **Settings** (ícone de engrenagem no topo)
3. Role até **Service Settings**
4. Encontre o campo **Root Directory** (ou **Source Directory**)
5. Digite: `LogiFlow CRM/backend`
6. Clique em **Deploy** ou aguarde o redeploy automático
7. Verifique os logs para confirmar que o build iniciou

**Esperado nos logs:**
```
Building project...
Installing dependencies...
Running build command...
```

### Passo 1.3: Adicionar Banco de Dados PostgreSQL

1. No projeto Railway, clique em **"New"** (botão azul no topo)
2. Selecione **"Database"**
3. Clique em **"Add PostgreSQL"**
4. Aguarde a criação (leva ~1-2 minutos)
5. Railway criará automaticamente as variáveis de ambiente:
   - `DATABASE_URL`
   - `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`

**Verificar:** Vá em **Settings** → **Variables** e confirme que `DATABASE_URL` aparece

### Passo 1.4: Adicionar Cache Redis

1. Clique em **"New"** novamente
2. Selecione **"Database"**
3. Clique em **"Add Redis"**
4. Aguarde a criação (leva ~1-2 minutos)
5. Railway criará automaticamente:
   - `REDIS_URL`
   - `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`

**Verificar:** Vá em **Settings** → **Variables** e confirme que `REDIS_URL` aparece

### Passo 1.5: Configurar Variáveis de Ambiente

1. No projeto Railway, vá em **Settings** → **Variables**
2. Clique em **"Add Variable"** para cada uma:

**Variáveis Obrigatórias:**

```
DEBUG = False
SECRET_KEY = <GERE-UMA-CHAVE-FORTE>
API_PREFIX = /api
API_VERSION = v1
ALLOWED_ORIGINS = https://logi-flow-blush.vercel.app,https://logi-flow-app-motorista.vercel.app,https://logi-flow-z315.vercel.app,https://logi-flow-wuhp.vercel.app,https://logiflow.com.br
```

**Como gerar SECRET_KEY (execute no terminal):**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Variáveis Opcionais (conforme necessário):**

```
GOOGLE_MAPS_API_KEY = <sua-chave>
MERCADOPAGO_ACCESS_TOKEN = <seu-token>
FOCUSNFE_TOKEN = <seu-token>
EVOLUTION_API_URL = <url-da-api>
EVOLUTION_API_KEY = <sua-chave>
SMTP_HOST = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = <seu-email>
SMTP_PASSWORD = <senha-de-app>
```

**Dica:** Copie as variáveis do arquivo `/LogiFlow CRM/backend/.env.railway` como referência.

### Passo 1.6: Aguardar Deploy Bem-Sucedido

1. Vá em **Deployments** no Railway
2. Aguarde o status mudar para **"Success"** (verde)
3. Se houver erro, clique em **"View Logs"** para diagnosticar

**Esperado nos logs:**
```
✓ Build completed successfully
✓ Starting application...
✓ Application started on port 8000
```

### Passo 1.7: Executar Migrações do Banco de Dados

Após o deploy bem-sucedido, execute as migrações:

**Opção A: Via Railway CLI (Recomendado)**

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Fazer login
railway login

# Conectar ao projeto
railway link

# Executar migrações
railway run alembic upgrade head
```

**Opção B: Via Railway Dashboard**

1. Vá em **Deployments** → selecione o deploy ativo
2. Clique em **"View Logs"**
3. Use o terminal integrado para executar:
   ```bash
   alembic upgrade head
   ```

### Passo 1.8: Obter URL do Backend

1. No Railway, vá em **Settings** → **Networking**
2. Clique em **"Generate Domain"** para obter um domínio `.railway.app`
3. Anote a URL completa (ex: `https://logiflow-backend.railway.app`)

**Verificar saúde do backend:**
```bash
curl https://seu-backend.railway.app/health
```

Resposta esperada:
```json
{"status": "ok"}
```

---

## 🔄 FASE 2: Atualizar Frontends no Vercel

**⚠️ Importante:** Substitua `https://logiflow-backend.railway.app` pela URL real do seu backend!

### Passo 2.1: Atualizar Frontend Principal

**Arquivo:** `/LogiFlow CRM/frontend/vercel.json`

✅ **Já atualizado!** Os rewrites agora apontam para:
```json
"destination": "https://logiflow-backend.railway.app/api/:path*"
```

### Passo 2.2: Atualizar App Motorista

**Arquivo:** `/LogiFlow CRM/app-motorista/vercel.json`

✅ **Já atualizado!** Os rewrites agora apontam para:
```json
"destination": "https://logiflow-backend.railway.app/api/:path*"
```

### Passo 2.3: Atualizar Portal Cliente

**Arquivo:** `/LogiFlow CRM/portal-cliente/vercel.json`

✅ **Já atualizado!** Os rewrites agora apontam para:
```json
"destination": "https://logiflow-backend.railway.app/api/:path*"
```

### Passo 2.4: Fazer Commit e Push

```bash
# Adicionar mudanças
git add LogiFlow\ CRM/frontend/vercel.json
git add LogiFlow\ CRM/app-motorista/vercel.json
git add LogiFlow\ CRM/portal-cliente/vercel.json

# Fazer commit
git commit -m "chore: atualizar URLs do backend para Railway"

# Fazer push
git push origin main
```

### Passo 2.5: Verificar Deploy no Vercel

1. Acesse [vercel.com](https://vercel.com)
2. Vá em cada projeto (frontend, app-motorista, portal-cliente)
3. Aguarde o deploy automático completar
4. Verifique o status (deve estar verde)

---

## ✅ FASE 3: Validar Integração

### Passo 3.1: Testar Health Check do Backend

```bash
curl https://seu-backend.railway.app/health
```

Resposta esperada:
```json
{"status": "ok"}
```

### Passo 3.2: Testar Documentação da API

Acesse no navegador:
```
https://seu-backend.railway.app/api/v1/docs
```

Você deve ver a documentação interativa do Swagger.

### Passo 3.3: Testar CORS

1. Abra um dos frontends (ex: `https://logiflow-frontend.vercel.app`)
2. Abra o console do navegador (F12)
3. Tente fazer login ou acessar uma funcionalidade que chame a API
4. Verifique se há erros de CORS

**Se houver erro de CORS:**
- Volte ao Railway
- Vá em **Settings** → **Variables**
- Verifique se `ALLOWED_ORIGINS` inclui o domínio do frontend
- Atualize se necessário

### Passo 3.4: Testar Autenticação

1. Acesse um dos frontends
2. Tente fazer login com credenciais válidas
3. Verifique se a autenticação funciona
4. Verifique se as requisições de API estão sendo feitas corretamente

### Passo 3.5: Verificar Logs do Railway

Se houver problemas:

1. Vá ao Railway Dashboard
2. Clique no serviço do backend
3. Vá em **Deployments** → **View Logs**
4. Procure por mensagens de erro
5. Ajuste as variáveis de ambiente conforme necessário

---

## 🔧 Solução de Problemas

### ❌ Erro: "Build failed"

**Causa:** Root Directory não configurado corretamente

**Solução:**
1. Vá em **Settings** → **Service Settings**
2. Confirme que **Root Directory** é `LogiFlow CRM/backend`
3. Clique em **Deploy** para tentar novamente

### ❌ Erro: "DATABASE_URL not found"

**Causa:** PostgreSQL não foi adicionado

**Solução:**
1. Clique em **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Aguarde a criação
3. Verifique se `DATABASE_URL` aparece em **Variables**

### ❌ Erro: "CORS policy blocked"

**Causa:** `ALLOWED_ORIGINS` não inclui o domínio do frontend

**Solução:**
1. Vá em **Settings** → **Variables**
2. Edite `ALLOWED_ORIGINS` para incluir:
   ```
   https://logiflow-frontend.vercel.app,https://logiflow-motorista.vercel.app,https://logiflow-cliente.vercel.app
   ```

### ❌ Erro: "Connection refused"

**Causa:** Backend não está respondendo

**Solução:**
1. Verifique se o deploy foi bem-sucedido (status verde)
2. Verifique os logs em **Deployments** → **View Logs**
3. Procure por erros de inicialização

### ❌ Erro: "Migrations failed"

**Causa:** Banco de dados não foi inicializado

**Solução:**
```bash
railway run alembic upgrade head
```

---

## 📋 Checklist Final

### Backend Railway
- [ ] Projeto criado no Railway
- [ ] Root Directory configurado: `LogiFlow CRM/backend`
- [ ] PostgreSQL adicionado
- [ ] Redis adicionado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy bem-sucedido (status verde)
- [ ] Migrações executadas
- [ ] Health check respondendo: `/health`
- [ ] Documentação acessível: `/api/v1/docs`
- [ ] URL do backend obtida

### Frontends Vercel
- [ ] `frontend/vercel.json` atualizado
- [ ] `app-motorista/vercel.json` atualizado
- [ ] `portal-cliente/vercel.json` atualizado
- [ ] Mudanças feitas commit e push
- [ ] Deploy automático completado em todos os frontends

### Validação
- [ ] Health check respondendo
- [ ] Documentação da API acessível
- [ ] Frontends conseguem fazer requisições
- [ ] Autenticação funcionando
- [ ] Sem erros de CORS no console

---

## 🎉 Próximas Etapas

Após completar este guia:

1. **Testar funcionalidades principais** em cada frontend
2. **Monitorar logs** do Railway nos primeiros dias
3. **Configurar alertas** no Railway para erros
4. **Fazer backup** do banco de dados PostgreSQL
5. **Documentar** qualquer configuração adicional necessária

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique os **logs do Railway** em **Deployments** → **View Logs**
2. Consulte a documentação:
   - [Railway Docs](https://docs.railway.app)
   - [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
3. Abra uma issue no repositório com os logs de erro

---

**Última atualização:** 27 de Fevereiro de 2026
**Status:** Pronto para implementação
