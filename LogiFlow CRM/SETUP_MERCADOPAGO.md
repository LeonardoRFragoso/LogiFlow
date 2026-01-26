# 🔧 Configuração do Mercado Pago - LogiFlow CRM

## 📋 Pré-requisitos

1. Conta no Mercado Pago (Brasil)
2. Acesso ao painel de desenvolvedores
3. Aplicação criada

---

## 🚀 Passo a Passo

### 1. Criar Aplicação no Mercado Pago

1. Acesse: https://www.mercadopago.com.br/developers/panel/app
2. Clique em **"Criar aplicação"**
3. Preencha:
   - **Nome:** LogiFlow CRM
   - **Descrição:** Sistema de CRM para transportadoras
   - **URL de retorno:** `https://app.logiflow.com.br/checkout/success`
4. Clique em **"Criar aplicação"**

### 2. Obter Credenciais

#### Para TESTES (Sandbox):

1. No painel da aplicação, vá em **"Credenciais"**
2. Selecione **"Credenciais de teste"**
3. Copie:
   - **Access Token:** `TEST-1234567890123456-010101-abcdef1234567890abcdef1234567890-123456789`
   - **Public Key:** `TEST-abcdef12-3456-7890-abcd-ef1234567890`

#### Para PRODUÇÃO:

1. No painel da aplicação, vá em **"Credenciais"**
2. Selecione **"Credenciais de produção"**
3. Copie:
   - **Access Token:** `APP-1234567890123456-010101-abcdef1234567890abcdef1234567890-123456789`
   - **Public Key:** `APP-abcdef12-3456-7890-abcd-ef1234567890`

⚠️ **IMPORTANTE:** Nunca commit as credenciais no Git!

### 3. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

```bash
# Mercado Pago - SANDBOX (TESTES)
MERCADOPAGO_ACCESS_TOKEN=TEST-1234567890123456-010101-abcdef1234567890abcdef1234567890-123456789
MERCADOPAGO_PUBLIC_KEY=TEST-abcdef12-3456-7890-abcd-ef1234567890
MERCADOPAGO_WEBHOOK_URL=https://api.logiflow.com.br/api/billing/webhooks/mercadopago

# URLs de retorno
CHECKOUT_SUCCESS_URL=https://app.logiflow.com.br/checkout/success
CHECKOUT_FAILURE_URL=https://app.logiflow.com.br/checkout/failure
CHECKOUT_PENDING_URL=https://app.logiflow.com.br/checkout/pending
```

**Para produção**, substitua `TEST-` por `APP-` nas credenciais.

### 4. Configurar Webhook no Mercado Pago

O webhook é essencial para receber notificações de pagamento.

#### 4.1. URL do Webhook

Sua URL pública de webhook deve ser:
```
https://api.logiflow.com.br/api/billing/webhooks/mercadopago
```

⚠️ **Requisitos do webhook:**
- Deve ser HTTPS (SSL válido)
- Deve ser acessível publicamente
- Deve responder rapidamente (< 5 segundos)

#### 4.2. Registrar Webhook no Painel

1. Acesse: https://www.mercadopago.com.br/developers/panel/app
2. Selecione sua aplicação **LogiFlow CRM**
3. Vá em **"Webhooks"** → **"Notificações IPN"**
4. Clique em **"Configurar notificações"**
5. Preencha:
   - **URL de notificação:** `https://api.logiflow.com.br/api/billing/webhooks/mercadopago`
   - **Eventos:**
     - ✅ `payment` (Pagamentos)
     - ✅ `subscription_preapproval` (Assinaturas)
6. Clique em **"Salvar"**

#### 4.3. Testar Webhook (Opcional)

O Mercado Pago envia uma notificação de teste ao salvar. Verifique os logs:

```bash
docker-compose logs -f backend | grep "Webhook"
```

Você deve ver:
```
📩 Webhook recebido do Mercado Pago: payment
✅ Webhook processado
```

### 5. Testar em Ambiente de Desenvolvimento

#### 5.1. Usando ngrok (para testes locais)

Se está testando localmente, use ngrok para expor sua API:

