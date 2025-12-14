# 🧪 Guia de Teste End-to-End - LogiFlow CRM

## 📋 Objetivo

Testar o fluxo completo desde a visita ao site até o provisionamento do tenant e uso do sistema.

---

## 🔄 Fluxo Completo

```
1. Visitante acessa site
2. Clica em "Assinar Agora"
3. Preenche dados no checkout
4. Realiza pagamento
5. Webhook processa pagamento
6. Tenant é provisionado
7. Email de boas-vindas enviado
8. Cliente acessa sistema
9. Testa limites do plano
```

---

## ✅ Checklist de Testes

### 1️⃣ Teste do Site de Divulgação

**URL**: `http://localhost:5174` (dev) ou `https://logiflow.com.br` (prod)

#### Verificações:

- [ ] **Página carrega corretamente**
  - Layout responsivo
  - Imagens carregam
  - Animações funcionam

- [ ] **Seção de Preços**
  - Planos exibidos: Starter (R$ 299), Professional (R$ 599), Enterprise (R$ 1.499)
  - Botão "🚀 Assinar Agora" visível em cada plano
  - Botão "📞 Solicitar Demonstração" visível

- [ ] **Clique em "Assinar Agora"**
  - Abre nova aba
  - URL correta: `http://localhost:3001/checkout?plan=starter`
  - Plano pré-selecionado no checkout

#### Comandos de Teste:

```bash
# Verificar se site está rodando
curl -I http://localhost:5174

# Verificar links dos botões
curl http://localhost:5174 | grep "checkout?plan="
```

---

### 2️⃣ Teste do Checkout

**URL**: `http://localhost:3001/checkout?plan=starter`

#### Verificações:

- [ ] **Página de Checkout carrega**
  - Plano correto pré-selecionado
  - Preço exibido corretamente
  - Formulário de dados visível

- [ ] **Seleção de Plano**
  - Pode trocar entre planos
  - Preço atualiza ao trocar
  - Features do plano exibidas

- [ ] **Formulário de Dados**
  ```
  Campos obrigatórios:
  - Nome da empresa
  - Nome do responsável
  - Email
  - Telefone
  - CPF/CNPJ
  ```

- [ ] **Método de Pagamento**
  - Cartão de crédito
  - PIX
  - Boleto

#### Dados de Teste:

```json
{
  "company_name": "Transportadora Teste Ltda",
  "contact_name": "João Silva",
  "contact_email": "teste@example.com",
  "contact_phone": "(11) 99999-9999",
  "cpf_cnpj": "12345678000190"
}
```

#### Cartões de Teste (Mercado Pago):

```
Aprovado:
  Número: 5031 4332 1540 6351
  CVV: 123
  Validade: 11/25
  Nome: APRO

Recusado:
  Número: 5031 4332 1540 6351
  CVV: 123
  Validade: 11/25
  Nome: OTHE
```

---

### 3️⃣ Teste de Pagamento

#### Verificações:

- [ ] **Processamento do Pagamento**
  - Loading exibido durante processamento
  - Sem erros no console
  - Redirecionamento correto

- [ ] **Cartão Aprovado**
  - Redireciona para: `/checkout/success`
  - Mensagem de sucesso exibida
  - Detalhes da assinatura mostrados

- [ ] **Cartão Recusado**
  - Redireciona para: `/checkout/failure`
  - Mensagem de erro clara
  - Opções de tentar novamente

- [ ] **PIX Pendente**
  - Redireciona para: `/checkout/pending`
  - QR Code exibido
  - Instruções de pagamento

#### Logs para Verificar:

```bash
# Backend - Ver processamento
tail -f backend/logs/api_*.log | grep "payment"

# Verificar webhook recebido
tail -f backend/logs/api_*.log | grep "webhook"
```

---

### 4️⃣ Teste do Webhook

**Endpoint**: `POST /api/billing/webhooks/mercadopago`

#### Verificações:

- [ ] **Webhook Recebido**
  ```bash
  # Ver logs
  tail -f backend/logs/api_*.log | grep "Webhook recebido"
  ```

- [ ] **Validação de Assinatura**
  - Webhook autenticado
  - Dados validados

- [ ] **Processamento**
  - Payment ID identificado
  - Status verificado
  - Ação apropriada tomada

#### Teste Manual do Webhook:

```bash
curl -X POST http://localhost:8000/api/billing/webhooks/mercadopago \
  -H "Content-Type: application/json" \
  -d '{
    "action": "payment.created",
    "data": {
      "id": "1234567890"
    },
    "type": "payment"
  }'
```

---

### 5️⃣ Teste de Provisionamento

#### Verificações:

- [ ] **Tenant Criado**
  ```sql
  -- Verificar no banco
  SELECT * FROM tenants ORDER BY created_at DESC LIMIT 1;
  ```

