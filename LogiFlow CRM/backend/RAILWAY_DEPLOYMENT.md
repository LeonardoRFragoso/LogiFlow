# 🚂 Deploy do Backend LogiFlow no Railway

Este guia detalha o processo completo de deploy do backend FastAPI do LogiFlow CRM no Railway.

## 📋 Pré-requisitos

- Conta no [Railway](https://railway.app)
- Repositório Git do projeto (GitHub, GitLab ou Bitbucket)
- Credenciais das APIs externas (Mercado Pago, Google Maps, etc.)

## 🚀 Passo a Passo

### 1. Criar Novo Projeto no Railway

1. Acesse [railway.app](https://railway.app) e faça login
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Escolha o repositório `LogiFlow`
5. Selecione a pasta `LogiFlow CRM/backend` como root directory

### 2. Adicionar Serviços de Banco de Dados

#### PostgreSQL

1. No projeto Railway, clique em **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway criará automaticamente as variáveis:
   - `DATABASE_URL` (URL completa)
   - `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` (individuais)

#### Redis

1. No projeto Railway, clique em **"New"** → **"Database"** → **"Add Redis"**
2. Railway criará automaticamente as variáveis:
   - `REDIS_URL` (URL completa)
   - `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` (individuais)

### 3. Configurar Variáveis de Ambiente

No Railway Dashboard, vá em **Settings** → **Variables** e adicione:

#### Variáveis Obrigatórias

```bash
# App
DEBUG=False
SECRET_KEY=<gere-uma-chave-secreta-forte-aqui>

# CORS - Adicione seus domínios
ALLOWED_ORIGINS=https://seu-frontend.railway.app,https://logiflow.com.br

# API Config
API_PREFIX=/api
API_VERSION=v1
```

#### Variáveis de Integrações (Opcionais)

Configure conforme necessário:

```bash
# Google Maps
GOOGLE_MAPS_API_KEY=<sua-chave>
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=<sua-chave>

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=<seu-token>
MERCADOPAGO_PUBLIC_KEY=<sua-chave-publica>
CHECKOUT_SUCCESS_URL=https://seu-frontend.railway.app/checkout/success
CHECKOUT_FAILURE_URL=https://seu-frontend.railway.app/checkout/failure
CHECKOUT_PENDING_URL=https://seu-frontend.railway.app/checkout/pending

# Focus NFe
FOCUSNFE_TOKEN=<seu-token>
FOCUSNFE_ENVIRONMENT=producao

# Evolution API (WhatsApp)
EVOLUTION_API_URL=<url-da-sua-evolution-api>
EVOLUTION_API_KEY=<sua-chave>
EVOLUTION_INSTANCE_NAME=logiflow

# Email SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<seu-email>
SMTP_PASSWORD=<senha-de-app>
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

**Dica:** Use o arquivo `.env.railway` como referência para todas as variáveis disponíveis.

### 4. Configurar Build e Deploy

O Railway detectará automaticamente os arquivos de configuração:

- `railway.json` - Configurações do Railway
- `nixpacks.toml` - Configurações de build
- `Procfile` - Comando de start (fallback)
- `requirements.txt` - Dependências Python
- `runtime.txt` - Versão do Python (3.11.7)

**Configuração automática:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4`
- **Healthcheck:** `/health`

### 5. Configurar Domínio Customizado (Opcional)

1. No Railway Dashboard, vá em **Settings** → **Networking**
2. Clique em **"Generate Domain"** para obter um domínio `.railway.app`
3. Ou adicione seu domínio customizado em **"Custom Domain"**

### 6. Executar Migrações do Banco de Dados

Após o primeiro deploy, execute as migrações Alembic:

**Opção 1: Via Railway CLI**

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Conectar ao projeto
railway link

# Executar migrações
railway run alembic upgrade head
```

**Opção 2: Via Railway Dashboard**

1. Vá em **Deployments** → selecione o deploy ativo
2. Clique em **"View Logs"**
3. Use o terminal integrado para executar:
   ```bash
   alembic upgrade head
   ```

### 7. Verificar Deploy

Acesse os endpoints de health check:

- `https://seu-backend.railway.app/health` - Liveness probe
- `https://seu-backend.railway.app/ready` - Readiness probe
- `https://seu-backend.railway.app/api/v1/docs` - Documentação Swagger (se DEBUG=True)

## 🔧 Configurações Avançadas

### Escalabilidade

Railway permite ajustar recursos:

1. **Settings** → **Resources**
2. Ajuste CPU e RAM conforme necessário
3. Configure auto-scaling se disponível no seu plano

### Monitoramento

- **Logs:** Acesse em **Deployments** → **View Logs**
- **Metrics:** Veja CPU, RAM e Network em **Metrics**
- **Alerts:** Configure em **Settings** → **Alerts**

### Variáveis de Ambiente por Ambiente

Railway suporta múltiplos ambientes:

1. Crie ambientes em **Settings** → **Environments**
2. Configure variáveis específicas por ambiente (dev, staging, production)

### Backup do Banco de Dados

Configure backups automáticos do PostgreSQL:

1. Acesse o serviço PostgreSQL
2. **Settings** → **Backups**
3. Configure frequência e retenção

## 🔒 Segurança

### Checklist de Segurança

- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` forte e única
- [ ] Variáveis sensíveis configuradas como secrets
- [ ] CORS configurado apenas para domínios permitidos
- [ ] HTTPS habilitado (Railway fornece automaticamente)
- [ ] Credenciais de APIs em variáveis de ambiente
- [ ] Backups do banco configurados

### Gerar SECRET_KEY Segura

```python
import secrets
print(secrets.token_urlsafe(32))
```

## 🐛 Troubleshooting

### Erro de Conexão com Banco de Dados

```bash
# Verificar se DATABASE_URL está configurada
railway variables

# Testar conexão
railway run python -c "from database import get_engine; get_engine().connect()"
```

### Erro de Importação de Módulos

```bash
# Verificar se todas as dependências foram instaladas
railway run pip list

# Reinstalar dependências
railway run pip install -r requirements.txt --force-reinstall
```

### Aplicação não inicia

1. Verifique os logs: **Deployments** → **View Logs**
2. Confirme que o `PORT` está sendo usado corretamente
3. Verifique se todas as variáveis obrigatórias estão configuradas

### Healthcheck falhando

```bash
# Testar healthcheck localmente
curl https://seu-backend.railway.app/health

# Verificar logs
railway logs
```

## 📚 Recursos Adicionais

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL on Railway](https://docs.railway.app/databases/postgresql)
- [Redis on Railway](https://docs.railway.app/databases/redis)

## 🔄 CI/CD Automático

Railway faz deploy automático quando você:

1. Faz push para a branch configurada (geralmente `main` ou `master`)
2. Cria uma Pull Request (se configurado)
3. Faz merge de PR

Configure em **Settings** → **Triggers**

## 📊 Monitoramento de Performance

### Logs Estruturados

A aplicação usa Loguru para logs estruturados. Acesse em:

```bash
railway logs --follow
```

### Métricas Customizadas

Configure integração com:
- Sentry (error tracking)
- DataDog (APM)
- New Relic (monitoring)

Via variáveis de ambiente no Railway.

## ✅ Checklist Final

Antes de colocar em produção:

- [ ] Todas as variáveis de ambiente configuradas
- [ ] PostgreSQL e Redis conectados
- [ ] Migrações executadas (`alembic upgrade head`)
- [ ] Healthcheck respondendo corretamente
- [ ] CORS configurado para domínios corretos
- [ ] DEBUG=False
- [ ] SECRET_KEY configurada
- [ ] Backups do banco configurados
- [ ] Domínio customizado configurado (se aplicável)
- [ ] Monitoramento e alertas configurados
- [ ] Documentação da API acessível (ou desabilitada)

---

**Suporte:** Para dúvidas, consulte a documentação do LogiFlow ou abra uma issue no repositório.