```bash
ngrok http 8000
```

Copie a URL gerada (ex: `https://abc123.ngrok.io`) e configure:

```bash
MERCADOPAGO_WEBHOOK_URL=https://abc123.ngrok.io/api/billing/webhooks/mercadopago
```

Depois, registre essa URL no painel do Mercado Pago.

#### 5.2. Testar Checkout

1. Inicie o backend:
```bash
cd backend
docker-compose up
```

2. Faça uma requisição de teste:
```bash
curl -X POST http://localhost:8000/api/billing/checkout/pix \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "plan": "professional",
    "payment_method": "pix"
  }'
```

3. Você receberá:
```json
{
  "success": true,
  "payment_id": "123456789",
  "qr_code": "00020126580014br.gov.bcb.pix...",
  "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "amount": 599.00
}
```

#### 5.3. Simular Pagamento Aprovado (Sandbox)

Para testar o fluxo completo no sandbox:

1. Use os **cartões de teste** do Mercado Pago:
   - **Aprovado:** `5031 4332 1540 6351`
   - **Rejeitado:** `5031 7557 3453 0604`

2. Dados do titular:
   - **Nome:** APRO (para aprovar) ou OTHE (para rejeitar)
   - **CPF:** 12345678909
   - **Validade:** 11/25
   - **CVV:** 123

3. O webhook será chamado automaticamente pelo MP

---

## ✅ Checklist de Validação

- [ ] Credenciais configuradas no `.env`
- [ ] Aplicação criada no painel do MP
- [ ] Webhook registrado e testado
- [ ] URL pública acessível (HTTPS)
- [ ] Logs do backend mostrando webhooks
- [ ] Teste de checkout PIX funcionando
- [ ] Teste de pagamento com cartão funcionando
- [ ] Provisionamento automático após pagamento
- [ ] Email de confirmação enviado
- [ ] Email de boas-vindas com credenciais enviado

---

## 🔍 Troubleshooting

### Webhook não está sendo chamado

1. **Verifique se a URL é HTTPS:**
   ```bash
   curl -I https://api.logiflow.com.br/api/billing/webhooks/mercadopago
   ```

2. **Verifique os logs do Mercado Pago:**
   - Acesse: https://www.mercadopago.com.br/developers/panel/app
   - Vá em "Webhooks" → "Histórico de notificações"

3. **Teste manualmente:**
   ```bash
   curl -X POST https://api.logiflow.com.br/api/billing/webhooks/mercadopago \
     -H "Content-Type: application/json" \
     -d '{
       "action": "payment.updated",
       "data": {"id": "123456789"}
     }'
   ```

### Pagamento não gera provisionamento

1. **Verifique se o `external_reference` está correto:**
   - Deve ser: `lead_{lead_id}`

2. **Verifique logs do backend:**
   ```bash
   docker-compose logs -f backend | grep "💳"
   ```

3. **Verifique se o lead existe:**
   ```sql
   SELECT * FROM leads WHERE id = 1;
   ```

### Erro "Mercado Pago não configurado"

Verifique se a variável `MERCADOPAGO_ACCESS_TOKEN` está definida:

```bash
docker-compose exec backend env | grep MERCADOPAGO
```

Se não aparecer, reinicie os containers:

```bash
docker-compose down
docker-compose up -d
```

---

## 📚 Documentação Oficial

- **Mercado Pago Developers:** https://www.mercadopago.com.br/developers
- **API Reference:** https://www.mercadopago.com.br/developers/pt/reference
- **Webhooks:** https://www.mercadopago.com.br/developers/pt/docs/your-integrations/notifications/webhooks
- **Cartões de Teste:** https://www.mercadopago.com.br/developers/pt/docs/testing/test-cards

---

## 🎯 Próximos Passos

Após configurar o Mercado Pago:

1. ✅ Configurar sistema de emails (SMTP)
2. ✅ Testar fluxo completo de conversão
3. ✅ Configurar outras integrações (Focus NFe, WhatsApp)
4. ✅ Deploy em produção

---

**Última atualização:** 23 de Janeiro de 2026
