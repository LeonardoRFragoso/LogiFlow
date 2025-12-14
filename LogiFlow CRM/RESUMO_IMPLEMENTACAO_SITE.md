# ✅ Resumo da Implementação - Integração Site → CRM

## 📊 Status Atual

### ✅ **CONCLUÍDO**

#### **1. Modelos de Dados (backend/models.py)**
- ✅ Enum `StatusLead` (novo, contatado, qualificado, convertido, perdido)
- ✅ Enum `StatusTenant` (active, suspended, cancelled, trial)
- ✅ Enum `PlanType` (starter, professional, enterprise)
- ✅ Enum `SubscriptionStatus` (active, past_due, cancelled, trial)
- ✅ Enum `PaymentGateway` (stripe, asaas, mercadopago)
- ✅ Model `Lead` - Captura de leads do site
- ✅ Model `Tenant` - Clientes SaaS (multi-tenant)
- ✅ Model `Subscription` - Assinaturas e pagamentos

#### **2. API Endpoints**

**Router: `/api/leads` (backend/routers/leads.py)**
- ✅ `POST /api/leads/` - Criar lead
- ✅ `GET /api/leads/` - Listar leads (com filtros)
- ✅ `GET /api/leads/{id}` - Obter lead específico
- ✅ `PATCH /api/leads/{id}` - Atualizar lead
- ✅ `DELETE /api/leads/{id}` - Deletar lead
- ✅ `GET /api/leads/stats/summary` - Estatísticas de leads

**Router: `/demo` (backend/routers/demo.py)**
- ✅ `POST /demo/request` - Formulário do site (INTEGRADO COM BD)
- ✅ `GET /demo/requests` - Listar solicitações
- ✅ `GET /demo/requests/{id}` - Obter solicitação específica

#### **3. Integração Backend**
- ✅ Router `leads` importado no `main.py`
- ✅ Endpoint `/demo/request` atualizado para salvar no banco
- ✅ Validação de email duplicado
- ✅ Status automático: "novo"

---

## 📋 O QUE FALTA IMPLEMENTAR

### **Fase 1: Banco de Dados (URGENTE)**
```bash
# Criar migrations para as novas tabelas
alembic revision --autogenerate -m "Add leads, tenants, subscriptions tables"
alembic upgrade head
```

**Tabelas a criar:**
- `leads` - Captura do site
- `tenants` - Clientes SaaS
- `subscriptions` - Assinaturas

### **Fase 2: Mover o Site**
```bash
# Comando para mover
cd "C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM"
move "LogiFlow-Site-Divulgacao" "LogiFlow CRM\site-divulgacao"
```

### **Fase 3: Atualizar Site**

