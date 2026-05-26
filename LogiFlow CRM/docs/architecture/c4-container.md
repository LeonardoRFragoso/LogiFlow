# LogiFlow CRM - C4 Model: Container Diagram (Nível 2)

> **Versão:** 1.0.0  
> **Atualizado:** Janeiro 2026

## Descrição

O Diagrama de Containers mostra os containers (aplicações, serviços, bancos de dados) que compõem o sistema LogiFlow CRM e como eles se comunicam.

---

## Diagrama Principal

```mermaid
C4Container
    title LogiFlow CRM - Diagrama de Containers

    Person(operador, "Operador", "Usuário do CRM")
    Person(motorista, "Motorista", "Usuário mobile")
    Person(cliente, "Cliente", "Acompanha entregas")

    Container_Boundary(logiflow, "LogiFlow CRM") {
        Container(frontend, "CRM Frontend", "Vue.js 3, Vite, TailwindCSS", "Interface principal do CRM")
        Container(app_motorista, "App Motorista", "Vue.js PWA", "Aplicativo para motoristas")
        Container(portal_cliente, "Portal Cliente", "Vue.js", "Portal de acompanhamento")
        Container(site, "Site Divulgação", "Vue.js", "Landing page institucional")
        
        Container(api, "API Backend", "FastAPI, Python 3.11", "API REST principal com regras de negócio")
        Container(celery_worker, "Celery Worker", "Celery, Python", "Processamento de tarefas assíncronas")
        Container(celery_beat, "Celery Beat", "Celery, Python", "Agendador de tarefas periódicas")
        
        ContainerDb(postgres, "PostgreSQL", "PostgreSQL 15", "Banco de dados principal")
        ContainerDb(redis, "Redis", "Redis 7", "Cache e message broker")
    }

    System_Ext(whatsapp, "WhatsApp API", "Mensageria")
    System_Ext(mercadopago, "MercadoPago", "Pagamentos")
    System_Ext(focusnfe, "Focus NFe", "Fiscal")
    System_Ext(maps, "Google Maps", "Mapas")

    Rel(operador, frontend, "Usa", "HTTPS")
    Rel(motorista, app_motorista, "Usa", "HTTPS")
    Rel(cliente, portal_cliente, "Usa", "HTTPS")
    
    Rel(frontend, api, "Consome", "REST/JSON")
    Rel(app_motorista, api, "Consome", "REST/JSON")
    Rel(portal_cliente, api, "Consome", "REST/JSON")
    Rel(site, api, "Consome", "REST/JSON")
    
    Rel(api, postgres, "Lê/Escreve", "SQL")
    Rel(api, redis, "Cache/Pub-Sub", "Redis Protocol")
    Rel(celery_worker, redis, "Consome tarefas", "Redis Protocol")
    Rel(celery_worker, postgres, "Lê/Escreve", "SQL")
    Rel(celery_beat, redis, "Agenda tarefas", "Redis Protocol")
    
    Rel(api, whatsapp, "Envia mensagens", "REST")
    Rel(api, mercadopago, "Pagamentos", "REST")
    Rel(api, focusnfe, "Documentos fiscais", "REST")
    Rel(api, maps, "Geocodificação", "REST")

    UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="1")
```

---

## Visão Detalhada (Flowchart)

