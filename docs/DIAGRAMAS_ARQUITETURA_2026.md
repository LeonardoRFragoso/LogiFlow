# 🎨 DIAGRAMAS E VISUALIZAÇÕES - LogiFlow CRM
## Representação Visual da Arquitetura e Fluxos

**Data:** 4 de Março de 2026

---

## 📊 1. Arquitetura em Camadas (Clean Architecture)

```
┌──────────────────────────────────────────────────────────────────────┐
│                          FRONTEND                                     │
│         CRM | App Motorista | Portal Cliente | Site Web             │
│                        (Vue.js 3, PWA)                              │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ HTTPS/REST
┌───────────────────────────▼──────────────────────────────────────────┐
│                    FASTAPI BACKEND                                    │
│                  (Clean Architecture)                                │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │           PRESENTATION LAYER (Camada 4)                      │   │
│  │  🔹 Routers (endpoints HTTP)                                │   │
│  │  🔹 API Validators (Pydantic)                              │   │
│  │  🔹 Middlewares (CORS, Auth, Tenant)                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                            ↑ ↓                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │          APPLICATION LAYER (Camada 3)                        │   │
│  │  🔹 Use Cases (orquestração)                                │   │
│  │  🔹 DTOs (Data Transfer Objects)                            │   │
│  │  🔹 Application Services                                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                            ↑ ↓                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │            DOMAIN LAYER (Camada 2)                           │   │
│  │  🔹 Entities (Cliente, Cotacao, Pedido)                    │   │
│  │  🔹 Value Objects (CNPJ, Email, Endereco)                 │   │
│  │  🔹 Domain Interfaces (IRepository, IService)              │   │
│  │  🔹 Domain Exceptions                                      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                            ↑ ↓                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │         INFRASTRUCTURE LAYER (Camada 1)                      │   │
│  │  🔹 Repository Implementations                              │   │
│  │  🔹 Database Access (SQLAlchemy)                            │   │
│  │  🔹 External API Clients                                    │   │
│  │  🔹 Cache Client (Redis)                                    │   │
│  │  🔹 Dependency Container (DI)                               │   │
│  └──────────────────────────────────────────────────────────────┘   │
└───────────────────────────┬──────────────────────────────────────────┘
                            │
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ PostgreSQL   │    │    Redis     │    │    Celery    │
│  DB          │    │   Cache      │    │   Task Queue │
└──────────────┘    └──────────────┘    └──────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES (Integrações)                          │
│  🔹 WhatsApp API   🔹 MercadoPago   🔹 Focus NFe   🔹 Google Maps   │
│  🔹 Melhor Envio   🔹 SendGrid      🔹 Evolution   🔹 Custom APIs   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 2. Fluxo de Requisição (Request Lifecycle)

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser/App)                      │
│              Makes HTTP Request with JWT Token                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Application                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 1: CORS Middleware                                  │ │
│  │ ✓ Verifica origin da requisição                          │ │
│  │ ✓ Permite solicitações cross-domain                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 2: Correlation Middleware                           │ │
│  │ ✓ Gera/injeta Correlation ID para rastreamento          │ │
│  │ ✓ Adiciona headers de logging                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 3: Tenant Middleware                                │ │
│  │ ✓ Extrai tenant_id do header ou token                    │ │
│  │ ✓ Valida se tenant existe e ativo                        │ │
│  │ ✓ Injeta tenant_id no context da request                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 4: Route Matching                                   │ │
│  │ ✓ Identifica qual router/endpoint vai processar          │ │
│  │ ✓ Ex: GET /api/v1/clientes → clientes.py                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 5: Dependency Injection                             │ │
│  │ ✓ Resolve dependências (Depends)                         │ │
│  │ ✓ Obtém DB session, User, etc via container.py           │ │
│  │ ✓ Injeta como parâmetros da função                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 6: Input Validation (Pydantic)                      │ │
│  │ ✓ Valida body/query params contra DTO schema             │ │
│  │ ✓ Type checking, range validation                        │ │
│  │ ✓ Se inválido: HTTP 422 Unprocessable Entity             │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 7: Authorization Check                              │ │
│  │ ✓ Verifica JWT token                                     │ │
│  │ ✓ Valida role/permissões                                │ │
│  │ ✓ Se falha: HTTP 403 Forbidden                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 8: Handler Execution                                │ │
│  │ ✓ Executa função do router (ex: criar_cliente)          │ │
│  │ ✓ Chama use case correspondente                          │ │
│  │ ✓ Aplica lógica de domínio                               │ │
│  │ ✓ Interage com banco e cache                             │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 9: Response Serialization                           │ │
│  │ ✓ Serializa resposta (DTO → JSON)                        │ │
│  │ ✓ HTTP 200 OK (ou status apropriado)                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ STEP 10: Response Middleware                             │ │
│  │ ✓ Adiciona headers customizados                          │ │
│  │ ✓ Compressão gzip                                        │ │
│  │ ✓ Logging de resposta                                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ HTTP Response   │
                    │ {status: 200,   │
                    │  data: {...}}   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Client App    │
                    │ Updates UI with │
                    │   response      │
                    └─────────────────┘
```

