# 🔑 Credenciais Mercado Pago - LogiFlow CRM

**Data de obtenção:** 13/12/2024  
**Status:** ✅ Credenciais de TESTE obtidas

---

## 📊 Informações da Aplicação

| Campo | Valor |
|-------|-------|
| **User ID** | 175427787 |
| **Número da aplicação** | <MP_APP_ID> |
| **Integração** | Checkout Transparente |
| **API** | API Pagamentos |
| **Status** | Em teste (ETAPA 1 DE 6) |

---

## 🔐 Credenciais de TESTE

### **Access Token (Backend)**
```
TEST-9fe539d2-d988-4714-aab9-8810bd5743a3
```

### **Public Key (Frontend)**
```
TEST-c4f6c02a-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```
*Nota: Obter a Public Key completa no painel do Mercado Pago*

---

## ⚙️ Configuração no Backend

### **Arquivo: `.env`**
```env
# Mercado Pago - TESTE
MERCADOPAGO_ACCESS_TOKEN=TEST-9fe539d2-d988-4714-aab9-8810bd5743a3
MERCADOPAGO_PUBLIC_KEY=TEST-c4f6c02a-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# URLs de retorno
CHECKOUT_SUCCESS_URL=http://localhost:3001/checkout/success
CHECKOUT_FAILURE_URL=http://localhost:3001/checkout/failure
CHECKOUT_PENDING_URL=http://localhost:3001/checkout/pending
```

### **Testar Configuração**
```bash
cd backend
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token:', os.getenv('MERCADOPAGO_ACCESS_TOKEN'))"
```

---

## 🌐 Configuração no Frontend

### **Arquivo: `frontend/.env`**
```env
VITE_MERCADOPAGO_PUBLIC_KEY=TEST-c4f6c02a-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### **Uso no Vue**
```javascript
// src/services/mercadopago.js
const mp = new MercadoPago(import.meta.env.VITE_MERCADOPAGO_PUBLIC_KEY);
```

---

## 🧪 Testar Integração

### **1. Testar Criação de Checkout**
```bash
curl -X POST http://localhost:8000/api/billing/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "plan": "professional",
    "payment_method": "credit_card",
    "card_token": "test_token_123"
  }'
```

### **2. Testar Pagamento PIX**
```bash
curl -X POST http://localhost:8000/api/billing/checkout/pix \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "plan": "starter",
    "payment_method": "pix"
  }'
```

### **3. Listar Planos**
```bash
curl http://localhost:8000/api/billing/plans
```

---

## 💳 Cartões de Teste

Use estes cartões para testar pagamentos:

### **Cartão Aprovado**
```
Número: 5031 4332 1540 6351
CVV: 123
Validade: 11/25
Nome: APRO
```

### **Cartão Recusado**
```
Número: 5031 7557 3453 0604
CVV: 123
Validade: 11/25
Nome: OTHE
```

### **Cartão Pendente**
```
Número: 5031 4332 1540 6351
CVV: 123
Validade: 11/25
Nome: CALL
```

**Documentação completa:** https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-test/test-cards

---

## 🔔 Configurar Webhook (Teste)

### **URL do Webhook**
```
https://seu-ngrok-url.ngrok.io/api/billing/webhooks/mercadopago
```

### **Passos:**
1. Instalar ngrok: `npm install -g ngrok`
2. Iniciar túnel: `ngrok http 8000`
3. Copiar URL pública (ex: `https://abc123.ngrok.io`)
4. Acessar: https://www.mercadopago.com.br/developers/panel/app/<MP_APP_ID>/webhooks
5. Adicionar URL: `https://abc123.ngrok.io/api/billing/webhooks/mercadopago`
6. Selecionar eventos: `payment` e `subscription`

### **Testar Webhook Localmente**
```bash
# Simular webhook
curl -X POST http://localhost:8000/api/billing/webhooks/mercadopago \
  -H "Content-Type: application/json" \
  -d '{
    "action": "payment.updated",
    "data": {
      "id": "123456789"
    }
  }'
```