**Arquivo: `site-divulgacao/.env.production`** (CRIAR)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_URL=http://localhost:3001
```

**Arquivo: `site-divulgacao/src/components/DemoModal.vue`** (ATUALIZAR linha 138)
```javascript
// ANTES:
const response = await fetch('http://localhost:8000/demo/request', {

// DEPOIS:
const response = await fetch(`${import.meta.env.VITE_API_URL}/demo/request`, {
```

### **Fase 4: Docker Compose**

**Adicionar ao `docker-compose.yml`:**
```yaml
  # Site de Divulgação
  site:
    build:
      context: ./site-divulgacao
      dockerfile: Dockerfile
    container_name: logiflow_site
    restart: unless-stopped
    ports:
      - "5173:80"
    networks:
      - logiflow_network
```

**Criar: `site-divulgacao/Dockerfile`**
```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Criar: `site-divulgacao/nginx.conf`**
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Fase 5: Frontend - Dashboard de Leads**

**Criar: `frontend/src/views/LeadsView.vue`**
```vue
<template>
  <div class="leads-dashboard">
    <h1>Gestão de Leads</h1>
    
    <!-- Filtros -->
    <div class="filters">
      <select v-model="filtroStatus">
        <option value="">Todos</option>
        <option value="novo">Novos</option>
        <option value="contatado">Contatados</option>
        <option value="qualificado">Qualificados</option>
        <option value="convertido">Convertidos</option>
        <option value="perdido">Perdidos</option>
      </select>
    </div>

    <!-- Lista de Leads -->
    <div class="leads-list">
      <div v-for="lead in leads" :key="lead.id" class="lead-card">
        <h3>{{ lead.name }}</h3>
        <p>{{ lead.company }}</p>
        <p>{{ lead.email }} | {{ lead.phone }}</p>
        <span :class="`badge ${lead.status}`">{{ lead.status }}</span>
        <button @click="abrirLead(lead)">Ver Detalhes</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const leads = ref([])
const filtroStatus = ref('')

const carregarLeads = async () => {
  const response = await axios.get('/api/leads', {
    params: { status: filtroStatus.value }
  })
  leads.value = response.data
}

onMounted(() => {
  carregarLeads()
})
</script>
```

### **Fase 6: Provisionamento de Tenants**

**Criar: `backend/routers/tenants.py`**
```python
@router.post("/provision")
async def provision_tenant(
    lead_id: int,
    subdomain: str,
    plan: str,
    trial_days: int = 14,
    db: Session = Depends(get_db)
):
    """
    Provisionar novo tenant a partir de um lead
    """
    # 1. Buscar lead
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(404, "Lead não encontrado")
    
    # 2. Criar banco de dados
    db_name = f"logiflow_tenant_{subdomain}"
    db_user = f"user_{subdomain}"
    db_password = generate_password()
    
    # 3. Criar tenant
    tenant = Tenant(
        subdomain=subdomain,
        company_name=lead.company,
        contact_name=lead.name,
        contact_email=lead.email,
        contact_phone=lead.phone,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        status="trial",
        plan=plan,
        trial_ends_at=datetime.utcnow() + timedelta(days=trial_days)
    )
    
    db.add(tenant)
    db.commit()
    
    # 4. Executar script de provisionamento
    # provision_database(db_name, db_user, db_password)
    
    # 5. Atualizar lead
    lead.status = "convertido"
    lead.converted_at = datetime.utcnow()
    lead.tenant_id = tenant.id
    db.commit()
    
    return {"success": True, "tenant": tenant}
```

### **Fase 7: Sistema de Billing**

**Integração com Asaas:**
```python
# backend/services/billing_service.py
import requests

class AsaasClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.asaas.com/api/v3"
    
    def create_customer(self, tenant: Tenant):
        """Criar cliente no Asaas"""
        response = requests.post(
            f"{self.base_url}/customers",
            headers={"access_token": self.api_key},
            json={
                "name": tenant.contact_name,
                "email": tenant.contact_email,
                "phone": tenant.contact_phone,
                "cpfCnpj": tenant.company_cnpj
            }
        )
        return response.json()
    
    def create_subscription(self, customer_id: str, plan_value: float):
        """Criar assinatura recorrente"""
        response = requests.post(
            f"{self.base_url}/subscriptions",
            headers={"access_token": self.api_key},
            json={
                "customer": customer_id,
                "billingType": "CREDIT_CARD",
                "value": plan_value,
                "cycle": "MONTHLY"
            }
        )
        return response.json()
```

---

## 🧪 Como Testar

### **1. Testar Endpoint de Demo**
```bash
curl -X POST http://localhost:8000/demo/request \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@teste.com",
    "phone": "(11) 99999-9999",
    "company": "Transportadora Teste",
    "vehicles": "15-50",
    "message": "Quero testar o sistema"
  }'
```

### **2. Listar Leads**
```bash
curl http://localhost:8000/api/leads
```

### **3. Estatísticas**
```bash
curl http://localhost:8000/api/leads/stats/summary
```

---

## 📈 Métricas de Sucesso

### **KPIs a Monitorar:**
- ✅ Taxa de conversão site → lead: **> 3%**
- ⏳ Tempo médio de resposta: **< 2 horas**
- ⏳ Taxa lead → trial: **> 30%**
- ⏳ Taxa trial → pago: **> 25%**

---

## 🚀 Próximos Passos Imediatos

1. **Criar migrations do banco de dados**
2. **Mover diretório do site**
3. **Atualizar DemoModal.vue com variável de ambiente**
4. **Adicionar serviço 'site' no docker-compose.yml**
5. **Testar integração completa**
6. **Criar dashboard de leads no frontend**
7. **Implementar provisionamento de tenants**
8. **Integrar sistema de billing (Asaas)**

---

**Documento atualizado:** 13/12/2024 às 12:45  
**Status:** Fase 1 completa (Modelos + Endpoints)  
**Próxima fase:** Migrations + Mover Site