- [ ] **Dados do Tenant**
  - company_name preenchido
  - subdomain gerado
  - plan correto
  - max_users, max_vehicles, max_orders_per_month configurados

- [ ] **Subscription Criada**
  ```sql
  SELECT * FROM subscriptions ORDER BY created_at DESC LIMIT 1;
  ```

- [ ] **Banco Isolado Criado**
  ```sql
  -- MySQL
  SHOW DATABASES LIKE 'tenant_%';
  ```

#### Logs de Provisionamento:

```bash
tail -f backend/logs/api_*.log | grep "provisionamento"
```

Deve mostrar:
```
🏢 Iniciando provisionamento do tenant: Transportadora Teste Ltda
   Subdomínio gerado: transportadora-teste
   Credenciais do banco geradas: tenant_abc123
✅ Tenant criado com sucesso! ID: 1
🗄️  Provisionando banco de dados isolado...
✅ Banco de dados 'tenant_abc123' criado e configurado!
📧 Enviando email de boas-vindas...
✅ Email de boas-vindas enviado!
✅ PROVISIONAMENTO COMPLETO!
```

---

### 6️⃣ Teste de Email

#### Verificações:

- [ ] **Email Enviado**
  ```bash
  # Ver logs de email
  tail -f backend/logs/api_*.log | grep "email"
  ```

- [ ] **Conteúdo do Email**
  - Assunto: "Bem-vindo ao LogiFlow CRM"
  - Nome da empresa correto
  - Subdomain correto
  - URL de acesso: `https://transportadora-teste.logiflow.com.br`
  - Credenciais de acesso
  - Senha temporária

- [ ] **Email Recebido**
  - Verificar caixa de entrada
  - Email não foi para spam
  - Links funcionam

#### Teste Manual de Email:

```python
# No backend
from services.email_service import send_welcome_email

send_welcome_email(
    tenant_id=1,
    company_name="Transportadora Teste",
    contact_name="João Silva",
    contact_email="seu-email@gmail.com",
    subdomain="transportadora-teste",
    plan="starter",
    admin_email="admin@teste.com",
    admin_password="senha123"
)
```

---

### 7️⃣ Teste de Acesso ao Sistema

**URL**: `http://localhost:3001` (ou subdomain do tenant)

#### Verificações:

- [ ] **Login**
  - Página de login carrega
  - Credenciais do email funcionam
  - Redireciona para dashboard

- [ ] **Dashboard**
  - Dados do tenant exibidos
  - Menu lateral funciona
  - Widgets carregam

- [ ] **Uso do Plano**
  - Acessar: `/usage` ou componente PlanUsageDashboard
  - Limites exibidos corretamente:
    ```
    Starter:
    - Usuários: 0/5
    - Veículos: 0/10
    - Pedidos: 0/500
    ```

---

### 8️⃣ Teste de Limites do Plano

#### Teste: Criar Veículos até o Limite

```bash
# Criar 10 veículos (limite do Starter)
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/veiculos \
    -H "Content-Type: application/json" \
    -H "X-Tenant-ID: 1" \
    -d "{
      \"placa\": \"ABC${i}234\",
      \"modelo\": \"Caminhão Teste $i\",
      \"tipo\": \"truck\"
    }"
done

# Tentar criar o 11º (deve falhar)
curl -X POST http://localhost:8000/api/veiculos \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: 1" \
  -d '{
    "placa": "ABC9999",
    "modelo": "Deve Falhar",
    "tipo": "truck"
  }'
```

**Resposta Esperada**:
```json
{
  "detail": "Limite de veículos atingido (10). Faça upgrade do seu plano."
}
```
Status: `403 Forbidden`

#### Teste: Verificar Estatísticas

```bash
curl http://localhost:8000/api/tenants/1/usage
```

**Resposta Esperada**:
```json
{
  "plan": "starter",
  "limits": {
    "users": {
      "max": 5,
      "current": 0,
      "available": 5
    },
    "vehicles": {
      "max": 10,
      "current": 10,
      "available": 0
    },
    "orders_per_month": {
      "max": 500,
      "current": 0,
      "available": 500
    }
  },
  "trial_ends_at": "2025-12-28T12:00:00",
  "is_trial": false
}
```

---

### 9️⃣ Teste de Upgrade de Plano

#### Verificações:

- [ ] **Modal de Upgrade**
  - Clique em "🚀 Fazer Upgrade"
  - Modal abre com planos disponíveis
  - Preços corretos exibidos

- [ ] **Processar Upgrade**
  ```bash
  curl -X POST http://localhost:8000/api/billing/subscriptions/1/upgrade \
    -H "Content-Type: application/json" \
    -d '{"new_plan": "professional"}'
  ```

