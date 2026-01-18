# Guia Completo de Configuração - LogiFlow CRM

## 🎯 Visão Geral

Este guia consolida TODAS as configurações necessárias para colocar o LogiFlow CRM em produção após a análise de gaps.

---

## ✅ Status da Implementação

### GAPS CRÍTICOS (Bloqueadores) ✅ COMPLETOS

| # | Gap | Status | Doc | Script Teste |
|---|-----|--------|-----|--------------|
| 1 | Mercado Pago | ✅ | [MERCADOPAGO_SETUP.md](MERCADOPAGO_SETUP.md) | `test_mercadopago.py` |
| 2 | Sistema de Emails | ✅ | [EMAIL_SETUP.md](EMAIL_SETUP.md) | `test_email.py` |
| 3 | Webhook → Provisionamento | ✅ | Integrado no código | N/A |

### GAPS IMPORTANTES (Funcionalidades Prometidas)

| # | Gap | Status | Doc | Script Teste |
|---|-----|--------|-----|--------------|
| 4 | Focus NFe (CT-e/MDF-e) | ✅ | [FOCUSNFE_SETUP.md](FOCUSNFE_SETUP.md) | `test_focusnfe.py` |
| 5 | Evolution API (WhatsApp) | ⚠️ | [Ver abaixo](#evolution-api) | N/A |
| 6 | Google Maps API | ⚠️ | [Ver abaixo](#google-maps-api) | N/A |
| 7 | Notificações Vendas | ⚠️ | [Ver abaixo](#notificacoes-slack-discord) | N/A |

---

## 🚀 Ordem de Implementação Recomendada

### Semana 1: CRÍTICOS (Sistema funcionando)

```
✅ Dia 1-2: Mercado Pago
   - Criar conta sandbox
   - Configurar credenciais
   - Testar checkout
   - Configurar webhook

✅ Dia 2-3: Sistema de Emails
   - Escolher provider SMTP
   - Configurar credenciais
   - Testar envios
   - Validar templates

✅ Dia 3-4: Webhook + Provisionamento
   - Testar fluxo completo
   - Validar emails automáticos
   - Ajustar retry

✅ Dia 5: Validação End-to-End
   - Site → Demo → Checkout → Pagamento → Provisionamento
```

### Semana 2: IMPORTANTES (Funcionalidades Core)

```
✅ Dia 1: Focus NFe
   - Criar conta
   - Upload certificado
   - Obter token
   - Testar emissão CT-e

⚠️ Dia 2: Evolution API (WhatsApp)
   - Instalar via Docker
   - Configurar instância
   - Testar envio

⚠️ Dia 3: Google Maps API
   - Criar projeto GCP
   - Ativar APIs
   - Obter key
   - Testar cotações

⚠️ Dia 4: Notificações
   - Configurar Slack/Discord
   - Testar webhooks
   - Integrar ao fluxo

Dia 5: Testes e ajustes
```

---

## 📋 Checklist Master de Configuração

### Backend - Variáveis de Ambiente

Copiar `.env.example` para `.env` e preencher:

```bash
# ========================================
# 🔴 CRÍTICO - Necessário para funcionar
# ========================================

# Email (SMTP) - CRÍTICO
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Senha de app
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br

# Mercado Pago - CRÍTICO
MERCADOPAGO_ACCESS_TOKEN=TEST-xxx  # ou APP_USR-xxx (produção)
MERCADOPAGO_PUBLIC_KEY=TEST-xxx
CHECKOUT_SUCCESS_URL=http://localhost:3001/checkout/success
CHECKOUT_FAILURE_URL=http://localhost:3001/checkout/failure
CHECKOUT_PENDING_URL=http://localhost:3001/checkout/pending

# Database - CRÍTICO
DB_HOST=localhost
DB_NAME=logiflow_crm
DB_USER=logiflow
DB_PASSWORD=logiflow123
DB_PORT=3306

# Redis - CRÍTICO
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis123

# ========================================
# 🟡 IMPORTANTE - Funcionalidades prometidas
# ========================================

# Focus NFe (CT-e/MDF-e) - IMPORTANTE
FOCUSNFE_TOKEN=homologacao_xxx  # ou producao_xxx
FOCUSNFE_ENVIRONMENT=homologacao

# WhatsApp / Evolution API - IMPORTANTE
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=REDACTED_EVOLUTION_API_KEY
EVOLUTION_INSTANCE_NAME=logiflow

# Google Maps API - IMPORTANTE
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Slack/Discord - IMPORTANTE
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/XXX

# ========================================
# 🟢 OPCIONAL - Modo simulação OK
# ========================================

# Rastreamento GPS (modo simulação ativo)
SASCAR_API_KEY=
SASCAR_SIMULATION_MODE=true

AUTOTRAC_USERNAME=
AUTOTRAC_SIMULATION_MODE=true

ONIXSAT_API_TOKEN=
ONIXSAT_SIMULATION_MODE=true
```

### Testes de Validação

Execute na ordem:

```bash
# 1. Testar Email
python scripts/test_email.py

# 2. Testar Mercado Pago
python scripts/test_mercadopago.py

# 3. Testar Focus NFe
python scripts/test_focusnfe.py

# 4. Testar backend completo
pytest backend/tests/test_email_service.py -v
```

---

## 🔧 Configurações Detalhadas por Serviço

### Evolution API (WhatsApp)

#### Instalação via Docker

```bash
# docker-compose.evolution.yml
version: '3.8'

services:
  evolution-api:
    image: atendai/evolution-api:latest
    ports:
      - "8080:8080"
    environment:
      - SERVER_URL=http://localhost:8080
      - AUTHENTICATION_API_KEY=REDACTED_EVOLUTION_API_KEY
    volumes:
      - evolution_data:/evolution/instances
    restart: unless-stopped

volumes:
  evolution_data:
```

Iniciar:
```bash
docker-compose -f docker-compose.evolution.yml up -d
```

#### Configuração

1. Acesse: http://localhost:8080
2. Autenticação: Header `apikey: REDACTED_EVOLUTION_API_KEY`
3. Criar instância:
```bash
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: REDACTED_EVOLUTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "logiflow",
    "qrcode": true
  }'
```

4. Escanear QR Code com WhatsApp

---

### Google Maps API

#### Passo 1: Criar Projeto

1. Acesse: https://console.cloud.google.com/
2. Criar novo projeto: "LogiFlow CRM"
3. Ativar APIs:
   - Maps JavaScript API
   - Distance Matrix API
   - Geocoding API
   - Places API

#### Passo 2: Obter API Key

1. APIs & Services → Credentials
2. Create Credentials → API Key
3. Copiar key: `AIzaSy...`

#### Passo 3: Restringir Key (Produção)

1. Edit API Key
2. Application restrictions: HTTP referrers
3. Website restrictions: `logiflow.com.br/*`
4. API restrictions: Selecionar apenas APIs necessárias

#### Teste

```bash
curl "https://maps.googleapis.com/maps/api/distancematrix/json?origins=São+Paulo,SP&destinations=Rio+de+Janeiro,RJ&key=SUA_KEY"
```

---

### Notificações Slack/Discord

#### Slack

1. Criar app: https://api.slack.com/apps
2. Incoming Webhooks → Activate
3. Add New Webhook to Workspace
4. Copiar URL: `https://hooks.slack.com/services/XXX`

Testar:
```bash
curl -X POST https://hooks.slack.com/services/XXX \
  -H "Content-Type: application/json" \
  -d '{"text": "🎯 Teste LogiFlow CRM"}'
```

#### Discord

1. Server Settings → Integrations → Webhooks
2. New Webhook
3. Copiar URL: `https://discord.com/api/webhooks/XXX`

Testar:
```bash
curl -X POST https://discord.com/api/webhooks/XXX \
  -H "Content-Type: application/json" \
  -d '{"content": "🎯 Teste LogiFlow CRM"}'
```

---

## 🧪 Validação End-to-End

### Fluxo Completo a Testar

```
1. ✅ Acessar site: http://localhost:5173
2. ✅ Preencher formulário de demo
3. ✅ Verificar email de confirmação recebido
4. ✅ Verificar notificação no Slack/Discord
5. ✅ Clicar em "Assinar Plano"
6. ✅ Preencher checkout
7. ✅ Usar cartão de teste MP
8. ✅ Aguardar webhook
9. ✅ Verificar provisionamento do tenant
10. ✅ Verificar email de credenciais
11. ✅ Fazer login com credenciais recebidas
12. ✅ Testar funcionalidades básicas
```

### Script de Teste Completo

Criar: `backend/scripts/test_end_to_end.py`

```python
"""
Teste end-to-end do fluxo completo
"""

import requests
import time

# 1. Solicitar demo
demo_response = requests.post("http://localhost:8000/demo/request", json={
    "name": "Teste E2E",
    "email": "teste-e2e@exemplo.com",
    "phone": "(11) 99999-9999",
    "company": "Empresa Teste E2E",
    "vehicles": "10"
})

print("1. Demo solicitado:", demo_response.json())

# 2. Simular criação de checkout
# (precisa ser manual via interface)

# 3. Verificar se tenant foi criado
# (após pagamento aprovado via webhook)

print("✅ Teste end-to-end iniciado")
print("Continue manualmente:")
print("- Verifique email de confirmação")
print("- Acesse checkout e pague com cartão teste")
print("- Aguarde provisionamento")
print("- Verifique email de credenciais")
```

---

## 📊 Métricas de Sucesso

### Backend Health Check

```bash
curl http://localhost:8000/health

# Esperado:
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "version": "1.0.0"
}
```

### Logs Importantes

Monitorar nos logs do backend:

```
✅ Email enviado para usuario@empresa.com
✅ Pagamento aprovado - processamento agendado
🚀 Provisionamento iniciado
✅ Tenant provisionado: empresa.logiflow.com.br
✅ Email de boas-vindas enviado
```

---

## 🚨 Troubleshooting Rápido

### Problema: Emails não estão enviando

```bash
# Verificar variáveis
echo $SMTP_USER
echo $SMTP_PASSWORD

# Testar
python scripts/test_email.py
```

### Problema: Webhook não recebe notificações

```bash
# Verificar logs
docker-compose logs -f backend | grep webhook

# Testar endpoint
curl -X POST http://localhost:8000/api/billing/webhooks/mercadopago \
  -H "Content-Type: application/json" \
  -d '{"type":"test"}'
```

### Problema: Provisionamento falha

```bash
# Verificar logs detalhados
docker-compose logs backend | grep provisionamento

# Verificar database
docker-compose exec db mysql -u root -p logiflow_crm
SELECT * FROM tenants ORDER BY created_at DESC LIMIT 5;
```

---

## 📝 Checklist Final Antes de Go-Live

### Infrastructure
- [ ] Servidor provisionado (DigitalOcean, AWS, etc)
- [ ] Domínio configurado (logiflow.com.br)
- [ ] SSL/HTTPS ativo (Let's Encrypt)
- [ ] Firewall configurado
- [ ] Backups automáticos ativos

### Backend
- [ ] Todas variáveis de produção configuradas
- [ ] Database em produção criado
- [ ] Redis em produção configurado
- [ ] Logs centralizados
- [ ] Monitoramento ativo (Sentry, etc)

### Integrações
- [ ] ✅ Mercado Pago em produção
- [ ] ✅ SMTP configurado (SendGrid/AWS SES)
- [ ] ⚠️ Focus NFe em produção (após credenciamento SEFAZ)
- [ ] ⚠️ Evolution API em produção
- [ ] ⚠️ Google Maps API em produção
- [ ] ⚠️ Slack/Discord configurado

### Frontend
- [ ] Build de produção gerado
- [ ] Assets otimizados
- [ ] CDN configurado (opcional)
- [ ] Analytics configurado (Google Analytics)

### Testes
- [ ] Teste end-to-end completo
- [ ] Teste com usuários beta
- [ ] Teste de carga (básico)
- [ ] Teste de segurança (OWASP básico)

### Documentação
- [ ] README atualizado
- [ ] Guias de configuração criados
- [ ] Runbook operacional criado
- [ ] FAQ de troubleshooting criado

### Legal/Compliance
- [ ] Termos de uso atualizados
- [ ] Política de privacidade atualizada
- [ ] LGPD compliance verificado
- [ ] Contratos de SLA preparados

---

## 🎉 Go Live!

Quando todos os itens acima estiverem ✅:

1. **Deploy em produção**
   ```bash
   git checkout main
   git pull origin main
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

2. **Smoke test em produção**
   ```bash
   curl https://api.logiflow.com.br/health
   ```

3. **Monitorar logs por 1 hora**

4. **Anunciar Go Live** 🚀

---

## 📞 Suporte

- **Documentação:** Este arquivo + docs individuais
- **Scripts de teste:** `backend/scripts/test_*.py`
- **Logs:** `docker-compose logs -f backend`
- **Email:** dev@logiflow.com.br

---

**Última atualização:** Janeiro 2026  
**Versão:** 1.0  
**Status:** ✅ Gaps Críticos Implementados | ⚠️ Gaps Importantes Documentados