---

## 👤 3. Fluxo de Autenticação e Multi-Tenancy

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOGIN FLOW                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User entra email + password                                │
│     ↓                                                            │
│  2. POST /api/v1/auth/login                                    │
│     ↓                                                            │
│  3. Backend valida credenciais no banco                        │
│     ├─ User não existe → HTTP 401 Unauthorized                │
│     ├─ Password errado → HTTP 401 Unauthorized                │
│     └─ ✓ OK → Continua                                        │
│     ↓                                                            │
│  4. Cria JWT token com payload:                               │
│     {                                                           │
│       "sub": "user_id",      ← Identificador do usuário       │
│       "tenant_id": "abc123", ← IMPORTANTE: Multi-tenancy      │
│       "role": "operador",    ← Role/Permissão                 │
│       "exp": 1234567890     ← Expiração                       │
│     }                                                           │
│     ↓                                                            │
│  5. Assina token com SECRET_KEY (HS256)                       │
│     ↓                                                            │
│  6. Retorna token + refresh_token ao cliente                  │
│     ↓                                                            │
│  7. Cliente armazena token (localStorage/sessionStorage)       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 REQUISIÇÕES SUBSEQUENTES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Header HTTP:                                                   │
│  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  │
│  X-Tenant-ID: abc123                   ← Redundante mas ok    │
│     ↓                                                            │
│  Backend middleware valida token:                              │
│  ├─ Decodifica JWT                                            │
│  ├─ Valida assinatura (SECRET_KEY)                            │
│  ├─ Checa expiração                                           │
│  └─ ✓ OK → Extrai user_id + tenant_id                        │
│     ↓                                                            │
│  Tenant Middleware adiciona tenant context:                   │
│  ├─ Carrega permissions do tenant                             │
│  ├─ Valida se tenant ativo                                    │
│  └─ Injeta tenant_id em todas as queries                      │
│     ↓                                                            │
│  Exemplopromoção de query no banco:                              │
│  SELECT * FROM clientes                                        │
│  WHERE tenant_id = 'abc123'  ← Isolamento!                    │
│  AND id = 'xyz789'                                           │
│     ↓                                                            │
│  ✓ Resposta retorna APENAS dados do tenant 'abc123'          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│           ISOLAMENTO DE DADOS POR TENANT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User "João" (Transportadora A, tenant_id='aaa')              │
│  ├─ VÊ clientes da transportadora A                            │
│  ├─ NÃO CONSEGUE ver clientes da transportadora B             │
│  ├─ NÃO CONSEGUE ver quotas de outro tenant                   │
│  └─ Bloqueado automaticamente pelo middleware                  │
│                                                                  │
│  User "Maria" (Transportadora B, tenant_id='bbb')             │
│  ├─ VÊ clientes da transportadora B                            │
│  ├─ NÃO CONSEGUE ver clientes da transportadora A             │
│  └─ Bloqueado automaticamente pelo middleware                  │
│                                                                  │
│  Admin (tenant_id=NULL ou especial)                           │
│  ├─ Pode visualizar todos tenants (com cuidado!)              │
│  └─ Verificação extra de permissões                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 4. Fluxo de Criação de Tenants (Provisionamento SaaS)

