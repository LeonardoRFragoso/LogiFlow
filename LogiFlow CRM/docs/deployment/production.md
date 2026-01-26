# LogiFlow CRM - Production Deployment

> Guia de deploy em produção (Render.com)

## Arquitetura de Produção

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERNET                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     CLOUDFLARE CDN                           │
│                    (SSL, DDoS, Cache)                        │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │ Frontend │    │   API    │    │   Site   │
       │ (Render) │    │ (Render) │    │ (Render) │
       └──────────┘    └────┬─────┘    └──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │PostgreSQL│  │  Redis   │  │  Celery  │
       │ (Render) │  │ (Render) │  │ (Render) │
       └──────────┘  └──────────┘  └──────────┘
```

## Deploy via Render.com

### 1. Pré-requisitos

- Conta no [Render.com](https://render.com)
- Repositório no GitHub conectado
- Secrets configurados

### 2. Configuração (render.yaml)

O projeto já possui `render.yaml` configurado:

```yaml
services:
  - type: web
    name: logiflow-api
    env: docker
    dockerfilePath: ./backend/Dockerfile
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: logiflow-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: logiflow-redis
          type: redis
          property: connectionString

databases:
  - name: logiflow-db
    plan: starter
    postgresMajorVersion: 15
```

### 3. Deploy Automático

O CI/CD está configurado para deploy automático:

- **Push para `main`** → Deploy em produção
- **Push para `develop`** → Deploy em staging

### 4. Deploy Manual

```bash
# Via Render CLI
render deploy

# Via GitHub Actions
gh workflow run cd.yml
```

## Checklist Pré-Deploy

### Código
- [ ] Todos os testes passando
- [ ] Lint sem erros
- [ ] Build do frontend OK
- [ ] Migrations testadas

### Configuração
- [ ] Variáveis de ambiente configuradas
- [ ] DEBUG=false
- [ ] SECRET_KEY único e seguro
- [ ] CORS configurado para domínio de produção

### Segurança
- [ ] HTTPS habilitado
- [ ] Secrets não expostos
- [ ] Rate limiting ativo
- [ ] Logs configurados

## Variáveis de Ambiente (Produção)

```bash
# Core
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=<256-bit-random-key>

# Database
DATABASE_URL=<render-postgres-url>

# Redis
REDIS_URL=<render-redis-url>

# External APIs
MERCADOPAGO_ACCESS_TOKEN=<production-token>
FOCUS_NFE_TOKEN=<production-token>
WHATSAPP_API_TOKEN=<production-token>

# CORS
ALLOWED_ORIGINS=https://app.logiflow.com.br,https://logiflow.com.br
```

## Monitoramento Pós-Deploy

### 1. Health Check

```bash
curl https://api.logiflow.com.br/health
# Esperado: {"status": "ok", "redis": true}

curl https://api.logiflow.com.br/ready
# Esperado: {"status": "ready", "redis": true}
```

### 2. Verificar Logs

```bash
# Via Render Dashboard
# ou via CLI
render logs logiflow-api
```

### 3. Testar Endpoints Críticos

```bash
# Login
curl -X POST https://api.logiflow.com.br/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test"}'
```

## Rollback

### Via Render Dashboard

1. Acesse Service → Deploys
2. Selecione deploy anterior
3. Clique "Rollback"

### Via CLI

```bash
render rollback logiflow-api <deploy-id>
```

## Scaling

### Horizontal (mais instâncias)

```yaml
# render.yaml
services:
  - type: web
    name: logiflow-api
    scaling:
      minInstances: 2
      maxInstances: 10
```

### Vertical (mais recursos)

```yaml
# render.yaml
services:
  - type: web
    name: logiflow-api
    plan: standard  # ou professional
```

## Disaster Recovery

### Backup do Banco

```bash
# Render faz backups automáticos diários
# Para backup manual:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
# Via Render Dashboard → Database → Backups → Restore
# ou via CLI
psql $DATABASE_URL < backup.sql
```

## Custos Estimados (Render.com)

| Recurso | Plano | Custo/mês |
|---------|-------|-----------|
| API (Web Service) | Starter | $7 |
| Frontend (Static) | Free | $0 |
| PostgreSQL | Starter | $7 |
| Redis | Starter | $7 |
| **Total** | | **~$21/mês** |

*Valores podem variar. Consulte [Render Pricing](https://render.com/pricing)*
