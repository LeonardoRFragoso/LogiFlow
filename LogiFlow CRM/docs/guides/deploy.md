# LogiFlow CRM - Guia de Deploy

## Deploy no Render

### Pré-requisitos

1. Conta no [Render](https://render.com)
2. Repositório Git conectado
3. Variáveis de ambiente configuradas

### Deploy via Blueprint

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **New** → **Blueprint**
3. Conecte seu repositório GitHub
4. Selecione o arquivo `render.yaml`
5. Clique em **Apply**

O Render criará automaticamente:
- ✅ API FastAPI (`logiflow-api`)
- ✅ Frontend Vue.js (`logiflow-frontend`)
- ✅ PostgreSQL (`logiflow-db`)
- ✅ Redis (`logiflow-redis`)

### Variáveis de Ambiente

Configure manualmente no painel do Render:

```env
# Integrações (opcional)
MELHOR_ENVIO_TOKEN=seu_token
FRENET_TOKEN=seu_token
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=sua_key

# ERP
OMIE_APP_KEY=sua_key
OMIE_APP_SECRET=seu_secret
BLING_API_KEY=sua_key

# WhatsApp
EVOLUTION_API_URL=https://sua-url
EVOLUTION_API_KEY=sua_key

# Pagamentos
MERCADOPAGO_ACCESS_TOKEN=seu_token
```

### Deploy Manual

```bash
# 1. Instalar Render CLI
npm install -g @render/cli

# 2. Login
render login

# 3. Deploy
render up
```

## Deploy Alternativo (Railway)

### railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "LogiFlow CRM/docker/api/Dockerfile"
  },
  "deploy": {
    "startCommand": "cd 'LogiFlow CRM/backend' && uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Comandos Railway

```bash
# Instalar CLI
npm install -g @railway/cli

# Login e deploy
railway login
railway init
railway up
```

## Verificação Pós-Deploy

### 1. Health Check

```bash
curl https://logiflow-api.onrender.com/health
# Esperado: {"status": "ok", ...}
```

### 2. Documentação API

Acesse: `https://logiflow-api.onrender.com/api/v1/docs`

### 3. Migrations

```bash
# Verificar status
render ssh logiflow-api
cd /app/backend
alembic current

# Aplicar migrations pendentes
alembic upgrade head
```

### 4. Logs

```bash
render logs logiflow-api --tail
```

## Domínio Customizado

1. No Render Dashboard, selecione o serviço
2. Vá em **Settings** → **Custom Domain**
3. Adicione seu domínio (ex: `api.logiflow.com.br`)
4. Configure DNS:
   ```
   CNAME api → logiflow-api.onrender.com
   ```

## Monitoramento

### Métricas Render

- CPU, Memory, Network no Dashboard
- Alertas de erro via email

### Logs Estruturados

A API usa loguru com formato JSON. Configure um serviço de logs:

```env
# Datadog
DD_API_KEY=sua_key

# Sentry
SENTRY_DSN=https://xxx@sentry.io/xxx
```

## Custos Estimados (Render)

| Serviço | Plano | Custo/mês |
|---------|-------|-----------|
| API | Starter | $7 |
| Frontend | Static Free | $0 |
| PostgreSQL | Starter | $7 |
| Redis | Starter | $0 |
| **Total** | | **~$14/mês** |

## Troubleshooting

### Build falhou

```bash
# Verificar logs de build
render logs logiflow-api --build

# Causas comuns:
# - requirements.txt inválido
# - Variáveis de ambiente faltando
# - Dockerfile incorreto
```

### API não responde

1. Verificar health check: `GET /health`
2. Verificar logs: `render logs logiflow-api`
3. Verificar variáveis de ambiente
4. Verificar conexão com banco

### Migrations falharam

```bash
# SSH no serviço
render ssh logiflow-api

# Verificar status
alembic current
alembic history

# Forçar upgrade
alembic upgrade head --sql  # Ver SQL
alembic upgrade head        # Executar
```