```
┌──────────────────────────────────────────────────────────────────┐
│          LEAD → TENANT PROVISIONADO (SaaS Flow)                  │
└──────────────────────────────────────────────────────────────────┘

STEP 1: Lead Solicita Demo
┌─────────────────────────────────────────────────────────────────┐
│ Página: site-divulgacao/ → Demo Form                           │
│ Usuário preenche:                                              │
│  - Nome da empresa                                             │
│  - Email                                                       │
│  - Telefone                                                    │
│ Clica: "Solicitar Demo"                                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
STEP 2: Backend Cria Lead
┌─────────────────────────────────────────────────────────────────┐
│ POST /api/v1/leads/criar                                       │
│                                                                │
│ Banco (tabela leads):                                          │
│ {                                                              │
│   id: "uuid1",                                                │
│   empresa: "Transportadora XYZ",                              │
│   email: "contato@xyz.com",                                   │
│   telefone: "11999999999",                                    │
│   status: "NEW"    ← Estado inicial                           │
│ }                                                              │
│                                                                │
│ ✓ Email enviado: "Obrigado! Agende sua demo"                │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
STEP 3: Lead Faz Alguma Ação (Demo, Trial, etc)
┌─────────────────────────────────────────────────────────────────┐
│ Opção A: Trial grátis 14 dias                                  │
│ Opção B: Demo agendada                                        │
│ Opção C: Compra plano                                         │
│                                                                │
│ Lead status → "QUALIFIED" ou "READY_TO_CONVERT"              │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
STEP 4: Lead Faz Checkout (MercadoPago)
┌─────────────────────────────────────────────────────────────────┐
│ Usuário é redirecionado para checkout                          │
│                                                                │
│ Preferência MercadoPago:                                       │
│ {                                                              │
│   "items": [{title: "Plano Pro", price: 199.90}],            │
│   "payer": {name: "João", email: "joao@xyz.com"},            │
│   "external_reference": "lead_uuid1"  ← Link para lead       │
│ }                                                              │
│                                                                │
│ Usuário paga com cartão/pix/boleto                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
STEP 5: Webhook de Pagamento Aprovado
┌─────────────────────────────────────────────────────────────────┐
│ POST /api/v1/webhooks/mercadopago                              │
│                                                                │
│ MercadoPago → Backend                                         │
│ {                                                              │
│   "action": "payment.approved",                               │
│   "data": {                                                   │
│     "id": "mp_payment_123",                                   │
│     "external_reference": "lead_uuid1",                       │
│     "status": "approved",                                     │
│     "amount": 199.90                                          │
│   }                                                            │
│ }                                                              │
│                                                                │
│ ✓ Webhook recebido com sucesso (HTTP 202 Accepted)           │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
STEP 6: Processamento Assincronamente (Celery)
┌─────────────────────────────────────────────────────────────────┐
│ Tarefa Celery em background:                                  │
│                                                                │
│ 1️⃣  Busca lead por external_reference                         │
│     lead = db.query(Lead).filter_by(id='lead_uuid1').first()  │
│                                                                │
│ 2️⃣  Cria novo Tenant                                          │
│     tenant = Tenant(                                          │
│       nome='Transportadora XYZ',                              │
│       cnpj='12.345.678/0001-90',                              │
│       plano='pro',                                            │
│       status='active'                                         │
│     )                                                          │
│     db.add(tenant)                                            │
│     db.commit()                                               │
│                                                                │
│ 3️⃣  Cria usuário Admin para tenant                            │
│     admin_password = generate_secure_password(12)  # abc123!  │
│     user = User(                                              │
│       tenant_id=tenant.id,                                    │
│       email='contato@xyz.com',                                │
│       password_hash=bcrypt(admin_password),                   │
│       role='admin'                                            │
│     )                                                          │
│     db.add(user)                                              │
│     db.commit()                                               │
│                                                                │
│ 4️⃣  Atualiza status do lead                                   │
│     lead.status = 'CONVERTED'                                 │
│     lead.tenant_id = tenant.id                                │
│     db.commit()                                               │
│                                                                │
│ 5️⃣  Envia email 1: Confirmação de pagamento                   │
│     to: contato@xyz.com                                       │
│     subject: "✅ Pagamento Confirmado"                        │
│     body: "Seu pagamento foi aprovado..."                     │
│                                                                │
│ 6️⃣  Envia email 2: Credenciais de acesso                      │
│     to: contato@xyz.com                                       │
│     subject: "🎉 Bem-vindo ao LogiFlow CRM!"                  │
│     body: "Acesse em https://app.logiflow.com.br"             │
│            "E-mail: contato@xyz.com"                          │
│            "Senha: abc123!"                                   │
│                                                                │
│ 7️⃣  Registra evento em auditoria                              │
│     AuditLog(                                                 │
│       action='TENANT_CREATED',                                │
│       tenant_id=tenant.id,                                    │
│       timestamp=now()                                         │
│     )                                                          │
│                                                                │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
STEP 7: Cliente Acessa Sistema
┌─────────────────────────────────────────────────────────────────┐
│ Cliente vai para https://app.logiflow.com.br                   │
│ ├─ Faz login com email + senha                                │
│ ├─ Backend valida credenciais                                 │
│ ├─ Gera JWT token com tenant_id                               │
│ ├─ Cliente recebe token                                       │
│ └─ Dashboard carrega com dados do tenant                      │
│                                                                │
│ ✓ SUCESSO: Novo tenant provisionado e ativo!                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📍 5. Fluxo GPS Real-Time

```
┌──────────────────────────────────────────────────────────────────┐
│           GPS TRACKING REAL-TIME ARCHITECTURE                     │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│   App Motorista     │  (PWA on mobile device)
│ ┌─────────────────┐ │
│ │ Navigator.      │ │  Acessa GPS do device a cada 5seg
│ │ Geolocation     │ │  { lat, lng, accuracy, velocity }
│ └────────┬────────┘ │
└──────────┼──────────┘
           │
           │ latitude, longitude, accuracy
           │ (HTTP POST + WebSocket fallback)
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (main.py)                       │
│                                                                   │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │ POST /api/v1/gps/update (REST endpoint)                  │  │
│ │                                                            │  │
│ │ Recebe: {                                                │  │
│ │   motorista_id: "mot123",                               │  │
│ │   latitude: -23.5505,                                   │  │
│ │   longitude: -46.6333,                                  │  │
│ │   accuracy: 15.5,                                       │  │
│ │   timestamp: 1640000000                                 │  │
│ │ }                                                        │  │
│ │                                                            │  │
│ │ ✓ Insere em banco (PostgreSQL)                          │  │
│ │ ✓ Publica em Redis (para WebSocket/SSE)               │  │
│ │ ✓ Cache atualizado                                      │  │
│ │ ✓ Retorna HTTP 200 OK                                   │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                   │
└───────────┬──────────────────────────────────────────────────────┘
            │
    ┌───────┴───────┬─────────────────┐
    │               │                 │
    ▼               ▼                 ▼
