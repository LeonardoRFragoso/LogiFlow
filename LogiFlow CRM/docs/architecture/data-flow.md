# LogiFlow CRM - Diagrama de Fluxo de Dados

> **Versão:** 1.0.0  
> **Atualizado:** Janeiro 2026

## Descrição

Este documento detalha os principais fluxos de dados do sistema LogiFlow CRM, mostrando como a informação transita entre os componentes.

---

## 1. Fluxo Principal: Cotação → Pedido → Entrega

```mermaid
flowchart TB
    subgraph Cliente["👤 Cliente"]
        SOL["Solicita Cotação"]
        APR["Aprova Cotação"]
        ACOMP["Acompanha Entrega"]
    end

    subgraph Frontend["🌐 Frontend CRM"]
        FORM_COT["Formulário<br/>de Cotação"]
        LIST_COT["Lista de<br/>Cotações"]
        TRACK["Tracking<br/>View"]
    end

    subgraph Backend["⚙️ Backend API"]
        R_COT["POST /cotacoes"]
        R_APR["PATCH /cotacoes/{id}/aprovar"]
        R_TRACK["GET /rastreamento/{codigo}"]
        
        SVC_CALC["Cálculo<br/>de Frete"]
        SVC_CREATE_PED["Criar<br/>Pedido"]
        SVC_GPS["GPS<br/>Service"]
    end

    subgraph External["🌐 Externo"]
        ME["Melhor Envio<br/>API"]
        WA["WhatsApp<br/>API"]
        MAPS["Google Maps<br/>API"]
    end

    subgraph Database["💾 Database"]
        TB_COT[("cotacoes")]
        TB_PED[("pedidos")]
        TB_ENT[("entregas")]
        TB_LOC[("localizacoes")]
    end

    %% Fluxo de Cotação
    SOL -->|"1. Dados"| FORM_COT
    FORM_COT -->|"2. Submit"| R_COT
    R_COT -->|"3. Consulta<br/>preços"| ME
    ME -->|"4. Cotações"| R_COT
    R_COT -->|"5. Calcula"| SVC_CALC
    SVC_CALC -->|"6. Salva"| TB_COT
    R_COT -->|"7. Notifica"| WA
    
    %% Fluxo de Aprovação
    APR -->|"8. Aprova"| LIST_COT
    LIST_COT -->|"9. Request"| R_APR
    R_APR -->|"10. Update"| TB_COT
    R_APR -->|"11. Cria"| SVC_CREATE_PED
    SVC_CREATE_PED -->|"12. Insert"| TB_PED
    SVC_CREATE_PED -->|"13. Insert"| TB_ENT
    R_APR -->|"14. Notifica"| WA

    %% Fluxo de Rastreamento
    ACOMP -->|"15. Tracking"| TRACK
    TRACK -->|"16. Request"| R_TRACK
    R_TRACK -->|"17. Query"| TB_ENT
    R_TRACK -->|"18. Query"| TB_LOC
    SVC_GPS -->|"19. Location"| MAPS
    R_TRACK -->|"20. Response"| TRACK

    style TB_COT fill:#336791,color:#fff
    style TB_PED fill:#336791,color:#fff
    style TB_ENT fill:#336791,color:#fff
    style TB_LOC fill:#336791,color:#fff
```

---

