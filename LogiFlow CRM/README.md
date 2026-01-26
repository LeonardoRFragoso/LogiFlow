# LogiFlow CRM

[![CI](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/ci.yml)
[![CD](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/cd.yml/badge.svg)](https://github.com/LeonardoRFragoso/LogiFlow/actions/workflows/cd.yml)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg)](https://vuejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> Sistema de CRM especializado para transportadoras, com gestão completa de cotações, pedidos, entregas e rastreamento GPS em tempo real.

## 🎯 Problema que Resolve

Transportadoras enfrentam desafios diários na gestão de operações logísticas:
- Cotações manuais e demoradas
- Falta de visibilidade sobre entregas em andamento
- Comunicação fragmentada com clientes e motoristas
- Dificuldade no controle financeiro e fiscal

O **LogiFlow CRM** centraliza todas essas operações em uma plataforma única, moderna e escalável.

## ✨ Features Principais

- ✅ **Gestão de Cotações** - Cotações automatizadas com múltiplas opções de frete
- ✅ **Controle de Pedidos** - Workflow completo do pedido à entrega
- ✅ **Rastreamento GPS** - Localização em tempo real dos motoristas
- ✅ **Multi-tenancy** - Suporte a múltiplas transportadoras isoladas
- ✅ **App Motorista** - PWA para motoristas em rota
- ✅ **Portal Cliente** - Acompanhamento de entregas pelos clientes
- ✅ **Integração Fiscal** - Emissão de CT-e e MDF-e via Focus NFe
- ✅ **Pagamentos** - Integração com MercadoPago
- ✅ **Notificações** - WhatsApp e Email automáticos
- ✅ **NPS & CSAT** - Pesquisas de satisfação

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (Vue.js 3)                      │
│         CRM  │  App Motorista  │  Portal Cliente            │
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
- **Backend:** FastAPI, SQLAlchemy, Pydantic, Celery
- **Frontend:** Vue.js 3, Vite, Pinia, TailwindCSS
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **Infrastructure:** Docker, GitHub Actions, Render.com

📖 [Documentação de Arquitetura](docs/architecture/layers.md)

## 🚀 Quick Start

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+

### Instalação

```bash
# Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd "LogiFlow CRM"

# Configure o ambiente
cp .env.example .env

# Inicie os containers
docker-compose up -d

# Acesse a aplicação
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/v1/docs
```

### Docker

```bash
# Ver logs
docker-compose logs -f api

# Rodar migrations
docker-compose exec api alembic upgrade head

# Rodar testes
docker-compose exec api pytest
```

📖 [Guia Completo de Instalação](docs/deployment/local.md)

## 📚 Documentação

| Documento | Descrição |
|-----------|-----------|
| [API Getting Started](docs/api/getting-started.md) | Quick start da API |
| [API Endpoints](docs/api/endpoints.md) | Referência de endpoints |
| [Architecture](docs/architecture/layers.md) | Clean Architecture |
| [C4 Diagrams](docs/architecture/c4-context.md) | Diagramas C4 |
| [ADRs](docs/adr/README.md) | Decisões arquiteturais |
| [Design Patterns](docs/patterns/README.md) | Padrões implementados |
| [Deployment](docs/deployment/production.md) | Guia de deploy |
| [Security](docs/security/owasp-checklist.md) | Checklist OWASP |
| [CI/CD](docs/guides/ci-cd.md) | Pipeline de CI/CD |
| [Observability](docs/observability/monitoring.md) | Logs, métricas, alertas |

## 🧪 Testes

```bash
# Testes unitários
pytest tests/unit -v

# Testes de integração
pytest tests/integration -v

# Coverage
pytest --cov=. --cov-report=html
```

## 📊 Design Patterns

Este projeto implementa:

- **Repository Pattern** - Abstração de acesso a dados ([docs](docs/patterns/repository.md))
- **Dependency Injection** - Inversão de controle ([docs](docs/patterns/dependency-injection.md))
- **DTO Pattern** - Transferência de dados ([docs](docs/patterns/dto.md))
- **Factory Pattern** - Criação de objetos ([docs](docs/patterns/factory.md))
- **Strategy Pattern** - Algoritmos intercambiáveis ([docs](docs/patterns/strategy.md))

📖 [Ver todos os ADRs](docs/adr/README.md)

## 🔒 Segurança

- ✅ Input validation (Pydantic)
- ✅ SQL Injection prevention (SQLAlchemy ORM)
- ✅ XSS prevention (Vue.js escaping)
- ✅ CSRF protection
- ✅ Rate limiting
- ✅ JWT authentication
- ✅ Multi-tenant isolation
- ✅ Secrets management

📖 [OWASP Checklist](docs/security/owasp-checklist.md)

## 🚢 Deploy

O projeto está configurado para deploy em **Render.com**:

```bash
# Deploy automático via GitHub Actions
# Push para main → Deploy em produção
# Push para develop → Deploy em staging
```

📖 [Guia de Deploy](docs/deployment/production.md)

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

📖 [Code Standards](docs/development/code-standards.md)

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Leonardo Fragoso**

- Portfolio: [portfolio-leonardo-fragoso-react.vercel.app](https://portfolio-leonardo-fragoso-react.vercel.app/)
- LinkedIn: [linkedin.com/in/leonardo-fragoso-921b166a](https://www.linkedin.com/in/leonardo-fragoso-921b166a/)
- GitHub: [@LeonardoRFragoso](https://github.com/LeonardoRFragoso)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
