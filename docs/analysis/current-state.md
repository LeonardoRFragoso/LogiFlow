# Estado Atual do Projeto (Current State)

> Data da análise: 2026-01-26

## 1. Visão Geral

O repositório está organizado como um **monorepo** contendo:

- Um **backend** em **Python/FastAPI** (`LogiFlow CRM/backend`)
- Múltiplos **frontends** em **Vue 3 + Vite**:
  - CRM principal (`LogiFlow CRM/frontend`)
  - App motorista (PWA) (`LogiFlow CRM/app-motorista`)
  - Portal do cliente (`LogiFlow CRM/portal-cliente`)
  - Site de divulgação (`LogiFlow CRM/site-divulgacao`)
- Infra de desenvolvimento/produção com **Docker Compose** e deploy via **Render.com** (`render.yaml`)

O backend atua como um **orquestrador** com módulos de:

- Autenticação (JWT + refresh token)
- Multi-tenancy
- Billing (MercadoPago)
- Fiscal (CT-e / MDF-e via Focus NFe)
- Operacional (cotações/pedidos/entregas/rastreamento)
- Integrações (ERP, WhatsApp/Evolution, GPS, Maps)
- Jobs (Celery + scheduler)

---

## 2. Componentes / Módulos Principais

### 2.1 Backend (FastAPI)

**Entrypoint:** `LogiFlow CRM/backend/main.py`

- **`routers/`**
  - Camada de apresentação HTTP: definição de endpoints, schemas Pydantic, tratamento de erros.
  - Observação: vários routers possuem **“storage simulado” em memória** (dicionários globais).

- **`services/`**
  - Implementações de regras e integrações de aplicação.
  - Exemplos: `mercadopago_service.py`, `integration_manager.py`, `fiscal_service.py`, `whatsapp_service.py`, `scheduler.py`, `encryption_service.py`.

- **`integrations/`**
  - Clientes/SDKs para sistemas externos (ex.: FocusNFe, ERPs, GPS, Maps).

- **`middleware/`**
  - `TenantMiddleware` (multi-tenancy)
  - `RateLimitMiddleware`
  - `correlation_middleware` (correlation id)
  - `rbac.py` (RBAC + auditoria)

- **`database.py` / `models.py` / `models/`**
  - Configuração de engine SQLAlchemy e modelos.
  - Migrações: `alembic/`.

### 2.2 Frontends (Vue)

- **CRM principal:** SPA administrativa.
- **App motorista:** PWA com Pinia.
- **Portal do cliente:** tracking.
- **Site divulgação:** landing page.

### 2.3 Infra / Deploy

- **Docker Compose local:** `LogiFlow CRM/docker-compose.yml`
  - MariaDB + Redis + API + 2 frontends + worker + beat
- **Render Blueprint:** `render.yaml`
  - Backend + 4 sites estáticos + Redis + Postgres

---

## 3. Dependências entre Módulos (Mapa de Dependência)

### 3.1 Fluxo técnico (alto nível)

- `main.py`
  - carrega `settings` (`config.py`)
  - inicializa `init_db()` (`database.py`)
  - injeta middlewares (`middleware/*`)
  - registra rotas (módulos de `routers/*`)

- `routers/*`
  - dependem de `config.py` (settings), `database.py` (get_db), `models/*` e, em alguns casos, `services/*` e `integrations/*`.

- `services/*`
  - dependem de `integrations/*` (clientes externos), `config.py` (chaves/config), e possivelmente `database.py`/models.

### 3.2 Dependências externas relevantes

- Focus NFe (CT-e/MDF-e)
- MercadoPago (billing)
- Redis (cache/broker)
- Evolution API (WhatsApp)
- ERPs (Omie/Bling/Tiny)
- Maps
- GPS (Sascar/Autotrac/Onixsat)

---

## 4. Tecnologias e Versões (observadas no repositório)

### 4.1 Backend

- **Python:** `3.11.7` (arquivo `backend/runtime.txt`)
- **FastAPI:** `>=0.104.0`
- **Uvicorn:** `>=0.24.0`
- **Pydantic:** `>=2.5.0`
- **SQLAlchemy:** `>=2.0.0`
- **Alembic:** `>=1.12.0`
- **Redis client:** `>=5.0.0`
- **Celery:** `>=5.3.0`
- **APScheduler:** `>=3.10.0`
- **JWT/Auth:** `python-jose`, `PyJWT`, `passlib[bcrypt]`
- **HTTP Clients:** `httpx`, `requests`

### 4.2 Frontend

- **CRM principal (`frontend/package.json`)**
  - Vue: `^3.4.0`
  - Vite: `^5.0.10`
  - Tailwind: `^3.4.0`
  - Pinia: `^2.1.7`

- **App motorista / Portal cliente / Site divulgação**
  - Vue: `^3.5.24`
  - Vite: `^7.2.4`
  - Tailwind: `^3.4.19` (app/portal) e `^4.1.18` (site)

> Observação: há **inconsistência de versões** (Vue/Vite/Tailwind) entre os frontends.

### 4.3 Infra

- **Docker Compose local**
  - MariaDB: `10.6`
  - Redis: `7-alpine`
  - Nginx (frontends)

