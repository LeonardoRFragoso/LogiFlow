# 🎨 4 Frontends Vue.js - LogiFlow CRM

## 📱 Visão Geral

O LogiFlow CRM possui **4 aplicações frontend independentes**, todas desenvolvidas em **Vue.js 3 + Vite + TailwindCSS**:

```
┌─────────────────────────────────────────────────────────┐
│           ECOSSISTEMA FRONTEND LOGIFLOW                 │
└─────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐
│  1. SISTEMA      │  │  2. APP          │
│  PRINCIPAL       │  │  MOTORISTA       │
│                  │  │                  │
│  • Dashboard     │  │  • Entregas      │
│  • Pedidos       │  │  • Rotas GPS     │
│  • Clientes      │  │  • Check-in/out  │
│  • Entregas      │  │  • Ocorrências   │
│  • Financeiro    │  │  • Mobile-first  │
│  • Relatórios    │  │                  │
│                  │  │                  │
│  :3001           │  │  :3002           │
└──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐
│  3. PORTAL       │  │  4. SITE         │
│  CLIENTE         │  │  DIVULGAÇÃO      │
│                  │  │                  │
│  • Rastreamento  │  │  • Landing page  │
│  • Cotações      │  │  • Institucional │
│  • Histórico     │  │  • Contato       │
│  • Faturas       │  │  • Marketing     │
│  • Self-service  │  │  • Blog          │
│                  │  │                  │
│  :3003           │  │  :5173           │
└──────────────────┘  └──────────────────┘
```

---

## 1️⃣ Sistema Principal (CRM Completo)

### **Localização**
```
frontend/
├── src/
│   ├── views/
│   │   ├── operacional/      # Pedidos, entregas
│   │   ├── frota/            # Motoristas, veículos
│   │   ├── financeiro/       # Faturamento, contas
│   │   ├── satisfacao/       # NPS, pesquisas
│   │   ├── crm/              # Contacts, Opportunities, Cases
│   │   └── gps/              # Rastreamento
│   ├── components/
│   ├── services/
│   └── router/
├── package.json
└── vite.config.js
```

### **Funcionalidades**
- ✅ Dashboard executivo
- ✅ Gestão de pedidos e entregas
- ✅ Cadastro de clientes
- ✅ Gestão de frota (motoristas e veículos)
- ✅ Módulo financeiro
- ✅ Rastreamento GPS
- ✅ Integração SuiteCRM (Contacts, Opportunities, Cases)
- ✅ Pesquisas NPS
- ✅ Relatórios e analytics

### **Acesso**
- **URL:** http://localhost:3001
- **Usuários:** Administradores, operadores, gestores
- **Porta Docker:** 3001

---

## 2️⃣ App Motorista

### **Localização**
```
app-motorista/
├── src/
│   ├── views/
│   │   ├── EntregasView.vue
│   │   ├── RotasView.vue
│   │   └── PerfilView.vue
│   ├── components/
│   ├── services/
│   └── router/
├── package.json
└── vite.config.js
```

### **Funcionalidades**
- ✅ Lista de entregas do dia
- ✅ Navegação GPS integrada
- ✅ Check-in/check-out de entregas
- ✅ Registro de ocorrências
- ✅ Foto de comprovante
- ✅ Assinatura digital
- ✅ Histórico de entregas
- ✅ Interface mobile-first

### **Acesso**
- **URL:** http://localhost:3002
- **Usuários:** Motoristas
- **Porta Docker:** 3002

### **Características**
- Design otimizado para mobile
- Funciona offline (PWA ready)
- Geolocalização em tempo real
- Push notifications

---

## 3️⃣ Portal Cliente

### **Localização**
```
portal-cliente/
├── src/
│   ├── views/
│   │   ├── RastreamentoView.vue
│   │   ├── CotacoesView.vue
│   │   ├── HistoricoView.vue
│   │   └── FaturasView.vue
│   ├── components/
│   ├── services/
│   └── router/
├── package.json
└── vite.config.js
```

### **Funcionalidades**
- ✅ Rastreamento de entregas em tempo real
- ✅ Solicitar cotações online
- ✅ Histórico de pedidos
- ✅ Download de faturas
- ✅ Área do cliente personalizada
- ✅ Notificações de status
- ✅ Chat de suporte

### **Acesso**
- **URL:** http://localhost:3003
- **Usuários:** Clientes finais
- **Porta Docker:** 3003

### **Características**
- Self-service completo
- Interface intuitiva
- Responsivo (mobile + desktop)
- Integração com API backend

---

## 4️⃣ Site Divulgação

### **Localização**
```
site-divulgacao/
├── src/
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── ServicosView.vue
│   │   ├── ContatoView.vue
│   │   └── BlogView.vue
│   ├── components/
│   └── router/
├── package.json
└── vite.config.js
```

### **Funcionalidades**
- ✅ Landing page institucional
- ✅ Apresentação de serviços
- ✅ Formulário de contato
- ✅ Blog/notícias
- ✅ Depoimentos de clientes
- ✅ FAQ
- ✅ SEO otimizado

### **Acesso**
- **URL:** http://localhost:5173
- **Usuários:** Público geral
- **Porta Docker:** 5173

### **Características**
- Design moderno e atrativo
- Performance otimizada
- SEO-friendly
- Formulários de captação de leads

---

## 🐳 Docker Configuration

### **docker-compose.production.yml**