---

## 🚀 Migrar para Produção

### **Quando estiver pronto:**

1. **Completar homologação no Mercado Pago**
   - Acessar: https://www.mercadopago.com.br/developers/panel/app/<MP_APP_ID>
   - Completar todas as 6 etapas
   - Solicitar credenciais de produção

2. **Obter credenciais de produção**
   ```
   Access Token: APP_USR-<set-MERCADOPAGO_ACCESS_TOKEN-in-runtime-environment>...
   Public Key: APP_USR-xxxxxxxx-xxxxxx-...
   ```

3. **Atualizar `.env` de produção**
   ```env
   MERCADOPAGO_ACCESS_TOKEN=APP_USR-<set-MERCADOPAGO_ACCESS_TOKEN-in-runtime-environment>...
   MERCADOPAGO_PUBLIC_KEY=APP_USR-xxxxxxxx-xxxxxx-...
   CHECKOUT_SUCCESS_URL=https://app.logiflow.com.br/checkout/success
   CHECKOUT_FAILURE_URL=https://app.logiflow.com.br/checkout/failure
   ```

4. **Configurar webhook em produção**
   - URL: `https://api.logiflow.com.br/api/billing/webhooks/mercadopago`
   - Eventos: `payment` e `subscription`

---

## 📋 Checklist de Implementação

### **Backend**
- [x] Instalar SDK: `pip install mercadopago>=2.2.0`
- [x] Criar serviço: `services/mercadopago_service.py`
- [x] Criar router: `routers/billing.py`
- [x] Adicionar credenciais no `.env`
- [ ] Testar endpoints localmente
- [ ] Configurar webhook com ngrok
- [ ] Testar fluxo completo de pagamento

### **Frontend**
- [ ] Adicionar SDK do MP no HTML
- [ ] Criar página de checkout: `views/CheckoutView.vue`
- [ ] Implementar formulário de cartão
- [ ] Implementar exibição de QR Code PIX
- [ ] Testar integração com backend
- [ ] Implementar página de sucesso/falha

### **Testes**
- [ ] Testar pagamento com cartão aprovado
- [ ] Testar pagamento com cartão recusado
- [ ] Testar pagamento PIX
- [ ] Testar webhook de pagamento aprovado
- [ ] Testar webhook de assinatura criada
- [ ] Testar cancelamento de assinatura

---

## 🔗 Links Úteis

- **Painel de Aplicações:** https://www.mercadopago.com.br/developers/panel/app/<MP_APP_ID>
- **Documentação API:** https://www.mercadopago.com.br/developers/pt/docs
- **Webhooks:** https://www.mercadopago.com.br/developers/panel/app/<MP_APP_ID>/webhooks
- **Cartões de Teste:** https://www.mercadopago.com.br/developers/pt/docs/checkout-api/integration-test/test-cards
- **SDK Python:** https://github.com/mercadopago/sdk-python

---

## ⚠️ Segurança

### **Boas Práticas:**
1. ✅ **Nunca** commitar credenciais no Git
2. ✅ Usar `.env` para armazenar tokens
3. ✅ Adicionar `.env` no `.gitignore`
4. ✅ Usar credenciais de TESTE em desenvolvimento
5. ✅ Usar credenciais de PRODUÇÃO apenas em produção
6. ✅ Validar webhooks com assinatura do MP
7. ✅ Usar HTTPS em produção

### **Arquivo `.gitignore`**
```gitignore
# Credenciais
.env
.env.local
.env.production

# Mercado Pago
mercadopago_credentials.txt
```

---

## 📞 Suporte

**Dúvidas sobre integração?**
- Documentação: https://www.mercadopago.com.br/developers/pt/support
- Fórum: https://www.mercadopago.com.br/developers/pt/support/forum
- Email: developers@mercadopago.com

---

**Documento criado:** 13/12/2024  
**Última atualização:** 13/12/2024  
**Status:** ✅ Credenciais de teste configuradas