┌──────────┐  ┌─────────┐        ┌────────────┐
│PostgreSQL│  │  Redis  │        │   Celery   │
│          │  │(channel)│        │(scheduled) │
│gps_      │  │streaming│        │tasks       │
│tracking  │  │         │        │            │
│  table   │  └─────────┘        └────────────┘
└──────────┘       │                    │
                   │                    │
                   ├─ Pub/Sub          ├─ Geofence check
                   │                    ├─ Route analytics
                   │                    └─ Alerts
                   │
                   ▼
        ┌────────────────────┐
        │ WebSocket Server   │
        │ (FastAPI + uvicorn)│
        │                    │
        │ Connected clients: │
        │ - CRM frontend     │
        │ - Manager view     │
        │ - Customer portal  │
        └────────────────────┘
            │
    ┌───────┴──────────┬──────────────┐
    │                  │              │
    ▼                  ▼              ▼
┌──────────┐  ┌──────────────┐  ┌──────────────┐
│CRM Map   │  │Manager View  │  │Portal Map    │
│          │  │(Dashboard)   │  │(Customer)    │
│Updates   │  │Updates live  │  │Updates live  │
│in real   │  │position      │  │ETA          │
│-time     │  │              │  │              │
└──────────┘  └──────────────┘  └──────────────┘

┌──────────────────────────────────────────────────────────────────┐
│              TIMELINE DA ATUALIZAÇÃO GPS                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ T=0s:   Motorista em posição A (lat1, lng1)                      │
│         App coleta coordenadas                                   │
│         │                                                         │
│ T=1s:   POST /gps/update enviado                                │
│         │                                                         │
│ T=2s:   Backend recebe, valida, insere                          │
│         │                                                         │
│ T=3s:   WebSocket publica para todos os clientes               │
│         │                                                         │
│ T=4s:   Clientes recebem e renderizam no mapa                  │
│         Motorista aparece em nova posição                       │
│         │                                                         │
│ T=5s:   App coleta nova posição (lat2, lng2)                   │
│         (ciclo repete)                                          │
│                                                                   │
│ Latência Total: ~2-3 segundos (depende de network)             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│            ANALYTICS & ALERTAS (Background Tasks)               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ Celery Task 1: Geofence Monitoring                              │
│ ├─ Verifica se motorista entrou em zona de entrega              │
│ ├─ Calcula distância até destino                                │
│ ├─ Se < 500m: Envia notificação WhatsApp "Chegou!"            │
│ └─ Atualiza status da entrega                                   │
│                                                                   │
│ Celery Task 2: Rota Analytics                                   │
│ ├─ Acumula histórico de posições                                │
│ ├─ Calcula distância percorrida                                 │
│ ├─ Detecta desvios de rota                                      │
│ └─ Estima tempo de chegada (ETA)                               │
│                                                                   │
│ Celery Task 3: Alertas                                          │
│ ├─ Velocidade anormalmente alta (excesso de velocidade)       │
│ ├─ Parada prolongada (> 1h sem movimento)                       │
│ ├─ Saiu da rota planejada                                       │
│ └─ Notifica gerente via WhatsApp/Email                         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 💰 6. Fluxo de Pagamento e Assinatura

