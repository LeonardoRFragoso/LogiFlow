# Configuração do Mercado Pago - LogiFlow CRM

## 💳 Visão Geral

O LogiFlow CRM usa o Mercado Pago para processar pagamentos recorrentes (assinaturas) e aceita:
- 💳 Cartão de Crédito (recorrente)
- 🔷 PIX (pagamento único mensal)
- 🧾 Boleto (disponível via configuração)

---

## 🚀 Configuração Passo a Passo

### ETAPA 1: Criar Conta no Mercado Pago

#### 1.1 Criar Conta de Desenvolvedor

1. Acesse: https://www.mercadopago.com.br/developers
2. Clique em **"Criar conta"** ou faça login
3. Complete o cadastro da empresa
4. Verifique seu email e CPF/CNPJ

#### 1.2 Criar Aplicação

1. No painel de desenvolvedor, vá em **"Suas integrações"**
2. Clique em **"Criar aplicação"**
3. Preencha:
   - **Nome:** LogiFlow CRM
   - **Descrição:** Sistema de gestão para transportadoras
   - **Categoria:** Serviços
   - **Modelo de integração:** Checkout Pro + Assinaturas
4. Salve a aplicação

---

### ETAPA 2: Obter Credenciais

#### 2.1 Credenciais de TESTE (Desenvolvimento)

1. No painel da aplicação, vá em **"Credenciais"**
2. Selecione **"Credenciais de teste"**
3. Copie:
   - **Access Token de teste:** `TEST-XXXXXXX...`
   - **Public Key de teste:** `TEST-XXXXXXX...`

#### 2.2 Credenciais de PRODUÇÃO

⚠️ **Só ative em produção após testes completos!**

1. Complete os dados da empresa no Mercado Pago
2. Aguarde aprovação (pode levar 1-2 dias)
3. No painel, vá em **"Credenciais"**
4. Selecione **"Credenciais de produção"**
5. Copie:
   - **Access Token:** `APP_USR-XXXXXXX...`
   - **Public Key:** `APP_USR-XXXXXXX...`

---

### ETAPA 3: Configurar no LogiFlow

#### 3.1 Adicionar Credenciais no `.env`

```bash
# backend/.env

# ========================================
# Mercado Pago - TESTE (Desenvolvimento)
# ========================================
MERCADOPAGO_ACCESS_TOKEN=TEST-9fe539d2-d988-4714-aab9-8810bd5743a3
MERCADOPAGO_PUBLIC_KEY=TEST-c4f6c02a-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# URLs de retorno após pagamento
CHECKOUT_SUCCESS_URL=http://localhost:3001/checkout/success
CHECKOUT_FAILURE_URL=http://localhost:3001/checkout/failure
CHECKOUT_PENDING_URL=http://localhost:3001/checkout/pending

# Webhook URL (configurar no painel do MP - próxima etapa)
# https://api.logiflow.com.br/api/billing/webhooks/mercadopago
```

#### 3.2 Para Produção

Quando estiver pronto para produção, substitua por:

```bash
# ========================================
# Mercado Pago - PRODUÇÃO
# ========================================
MERCADOPAGO_ACCESS_TOKEN=APP_USR-<set-MERCADOPAGO_ACCESS_TOKEN-in-runtime-environment>
MERCADOPAGO_PUBLIC_KEY=APP_USR-xxxxxxxx-xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# URLs de produção
CHECKOUT_SUCCESS_URL=https://app.logiflow.com.br/checkout/success
CHECKOUT_FAILURE_URL=https://app.logiflow.com.br/checkout/failure
CHECKOUT_PENDING_URL=https://app.logiflow.com.br/checkout/pending
```

---

### ETAPA 4: Configurar Webhook

O webhook é crucial para receber notificações de pagamento aprovado e provisionar o tenant automaticamente.

#### 4.1 No Painel do Mercado Pago

1. Vá em **"Suas integrações" → Sua aplicação**
2. Clique em **"Webhooks"**
3. Clique em **"Configurar webhooks"**
4. Preencha:
   - **URL:** `https://api.logiflow.com.br/api/billing/webhooks/mercadopago`
   - **Eventos:** Selecione:
     - `payment.created`
     - `payment.updated`
     - `subscription.created`
     - `subscription.updated`
     - `subscription.cancelled`