- **Render Blueprint**
  - Redis (managed)
  - PostgreSQL (managed)

---

## 5. Fluxos Críticos de Negócio (mapeamento inicial)

### 5.1 Autenticação (login + refresh)

- Endpoint: `POST /api/v1/auth/login`
- Implementação: `routers/auth.py`
  - Verifica credenciais via SQLAlchemy (`User`)
  - Gera access token JWT + refresh token persistido (`RefreshToken`)

### 5.2 Multi-tenancy (resolução de tenant)

- Middleware: `middleware/tenant.py`
  - Resolve tenant por JWT claim `tenant_id` (preferido)
  - Fallback: subdomínio
  - Fallback: header `X-Tenant-ID`
  - Validação atual do tenant é **mockada** (retorna dict fixo)

### 5.3 Operacional: Cotações → Pedidos

- `routers/cotacoes.py`
  - CRUD e workflow (rascunho → enviada → aprovada → convertida)
  - Persistência atual: **`cotacoes_db` em memória**

- `routers/pedidos.py`
  - CRUD e workflow de status de transporte
  - Persistência atual: **`pedidos_db` em memória** (+ seed opcional)

> Observação: o fluxo “aprovar cotação cria pedido” está como TODO (criação simulada).

### 5.4 Fiscal: Emissão CT-e / MDF-e

- `routers/fiscal.py`
  - Emissão/consulta/cancelamento/download PDF/XML
  - Integração: `integrations/fiscal/focusnfe.py`
  - Suporte a credenciais por tenant via `services/integration_manager.py` (referenciado)

---

## 6. Code Smells e Anti-patterns (principais achados)

### 6.1 Persistência “simulada” em memória em módulos de negócio

- `routers/cotacoes.py`, `routers/pedidos.py` e outros: uso de dicionários globais como “DB”.
- Riscos:
  - perda de dados ao reiniciar
  - comportamento inconsistente em múltiplas instâncias (escala horizontal)
  - dificulta testes de integração e observabilidade

### 6.2 Mistura de responsabilidades (routers fazendo regras de negócio)

- Muitos routers contêm:
  - validação
  - regras de domínio
  - persistência (mesmo que simulada)
  - formatação de resposta

Isso indica necessidade de **separação por camadas** (presentation/application/domain/infrastructure).

### 6.3 Inconsistência de banco/URL de banco

- `backend/database.py` e `config.get_database_url()` constroem **MySQL + PyMySQL**.
- `render.yaml` provisiona **PostgreSQL**.
- `docker-compose.yml` usa **MariaDB**.

Risco: ambiente de deploy divergir do ambiente local, e migrations/queries quebrarem em produção.

### 6.4 Segurança: defaults perigosos e comportamento em import

- `SECRET_KEY` tem default fraco e aparece também em `docker-compose.yml` com placeholder tipo “django-insecure...”.
- `routers/auth.py` cria usuário admin **durante import** (`_criar_usuario_admin()`), o que:
  - gera side-effects em import
  - dificulta testes e previsibilidade
  - pode ser inseguro/indesejado em produção

### 6.5 Multi-tenancy incompleto / mock

- `TenantMiddleware._validate_tenant()` retorna mock e não valida no banco.
- Isso compromete isolamento real por tenant.

### 6.6 Inconsistência de bibliotecas JWT

- `routers/auth.py` usa `jose.jwt`.
- `middleware/tenant.py` usa `jwt` (PyJWT).

Risco: divergências de validação/claims/algoritmos.

### 6.7 Possíveis bugs por tipagem/uso de ORM

- Em `routers/auth.py`, `get_current_admin()` usa `current_user["tipo"]` como se fosse dict, mas `current_user` é um objeto ORM `User`.
- Em `routers/fiscal.py`, há `from auth import get_current_user` (parece um import incorreto; o módulo está em `routers/auth.py`).

---

## 7. Pontos de Atenção para Refatoração (prioridades)

- Definir **uma arquitetura alvo** (Clean Architecture / layered) antes de mover código.
- Consolidar decisão de **banco de dados** (PostgreSQL vs MySQL/MariaDB) e alinhar:
  - `config.py`/`database.py`
  - docker-compose
  - render.yaml
  - migrations
- Migrar gradualmente routers “stateful” para:
  - `application` (use cases)
  - `domain` (entidades/regras)
  - `infrastructure` (repos + integrações)
- Padronizar autenticação e tenant:
  - um único mecanismo JWT
  - tenant id como claim obrigatório em rotas autenticadas
- Reduzir side-effects em import (criação de admin/seed)
- Padronizar versões dos frontends (Vue/Vite/Tailwind) para facilitar CI/CD.

---

## 8. Próximos Passos (conforme sua Fase 1)

- Fase 1.2: gerar diagramas C4 e data-flow com Mermaid com base nos componentes acima.
- Fase 1.3: formalizar ADRs (backend FastAPI, DB, auth, patterns, estrutura de pastas).
- Fase 1.4/1.5: iniciar refatoração incremental com Repository/DTO/DI/Strategy/Factory, priorizando módulos críticos (auth, tenants, fiscal, billing).
