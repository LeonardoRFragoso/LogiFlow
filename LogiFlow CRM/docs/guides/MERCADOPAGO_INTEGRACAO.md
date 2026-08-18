# 💳 Integração Mercado Pago - LogiFlow CRM

## 📊 Credenciais da Aplicação

**Dados da sua aplicação no Mercado Pago:**
- **User ID**: 175427787
- **Número da aplicação**: <MP_APP_ID>
- **Integração**: Checkout Transparente
- **API**: API Pagamentos
- **Status**: Em teste (ETAPA 1 DE 6)

---

## ✅ O QUE FOI IMPLEMENTADO

### **1. Serviço de Integração**
`@C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM\LogiFlow CRM\backend\services\mercadopago_service.py`

**Funcionalidades:**
- ✅ Criar clientes (customers)
- ✅ Criar planos de assinatura
- ✅ Criar assinaturas recorrentes
- ✅ Processar pagamentos únicos
- ✅ Gerar pagamentos PIX com QR Code
- ✅ Processar webhooks
- ✅ Cancelar assinaturas
- ✅ Consultar status de pagamentos

### **2. Router de Billing**
`@C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM\LogiFlow CRM\backend\routers\billing.py`

**Endpoints:**
- ✅ `POST /api/billing/checkout` - Criar checkout com cartão
- ✅ `POST /api/billing/checkout/pix` - Criar pagamento PIX
- ✅ `GET /api/billing/subscriptions/{tenant_id}` - Obter assinatura
- ✅ `POST /api/billing/subscriptions/{id}/cancel` - Cancelar assinatura
- ✅ `POST /api/billing/subscriptions/{id}/upgrade` - Upgrade de plano
- ✅ `POST /api/billing/webhooks/mercadopago` - Webhook do MP
- ✅ `GET /api/billing/plans` - Listar planos disponíveis
- ✅ `GET /api/billing/plans/{name}` - Detalhes de um plano

### **3. Planos Configurados**

#### **Starter - R$ 299/mês**
- Até 5 usuários
- Gestão de clientes
- Cotações e pedidos
- Rastreamento básico
- App do motorista
- Portal do cliente
- Suporte por email

#### **Professional - R$ 599/mês**
- Até 15 usuários
- Tudo do Starter +
- Emissão de CT-e/MDF-e
- Integrações avançadas
- WhatsApp integrado
- Relatórios customizados
- Suporte prioritário

#### **Enterprise - R$ 1.499/mês**
- Usuários ilimitados
- Tudo do Professional +
- Integrações ERP/TMS
- Onboarding dedicado
- Suporte 24/7
- SLA garantido

---

## 🔧 Configuração

### **1. Variáveis de Ambiente**

Adicione ao `.env`:
```env
# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=APP_USR-<set-MERCADOPAGO_ACCESS_TOKEN-in-runtime-environment>
MERCADOPAGO_PUBLIC_KEY=APP_USR-xxxxxxxx-xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# URLs de retorno
CHECKOUT_SUCCESS_URL=https://app.logiflow.com.br/checkout/success
CHECKOUT_FAILURE_URL=https://app.logiflow.com.br/checkout/failure
```

### **2. Instalar Dependências**

```bash
cd backend
pip install mercadopago>=2.2.0
```

### **3. Configurar Webhook no Mercado Pago**

1. Acesse: https://www.mercadopago.com.br/developers/panel/app/<MP_APP_ID>/webhooks
2. Adicione a URL: `https://api.logiflow.com.br/api/billing/webhooks/mercadopago`
3. Selecione eventos:
   - ✅ `payment` (Pagamentos)
   - ✅ `subscription` (Assinaturas)

---

## 🚀 Como Usar

### **Fluxo 1: Checkout com Cartão de Crédito**

```javascript
// 1. Frontend: Coletar dados do cartão e gerar token
const mp = new MercadoPago('PUBLIC_KEY');
const cardToken = await mp.createCardToken({
  cardNumber: '4111111111111111',
  cardholderName: 'João Silva',
  cardExpirationMonth: '12',
  cardExpirationYear: '2025',
  securityCode: '123',
  identificationType: 'CPF',
  identificationNumber: '12345678900'
});

// 2. Enviar para backend
const response = await fetch('/api/billing/checkout', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    lead_id: 123,
    plan: 'professional',
    payment_method: 'credit_card',
    card_token: cardToken.id
  })
});

const data = await response.json();
// Redirecionar para: data.init_point
```

### **Fluxo 2: Pagamento PIX**

```javascript
// 1. Solicitar pagamento PIX
const response = await fetch('/api/billing/checkout/pix', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    lead_id: 123,
    plan: 'starter',
    payment_method: 'pix'
  })
});

const data = await response.json();

// 2. Exibir QR Code para o usuário
console.log('QR Code:', data.qr_code);
console.log('QR Code Base64:', data.qr_code_base64);
console.log('Link do PIX:', data.ticket_url);

// 3. Aguardar webhook de confirmação
```

### **Fluxo 3: Webhook (Automático)**

Quando um pagamento é aprovado, o Mercado Pago envia:

```json
{
  "action": "payment.updated",
  "data": {
    "id": "123456789"
  }
}
```

O backend processa automaticamente e:
1. Atualiza status do pagamento
2. Provisiona tenant (se primeiro pagamento)
3. Ativa assinatura
4. Envia email de boas-vindas

---

## 🧪 Testes

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

### **4. Simular Webhook**