5. Salve

#### 4.2 Para Desenvolvimento Local (ngrok)

Para testar webhooks localmente:

```bash
# Instalar ngrok
npm install -g ngrok

# Expor porta 8000
ngrok http 8000
```

Copie a URL gerada (ex: `https://abc123.ngrok.io`) e configure no Mercado Pago:
```
https://abc123.ngrok.io/api/billing/webhooks/mercadopago
```

---

## ✅ Testar Integração

### Teste 1: Verificar Credenciais

```bash
cd backend
python scripts/test_mercadopago.py
```

### Teste 2: Criar Checkout de Teste

1. Acesse o site: http://localhost:5173
2. Clique em **"Assinar Agora"** em qualquer plano
3. Preencha os dados
4. Use cartões de teste do Mercado Pago:

#### Cartões de Teste

| Cartão | Número | CVV | Validade | Resultado |
|--------|--------|-----|----------|-----------|
| Mastercard | 5031 4332 1540 6351 | 123 | 11/25 | ✅ Aprovado |
| Visa | 4235 6477 2802 5682 | 123 | 11/25 | ✅ Aprovado |
| Mastercard | 5031 7557 3453 0604 | 123 | 11/25 | ❌ Recusado |

**Titular:** APRO (aprovado) ou OTHE (recusado)  
**CPF:** 12345678909

### Teste 3: Verificar Webhook

Após pagamento de teste:

1. Verifique logs do backend:
   ```bash
   docker compose -f docker/docker-compose.yml logs -f backend
   ```

2. Deve aparecer:
   ```
   📩 Webhook recebido do Mercado Pago
   ✅ Pagamento aprovado: payment_id_123
   🚀 Iniciando provisionamento de tenant...
   ```

---

## 🔍 Fluxo Completo de Pagamento

```
1. Usuário escolhe plano no site
   ↓
2. Frontend chama POST /api/billing/checkout
   ↓
3. Backend cria preferência no Mercado Pago
   ↓
4. Usuário redirecionado para página de pagamento do MP
   ↓
5. Usuário paga com cartão/PIX
   ↓
6. Mercado Pago processa pagamento
   ↓
7. MP envia webhook para nosso backend
   ↓
8. Backend recebe notificação de payment.approved
   ↓
9. Backend provisiona tenant automaticamente
   ↓
10. Backend envia email com credenciais
   ↓
11. Cliente acessa sistema e começa a usar!
```

---

## 🛠️ Troubleshooting

### Problema: "Invalid access token"

**Causa:** Credenciais incorretas ou expiradas

**Solução:**
- Verifique se copiou o token completo (começa com `TEST-` ou `APP_USR-`)
- Confirme que não há espaços extras
- Regenere as credenciais no painel do MP

---

### Problema: Webhook não recebe notificações

**Causa:** URL do webhook incorreta ou inacessível

**Solução:**
1. Verifique se a URL está correta no painel do MP
2. Teste se a URL está acessível:
   ```bash
   curl -X POST https://api.logiflow.com.br/api/billing/webhooks/mercadopago \
     -H "Content-Type: application/json" \
     -d '{"type":"test"}'
   ```
3. Para local, use ngrok
4. Verifique firewall do servidor

---

### Problema: "Payment preference creation failed"

**Causa:** Dados incompletos ou inválidos

**Solução:**
- Verifique logs do backend para erro detalhado
- Confirme que todos os dados obrigatórios estão preenchidos
- Verifique formato do email (deve ser válido)

---

### Problema: Pagamento aprovado mas tenant não criado

**Causa:** Webhook recebido mas provisionamento falhou

**Solução:**
1. Verifique logs do backend:
   ```bash
   docker compose -f docker/docker-compose.yml logs backend | grep "provisionamento"
   ```
2. Verifique se database está acessível
3. Verifique se há erro na criação do tenant
4. Sistema de retry tentará novamente automaticamente

---

## 📊 Monitoramento

### Logs Importantes