```yaml
services:
  # Frontend 1 - Sistema Principal
  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend/Dockerfile
    container_name: logiflow_frontend
    ports:
      - "3001:80"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_SUITECRM_URL=http://localhost:8080

  # Frontend 2 - App Motorista
  app-motorista:
    build:
      context: ./app-motorista
      dockerfile: ../docker/app-motorista/Dockerfile
    container_name: logiflow_app_motorista
    ports:
      - "3002:80"
    environment:
      - VITE_API_URL=http://localhost:8000

  # Frontend 3 - Site Divulgação
  site-divulgacao:
    build:
      context: ./site-divulgacao
      dockerfile: ../docker/site/Dockerfile
    container_name: logiflow_site
    ports:
      - "5173:80"
    environment:
      - VITE_API_URL=http://localhost:8000

  # Frontend 4 - Portal Cliente
  portal-cliente:
    build:
      context: ./portal-cliente
      dockerfile: ../docker/portal-cliente/Dockerfile
    container_name: logiflow_portal_cliente
    ports:
      - "3003:80"
    environment:
      - VITE_API_URL=http://localhost:8000
```

---

## 🔧 Stack Técnico Comum

Todos os 4 frontends compartilham:

### **Framework & Build**
- ⚡ **Vue.js 3** - Framework progressivo
- ⚡ **Vite** - Build tool ultra-rápido
- ⚡ **Vue Router 4** - Roteamento SPA

### **Styling**
- 🎨 **TailwindCSS 3** - Utility-first CSS
- 🎨 **PostCSS** - Transformações CSS
- 🎨 **Autoprefixer** - Compatibilidade cross-browser

### **HTTP & State**
- 🔌 **Axios** - Cliente HTTP
- 🔌 **Pinia** (opcional) - State management

### **Deployment**
- 🐳 **Docker** - Containerização
- 🌐 **Nginx Alpine** - Web server
- 📦 **Multi-stage build** - Otimização de imagem

---

## 📊 Comparação

| Característica | Sistema Principal | App Motorista | Portal Cliente | Site Divulgação |
|----------------|-------------------|---------------|----------------|-----------------|
| **Público** | Interno | Motoristas | Clientes | Público geral |
| **Autenticação** | ✅ Obrigatória | ✅ Obrigatória | ✅ Obrigatória | ❌ Pública |
| **Mobile-first** | ❌ Desktop | ✅ Sim | ✅ Sim | ✅ Sim |
| **Offline** | ❌ Não | ✅ PWA | ❌ Não | ❌ Não |
| **GPS** | ✅ Rastreamento | ✅ Navegação | ✅ Rastreamento | ❌ Não |
| **Complexidade** | 🔴 Alta | 🟡 Média | 🟡 Média | 🟢 Baixa |
| **Integrações** | SuiteCRM, API | API | API | API (forms) |

---

## 🚀 Como Rodar Localmente

### **Desenvolvimento (individual)**

```bash
# Sistema Principal
cd frontend
npm install
npm run dev
# Acessa: http://localhost:5173

# App Motorista
cd app-motorista
npm install
npm run dev
# Acessa: http://localhost:5174

# Portal Cliente
cd portal-cliente
npm install
npm run dev
# Acessa: http://localhost:5175

# Site Divulgação
cd site-divulgacao
npm install
npm run dev
# Acessa: http://localhost:5176
```

### **Produção (Docker - todos juntos)**

```bash
# Iniciar todos os 4 frontends
docker-compose -f docker-compose.production.yml up -d

# Acessar:
# - Sistema: http://localhost:3001
# - App Motorista: http://localhost:3002
# - Portal Cliente: http://localhost:3003
# - Site: http://localhost:5173
```

---

## 🔐 Autenticação

### **Sistema Principal + App Motorista + Portal Cliente**
- JWT Token via API FastAPI
- Login: `/api/v1/auth/login`
- Refresh: `/api/v1/auth/refresh`
- Storage: `localStorage`

### **Site Divulgação**
- Sem autenticação (público)
- Formulários enviam para API

---

## 📱 Responsividade

### **Breakpoints TailwindCSS**
```css
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
2xl: 1536px /* Extra large */
```

### **Prioridades**
- **Sistema Principal:** Desktop-first
- **App Motorista:** Mobile-first (PWA)
- **Portal Cliente:** Mobile-first
- **Site Divulgação:** Mobile-first

---

## 🎯 Roadmap

### **Próximas Features**

**Sistema Principal:**
- [ ] Dashboard em tempo real (WebSockets)
- [ ] Relatórios avançados
- [ ] Integração WhatsApp Business

**App Motorista:**
- [ ] Modo offline completo
- [ ] Push notifications
- [ ] Gamificação

**Portal Cliente:**
- [ ] Chat em tempo real
- [ ] Agendamento de coletas
- [ ] Programa de fidelidade

**Site Divulgação:**
- [ ] Blog CMS
- [ ] Calculadora de frete
- [ ] Chatbot

---

## 📞 Suporte

**Documentação completa:** `DOCKER_STACK_COMPLETO.md`

**Comandos úteis:**
```bash
# Ver logs de um frontend
docker-compose -f docker-compose.production.yml logs -f frontend
docker-compose -f docker-compose.production.yml logs -f app-motorista
docker-compose -f docker-compose.production.yml logs -f portal-cliente
docker-compose -f docker-compose.production.yml logs -f site-divulgacao

# Rebuild de um frontend
docker-compose -f docker-compose.production.yml build --no-cache frontend
docker-compose -f docker-compose.production.yml up -d frontend
```

---

**Criado em:** 16/12/2024  
**Versão:** 1.0.0  
**Stack:** Vue.js 3 + Vite + TailwindCSS + Docker
