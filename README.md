<div align="center">

# 🚛 LogiFlow CRM

### Sistema CRM SaaS Completo para Transportadoras e Logística

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.4+-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-5.0+-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)](/)

<br/>

**LogiFlow** é uma plataforma brasileira que unifica **gestão comercial, operacional e fiscal** para transportadoras em um único sistema, com emissão de CT-e/MDF-e integrada, rastreamento GPS em tempo real e múltiplas integrações.

[Demonstração](#-demonstração) • [Funcionalidades](#-funcionalidades) • [Tecnologias](#-stack-tecnológico) • [Instalação](#-instalação) • [Documentação](#-documentação)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Proposta de Valor](#-proposta-de-valor)
- [Funcionalidades](#-funcionalidades)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitetura](#-arquitetura)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Deploy](#-deploy)
- [Integrações](#-integrações)
- [API Reference](#-api-reference)
- [Documentação](#-documentação)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O LogiFlow CRM é uma solução completa desenvolvida especificamente para o setor de **transporte e logística brasileiro**, oferecendo:

- **CRM Comercial** - Gestão de leads, oportunidades e clientes
- **TMS Operacional** - Cotações, pedidos, entregas e rastreamento
- **Emissor Fiscal** - CT-e e MDF-e integrados (Focus NFe)
- **Gestão de Frota** - Veículos, motoristas e manutenção
- **Customer Success** - NPS, CSAT e Health Score automatizados
- **Multi-Tenancy** - Arquitetura SaaS com isolamento de dados

---

## 💎 Proposta de Valor

| Benefício | Descrição |
|-----------|-----------|
| 🎯 **Tudo em um só lugar** | Elimina 3-4 sistemas separados (CRM + TMS + Emissor Fiscal + Rastreamento) |
| 💰 **Preço acessível** | 60-70% mais barato que soluções enterprise |
| ⚡ **Setup em 48h** | Sem projetos de meses; cliente opera em 2 dias |
| 📅 **Sem fidelidade** | Pagamento mensal, cancele quando quiser |
| 🇧🇷 **100% brasileiro** | Focado nas necessidades fiscais e operacionais do Brasil |

---

## ✨ Funcionalidades

### 📊 Módulo Comercial (CRM)
- Gestão completa de **Leads** com funil de vendas
- **Oportunidades** e pipeline comercial
- Cadastro de **Clientes** (PF/PJ)
- **Dashboard** com métricas em tempo real
- Histórico de interações e atividades

### 🚚 Módulo Operacional (TMS)
- **Cotações de Frete** com cálculo automático por região/peso/volume
- **Pedidos de Frete** - gestão do ciclo completo
- **Entregas** - rastreamento e status em tempo real
- **Ocorrências** - registro de avarias, atrasos, devoluções
- Integração com **Melhor Envio** para cotações multi-transportadora

### 🚗 Gestão de Frota
- Cadastro de **Veículos** com documentação
- Controle de **Motoristas** com CNH e vencimentos
- Rastreamento **GPS** em tempo real
- Integração com rastreadores: **Sascar**, **Autotrac**, **Onixsat**
- **App do Motorista** (PWA) para coleta de posição

### 📄 Módulo Fiscal
- Emissão de **CT-e** (Conhecimento de Transporte Eletrônico)
- Emissão de **MDF-e** (Manifesto de Documentos Fiscais)
- Integração com **Focus NFe**
- Consulta de status e cancelamento
- Download de XML e DACTE/DAMDFE

### 💳 Billing & Pagamentos
- Sistema de **planos e assinaturas** (Starter, Professional, Enterprise)
- Integração com **MercadoPago**
- Controle de **quotas** por plano
- Checkout integrado com webhooks

### 📈 Customer Success
- **Health Score** automático por cliente
- Pesquisas **NPS** e **CSAT** automatizadas
- Alertas de churn e oportunidades de upsell
- Dashboard de satisfação

### 🔗 Integrações ERP
- **Omie** - Sincronização de clientes, produtos e pedidos
- **Bling** - Integração completa
- **Tiny** - Sincronização bidirecional

### 📱 Comunicação
- Notificações via **WhatsApp** (Evolution API)
- Templates de mensagens configuráveis
- Alertas automáticos de status de entrega

---

## 🛠 Stack Tecnológico

### Backend
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.104+ | Framework web assíncrono |
| **SQLAlchemy** | 2.0+ | ORM |
| **Alembic** | 1.12+ | Migrações de banco |
| **Pydantic** | 2.5+ | Validação de dados |
| **Redis** | 5.0+ | Cache e filas |
| **Celery** | 5.3+ | Tarefas assíncronas |
| **APScheduler** | 3.10+ | Agendamento de jobs |
| **Loguru** | 0.7+ | Logging |

### Frontend Principal (CRM)
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Vue.js** | 3.4+ | Framework reativo |
| **Vite** | 5.0+ | Build tool |
| **Pinia** | 2.1+ | State management |
| **Vue Router** | 4.2+ | Roteamento SPA |
| **TailwindCSS** | 3.4+ | Estilização utility-first |
| **Axios** | 1.6+ | HTTP client |
| **Day.js** | 1.11+ | Manipulação de datas |

### Aplicações Adicionais
| Aplicação | Tecnologia | Descrição |
|-----------|------------|-----------|
| **App Motorista** | Vue 3 + PWA | App mobile para motoristas |
| **Portal Cliente** | Vue 3 | Portal de rastreamento para clientes |
| **Site Divulgação** | Vue 3 | Landing page institucional |

### Banco de Dados & Infraestrutura
| Tecnologia | Uso |
|------------|-----|
| **PostgreSQL** | Banco principal (produção) |
| **SQLite** | Desenvolvimento local |
| **MariaDB** | Suporte SuiteCRM |
| **Redis** | Cache, sessões, filas |
| **Docker** | Containerização |
| **Nginx** | Reverse proxy |

---

## 🏗 Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTENDS (Vue 3 + Vite)                     │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│   CRM Principal │  App Motorista  │ Portal Cliente  │    Site       │
│   (SPA Admin)   │     (PWA)       │  (Tracking)     │  (Landing)    │
└────────┬────────┴────────┬────────┴────────┬────────┴───────┬───────┘
         │                 │                 │                │
         └─────────────────┴────────┬────────┴────────────────┘
                                    │ REST API (JSON)
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND ORQUESTRADOR (FastAPI)                    │
├─────────────────────────────────────────────────────────────────────┤
│  🔐 Auth & RBAC  │  💳 Billing  │  📊 Analytics  │  🔄 Sync Engine  │
├─────────────────────────────────────────────────────────────────────┤
│                          MIDDLEWARES                                 │
│  • Rate Limiting  • CORS  • Tenant Isolation  • Correlation ID      │
├─────────────────────────────────────────────────────────────────────┤
│                          INTEGRAÇÕES                                 │
│  📄 Focus NFe  │  📦 ERPs  │  📍 GPS  │  💬 WhatsApp  │  🗺 Maps    │
└────────┬────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│   PostgreSQL    │      Redis       │     Celery      │  Scheduler   │
│   (Database)    │  (Cache/Queue)   │ (Async Tasks)   │   (Jobs)     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
LogiFlow/
├── LogiFlow CRM/
│   ├── backend/                    # API FastAPI
│   │   ├── routers/               # Endpoints da API (30+ routers)
│   │   │   ├── auth.py            # Autenticação JWT
│   │   │   ├── billing.py         # Planos e pagamentos
│   │   │   ├── cotacoes.py        # Cotações de frete
│   │   │   ├── pedidos.py         # Pedidos de frete
│   │   │   ├── motoristas.py      # Gestão de motoristas
│   │   │   ├── veiculos.py        # Gestão de frota
│   │   │   ├── fiscal.py          # CT-e / MDF-e
│   │   │   ├── gps_tracking.py    # Rastreamento GPS
│   │   │   ├── nps.py             # Pesquisas NPS/CSAT
│   │   │   ├── health_score.py    # Customer Success
│   │   │   └── ...
│   │   ├── integrations/          # Clientes de APIs externas
│   │   │   ├── erp/               # Omie, Bling, Tiny
│   │   │   ├── fiscal/            # Focus NFe
│   │   │   ├── gps/               # Sascar, Autotrac, Onixsat
│   │   │   ├── frete/             # Melhor Envio
│   │   │   └── maps/              # Google Maps
│   │   ├── services/              # Lógica de negócio
│   │   ├── middleware/            # Rate limit, tenant, CORS
│   │   ├── models.py              # Modelos SQLAlchemy
│   │   ├── config.py              # Configurações
│   │   ├── main.py                # Aplicação FastAPI
│   │   └── requirements.txt
│   │
│   ├── frontend/                  # CRM Principal (Vue 3)
│   │   ├── src/
│   │   │   ├── views/             # 37 telas
│   │   │   ├── components/        # Componentes reutilizáveis
│   │   │   ├── stores/            # Pinia stores
│   │   │   ├── router/            # Vue Router
│   │   │   └── services/          # API services
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   ├── app-motorista/             # PWA do Motorista
│   ├── portal-cliente/            # Portal de Rastreamento
│   ├── site-divulgacao/           # Landing Page
│   │
│   ├── docker/                    # Configurações Docker
│   ├── docs/                      # Documentação detalhada
│   ├── scripts/                   # Scripts de automação
│   ├── templates/                 # Templates de importação
│   │
│   ├── docker-compose.yml         # Orquestração local
│   ├── docker-compose.production.yml
│   └── render.yaml                # Deploy Render.com
│
├── render.yaml                    # Blueprint principal
└── README.md                      # Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos

- **Python** 3.11+
- **Node.js** 18+
- **Docker** e **Docker Compose** (recomendado)
- **PostgreSQL** 15+ ou **SQLite** (dev)
- **Redis** 5+

### Opção 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd LogiFlow/LogiFlow\ CRM

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Suba todos os serviços
docker-compose up -d

# Acesse:
# - Frontend CRM: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/api/v1/docs
```

### Opção 2: Desenvolvimento Local

```bash
# Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd LogiFlow/LogiFlow\ CRM

# ===== BACKEND =====
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure o ambiente
cp .env.example .env

# Execute as migrações
alembic upgrade head

# Inicie o backend
uvicorn main:app --reload --port 8000

# ===== FRONTEND (novo terminal) =====
cd ../frontend
npm install
npm run dev
```

---

## ⚙ Configuração

### Variáveis de Ambiente Principais

```env
# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost:5432/logiflow

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Segurança
SECRET_KEY=sua-chave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_PREFIX=/api
API_VERSION=v1
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Integrações (opcionais)
FOCUS_NFE_TOKEN=
MERCADOPAGO_ACCESS_TOKEN=
GOOGLE_MAPS_API_KEY=
MELHOR_ENVIO_TOKEN=
EVOLUTION_API_URL=
EVOLUTION_API_KEY=
```

---

## ☁ Deploy

### Render.com (Recomendado)

O projeto inclui `render.yaml` configurado para deploy completo:

```bash
# O blueprint inclui:
# - Backend FastAPI (logiflow-api)
# - Frontend CRM (logiflowcrm)
# - App Motorista (logiflow-app-motorista)
# - Portal Cliente (logiflow-portal-cliente)
# - Site Divulgação (logiflow-site)
# - PostgreSQL Database
# - Redis Cache
```

1. Conecte seu repositório ao Render.com
2. Selecione "Blueprint" e aponte para `render.yaml`
3. Configure as variáveis de ambiente
4. Deploy!

### Docker Production

```bash
docker-compose -f docker-compose.production.yml up -d
```

---

## 🔌 Integrações

| Integração | Status | Descrição |
|------------|--------|-----------|
| **Focus NFe** | ✅ Implementado | Emissão de CT-e e MDF-e |
| **MercadoPago** | ✅ Implementado | Pagamentos e assinaturas |
| **Google Maps** | ✅ Implementado | Geocoding e rotas |
| **Melhor Envio** | ✅ Implementado | Cotações multi-transportadora |
| **WhatsApp (Evolution)** | ✅ Implementado | Notificações automáticas |
| **Omie ERP** | ✅ Implementado | Sincronização completa |
| **Bling ERP** | ✅ Implementado | Sincronização completa |
| **Tiny ERP** | ✅ Implementado | Sincronização completa |
| **Sascar GPS** | ✅ Implementado | Rastreamento em tempo real |
| **Autotrac GPS** | ✅ Implementado | Rastreamento em tempo real |
| **Onixsat GPS** | ✅ Implementado | Rastreamento em tempo real |

---

## 📚 API Reference

A API segue padrões REST e está documentada via OpenAPI/Swagger.

**Endpoints principais:**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/auth/login` | Autenticação |
| `GET` | `/api/v1/cotacoes` | Listar cotações |
| `POST` | `/api/v1/cotacoes` | Criar cotação |
| `GET` | `/api/v1/pedidos` | Listar pedidos |
| `POST` | `/api/v1/fiscal/cte/emitir` | Emitir CT-e |
| `GET` | `/api/v1/gps/posicoes` | Posições GPS |
| `GET` | `/api/v1/dashboard/metrics` | Métricas dashboard |

**Documentação interativa:** `http://localhost:8000/api/v1/docs`

---

## 📖 Documentação

| Documento | Descrição |
|-----------|-----------|
| [Guia de Configuração GPS](LogiFlow%20CRM/COMO_CONFIGURAR_GPS.md) | Setup de rastreadores |
| [Configuração de Integrações](LogiFlow%20CRM/COMO_CONFIGURAR_INTEGRACOES.md) | ERPs e APIs externas |
| [Configuração Melhor Envio](LogiFlow%20CRM/COMO_CONFIGURAR_MELHOR_ENVIO.md) | Cotações de frete |
| [Deploy Render](LogiFlow%20CRM/DEPLOY_RENDER.md) | Deploy em produção |
| [Docker Stack](LogiFlow%20CRM/DOCKER_STACK_COMPLETO.md) | Infraestrutura Docker |
| [Sistema de Permissões](LogiFlow%20CRM/SISTEMA_PERMISSOES_PLANOS.md) | RBAC e planos |

---

## 🧪 Testes

```bash
cd LogiFlow\ CRM/backend

# Instalar dependências de teste
pip install -r requirements-test.txt

# Executar testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html
```

---

## 📊 Planos e Preços

| Plano | Usuários | Cotações/mês | CT-e/mês | Recursos |
|-------|----------|--------------|----------|----------|
| **Starter** | 3 | 100 | 50 | CRM + TMS básico |
| **Professional** | 10 | 500 | 200 | + Fiscal + GPS |
| **Enterprise** | Ilimitado | Ilimitado | Ilimitado | + API + Suporte dedicado |

---

## 🤝 Contribuição

Este é um projeto proprietário. Para contribuições ou parcerias, entre em contato.

---

## 📄 Licença

**Projeto Proprietário** - Todos os direitos reservados.

© 2024-2025 LogiFlow CRM

---

<div align="center">

### 🚛 LogiFlow CRM

**Sua transportadora no controle. Do comercial à entrega.**

[Website](https://logiflow-site.onrender.com) • [Documentação](LogiFlow%20CRM/docs/) • [Suporte](mailto:suporte@logiflow.com.br)

</div>
