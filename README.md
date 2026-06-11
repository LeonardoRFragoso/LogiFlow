# 🚛 LogiFlow CRM

<div align="center">

[![CI](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/ci.yml)
[![CD](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/cd.yml/badge.svg)](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/cd.yml)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

**SaaS enterprise para transportadoras: CRM + TMS + fiscal + GPS — 60-70% mais acessível que concorrentes**

[🌐 Acessar Sistema](https://logi-flow-wuhp.vercel.app) • [📖 Documentação](LogiFlow%20CRM/docs/) • [🚀 Quick Start](#-quick-start)

</div>

---

## 🎯 Problema que Resolve

Transportadoras enfrentam desafios diários na gestão de operações logísticas:
- Cotações manuais e demoradas
- Falta de visibilidade sobre entregas em andamento
- Comunicação fragmentada com clientes e motoristas
- Dificuldade no controle financeiro e fiscal

O **LogiFlow CRM** centraliza todas essas operações em uma plataforma única, moderna e escalável — sendo 60-70% mais acessível que soluções enterprise tradicionais.

---

## ✨ Funcionalidades Principais

| Módulo | Descrição |
|--------|-----------|
| **CRM** | Gestão comercial completa com cotações e pedidos |
| **TMS** | Controle de frota e rastreamento GPS em tempo real |
| **Fiscal** | Emissão de CT-e / MDF-e via Focus NFe + integração SEFAZ |
| **ERP** | Integração com Omie, Bling e Tiny |
| **App Motorista** | PWA offline-first para motoristas em rota |
| **Portal Cliente** | Acompanhamento de entregas em tempo real |
| **Multi-tenant** | Suporte a múltiplas transportadoras com isolamento de dados |
| **Notificações** | WhatsApp e e-mail automáticos |
| **NPS / CSAT** | Pesquisas de satisfação integradas |

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND (Vue.js 3 + TailwindCSS)               │
│      CRM Principal  │  App Motorista  │  Portal Cliente      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│    Presentation → Application → Domain ← Infrastructure     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │PostgreSQL│    │  Redis   │    │  Celery  │
       └──────────┘    └──────────┘    └──────────┘
```

**Stack Técnica:**

| Camada | Tecnologias |
|--------|-------------|
| **Backend** | FastAPI, SQLAlchemy, Pydantic, Celery |
| **Frontend** | Vue.js 3, Vite, Pinia, TailwindCSS |
| **Database** | PostgreSQL 15 |
| **Cache** | Redis 7 |
| **Infraestrutura** | Docker, GitHub Actions, Render.com |

---

## 🚀 Quick Start

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+

### Instalação

```bash
# Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd LogiFlow/"LogiFlow CRM"

# Configure o ambiente
cp backend/.env.example .env

# Inicie os containers
docker compose -f docker/docker-compose.yml up -d
```

**Acesso após iniciar:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/v1/docs

---

## 📁 Estrutura do Repositório

```
LogiFlow/
├── LogiFlow CRM/          # Aplicação principal
│   ├── backend/           # FastAPI — Clean Architecture
│   ├── frontend/          # Vue.js 3 — CRM e admin
│   ├── app-motorista/     # PWA offline para motoristas
│   ├── portal-cliente/    # Portal de rastreamento
│   ├── site-divulgacao/   # Site institucional
│   ├── docker/            # Docker Compose
│   └── docs/              # Documentação técnica completa
├── helm/                  # Kubernetes Helm charts
└── tasks/                 # Automações e scripts
```

---

## 📚 Documentação

Toda a documentação está em [`LogiFlow CRM/docs/`](LogiFlow%20CRM/docs/):

| Documento | Descrição |
|-----------|-----------|
| [API Endpoints](LogiFlow%20CRM/docs/api/endpoints.md) | Referência completa da API |
| [Architecture](LogiFlow%20CRM/docs/architecture/layers.md) | Clean Architecture |
| [ADRs](LogiFlow%20CRM/docs/adr/README.md) | Decisões arquiteturais |
| [Deploy](LogiFlow%20CRM/docs/deployment/production.md) | Guia de produção |
| [Security](LogiFlow%20CRM/docs/security/owasp-checklist.md) | Checklist OWASP |

---

## 🔒 Segurança

- ✅ Input validation com Pydantic
- ✅ Prevenção de SQL Injection (SQLAlchemy ORM)
- ✅ Rate limiting
- ✅ Autenticação JWT
- ✅ Isolamento multi-tenant
- ✅ Gerenciamento de segredos

---

## 🧪 Testes

```bash
cd "LogiFlow CRM"

# Testes unitários
pytest tests/unit -v

# Testes de integração
pytest tests/integration -v

# Coverage
pytest --cov=. --cov-report=html
```

---

## 📄 Licença

MIT — veja [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Leonardo Fragoso**

- GitHub: [@LeonardoRFragoso](https://github.com/LeonardoRFragoso)
- LinkedIn: [linkedin.com/in/leonardo-fragoso-921b166a](https://www.linkedin.com/in/leonardo-fragoso-921b166a/)
- Portfolio: [leonardofragosodev.netlify.app](https://leonardofragosodev.netlify.app/)

---

<div align="center">

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>