```
┌───────────────────────────────────────────────────────────────────┐
│           PAYMENT & SUBSCRIPTION FLOW (MercadoPago)               │
└───────────────────────────────────────────────────────────────────┘

STEP 1: User navega para checkout
┌────────────────────────────────────────────────────────────────┐
│ URL: https://app.logiflow.com.br/checkout                      │
│ Componente: CheckoutView.vue                                   │
│                                                                │
│ Mostra:                                                        │
│ ├─ Opção de plano (Free / Pro / Enterprise)                   │
│ ├─ Valor mensal                                              │
│ ├─ Features de cada plano                                    │
│ └─ Botão "Assinar com MercadoPago"                           │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
STEP 2: Backend cria preferência de pagamento
┌────────────────────────────────────────────────────────────────┐
│ POST /api/v1/billing/criar-preferencia-mercadopago             │
│                                                                │
│ Backend:                                                       │
│ mp_service = MercadoPagoService()                             │
│ preference = {                                                │
│   "items": [{                                                │
│     "title": "LogiFlow CRM - Plano Pro",                      │
│     "quantity": 1,                                           │
│     "unit_price": 199.90                                     │
│   }],                                                         │
│   "payer": {                                                 │
│     "name": usuario.nome,                                    │
│     "email": usuario.email                                   │
│   },                                                          │
│   "external_reference": f"lead_{tenant_id}",                 │
│   "back_urls": {                                             │
│     "success": "https://app.logiflow.com.br/checkout/success",│
│     "failure": "https://app.logiflow.com.br/checkout/failure",│
│     "pending": "https://app.logiflow.com.br/checkout/pending" │
│   },                                                          │
│   "auto_return": "approved"                                  │
│ }                                                             │
│                                                                │
│ response = mp_client.create_preference(preference)           │
│ Retorna: {                                                   │
│   "id": "preferences_id_123",                               │
│   "init_point": "https://www.mercadopago.com.br/checkout/...│
│ }                                                             │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
STEP 3: Frontend redireciona para MercadoPago
┌────────────────────────────────────────────────────────────────┐
│ Frontend recebe init_point URL                                 │
│ window.location.href = init_point                              │
│                                                                │
│ Usuário é redirecionado para MercadoPago                       │
│ https://www.mercadopago.com.br/checkout/...                  │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
STEP 4: Pagamento no MercadoPago
┌────────────────────────────────────────────────────────────────┐
│ Usuário preenche dados de pagamento:                          │
│                                                                │
│ Opções:                                                        │
│ ├─ Cartão de crédito/débito                                 │
│ ├─ Pix instantâneo                                          │
│ ├─ Boleto                                                   │
│ ├─ Transferência bancária                                   │
│ └─ Conta MercadoPago                                        │
│                                                                │
│ Processa pagamento...                                         │
│                                                                │
│ Resultado:                                                     │
│ ├─ ✅ Approved  → Redireciona para /checkout/success         │
│ ├─ ❌ Rejected  → Redireciona para /checkout/failure         │
│ └─ ⏳ Pending   → Redireciona para /checkout/pending         │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
STEP 5: Webhook do MercadoPago
┌────────────────────────────────────────────────────────────────┐
│ MercadoPago → Backend Webhook                                  │
│                                                                │
│ POST /api/v1/webhooks/mercadopago                             │
│ {                                                              │
│   "id": "webhook_event_123",                                  │
│   "topic": "payment",                                         │
│   "resource": "https://.../v1/payments/12345",               │
│   "action": "payment.approved"                                │
│ }                                                              │
│                                                                │
│ Ou POST (com payment_data):                                    │
│ {                                                              │
│   "action": "payment.approved",                               │
│   "data": {                                                   │
│     "id": "payment_id_123",                                   │
│     "external_reference": "lead_abc123",                      │
│     "status": "approved",                                     │
│     "amount": 199.90                                          │
│   }                                                            │
│ }                                                              │
│                                                                │
│ Backend retorna HTTP 202 Accepted (não bloqueia)             │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
STEP 6: Processamento em Background (Celery)
┌────────────────────────────────────────────────────────────────┐
│ @celery_app.task                                               │
│ async def process_approved_payment(payment_id: str):          │
│                                                                │
│   6.1. Fetch payment details                                  │
│        payment = mp_client.get_payment(payment_id)            │
│                                                                │
│   6.2. Find lead                                              │
│        external_ref = payment.external_reference              │
│        lead = db.query(Lead).filter_by(id=external_ref).first│
│        if not lead: return  # Ignore unknown payments         │
│                                                                │
│   6.3. Create new Tenant                                      │
│        tenant = Tenant(                                       │
│          nome=lead.empresa,                                   │
│          cnpj=lead.cnpj,                                      │
│          email=lead.email,                                    │
│          plano="pro",                                         │
│          status="active"                                      │
│        )                                                       │
│        db.add(tenant)                                         │
│        db.flush()  # Get tenant.id before commit             │
│                                                                │
│   6.4. Create admin user                                      │
│        password = generate_secure_password(12)                │
│        user = User(                                           │
│          tenant_id=tenant.id,                                 │
│          email=lead.email,                                    │
│          password_hash=hash_password(password),               │
│          role="admin"                                         │
│        )                                                       │
│        db.add(user)                                           │
│                                                                │
│   6.5. Create subscription record                             │
│        subscription = Subscription(                           │
│          tenant_id=tenant.id,                                 │
│          plano="pro",                                         │
│          valor_mensal=199.90,                                 │
│          status="active",                                     │
│          payment_id=payment_id,                               │
│          next_billing_date=now() + timedelta(days=30)        │
│        )                                                       │
│        db.add(subscription)                                   │
│                                                                │
│   6.6. Commit all                                             │
│        db.commit()                                            │
│                                                                │
│   6.7. Send confirmation email                                │
│        email_service.send_payment_confirmation(               │
│          to=lead.email,                                       │
│          tenant_name=lead.empresa,                            │
│          amount=199.90                                        │
│        )                                                       │
│                                                                │
│   6.8. Send credentials email                                 │
│        email_service.send_welcome_email(                      │
│          to=lead.email,                                       │
│          usuario=lead.email,                                  │
│          senha=password,                                      │
│          app_url="https://app.logiflow.com.br"               │
│        )                                                       │
│                                                                │
│   6.9. Update lead status                                     │
│        lead.status = "CONVERTED"                              │
│        lead.tenant_id = tenant.id                             │
│        db.commit()                                            │
│                                                                │
│   6.10. Log event                                             │
│         AuditLog(                                             │
│           action="PAYMENT_APPROVED",                          │
│           tenant_id=tenant.id,                                │
│           metadata={"payment_id": payment_id}                 │
│         )                                                      │
│                                                                │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
STEP 7: Customer Receives Access
┌────────────────────────────────────────────────────────────────┐
│ Email 1: Confirmação de Pagamento                              │
│ ├─ Assunto: "✅ Pagamento Confirmado"                         │
│ ├─ Inclui: Valor, data, comprovante                           │
│ └─ Próxima cobrança: 30 dias                                  │
│                                                                │
│ Email 2: Credenciais de Acesso                                │
│ ├─ Assunto: "🎉 Bem-vindo ao LogiFlow CRM!"                  │
│ ├─ Contém: Email de login                                     │
│ ├─ Contém: Senha temporária                                   │
│ └─ Link: https://app.logiflow.com.br/login                   │
│                                                                │
│ ✓ Tenant ativo                                                │
│ ✓ User admin criado                                           │
│ ✓ Acesso liberado                                             │
│ ✓ Ciclo de faturamento iniciado                               │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 7. Matriz de Módulos e Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│  MÓDULO/FEATURE              Backend Router    Frontend View    │
├─────────────────────────────────────────────────────────────────┤
│  Gestão de Clientes          routers/          views/clientes/  │
│  routers/clientes.py         clientes.py       ListaClientes    │
│                              routers/admin     ClienteDetalhes  │
├─────────────────────────────────────────────────────────────────┤
│  Cotações de Frete           routers/          views/cotacao/   │
│                              cotacoes.py       ListaCotacoes    │
│                              cotacao_          CotacaoForm      │
│                              automatica.py     CotacaoDetalhes  │
├─────────────────────────────────────────────────────────────────┤
│  Pedidos                     routers/pedidos   views/pedidos/   │
│                              .py               ListaPedidos     │
│                              routers/billing   PedidoDetalhes   │
│                              .py               PedidoTimeline   │
├─────────────────────────────────────────────────────────────────┤
│  Rastreamento de Entregas    routers/          views/entregas/  │
│                              entregas.py       EntregasMapa     │
│                              routers/gps_      EntregaDetalhes  │
│                              tracking.py                        │
├─────────────────────────────────────────────────────────────────┤
│  GPS Real-Time               routers/gps_      views/gps/       │
│                              tracking.py       GPSMapa          │
│                              routers/gps_      HistoricoRotas   │
│                              self_service.py   AlertasGeofence  │
├─────────────────────────────────────────────────────────────────┤
│  Documentos Fiscais (CT-e)   routers/fiscal    views/fiscal/    │
│                              .py               EmissaoCte       │
│                              integrations/     HistoricoFiscal  │
│                              focusnfe/                          │
├─────────────────────────────────────────────────────────────────┤
│  Motoristas & Frota          routers/          views/frota/     │
│                              motoristas.py     Listamotoristas  │
│                              routers/          ListaVeiculos    │
│                              veiculos.py                        │
├─────────────────────────────────────────────────────────────────┤
│  Pagamentos & Billing        routers/billing   views/checkout/  │
│                              .py               CheckoutView     │
│                              services/mp       PlansView        │
│                              mercadopago       UsageView        │
├─────────────────────────────────────────────────────────────────┤
│  Notificações WhatsApp       routers/          (Sem UI, apenas  │
│                              whatsapp.py       backend)         │
│                              services/                          │
│                              whatsapp_       (Automático via    │
│                              service.py        eventos)         │
├─────────────────────────────────────────────────────────────────┤
│  Pesquisas NPS/CSAT          routers/nps.py    views/           │
│                                                satisfacao/      │
│                                                PesquisasView    │
├─────────────────────────────────────────────────────────────────┤
│  Leads & Demo                routers/leads.py  views/demo/      │
│                              routers/demo.py   DemoRequestView  │
├─────────────────────────────────────────────────────────────────┤
│  Dashboard & Relatórios      routers/          views/dashboard  │
│                              dashboard.py      DashboardView    │
│                              routers/          Reports          │
│                              erp.py            Analytics        │
├─────────────────────────────────────────────────────────────────┤
│  Configurações de Tenant     routers/          views/config/    │
│                              tenants.py        TenantConfig     │
│                              routers/tenant   IntegrationSetup  │
│                              _credentials.py  WebhookConfig     │
├─────────────────────────────────────────────────────────────────┤
│  CRM Enterprise (SaaS)       routers/crm_      views/crm/       │
│                              enterprise.py     EnterpriseView   │
├─────────────────────────────────────────────────────────────────┤
│  Integrações                 routers/          views/config/    │
│ (Melhor Envio, etc)          integrations.py   APIIntegrations  │
│                              integrations/                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🌊 8. Arquitetura de Dados em Tempo Real

```
                    ┌─────────────────────────┐
                    │     App Motorista       │
                    │  (PWA com geolocation)  │
                    └────────────┬────────────┘
                                 │
                    POST /api/v1/gps/update
                 latitude, longitude, timestamp
                                 │
                    ┌────────────▼────────────┐
                    │   FastAPI Backend       │
                    │ (Real-time endpoint)    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Application Layer      │
                    │ (Process & validate)    │
                    └────────────┬────────────┘
                                 │
           ┌─────────────────────┼────────────────────┐
           │                     │                    │
           ▼                     ▼                    ▼
    ┌─────────────┐      ┌──────────────┐    ┌──────────────┐
    │ PostgreSQL  │      │    Redis     │    │   Celery     │
    │   (Persist) │      │ (Real-time)  │    │  (Analytics) │
    │  gps_       │      │  pub/sub     │    │              │
    │ tracking    │      │  streams     │    │ Geofence     │
    │   table     │      │              │    │ checking     │
    └─────────────┘      └──────────────┘    └──────────────┘
                                 │
                    ┌────────────▼───────────┐
                    │     WebSocket Server   │
                    │ (FastAPI + uvicorn)     │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼───────────────────────┐
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────────┐    ┌────────────────┐    ┌──────────────┐
    │ CRM Frontend │    │   Manager      │    │    Portal    │
    │    (Vue.js)  │    │   Dashboard    │    │    Cliente   │
    │              │    │  (Real-time)   │    │  (Tracking)  │
    │ Renderiza    │    │                │    │              │
    │ mapa ao      │    │ Monitora       │    │ Acompanha    │
    │ vivo         │    │ motoristas     │    │ entrega      │
    └──────────────┘    └────────────────┘    └──────────────┘