```mermaid
flowchart TB
    subgraph Clients["🖥️ Aplicações Cliente"]
        FE["🌐 CRM Frontend<br/>━━━━━━━━━━━━━━<br/>Vue.js 3 + Vite<br/>TailwindCSS<br/>Pinia + Vue Router<br/>━━━━━━━━━━━━━━<br/>Port: 3001"]
        
        APP["📱 App Motorista<br/>━━━━━━━━━━━━━━<br/>Vue.js PWA<br/>GPS Tracking<br/>━━━━━━━━━━━━━━<br/>Port: 3002"]
        
        PORTAL["👤 Portal Cliente<br/>━━━━━━━━━━━━━━<br/>Vue.js<br/>Tracking público<br/>━━━━━━━━━━━━━━<br/>Port: 3003"]
        
        SITE["🏢 Site Divulgação<br/>━━━━━━━━━━━━━━<br/>Vue.js<br/>Landing Page<br/>━━━━━━━━━━━━━━<br/>Port: 5173"]
    end

    subgraph Backend["⚙️ Backend Services"]
        API["🚀 FastAPI Backend<br/>━━━━━━━━━━━━━━<br/>Python 3.11<br/>Uvicorn ASGI<br/>SQLAlchemy 2.0<br/>Pydantic v2<br/>━━━━━━━━━━━━━━<br/>Port: 8000"]
        
        WORKER["⚡ Celery Worker<br/>━━━━━━━━━━━━━━<br/>Tarefas Async<br/>• E-mails<br/>• WhatsApp<br/>• Relatórios"]
        
        BEAT["⏰ Celery Beat<br/>━━━━━━━━━━━━━━<br/>Scheduler<br/>• NPS automático<br/>• Alertas<br/>• Limpeza cache"]
    end

    subgraph Data["💾 Data Layer"]
        PG[("🐘 PostgreSQL 15<br/>━━━━━━━━━━━━━━<br/>Banco Principal<br/>Multi-tenant<br/>Alembic Migrations<br/>━━━━━━━━━━━━━━<br/>Port: 5432")]
        
        RD[("🔴 Redis 7<br/>━━━━━━━━━━━━━━<br/>Cache + Broker<br/>Rate Limiting<br/>Session Store<br/>━━━━━━━━━━━━━━<br/>Port: 6379")]
    end

    subgraph External["🌐 APIs Externas"]
        WA["📱 WhatsApp"]
        MP["💳 MercadoPago"]
        NFE["📄 Focus NFe"]
        MAPS["🗺️ Google Maps"]
        ME["📦 Melhor Envio"]
        SMTP["📧 SMTP"]
    end

    FE & APP & PORTAL & SITE -->|"REST/JSON<br/>HTTPS"| API
    
    API -->|"SQLAlchemy<br/>asyncpg"| PG
    API -->|"redis-py<br/>Cache"| RD
    
    API -->|"Enqueue"| RD
    RD -->|"Consume"| WORKER
    WORKER -->|"SQL"| PG
    
    BEAT -->|"Schedule"| RD
    
    API & WORKER -->|"REST"| WA & MP & NFE & MAPS & ME
    API & WORKER -->|"SMTP"| SMTP

    style API fill:#1168bd,stroke:#0b4884,color:#fff
    style PG fill:#336791,stroke:#1a3d5c,color:#fff
    style RD fill:#dc382d,stroke:#a02a23,color:#fff
```

---

## Descrição dos Containers

### Aplicações Frontend

| Container | Tecnologia | Porta | Descrição |
|-----------|------------|-------|-----------|
| **CRM Frontend** | Vue.js 3, Vite, TailwindCSS | 3001 | Interface principal do CRM para operadores |
| **App Motorista** | Vue.js PWA | 3002 | Aplicativo progressivo para motoristas com GPS |
| **Portal Cliente** | Vue.js | 3003 | Portal de rastreamento para clientes finais |
| **Site Divulgação** | Vue.js | 5173 | Landing page institucional com formulário de contato |

### Serviços Backend

| Container | Tecnologia | Porta | Descrição |
|-----------|------------|-------|-----------|
| **API Backend** | FastAPI, Python 3.11, Uvicorn | 8000 | API REST principal com todas as regras de negócio |
| **Celery Worker** | Celery 5.3, Python | - | Processador de tarefas assíncronas (e-mails, WhatsApp) |
| **Celery Beat** | Celery Beat | - | Agendador de tarefas periódicas (NPS, alertas) |

### Data Stores

| Container | Tecnologia | Porta | Descrição |
|-----------|------------|-------|-----------|
| **PostgreSQL** | PostgreSQL 15 Alpine | 5432 | Banco de dados relacional principal |
| **Redis** | Redis 7 Alpine | 6379 | Cache, rate limiting e message broker |

