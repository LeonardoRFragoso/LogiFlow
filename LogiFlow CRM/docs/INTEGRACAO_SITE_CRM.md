# 🔗 Integração Site de Divulgação → CRM LogiFlow

## 📋 Resumo Executivo

Este documento descreve a integração completa entre o site de divulgação (landing page) e o sistema CRM LogiFlow, incluindo captura de leads, sistema de billing e provisionamento de tenants.

---

## 🎯 Objetivos da Integração

### ✅ O que será implementado:

1. **Captura de Leads** - Formulário de demo → Banco de dados
2. **Gestão de Leads** - Dashboard para equipe de vendas
3. **Sistema de Billing** - Checkout e cobrança recorrente
4. **Provisionamento de Tenants** - Criação automática de contas
5. **Roteamento de Domínios** - Site público + App privado

---

## 🏗️ Arquitetura Proposta

```
┌─────────────────────────────────────────────────────────────┐
│                    DOMÍNIOS & ROTEAMENTO                     │
├─────────────────────────────────────────────────────────────┤
│  logiflow.com.br          → Site de Divulgação (Vue)        │
│  app.logiflow.com.br      → Frontend CRM (Vue)              │
│  api.logiflow.com.br      → Backend API (FastAPI)           │
│  crm.logiflow.com.br      → SuiteCRM (PHP)                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    NGINX (Proxy Reverso)                     │
├─────────────────────────────────────────────────────────────┤
│  • SSL/TLS (Let's Encrypt)                                  │
│  • Rate Limiting                                             │
│  • CORS Configuration                                        │
│  • Load Balancing                                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────┬──────────────┬──────────────┬───────────────┐
│   Site       │   Frontend   │   Backend    │   SuiteCRM    │
│   (Port 5173)│   (Port 3001)│   (Port 8000)│   (Port 8080) │
└──────────────┴──────────────┴──────────────┴───────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    BANCO DE DADOS                            │
├─────────────────────────────────────────────────────────────┤
│  • leads (captura do site)                                  │
│  • tenants (clientes SaaS)                                  │
│  • subscriptions (planos e pagamentos)                      │
│  • usage_metrics (métricas de uso)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de Diretórios (Após Integração)

```
LogiFlow CRM/
├── backend/                    # FastAPI
│   ├── routers/
│   │   ├── leads.py           # ✨ NOVO - Gestão de leads
│   │   ├── demo.py            # ✨ NOVO - Endpoint de demo
│   │   ├── tenants.py         # ✨ NOVO - Multi-tenant
│   │   └── billing.py         # ✨ NOVO - Cobrança
│   ├── models.py              # ✨ ATUALIZAR - Adicionar Lead, Tenant
│   └── services/
│       ├── lead_service.py    # ✨ NOVO - Lógica de leads
│       └── tenant_service.py  # ✨ NOVO - Provisionamento
│
├── site-divulgacao/           # ✨ MOVER AQUI (era LogiFlow-Site-Divulgacao)
│   ├── src/
│   │   ├── components/
│   │   │   └── DemoModal.vue  # ✨ ATUALIZAR - API endpoint
│   │   └── .env.production    # ✨ NOVO - Variáveis de produção
│   └── docker/
│       └── Dockerfile         # ✨ NOVO - Build do site
│
├── frontend/                   # App CRM (já existe)
├── suitecrm/                   # SuiteCRM (já existe)
├── docker/
│   └── nginx/
│       └── sites/
│           ├── site.conf      # ✨ NOVO - Config do site público
│           ├── app.conf       # ✨ NOVO - Config do app
│           └── api.conf       # ✨ NOVO - Config da API
│
└── docker-compose.yml         # ✨ ATUALIZAR - Adicionar serviço 'site'
```

---

## 🗄️ Modelo de Dados - Tabela `leads`

```sql
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    company VARCHAR(150) NOT NULL,
    vehicles VARCHAR(20),
    message TEXT,
    status ENUM('novo', 'contatado', 'qualificado', 'convertido', 'perdido') DEFAULT 'novo',
    source VARCHAR(50) DEFAULT 'site',
    assigned_to INT,  -- ID do vendedor
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    converted_at TIMESTAMP NULL,
    tenant_id INT NULL,  -- Se convertido, ID do tenant criado
    
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);
```

---

## 🗄️ Modelo de Dados - Tabela `tenants`

```sql
CREATE TABLE tenants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subdomain VARCHAR(50) NOT NULL UNIQUE,
    company_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(150) NOT NULL,
    contact_email VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(20),
    
    -- Banco de dados dedicado
    db_name VARCHAR(100) NOT NULL UNIQUE,
    db_user VARCHAR(100) NOT NULL,
    db_password VARCHAR(255) NOT NULL,
    
    -- Storage
    s3_bucket VARCHAR(100),
    
    -- Status
    status ENUM('active', 'suspended', 'cancelled', 'trial') DEFAULT 'trial',
    trial_ends_at TIMESTAMP NULL,
    
    -- Plano
    plan ENUM('starter', 'professional', 'enterprise') DEFAULT 'starter',
    max_users INT DEFAULT 5,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP NULL,
    
    INDEX idx_subdomain (subdomain),
    INDEX idx_status (status),
    INDEX idx_contact_email (contact_email)
);
```

---

## 🗄️ Modelo de Dados - Tabela `subscriptions`

```sql
CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    plan ENUM('starter', 'professional', 'enterprise') NOT NULL,
    status ENUM('active', 'past_due', 'cancelled', 'trial') DEFAULT 'trial',
    
    -- Valores
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'BRL',
    billing_cycle ENUM('monthly', 'yearly') DEFAULT 'monthly',
    
    -- Datas
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    trial_ends_at TIMESTAMP NULL,
    cancelled_at TIMESTAMP NULL,
    
    -- Gateway de pagamento
    payment_gateway ENUM('stripe', 'asaas', 'mercadopago') DEFAULT 'asaas',
    gateway_subscription_id VARCHAR(255),
    gateway_customer_id VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_status (status),
    INDEX idx_current_period_end (current_period_end)
);
```

---

## 🔌 Endpoints da API

### **1. Captura de Lead (Formulário de Demo)**

```http
POST /api/demo/request
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@transportadora.com.br",
  "phone": "(11) 99999-9999",
  "company": "Transportadora XYZ",
  "vehicles": "15-50",
  "message": "Quero conhecer o sistema"
}