## 2. Fluxo de Autenticação Multi-Tenant

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário
    participant FE as Frontend
    participant API as FastAPI
    participant MW as Middlewares
    participant DB as PostgreSQL
    participant REDIS as Redis

    rect rgb(240, 248, 255)
        Note over U,REDIS: Login Flow
        U->>FE: Email + Senha
        FE->>API: POST /auth/login
        API->>DB: SELECT * FROM users WHERE email=?
        DB-->>API: User + Tenant
        API->>API: Verify password (bcrypt)
        API->>API: Generate JWT (tenant_id in payload)
        API->>REDIS: Store session
        API-->>FE: {token, user, tenant}
        FE->>FE: Store token (localStorage)
    end

    rect rgb(255, 248, 240)
        Note over U,REDIS: Authenticated Request
        U->>FE: Ação no sistema
        FE->>API: Request + Authorization: Bearer {token}
        API->>MW: TenantMiddleware
        MW->>MW: Decode JWT
        MW->>MW: Extract tenant_id
        MW->>REDIS: Check rate limit
        REDIS-->>MW: OK
        MW->>API: Inject tenant_context
        API->>DB: Query with tenant_id filter
        DB-->>API: Tenant-scoped data
        API-->>FE: Response
    end

    rect rgb(255, 240, 240)
        Note over U,REDIS: Token Refresh
        FE->>API: POST /auth/refresh
        API->>REDIS: Validate refresh token
        REDIS-->>API: Valid
        API->>API: Generate new access token
        API-->>FE: {new_token}
    end
```

---

## 3. Fluxo de Pagamento (MercadoPago)

```mermaid
flowchart TB
    subgraph User["👤 Usuário"]
        SELECT_PLAN["Seleciona Plano"]
        PAY["Efetua Pagamento"]
    end

    subgraph Frontend["🌐 Frontend"]
        PRICING["Pricing Page"]
        CHECKOUT["Checkout Page"]
        SUCCESS["Success Page"]
    end

    subgraph Backend["⚙️ Backend"]
        R_CHECKOUT["POST /billing/checkout"]
        R_WEBHOOK["POST /billing/webhook"]
        SVC_MP["MercadoPago<br/>Service"]
        SVC_TENANT["Tenant<br/>Provisioning"]
    end

    subgraph MercadoPago["💳 MercadoPago"]
        MP_CREATE["Create<br/>Preference"]
        MP_CHECKOUT["Checkout<br/>Page"]
        MP_WEBHOOK["Webhook<br/>Event"]
    end

    subgraph Database["💾 Database"]
        TB_SUB[("subscriptions")]
        TB_PAY[("payments")]
        TB_TENANT[("tenants")]
    end

    %% Checkout Flow
    SELECT_PLAN -->|"1. Escolhe"| PRICING
    PRICING -->|"2. Checkout"| R_CHECKOUT
    R_CHECKOUT -->|"3. Create<br/>Preference"| SVC_MP
    SVC_MP -->|"4. API Call"| MP_CREATE
    MP_CREATE -->|"5. Preference ID"| SVC_MP
    SVC_MP -->|"6. Salva"| TB_SUB
    R_CHECKOUT -->|"7. Checkout URL"| CHECKOUT
    CHECKOUT -->|"8. Redirect"| MP_CHECKOUT
    
    PAY -->|"9. Paga"| MP_CHECKOUT
    MP_CHECKOUT -->|"10. Webhook"| MP_WEBHOOK
    MP_WEBHOOK -->|"11. POST"| R_WEBHOOK
    R_WEBHOOK -->|"12. Valida"| SVC_MP
    SVC_MP -->|"13. Update"| TB_PAY
    SVC_MP -->|"14. Update"| TB_SUB
    R_WEBHOOK -->|"15. Provisiona"| SVC_TENANT
    SVC_TENANT -->|"16. Update"| TB_TENANT
    R_WEBHOOK -->|"17. Redirect"| SUCCESS

    style MP_CREATE fill:#009ee3,color:#fff
    style MP_CHECKOUT fill:#009ee3,color:#fff
    style MP_WEBHOOK fill:#009ee3,color:#fff