---

## Comunicação Entre Containers

### Protocolos Internos

```
Frontend Apps → API Backend
├── Protocolo: HTTPS (REST)
├── Formato: JSON
├── Autenticação: JWT Bearer Token
└── Headers: X-Tenant-ID, X-Correlation-ID

API Backend → PostgreSQL
├── Protocolo: PostgreSQL Wire Protocol
├── Driver: asyncpg / psycopg2
├── Pool: SQLAlchemy connection pool
└── Isolation: Read Committed

API Backend → Redis
├── Protocolo: Redis Protocol
├── Driver: redis-py
├── Uso: Cache, Rate Limit, Pub/Sub
└── Databases: 0 (Celery), 1 (Cache)

Celery Worker ↔ Redis
├── Protocolo: Redis Protocol
├── Padrão: Producer/Consumer
└── Serialization: JSON
```

### Fluxo de Requisições

```mermaid
sequenceDiagram
    participant U as Usuário
    participant FE as Frontend
    participant API as FastAPI
    participant RD as Redis
    participant PG as PostgreSQL
    participant CW as Celery Worker
    
    U->>FE: Ação no sistema
    FE->>API: REST Request + JWT
    API->>RD: Check rate limit
    RD-->>API: OK
    API->>RD: Check cache
    alt Cache hit
        RD-->>API: Cached data
    else Cache miss
        API->>PG: Query
        PG-->>API: Result
        API->>RD: Set cache
    end
    API-->>FE: JSON Response
    
    Note over API,CW: Tarefas Assíncronas
    API->>RD: Enqueue task
    CW->>RD: Dequeue task
    CW->>PG: Process & Save
```

---

## Configuração Docker

### docker compose -f docker/docker-compose.yml (Resumo)

```yaml
services:
  db:           # PostgreSQL 15 Alpine
  redis:        # Redis 7 Alpine
  api:          # FastAPI Backend
  frontend:     # Vue.js CRM
  site:         # Vue.js Landing Page
  celery_worker: # Celery Worker
  celery_beat:  # Celery Beat Scheduler
  adminer:      # DB Admin (dev only)
```

### Volumes Persistentes

| Volume | Container | Caminho |
|--------|-----------|---------|
| `postgres_data` | db | `/var/lib/postgresql/data` |
| `redis_data` | redis | `/data` |
| `static_volume` | api | `/app/staticfiles` |
| `media_volume` | api | `/app/media` |

### Rede

```
Network: logiflow_network (bridge)
├── db (postgres)
├── redis
├── api
├── frontend
├── site
├── celery_worker
└── celery_beat
```

---

## Escalabilidade

### Horizontal Scaling

| Container | Escalável | Estratégia |
|-----------|-----------|------------|
| API Backend | ✅ Sim | Load Balancer + múltiplas instâncias |
| Celery Worker | ✅ Sim | Múltiplos workers por fila |
| Frontend | ✅ Sim | CDN + múltiplas instâncias |
| PostgreSQL | ⚠️ Limitado | Read replicas |
| Redis | ⚠️ Limitado | Redis Cluster |

### Resource Limits (Recomendado)

| Container | CPU | Memory |
|-----------|-----|--------|
| API | 1-2 cores | 512MB-1GB |
| Celery Worker | 0.5-1 core | 256MB-512MB |
| PostgreSQL | 2-4 cores | 2GB-4GB |
| Redis | 0.5 core | 256MB |
| Frontend | 0.25 core | 128MB |

---

## Health Checks

| Container | Endpoint/Comando | Intervalo |
|-----------|------------------|-----------|
| API | `GET /health` | 15s |
| PostgreSQL | `pg_isready` | 10s |
| Redis | `redis-cli ping` | 10s |
| Celery Worker | `celery inspect ping` | 30s |

---

*Documento parte da documentação arquitetural do LogiFlow CRM - Modelo C4*
