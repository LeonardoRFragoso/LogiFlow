# 🚀 Deploy Completo LogiFlow - Render.com

## 📋 Todos os Serviços Deployados

### 🔧 **Backend & Infrastructure**

1. **logiflow-api** (Backend FastAPI)
   - URL: `https://logiflow-api.onrender.com`
   - Tipo: Web Service (Python)
   - Healthcheck: `/health`

2. **logiflow-db** (PostgreSQL)
   - Tipo: Database
   - Plan: Free (shared)

3. **logiflow-redis** (Redis)
   - Tipo: Redis
   - Plan: Free

---

### 🎨 **Frontends (4 Aplicações)**

4. **logiflowcrm** (Frontend Principal)
   - URL: `https://logiflowcrm.onrender.com`
   - Tipo: Static Site (Vue 3)
   - Descrição: Sistema CRM completo para gestores

5. **logiflow-app-motorista** (App do Motorista PWA)
   - URL: `https://logiflow-app-motorista.onrender.com`
   - Tipo: Static Site (Vue 3 PWA)
   - Descrição: App para motoristas gerenciarem entregas
   - Instalável como PWA no celular

6. **logiflow-portal-cliente** (Portal de Rastreamento)
   - URL: `https://logiflow-portal-cliente.onrender.com`
   - Tipo: Static Site (Vue 3 PWA)
   - Descrição: Portal público para clientes rastrearem entregas

7. **logiflow-site** (Site de Divulgação)
   - URL: `https://logiflow-site.onrender.com`
   - Tipo: Static Site (Vue 3)
   - Descrição: Landing page de vendas e marketing

---

## 📊 **Resumo da Arquitetura**

```
┌─────────────────────────────────────────────────────────┐
│                    RENDER.COM SERVICES                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🌐 FRONTENDS (Static Sites)                           │
│  ├─ logiflowcrm.onrender.com        (CRM Principal)    │
│  ├─ logiflow-app-motorista.onrender.com  (App PWA)     │
│  ├─ logiflow-portal-cliente.onrender.com (Tracking)    │
│  └─ logiflow-site.onrender.com      (Landing Page)     │
│                                                          │
│  🔧 BACKEND                                             │
│  └─ logiflow-api.onrender.com       (FastAPI)          │
│                                                          │
│  💾 DADOS                                               │
│  ├─ logiflow-db                     (PostgreSQL)       │
│  └─ logiflow-redis                  (Redis Cache)      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔗 **Integrações Entre Serviços**

### Frontend Principal → Backend
```
https://logiflowcrm.onrender.com/api/*
  ↓ rewrite
https://logiflow-api.onrender.com/api/*
```

### App Motorista → Backend
```
https://logiflow-app-motorista.onrender.com/api/*
  ↓ rewrite
https://logiflow-api.onrender.com/api/*
```

### Portal Cliente → Backend
```
https://logiflow-portal-cliente.onrender.com/api/*
  ↓ rewrite
https://logiflow-api.onrender.com/api/*
```

---

## 👥 **Usuários por Aplicação**

### 🎯 **Frontend Principal (CRM)**
**Para:** Gestores e operadores da transportadora
**Login:**
```
Email: admin@logiflow.com
Senha: admin123
```

### 🚚 **App do Motorista (PWA)**
**Para:** Motoristas em campo
**Login:**
```
Email: motorista@logiflow.com
Senha: motorista123

OU