```

---

## 4. Fluxo de Emissão Fiscal (CT-e)

```mermaid
sequenceDiagram
    autonumber
    participant U as Operador
    participant FE as Frontend
    participant API as FastAPI
    participant SVC as FiscalService
    participant NFE as Focus NFe
    participant DB as PostgreSQL
    participant WA as WhatsApp

    U->>FE: Seleciona Pedido
    FE->>API: GET /pedidos/{id}
    API->>DB: SELECT pedido + cliente
    DB-->>API: Dados completos
    API-->>FE: PedidoDTO

    U->>FE: Emitir CT-e
    FE->>API: POST /fiscal/cte
    API->>SVC: emit_cte(pedido_data)
    
    SVC->>SVC: Monta XML CT-e
    SVC->>NFE: POST /cte/emitir
    
    alt Sucesso
        NFE-->>SVC: {chave, protocolo, xml}
        SVC->>DB: INSERT INTO cte
        SVC->>DB: UPDATE pedido SET cte_chave
        SVC-->>API: CTeResponseDTO
        API->>WA: Envia CT-e para cliente
        API-->>FE: Sucesso
    else Erro SEFAZ
        NFE-->>SVC: {erro, motivo}
        SVC-->>API: FiscalException
        API-->>FE: Erro de validação
    end

    Note over U,WA: Fluxo similar para MDF-e
```

---

## 5. Fluxo de GPS Tracking

```mermaid
flowchart TB
    subgraph Motorista["📱 App Motorista"]
        GPS["GPS<br/>Sensor"]
        APP["App PWA"]
    end

    subgraph Backend["⚙️ Backend"]
        R_GPS["POST /gps/tracking"]
        SVC_CACHE["Cache<br/>Service"]
        SVC_HIST["History<br/>Service"]
        WS["WebSocket<br/>Server"]
    end

    subgraph Storage["💾 Storage"]
        REDIS[("Redis<br/>Current Position")]
        PG[("PostgreSQL<br/>History")]
    end

    subgraph Clients["👥 Clientes"]
        PORTAL["Portal Cliente"]
        CRM["CRM Dashboard"]
    end

    GPS -->|"1. Coords"| APP
    APP -->|"2. POST<br/>lat, lng, timestamp"| R_GPS
    R_GPS -->|"3. Cache<br/>current"| SVC_CACHE
    SVC_CACHE -->|"4. SET"| REDIS
    R_GPS -->|"5. Save<br/>history"| SVC_HIST
    SVC_HIST -->|"6. INSERT"| PG
    R_GPS -->|"7. Broadcast"| WS
    WS -->|"8. Push"| PORTAL
    WS -->|"8. Push"| CRM
    
    PORTAL -->|"9. Subscribe"| WS
    CRM -->|"9. Subscribe"| WS
    
    PORTAL & CRM -->|"10. GET current"| R_GPS
    R_GPS -->|"11. GET"| REDIS
    REDIS -->|"12. Position"| R_GPS

    style REDIS fill:#dc382d,color:#fff
    style PG fill:#336791,color:#fff
```

---

## 6. Fluxo de Pesquisa NPS Automática

```mermaid
flowchart TB
    subgraph Scheduler["⏰ Celery Beat"]
        CRON["Cron Job<br/>Diário 10h"]
    end

    subgraph Worker["⚡ Celery Worker"]
        TASK["Task:<br/>check_pending_surveys"]
        SVC_NPS["NPS<br/>Service"]
    end

    subgraph Backend["⚙️ Backend"]
        R_NPS["POST /satisfacao/responder"]
    end

    subgraph External["🌐 External"]
        WA["WhatsApp"]
        EMAIL["SMTP"]
    end

    subgraph Database["💾 Database"]
        TB_ENT[("entregas")]
        TB_SUR[("surveys")]
        TB_RESP[("survey_responses")]
    end

    subgraph Cliente["👤 Cliente"]
        RESP["Responde<br/>Pesquisa"]
    end

    %% Envio automático
    CRON -->|"1. Trigger"| TASK
    TASK -->|"2. Query entregas<br/>concluídas há 24h"| TB_ENT
    TB_ENT -->|"3. Lista"| TASK
    TASK -->|"4. Para cada"| SVC_NPS
    SVC_NPS -->|"5. Cria survey"| TB_SUR
    SVC_NPS -->|"6. Envia link"| WA
    SVC_NPS -->|"6. Envia link"| EMAIL

    %% Resposta
    RESP -->|"7. Acessa link"| R_NPS
    R_NPS -->|"8. Valida token"| TB_SUR
    RESP -->|"9. Envia nota<br/>+ comentário"| R_NPS
    R_NPS -->|"10. Salva"| TB_RESP
    R_NPS -->|"11. Update<br/>status"| TB_SUR
    R_NPS -->|"12. Categoriza<br/>Promotor/Neutro/Detrator"| TB_RESP

    style CRON fill:#6c757d,color:#fff
    style TASK fill:#ffc107,color:#000