┌────────────────────────────────────────────────────────────────┐
│  PERFORMANCE CHARACTERISTICS                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Collection Frequency:  5 seconds (App Motorista)            │
│  Update Frequency:      Env-dependent (10-30 updates/sec)    │
│  WebSocket Broadcast:   ~100ms delay from collection          │
│  DB Persistence:        ~2-3 seconds after collection         │
│                                                                │
│  Typical Throughput:    100 motoristas × 12 updates/min       │
│                         = 1,200 updates/min                   │
│                         = 20 updates/second                   │
│                                                                │
│  Data Retention:        30 dias (configurable)               │
│  Archival Strategy:     Move old data to cold storage        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## ✅ 9. Checklist de Status do Projeto

```
┌──────────────────────────────────────────────────────────────┐
│               FUNCIONALIDADES IMPLEMENTADAS                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  BACKEND CORE:                                              │
│  ✅ FastAPI REST API                                        │
│  ✅ PostgreSQL Database with Alembic migrations            │
│  ✅ SQLAlchemy ORM                                          │
│  ✅ JWT Authentication                                      │
│  ✅ Multi-tenancy middleware                               │
│  ✅ Redis caching                                           │
│  ✅ Celery task queue                                       │
│  ✅ Error handling & logging                               │
│                                                              │
│  FEATURES:                                                  │
│  ✅ Gestão de Clientes (CRUD)                              │
│  ✅ Cotações automáticas (Melhor Envio)                    │
│  ✅ Pedidos e Entregas                                      │
│  ✅ GPS Real-time tracking                                  │
│  ✅ Documentos Fiscais (CT-e/MDF-e via Focus)            │
│  ✅ Pagamentos (MercadoPago)                                │
│  ✅ WhatsApp notifications                                  │
│  ✅ Email notifications (SendGrid)                         │
│  ✅ NPS/CSAT surveys                                        │
│  ✅ Leads management                                        │
│  ✅ Dashboard & analytics                                   │
│                                                              │
│  FRONTEND (CRM):                                            │
│  ✅ Vue.js 3 SPA                                            │
│  ✅ Pinia state management                                  │
│  ✅ Vue Router                                              │
│  ✅ TailwindCSS styling                                     │
│  ✅ Responsive design                                        │
│  ✅ Axios for HTTP                                          │
│  ✅ Dark mode (opcional)                                    │
│                                                              │
│  APP MOTORISTA:                                             │
│  ✅ PWA (Progressive Web App)                               │
│  ✅ Geolocation API integration                            │
│  ✅ Delivery management                                      │
│  ✅ GPS tracking                                            │
│  ✅ Photo capture                                           │
│  ✅ Signature capture                                       │
│  ✅ Offline capability                                      │
│                                                              │
│  PORTAL CLIENTE:                                            │
│  ✅ Order tracking                                          │
│  ✅ Quote requests                                          │
│  ✅ Account management                                      │
│  ✅ Real-time ETA                                           │
│                                                              │
│  SITE (Marketing):                                          │
│  ✅ Homepage                                                │
│  ✅ Features page                                           │
│  ✅ Pricing page                                            │
│  ✅ Demo request form                                       │
│  ✅ Blog (optional)                                         │
│  ✅ Contact form                                            │
│                                                              │
│  DEVOPS:                                                    │
│  ✅ Docker Compose                                          │
│  ✅ GitHub Actions CI/CD                                    │
│  ✅ Environment configuration                               │
│  ✅ Logging                                                 │
│  ⚠️  Helm charts (não implementado)                        │
│  ⚠️  Kubernetes support (não implementado)                 │
│                                                              │
│  SEGURANÇA:                                                 │
│  ✅ JWT authentication                                      │
│  ✅ Password hashing (bcrypt)                               │
│  ✅ CORS configuration                                      │
│  ⚠️  Rate limiting (parcial)                               │
│  ⚠️  API key rotation (não implementado)                   │
│                                                              │
│  TESTES:                                                    │
│  ⚠️  Unit tests (cobertura ~30%)                           │
│  ⚠️  Integration tests (parcial)                           │
│  ⚠️  E2E tests (não implementado)                          │
│  ⚠️  Performance tests (não implementado)                  │
│                                                              │
│  OBSERVABILIDADE:                                           │
│  ✅ Loguru logging                                          │
│  ⚠️  Prometheus metrics (não implementado)                 │
│  ⚠️  APM/Jaeger (não implementado)                         │
│  ⚠️  Monitoring/Alerting (não implementado)                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📈 10. Tendências de Crescimento e Escalabilidade

```
┌───────────────────────────────────────────────────────────────┐
│     CRESCIMENTO ESPERADO & ESTRATÉGIA DE ESCALABILIDADE        │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Q1 2026 (Atual):                                             │
│  • Usuários: ~100                                            │
│  • Tenants: ~20                                              │
│  • Capacidade de servidor: ✅ Abundante                      │
│  • Estratégia: Monolito simples, tudo no mesmo servidor     │
│                                                               │
│  Q2 2026:                                                    │
│  • Usuários: ~500                                            │
│  • Tenants: ~50                                              │
│  • Ponto crítico: Database queries começam a lentificar     │
│  • Ação: Implementar índices de banco, aumentar cache Redis │
│                                                               │
│  Q3 2026:                                                    │
│  • Usuários: ~2,000                                          │
│  • Tenants: ~150                                             │
│  • Ponto crítico: Processamento de GPS pesado               │
│  • Ação: Separar worker Celery em servidor diferente        │
│           Migrar GPS para TimescaleDB                       │
│                                                               │
│  Q4 2026+:                                                   │
│  • Usuários: >5,000                                          │
│  • Tenants: >300                                             │
│  • Ponto crítico: Monolito atingindo limite                 │
│  • Ação: Considerar arquitetura de microserviços:          │
│    ├─ API Service (FastAPI)                                │
│    ├─ GPS Service (dedicado ao rastreamento)              │
│    ├─ Notification Service (WhatsApp/Email)               │
│    ├─ Fiscal Service (CT-e/MDF-e)                        │
│    ├─ Billing Service (Pagamentos)                        │
│    └─ Orchestration (Kubernetes)                          │
│                                                               │
│  SCALING LAYERS:                                             │
│                                                               │
│  1. Database:                                                │
│     Current: PostgreSQL single instance                     │
│     Growth 1: Add read replicas                             │
│     Growth 2: Partitioning (tenant_id)                      │
│     Growth 3: Sharding if needed                            │
│                                                               │
│  2. API:                                                    │
│     Current: Single FastAPI instance                        │
│     Growth 1: Gunicorn múltiplos workers                    │
│     Growth 2: Load balancer (Nginx)                         │
│     Growth 3: Kubernetes Replicas                           │
│                                                               │
│  3. Cache:                                                  │
│     Current: Single Redis instance                          │
│     Growth 1: Redis Cluster mode                            │
│     Growth 2: Distributed cache (Memcached failover)        │
│                                                               │
│  4. Jobs:                                                   │
│     Current: Single Celery worker                           │
│     Growth 1: Multiple workers (diferentes queues)          │
│     Growth 2: Auto-scaling based on queue depth             │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 📝 Resumo Final

O **LogiFlow CRM** é uma aplicação bem arquitetada com:

✅ **Pontos Fortes**
- Clean Architecture implementada
- Multi-tenancy seguro
- Stack moderno (FastAPI, Vue 3, PostgreSQL)
- Integrações robustas (WhatsApp, MercadoPago, Focus NFe)
- Features avançadas (GPS real-time, SaaS automático)

⚠️ **Melhorias Necessárias**
- Aumentar cobertura de testes
- Implementar observabilidade (Prometheus)
- Otimizar performance (DataLoader, índices DB)
- Security: Rate limiting, CORS mais restritivo

🚀 **Pronto para**
- Produção de pequena escala (~100-500 usuários)
- Crescimento planejado com roadmap de microserviços
- Features futuras: GraphQL, CQRS, Event Sourcing