Qualquer um dos motoristas seedados:
- carlos@logiflow.com
- pedro@logiflow.com
- joao@logiflow.com
```

### 📦 **Portal do Cliente (Tracking)**
**Para:** Clientes finais (rastreamento público)
**Acesso:** Sem login, busca por código
**Códigos de teste:**
```
ENT-2024-0001
ENT-2024-0002
ENT-2024-0003
```

### 🌐 **Site de Divulgação**
**Para:** Visitantes e potenciais clientes
**Funcionalidades:**
- Informações sobre o sistema
- Solicitar demonstração
- Ver preços
- FAQ

---

## 🔐 **Variáveis de Ambiente Configuradas**

### Backend (logiflow-api)
```env
DATABASE_URL=<auto-gerado pelo Render>
REDIS_URL=<auto-gerado pelo Render>
SECRET_KEY=<auto-gerado>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=false
API_PREFIX=/api
API_VERSION=v1
ALLOWED_ORIGINS=*
```

---

## 🚀 **Como Fazer Deploy**

### **Opção 1: Via Blueprint (Automático)**

1. Commit do `render.yaml` atualizado
2. Push para GitHub
3. No Render Dashboard, clique em **"Sync"** no Blueprint
4. Aguarde o deploy de todos os 7 serviços

### **Opção 2: Manual (Um por vez)**

Se o Blueprint falhar, crie cada serviço manualmente no Render Dashboard.

---

## ⚠️ **Serviços NÃO Incluídos (Requerem Infraestrutura Externa)**

### 📱 **Evolution API (WhatsApp)**
**Por quê não está no Render?**
- Precisa de conexão WebSocket persistente
- Requer armazenamento de sessão WhatsApp
- Render Free Tier não suporta

**Alternativa:**
- VPS próprio (Contabo, DigitalOcean) - ~R$ 30/mês
- Evolution API Cloud - ~R$ 30/mês
- Railway.app - Free tier limitado

### 🏢 **SuiteCRM (CRM Avançado)**
**Por quê não está no Render?**
- Aplicação PHP muito pesada (>500MB)
- Requer Apache/Nginx + PHP-FPM + MySQL
- Render Free Tier não suporta apps PHP complexos

**Alternativa:**
- Hostinger PHP - ~R$ 20/mês
- Cloudways - ~$12/mês
- VPS próprio

---

## 📊 **Monitoramento e Logs**

### Ver Logs em Tempo Real
```bash
# Render CLI (se instalado)
render logs -s logiflow-api
render logs -s logiflowcrm
render logs -s logiflow-app-motorista
render logs -s logiflow-portal-cliente
render logs -s logiflow-site
```

### Via Dashboard
1. Acesse https://dashboard.render.com
2. Clique no serviço desejado
3. Vá em **Logs** na sidebar

---

## 🧪 **Testar Todos os Serviços**

### 1. Backend API
```bash
curl https://logiflow-api.onrender.com/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-15T20:00:00"
}
```

### 2. Frontend Principal
Abra: https://logiflowcrm.onrender.com
- Deve carregar a tela de login

### 3. App Motorista
Abra: https://logiflow-app-motorista.onrender.com
- Deve carregar o login do motorista
- Testar instalação como PWA

### 4. Portal Cliente
Abra: https://logiflow-portal-cliente.onrender.com
- Deve carregar a busca de rastreamento
- Buscar: ENT-2024-0001

### 5. Site Divulgação
Abra: https://logiflow-site.onrender.com
- Deve carregar a landing page
- Testar formulário de demo

---

## 💰 **Custos (Free Tier)**

| Serviço | Tipo | Custo |
|---------|------|-------|
| logiflow-api | Web Service | Free |
| logiflowcrm | Static Site | Free |
| logiflow-app-motorista | Static Site | Free |
| logiflow-portal-cliente | Static Site | Free |
| logiflow-site | Static Site | Free |
| logiflow-db | PostgreSQL | Free |
| logiflow-redis | Redis | Free |
| **TOTAL** | | **R$ 0/mês** |

**Limitações Free Tier:**
- Spin down após 15min de inatividade
- 750h/mês de runtime por serviço
- 100GB bandwidth/mês
- 1GB de DB
- 25MB Redis

---

## 🎯 **Próximos Passos**

### 1. Domínios Personalizados (Opcional)
```
logiflow.com.br           → logiflow-site
app.logiflow.com.br       → logiflowcrm
motorista.logiflow.com.br → logiflow-app-motorista
rastreio.logiflow.com.br  → logiflow-portal-cliente
api.logiflow.com.br       → logiflow-api
```

### 2. Upgrade para Planos Pagos (Quando necessário)
- **Starter** ($7/mês): Sem spin down, mais recursos
- **Standard** ($25/mês): Ainda mais recursos
- **Pro** ($85/mês): Recursos enterprise

### 3. Integrações Externas
- Google Maps API (cálculo de rotas)
- Focus NFe (emissão CT-e)
- Evolution API (WhatsApp)
- Melhor Envio (cotação frete)

---

## ✅ **Checklist de Deploy**

- [ ] PyJWT adicionado ao requirements.txt
- [ ] render.yaml atualizado com 7 serviços
- [ ] Commit e push para GitHub
- [ ] Sync do Blueprint no Render
- [ ] Aguardar deploy de todos os serviços
- [ ] Testar cada URL
- [ ] Testar login em cada aplicação
- [ ] Verificar integração frontend → backend
- [ ] Verificar PWA (app motorista e portal)
- [ ] Popular banco com seed data
- [ ] Documentar URLs para equipe

---

**Última atualização:** 2025-12-15  
**Versão:** 1.0.0 - Deploy Completo

