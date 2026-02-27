# 🔧 Configuração de Variáveis de Ambiente no Railway

## 📋 Variáveis Obrigatórias

Estas variáveis **DEVEM** ser configuradas no Railway Dashboard para o backend funcionar:

### 1. Configurações da Aplicação

```
DEBUG=False
SECRET_KEY=<GERE-UMA-CHAVE-SECRETA-FORTE>
API_PREFIX=/api
API_VERSION=v1
```

**Como gerar SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2. CORS - URLs dos Frontends

```
ALLOWED_ORIGINS=https://logi-flow-blush.vercel.app,https://logi-flow-app-motorista.vercel.app,https://logi-flow-z315.vercel.app,https://logi-flow-wuhp.vercel.app,https://logiflow.com.br
```

**Domínios configurados:**
- Frontend Principal: `https://logi-flow-blush.vercel.app`
- App Motorista: `https://logi-flow-app-motorista.vercel.app`
- Portal Cliente: `https://logi-flow-z315.vercel.app`
- Site Divulgação: `https://logi-flow-wuhp.vercel.app`
- Domínio customizado: `https://logiflow.com.br`

### 3. Banco de Dados (PostgreSQL)

Railway fornece automaticamente quando você adiciona PostgreSQL:
- `DATABASE_URL` ✅ (automático)
- `PGHOST` ✅ (automático)
- `PGPORT` ✅ (automático)
- `PGDATABASE` ✅ (automático)
- `PGUSER` ✅ (automático)
- `PGPASSWORD` ✅ (automático)

### 4. Cache (Redis)

Railway fornece automaticamente quando você adiciona Redis:
- `REDIS_URL` ✅ (automático)
- `REDIS_HOST` ✅ (automático)
- `REDIS_PORT` ✅ (automático)
- `REDIS_PASSWORD` ✅ (automático)

---

## 📦 Variáveis de Integrações (Opcionais)

Configure conforme necessário para sua aplicação:

### Google Maps
```
GOOGLE_MAPS_API_KEY=<sua-chave-api>
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=<sua-chave-api>
```

### Mercado Pago (Pagamentos)
```
MERCADOPAGO_ACCESS_TOKEN=<seu-access-token>
MERCADOPAGO_PUBLIC_KEY=<sua-chave-publica>
MERCADOPAGO_WEBHOOK_URL=https://seu-backend.railway.app/api/billing/webhooks/mercadopago
CHECKOUT_SUCCESS_URL=https://seu-frontend.vercel.app/checkout/success
CHECKOUT_FAILURE_URL=https://seu-frontend.vercel.app/checkout/failure
CHECKOUT_PENDING_URL=https://seu-frontend.vercel.app/checkout/pending
```

### Focus NFe (CT-e/MDF-e)
```
FOCUSNFE_TOKEN=<seu-token>
FOCUSNFE_ENVIRONMENT=producao
```

### Evolution API (WhatsApp)
```
EVOLUTION_API_URL=<url-da-sua-evolution-api>
EVOLUTION_API_KEY=<sua-chave-api>
EVOLUTION_INSTANCE_NAME=logiflow
```

### Email (SMTP)
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

### ERP Integrations
```
# Omie ERP
OMIE_APP_KEY=<sua-chave>
OMIE_APP_SECRET=<seu-secret>

# Bling ERP
BLING_ACCESS_TOKEN=<seu-token>
```

### Frete e Rastreamento
```
# Melhor Envio
MELHOR_ENVIO_TOKEN=<seu-token>
MELHOR_ENVIO_SANDBOX=false

# Frenet
FRENET_TOKEN=<seu-token>

# Sascar GPS
SASCAR_API_KEY=<sua-chave>
SASCAR_API_SECRET=<seu-secret>
SASCAR_SIMULATION_MODE=false

# Autotrac GPS
AUTOTRAC_USERNAME=<seu-usuario>
AUTOTRAC_PASSWORD=<sua-senha>
AUTOTRAC_SIMULATION_MODE=false

# Onixsat GPS
ONIXSAT_API_TOKEN=<seu-token>
ONIXSAT_SIMULATION_MODE=false
```

---

## 🚀 Como Configurar no Railway Dashboard

### Passo 1: Acessar Settings
1. Abra o projeto no Railway
2. Clique no serviço do backend
3. Vá em **Settings** (ícone de engrenagem)

### Passo 2: Ir para Variables
1. Role até **Variables**
2. Clique em **Add Variable**

### Passo 3: Adicionar Variáveis
1. Digite o nome da variável (ex: `DEBUG`)
2. Digite o valor (ex: `False`)
3. Clique em **Add**
4. Repita para todas as variáveis

### Passo 4: Confirmar
1. Após adicionar todas as variáveis, o Railway fará redeploy automático
2. Verifique os logs para confirmar que a aplicação iniciou corretamente

---

## ✅ Checklist de Configuração

### Obrigatórias
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=<chave-forte>`
- [ ] `API_PREFIX=/api`
- [ ] `API_VERSION=v1`
- [ ] `ALLOWED_ORIGINS=<seus-domínios>`
- [ ] PostgreSQL adicionado (DATABASE_URL automático)
- [ ] Redis adicionado (REDIS_URL automático)

### Recomendadas
- [ ] Google Maps configurado
- [ ] Mercado Pago configurado
- [ ] Email SMTP configurado
- [ ] Focus NFe configurado (se usar CT-e/MDF-e)
- [ ] Evolution API configurado (se usar WhatsApp)

### Opcionais
- [ ] ERP Integrations
- [ ] Frete e Rastreamento
- [ ] Outras integrações conforme necessário

---

## 🔍 Verificar Configuração

Após configurar todas as variáveis:

### 1. Verificar Health Check
```bash
curl https://seu-backend.railway.app/health
```

Resposta esperada:
```json
{"status": "ok"}
```

### 2. Verificar Documentação da API
```
https://seu-backend.railway.app/api/v1/docs
```

### 3. Verificar Logs
No Railway Dashboard:
1. Clique em **Deployments**
2. Selecione o deploy ativo
3. Clique em **View Logs**
4. Procure por erros de inicialização

---

## 🐛 Troubleshooting

### Erro: "DATABASE_URL not found"
**Solução:** Adicione PostgreSQL no Railway e aguarde a variável aparecer automaticamente.

### Erro: "REDIS_URL not found"
**Solução:** Adicione Redis no Railway e aguarde a variável aparecer automaticamente.

### Erro: "CORS policy blocked"
**Solução:** Verifique se `ALLOWED_ORIGINS` inclui o domínio do seu frontend.

### Erro: "Secret key not configured"
**Solução:** Gere uma chave secreta forte e configure `SECRET_KEY`.

---

## 📚 Referências

- [Railway Variables Documentation](https://docs.railway.app/develop/variables)
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [Environment Variables Best Practices](https://12factor.net/config)

---

**Última atualização:** 27 de Fevereiro de 2026