```bash
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

## 📱 Integração no Frontend

### **Página de Checkout (Vue)**

```vue
<template>
  <div class="checkout">
    <h1>Finalizar Assinatura</h1>
    
    <!-- Seleção de Plano -->
    <div class="plans">
      <div v-for="plan in plans" :key="plan.name" 
           @click="selectedPlan = plan"
           :class="{ active: selectedPlan === plan }">
        <h3>{{ plan.name }}</h3>
        <p class="price">R$ {{ plan.amount }}/mês</p>
        <ul>
          <li v-for="feature in plan.features" :key="feature">
            {{ feature }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Método de Pagamento -->
    <div class="payment-methods">
      <button @click="paymentMethod = 'credit_card'" 
              :class="{ active: paymentMethod === 'credit_card' }">
        💳 Cartão de Crédito
      </button>
      <button @click="paymentMethod = 'pix'" 
              :class="{ active: paymentMethod === 'pix' }">
        📱 PIX
      </button>
    </div>

    <!-- Formulário de Cartão -->
    <div v-if="paymentMethod === 'credit_card'" class="card-form">
      <input v-model="cardNumber" placeholder="Número do cartão" />
      <input v-model="cardName" placeholder="Nome no cartão" />
      <div class="row">
        <input v-model="cardExpiry" placeholder="MM/AA" />
        <input v-model="cardCvv" placeholder="CVV" />
      </div>
    </div>

    <!-- Botão de Pagamento -->
    <button @click="processPayment" :disabled="loading">
      {{ loading ? 'Processando...' : 'Finalizar Pagamento' }}
    </button>

    <!-- QR Code PIX -->
    <div v-if="pixQrCode" class="pix-qrcode">
      <img :src="`data:image/png;base64,${pixQrCode}`" />
      <p>Escaneie o QR Code para pagar</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const plans = ref([])
const selectedPlan = ref(null)
const paymentMethod = ref('credit_card')
const loading = ref(false)
const pixQrCode = ref(null)

const cardNumber = ref('')
const cardName = ref('')
const cardExpiry = ref('')
const cardCvv = ref('')

onMounted(async () => {
  const response = await axios.get('/api/billing/plans')
  plans.value = Object.values(response.data.plans)
  selectedPlan.value = plans.value[0]
})

const processPayment = async () => {
  loading.value = true
  
  try {
    if (paymentMethod.value === 'pix') {
      // Pagamento PIX
      const response = await axios.post('/api/billing/checkout/pix', {
        lead_id: leadId.value,
        plan: selectedPlan.value.name.toLowerCase().split(' ')[1],
        payment_method: 'pix'
      })
      
      pixQrCode.value = response.data.qr_code_base64
      
    } else {
      // Cartão de Crédito
      // 1. Gerar token do cartão
      const mp = new MercadoPago(import.meta.env.VITE_MP_PUBLIC_KEY)
      const cardToken = await mp.createCardToken({
        cardNumber: cardNumber.value,
        cardholderName: cardName.value,
        // ... outros campos
      })
      
      // 2. Enviar para backend
      const response = await axios.post('/api/billing/checkout', {
        lead_id: leadId.value,
        plan: selectedPlan.value.name.toLowerCase().split(' ')[1],
        payment_method: 'credit_card',
        card_token: cardToken.id
      })
      
      // 3. Redirecionar
      window.location.href = response.data.init_point
    }
  } catch (error) {
    alert('Erro ao processar pagamento')
  } finally {
    loading.value = false
  }
}
</script>
```

---

## 🔒 Segurança

### **Boas Práticas:**
1. ✅ **Nunca** armazene dados de cartão no backend
2. ✅ Use tokens do Mercado Pago para processar pagamentos
3. ✅ Valide webhooks com assinatura
4. ✅ Use HTTPS em produção
5. ✅ Armazene access_token em variável de ambiente
6. ✅ Implemente rate limiting nos endpoints

---

## 📊 Monitoramento

### **Métricas a Acompanhar:**
- Taxa de conversão checkout → pagamento
- Taxa de aprovação de pagamentos
- Churn rate mensal
- MRR (Monthly Recurring Revenue)
- LTV (Lifetime Value)

### **Dashboard Sugerido:**
```
┌─────────────────────────────────────────────────┐
│ BILLING DASHBOARD                               │
├─────────────────────────────────────────────────┤
│ MRR: R$ 45.000                                  │
│ Assinaturas Ativas: 85                          │
│ Trial: 12                                       │
│ Churn (mês): 2.3%                               │
├─────────────────────────────────────────────────┤
│ Pagamentos Pendentes: 3                         │
│ Inadimplentes: 1                                │
└─────────────────────────────────────────────────┘
```

---

## 🚨 Próximos Passos

1. **Obter Access Token de Produção**
   - Completar etapas de homologação no MP
   - Ativar aplicação em produção

2. **Configurar Webhook em Produção**
   - URL: `https://api.logiflow.com.br/api/billing/webhooks/mercadopago`

3. **Implementar Provisionamento Automático**
   - Criar tenant após primeiro pagamento
   - Enviar email de boas-vindas
   - Configurar trial de 14 dias

4. **Criar Página de Checkout no Frontend**
   - Integrar SDK do Mercado Pago
   - Formulário de cartão
   - Exibição de QR Code PIX

5. **Implementar Gestão de Inadimplência**
   - Suspender tenant após 7 dias
   - Cancelar após 30 dias
   - Emails de cobrança

---

**Documento criado:** 13/12/2024  
**Status:** Integração implementada, aguardando testes  
**Próxima etapa:** Obter credenciais de produção