Response 201:
{
  "success": true,
  "lead_id": 123,
  "message": "Solicitação recebida! Entraremos em contato em até 24h."
}
```

### **2. Listar Leads (Dashboard de Vendas)**

```http
GET /api/leads?status=novo&limit=50
Authorization: Bearer {token}

Response 200:
{
  "total": 45,
  "leads": [
    {
      "id": 123,
      "name": "João Silva",
      "email": "joao@transportadora.com.br",
      "company": "Transportadora XYZ",
      "status": "novo",
      "created_at": "2024-12-13T10:30:00Z"
    }
  ]
}
```

### **3. Criar Tenant (Provisionamento)**

```http
POST /api/tenants/provision
Authorization: Bearer {token}
Content-Type: application/json

{
  "lead_id": 123,
  "subdomain": "transportadora-xyz",
  "plan": "professional",
  "trial_days": 14
}

Response 201:
{
  "success": true,
  "tenant": {
    "id": 45,
    "subdomain": "transportadora-xyz",
    "url": "https://transportadora-xyz.logiflow.com.br",
    "db_name": "logiflow_tenant_45",
    "status": "trial",
    "trial_ends_at": "2024-12-27T23:59:59Z"
  },
  "credentials": {
    "username": "admin",
    "password": "temp_password_123",
    "login_url": "https://transportadora-xyz.logiflow.com.br/login"
  }
}
```

---

## 🚀 Fluxo de Conversão Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. VISITANTE ACESSA SITE                                    │
│    → logiflow.com.br                                        │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. PREENCHE FORMULÁRIO DE DEMO                              │
│    → DemoModal.vue                                          │
│    → POST /api/demo/request                                 │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. LEAD SALVO NO BANCO                                      │
│    → Tabela: leads                                          │
│    → Status: "novo"                                         │
│    → Email automático enviado                               │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. VENDEDOR QUALIFICA LEAD                                  │
│    → Dashboard de Leads (app.logiflow.com.br/leads)        │
│    → Contato via WhatsApp/Email/Telefone                   │
│    → Status: "novo" → "qualificado"                         │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. LEAD ACEITA TRIAL                                        │
│    → Vendedor clica "Criar Trial"                          │
│    → POST /api/tenants/provision                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. PROVISIONAMENTO AUTOMÁTICO                               │
│    → Criar banco de dados: logiflow_tenant_X               │
│    → Importar schema do SuiteCRM                           │
│    → Criar usuário admin                                    │
│    → Criar bucket S3                                        │
│    → Registrar tenant na metabase                          │
│    → Status: "trial" (14 dias)                             │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. EMAIL DE BOAS-VINDAS                                     │
│    → Credenciais de acesso                                  │
│    → URL: https://empresa.logiflow.com.br                  │
│    → Vídeos de onboarding                                   │
│    → Agendamento de treinamento                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. CLIENTE USA O SISTEMA (Trial 14 dias)                   │
│    → Health score monitorado                                │
│    → Alertas de uso baixo                                   │
│    → CS proativo                                            │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. CONVERSÃO PARA PAGO                                      │
│    → Checkout (Stripe/Asaas)                               │
│    → Plano: Starter/Professional/Enterprise                │
│    → Status: "trial" → "active"                            │
│    → Lead: "qualificado" → "convertido"                    │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. COBRANÇA RECORRENTE                                     │
│    → Webhook do gateway de pagamento                       │
│    → Atualização de status                                  │
│    → Renovação automática                                   │
│    → Suspensão por inadimplência                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Checklist de Implementação

### **Fase 1: Estrutura Básica (2-3 dias)**
- [ ] Mover `LogiFlow-Site-Divulgacao` → `LogiFlow CRM/site-divulgacao`
- [ ] Adicionar modelos `Lead`, `Tenant`, `Subscription` em `backend/models.py`
- [ ] Criar migrations do banco de dados
- [ ] Criar router `backend/routers/leads.py`
- [ ] Criar router `backend/routers/demo.py`
- [ ] Criar endpoint `POST /api/demo/request`

### **Fase 2: Integração Site (1-2 dias)**
- [ ] Atualizar `DemoModal.vue` com variável de ambiente
- [ ] Criar `.env.production` no site
- [ ] Adicionar serviço `site` no `docker-compose.yml`
- [ ] Criar `Dockerfile` para o site
- [ ] Testar formulário → backend → banco

### **Fase 3: Dashboard de Leads (2-3 dias)**
- [ ] Criar view `LeadsView.vue` no frontend
- [ ] Implementar CRUD de leads
- [ ] Sistema de filtros (status, data, origem)
- [ ] Atribuição de leads para vendedores
- [ ] Histórico de interações

### **Fase 4: Provisionamento (3-5 dias)**
- [ ] Criar router `backend/routers/tenants.py`
- [ ] Implementar `tenant_service.py`
- [ ] Script de criação de banco de dados
- [ ] Script de importação do schema SuiteCRM
- [ ] Criação de bucket S3
- [ ] Email de boas-vindas

### **Fase 5: Billing (3-5 dias)**
- [ ] Integração com Asaas/Stripe
- [ ] Página de checkout
- [ ] Webhooks de pagamento
- [ ] Gestão de assinaturas
- [ ] Suspensão por inadimplência

### **Fase 6: Nginx & Deploy (2-3 dias)**
- [ ] Configurar roteamento de domínios
- [ ] SSL/TLS com Let's Encrypt
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Deploy em staging
- [ ] Deploy em produção

---

## 🔐 Variáveis de Ambiente

### **Site de Divulgação (.env.production)**
```env
VITE_API_URL=https://api.logiflow.com.br
VITE_APP_URL=https://app.logiflow.com.br
VITE_SITE_NAME=LogiFlow CRM
```

### **Backend (.env)**
```env
# Billing
ASAAS_API_KEY=your_asaas_key
STRIPE_SECRET_KEY=your_stripe_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@logiflow.com.br
SMTP_PASSWORD=<YOUR_PASSWORD_HERE>

# S3/Storage
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET_PREFIX=logiflow-tenant-
AWS_REGION=us-east-1
```

---

## 📊 Métricas de Sucesso

### **KPIs de Marketing**
- Taxa de conversão site → lead: **> 3%**
- Tempo médio de resposta ao lead: **< 2 horas**
- Taxa de qualificação de leads: **> 40%**

### **KPIs de Vendas**
- Taxa de conversão lead → trial: **> 30%**
- Taxa de conversão trial → pago: **> 25%**
- Tempo médio de fechamento: **< 7 dias**

### **KPIs de Produto**
- Tempo de provisionamento: **< 5 minutos**
- Uptime do sistema: **> 99.5%**
- Health score médio: **> 70**

---

## 🚨 Próximos Passos Imediatos

1. **Mover o site** para dentro do projeto CRM
2. **Criar modelos de dados** (Lead, Tenant, Subscription)
3. **Implementar endpoint** `/api/demo/request`
4. **Testar integração** formulário → backend → banco
5. **Criar dashboard** de leads para vendedores

---

**Documento criado em:** 13/12/2024  
**Versão:** 1.0  
**Autor:** LogiFlow Team