```python
# Checkout criado
📦 Checkout criado para plano starter - Lead ID: 123

# Pagamento aprovado
✅ Pagamento aprovado: MP_1234567890

# Provisionamento iniciado
🚀 Provisionamento iniciado para payment_id: 1234

# Tenant criado
✅ Tenant provisionado: exemplo.logiflow.com.br

# Email enviado
📧 Credenciais enviadas para: cliente@empresa.com
```

### Métricas para Monitorar

- Taxa de conversão (checkout → pagamento)
- Taxa de aprovação de pagamentos
- Tempo médio de provisionamento
- Taxa de falha no webhook
- Chargebacks e contestações

---

## 💰 Custos do Mercado Pago

### Taxas (Brasil - 2025)

| Método | Taxa por Transação |
|--------|-------------------|
| Cartão de Crédito | 4,99% + R$ 0,40 |
| Cartão de Débito | 3,79% + R$ 0,40 |
| PIX | 0,99% |
| Boleto | R$ 3,49 |

### Assinaturas (Recorrência)

- **Sem taxa adicional** além da transação
- Cobranças automáticas mensais
- Gestão de inadimplência inclusa

### Exemplo de Cálculo

Para plano Professional (R$ 599/mês) com cartão:
- Valor cobrado do cliente: R$ 599,00
- Taxa MP (4,99%): R$ 29,89
- Taxa fixa: R$ 0,40
- **Você recebe:** R$ 568,71
- **Margem líquida:** 95%

---

## 🔐 Segurança

### Boas Práticas

1. **Nunca exponha credenciais**
   - Use variáveis de ambiente
   - Não commite credenciais no git
   - Use secrets manager em produção

2. **Valide webhooks**
   - Implemente validação de assinatura
   - Verifique origem do request
   - Use HTTPS sempre

3. **Proteja dados de pagamento**
   - Nunca armazene dados de cartão
   - Use tokens do MP para pagamentos
   - Criptografe dados sensíveis

4. **Monitore fraudes**
   - Implemente rate limiting
   - Monitore padrões suspeitos
   - Use ferramentas anti-fraude do MP

---

## 📝 Checklist de Implementação

### Desenvolvimento
- [ ] Criar conta Mercado Pago
- [ ] Criar aplicação
- [ ] Obter credenciais de teste
- [ ] Configurar no `.env`
- [ ] Testar criação de checkout
- [ ] Testar pagamento com cartão de teste
- [ ] Configurar webhook (ngrok)
- [ ] Validar recebimento de webhook
- [ ] Testar provisionamento automático
- [ ] Verificar email de credenciais

### Homologação
- [ ] Obter credenciais de produção
- [ ] Configurar URLs de produção
- [ ] Configurar webhook em domínio real
- [ ] Testar com valores reais (R$ 0,01)
- [ ] Validar fluxo completo
- [ ] Testar cenários de erro
- [ ] Validar cancelamento de assinatura
- [ ] Documentar processo

### Produção
- [ ] Ativar monitoramento
- [ ] Configurar alertas
- [ ] Implementar retry de webhooks
- [ ] Documentar runbook
- [ ] Treinar equipe de suporte
- [ ] Preparar FAQ para clientes

---

## 🆘 Suporte

### Documentação Oficial
- **API Mercado Pago:** https://www.mercadopago.com.br/developers/pt/docs
- **Assinaturas:** https://www.mercadopago.com.br/developers/pt/docs/subscriptions
- **Webhooks:** https://www.mercadopago.com.br/developers/pt/docs/webhooks

### Suporte Mercado Pago
- **Chat:** Painel do desenvolvedor
- **Email:** developers@mercadopago.com
- **Forum:** https://www.mercadopago.com.br/developers/pt/support

---

## 🎯 Próximos Passos

Após configurar o Mercado Pago:

1. ✅ Integrar webhook ao provisionamento (GAP #3)
2. Implementar gestão de assinaturas
3. Implementar upgrades/downgrades de plano
4. Implementar controle de inadimplência
5. Criar dashboard financeiro

---

**Última atualização:** Janeiro 2026  
**Versão:** 1.0