- [ ] **Limites Atualizados**
  ```bash
  # Verificar novos limites
  curl http://localhost:8000/api/tenants/1/usage
  ```

  Deve mostrar:
  ```json
  {
    "plan": "professional",
    "limits": {
      "users": {"max": 15, ...},
      "vehicles": {"max": 30, ...},
      "orders_per_month": {"max": "ilimitado", ...}
    }
  }
  ```

- [ ] **Criar Mais Veículos**
  - Agora pode criar até 30 veículos
  - Pedidos ilimitados

---

### 🔟 Teste de Integração Completa

#### Cenário: Novo Cliente

1. **Visita o Site**
   ```
   ✓ Acessa http://localhost:5174
   ✓ Navega até seção de preços
   ```

2. **Escolhe Plano Professional**
   ```
   ✓ Clica em "🚀 Assinar Agora" no plano Professional
   ✓ Abre checkout com plano=professional
   ```

3. **Preenche Dados**
   ```
   ✓ Nome: Transportadora XYZ
   ✓ Email: xyz@example.com
   ✓ Telefone: (11) 98888-8888
   ```

4. **Paga com Cartão**
   ```
   ✓ Cartão de teste aprovado
   ✓ Pagamento processado
   ```

5. **Sistema Provisiona**
   ```
   ✓ Tenant criado
   ✓ Banco isolado criado
   ✓ Email enviado
   ```

6. **Cliente Acessa**
   ```
   ✓ Recebe email com credenciais
   ✓ Faz login no sistema
   ✓ Vê dashboard
   ```

7. **Usa o Sistema**
   ```
   ✓ Cria 5 motoristas (limite: 15)
   ✓ Cria 10 veículos (limite: 30)
   ✓ Cria 100 pedidos (ilimitado)
   ```

8. **Verifica Limites**
   ```
   ✓ Dashboard mostra uso correto
   ✓ Não atinge limites
   ✓ Sistema funciona normalmente
   ```

---

## 📊 Métricas de Sucesso

### Performance

- [ ] Checkout carrega em < 2s
- [ ] Pagamento processa em < 5s
- [ ] Provisionamento completa em < 30s
- [ ] Email enviado em < 10s

### Funcionalidade

- [ ] 100% dos pagamentos aprovados são provisionados
- [ ] 100% dos emails são enviados
- [ ] 100% dos limites são respeitados
- [ ] 0% de erros críticos

### Experiência

- [ ] Fluxo intuitivo e claro
- [ ] Mensagens de erro úteis
- [ ] Feedback visual em cada etapa
- [ ] Sem etapas desnecessárias

---

## 🐛 Problemas Comuns

### Checkout não abre

**Causa**: Frontend não está rodando ou URL incorreta

**Solução**:
```bash
cd frontend
npm run dev
# Verificar porta: http://localhost:3001
```

### Pagamento não processa

**Causa**: Token do Mercado Pago inválido

**Solução**:
```bash
# Verificar .env
cat backend/.env | grep MERCADOPAGO
# Usar token de teste correto
```

### Webhook não recebe

**Causa**: Ngrok não configurado ou URL incorreta

**Solução**:
```bash
# Instalar ngrok
ngrok http 8000

# Copiar URL e configurar no Mercado Pago
# https://xxxx.ngrok.io/api/billing/webhooks/mercadopago
```

### Email não envia

**Causa**: SMTP não configurado

**Solução**:
```bash
# Verificar .env
cat backend/.env | grep SMTP
# Usar senha de app do Gmail
```

### Limite não funciona

**Causa**: Middleware não integrado

**Solução**:
```python
# Adicionar no endpoint
from middleware.plan_limits import check_vehicle_limit

@router.post("/veiculos")
def criar_veiculo(...):
    check_vehicle_limit(tenant, db)
    # ...
```

---

## ✅ Checklist Final de Teste

### Desenvolvimento

- [ ] Todos os serviços rodando (backend, frontend, site)
- [ ] Banco de dados acessível
- [ ] Redis rodando (se usado)
- [ ] Variáveis de ambiente configuradas

### Fluxo Básico

- [ ] Site → Checkout → Pagamento → Provisionamento
- [ ] Email de boas-vindas recebido
- [ ] Login funciona
- [ ] Dashboard carrega

### Limites

- [ ] Limite de usuários funciona
- [ ] Limite de veículos funciona
- [ ] Limite de pedidos funciona
- [ ] Upgrade de plano atualiza limites

### Integrações

- [ ] Mercado Pago processa pagamentos
- [ ] Webhook recebe notificações
- [ ] SMTP envia emails
- [ ] Banco isolado é criado

---

## 🎉 Teste Completo!

Se todos os itens acima passaram, o sistema está funcionando corretamente end-to-end! 🚀

**Próximos Passos**:
1. Documentar bugs encontrados
2. Corrigir problemas identificados
3. Repetir testes após correções
4. Preparar para produção
