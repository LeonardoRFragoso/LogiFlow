# LogiFlow CRM

> CRM SaaS especializado para Transportadoras e Logística, baseado em SuiteCRM

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)
![PHP](https://img.shields.io/badge/PHP-8.1-purple)
![Python](https://img.shields.io/badge/Python-3.11-green)

## 📋 Visão Geral

LogiFlow CRM é uma plataforma completa para gestão de transportadoras, integrando:

- **CRM Comercial**: Cotações, clientes, funil de vendas
- **Operacional**: Pedidos de frete, entregas, rastreamento
- **Frota**: Motoristas, veículos, manutenções
- **Fiscal**: Emissão de CT-e/MDF-e integrada
- **Financeiro**: Faturamento, custos, lucratividade

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                         NGINX                                │
│                    (Proxy/Load Balancer)                     │
└─────────────────┬───────────────────────┬───────────────────┘
                  │                       │
         ┌────────▼────────┐     ┌────────▼────────┐
         │    SuiteCRM     │     │    FastAPI      │
         │   (PHP-FPM)     │     │   (Python)      │
         │                 │     │                 │
         │  - Módulos CRM  │     │  - Auth/JWT     │
         │  - API V8       │     │  - Billing      │
         │  - Workflows    │     │  - Integrações  │
         └────────┬────────┘     └────────┬────────┘
                  │                       │
         ┌────────▼───────────────────────▼────────┐
         │              MariaDB + Redis             │
         └─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Pré-requisitos

- Docker & Docker Compose
- Git

### Instalação

```bash
# Clonar repositório
git clone https://github.com/sua-empresa/logiflow-crm.git
cd logiflow-crm

# Configurar ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Iniciar ambiente de desenvolvimento
./scripts/setup_dev.sh

# Ou manualmente:
docker compose up -d
```

### Acessos

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| SuiteCRM | http://localhost | Configurar na instalação |
| API Docs | http://localhost:8000/docs | - |
| Adminer | http://localhost:8080 | root / (ver .env) |

## 📁 Estrutura do Projeto

```
logiflow-crm/
├── docker/                    # Configurações Docker
│   ├── api/                   # Dockerfile FastAPI
│   ├── suitecrm/              # Dockerfile PHP-FPM
│   └── nginx/                 # Configurações Nginx
├── backend/                   # API Python (FastAPI)
│   ├── routers/               # Endpoints da API
│   ├── integrations/          # Integrações externas
│   └── worker.py              # Celery tasks
├── suitecrm/                  # SuiteCRM (montado via volume)
│   └── custom/                # Customizações
│       ├── modules/           # Módulos custom
│       ├── themes/            # Tema LogiFlow
│       └── Extension/         # Extensões
├── scripts/                   # Scripts de automação
├── tenants/                   # Credenciais de tenants (git ignored)
├── backups/                   # Backups locais (git ignored)
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Módulos Custom

| Módulo | Descrição |
|--------|-----------|
| `Cotacoes` | Propostas comerciais de frete |
| `PedidosFrete` | Pedidos confirmados |
| `Entregas` | Rastreamento de entregas |
| `Motoristas` | Cadastro de motoristas |
| `Veiculos` | Gestão de frota |
| `Ocorrencias` | Registro de problemas |

## 📡 API Endpoints

### Autenticação
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Renovar token

### Operacional
- `GET /api/cotacoes` - Listar cotações
- `POST /api/cotacoes` - Criar cotação
- `PATCH /api/cotacoes/{id}/aprovar` - Aprovar cotação
- `GET /api/pedidos` - Listar pedidos
- `GET /api/entregas/ativas` - Entregas em andamento

### Tenants (Admin)
- `GET /api/tenants` - Listar tenants
- `POST /api/tenants` - Provisionar novo tenant

## 🔐 Segurança

- Autenticação via JWT (API) e OAuth2 (SuiteCRM)
- HTTPS obrigatório em produção
- Rate limiting configurado no Nginx
- Senhas hasheadas com bcrypt
- Isolamento de dados por tenant (DB separado)

## 📊 Monitoramento

- **Health Check**: `GET /health`
- **Logs**: `docker compose logs -f`
- **Métricas**: Prometheus (configurar)
- **Erros**: Sentry (configurar DSN no .env)

## 🛠️ Comandos Úteis

```bash
# Ver logs
docker compose logs -f api

# Acessar container
docker compose exec api bash

# Reiniciar serviço
docker compose restart suitecrm

# Backup de tenant
./scripts/backup_tenant.sh nome-tenant

# Provisionar novo tenant
./scripts/provision_tenant.sh nome-tenant email@empresa.com
```

## 📅 Roadmap

- [x] Infraestrutura Docker
- [x] API FastAPI base
- [ ] Módulos SuiteCRM completos
- [ ] Integração CT-e (Focus NFe)
- [ ] App motorista (PWA)
- [ ] Portal do cliente
- [ ] Dashboard operacional
- [ ] Integração WhatsApp

## 📄 Licença

Software proprietário - LogiFlow CRM © 2024

## 📞 Suporte

- Email: suporte@logiflow.com.br
- Docs: https://docs.logiflow.com.br