```

---

## 7. Fluxo de Rate Limiting

```mermaid
sequenceDiagram
    autonumber
    participant C as Cliente
    participant MW as RateLimitMiddleware
    participant REDIS as Redis
    participant API as FastAPI
    
    C->>MW: Request
    MW->>MW: Extract IP/User ID
    MW->>REDIS: INCR rate:{key}
    REDIS-->>MW: Current count
    
    alt count <= limit
        MW->>REDIS: EXPIRE rate:{key} 60
        MW->>API: Forward request
        API-->>C: 200 OK
    else count > limit
        MW-->>C: 429 Too Many Requests
        Note over C,MW: Retry-After: 60
    end
```

---

## 8. Diagrama de Entidade-Relacionamento (Simplificado)

```mermaid
erDiagram
    TENANT ||--o{ USER : has
    TENANT ||--o{ CLIENTE : has
    TENANT ||--o{ MOTORISTA : has
    TENANT ||--o{ VEICULO : has
    TENANT ||--o{ SUBSCRIPTION : has
    
    CLIENTE ||--o{ COTACAO : requests
    COTACAO ||--o| PEDIDO : generates
    PEDIDO ||--o{ ENTREGA : has
    PEDIDO ||--o| CTE : has
    PEDIDO ||--o| MDFE : has
    
    MOTORISTA ||--o{ ENTREGA : delivers
    VEICULO ||--o{ ENTREGA : used_in
    ENTREGA ||--o{ LOCALIZACAO : tracked_by
    ENTREGA ||--o| SURVEY : triggers
    SURVEY ||--o| SURVEY_RESPONSE : answered_by
    
    SUBSCRIPTION ||--o{ PAYMENT : has

    TENANT {
        uuid id PK
        string nome
        string cnpj
        string plano
        boolean ativo
    }
    
    CLIENTE {
        uuid id PK
        uuid tenant_id FK
        string razao_social
        string cnpj
        string email
    }
    
    COTACAO {
        uuid id PK
        uuid cliente_id FK
        string origem
        string destino
        decimal valor
        string status
    }
    
    PEDIDO {
        uuid id PK
        uuid cotacao_id FK
        date data_coleta
        string status
    }
    
    ENTREGA {
        uuid id PK
        uuid pedido_id FK
        uuid motorista_id FK
        string status
        timestamp entregue_em
    }
```

---

## 9. Resumo dos Fluxos de Dados

| Fluxo | Origem | Destino | Trigger | Frequência |
|-------|--------|---------|---------|------------|
| Cotação | Cliente | PostgreSQL | User action | On-demand |
| Pedido | Cotação | PostgreSQL | Aprovação | On-demand |
| GPS | App Motorista | Redis + PG | Timer (30s) | Contínuo |
| Pagamento | MercadoPago | PostgreSQL | Webhook | On-demand |
| NPS | Celery Beat | Cliente | Cron | Diário |
| Fiscal | Operador | Focus NFe | User action | On-demand |
| Auth | User | Redis | Login | On-demand |

---

*Documento parte da documentação arquitetural do LogiFlow CRM*
