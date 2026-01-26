# LogiFlow CRM - C4 Model: Component Diagram (Nível 3)

> **Versão:** 1.0.0  
> **Atualizado:** Janeiro 2026

## Descrição

O Diagrama de Componentes mostra a estrutura interna dos principais containers, detalhando os componentes, suas responsabilidades e interações.

---

## 1. API Backend - Componentes

```mermaid
flowchart TB
    subgraph API["🚀 FastAPI Backend"]
        subgraph Presentation["📡 Presentation Layer"]
            ROUTERS["Routers (32)<br/>━━━━━━━━━━━<br/>auth, billing,<br/>cotacoes, pedidos,<br/>motoristas, fiscal..."]
            MIDDLEWARE["Middlewares<br/>━━━━━━━━━━━<br/>CORS, Tenant,<br/>RateLimit,<br/>Correlation"]
            HANDLERS["Exception<br/>Handlers"]
        end
        
        subgraph Application["⚙️ Application Layer"]
            USECASES["Use Cases<br/>━━━━━━━━━━━<br/>CriarCliente<br/>CriarCotacao<br/>AprovarCotacao"]
            DTOS["DTOs<br/>━━━━━━━━━━━<br/>ClienteDTO<br/>CotacaoDTO<br/>PedidoDTO"]
        end
        
        subgraph Domain["🏛️ Domain Layer"]
            ENTITIES["Entities<br/>━━━━━━━━━━━<br/>Cliente, Cotacao<br/>Pedido, Entrega<br/>Motorista, Veiculo"]
            VO["Value Objects<br/>━━━━━━━━━━━<br/>CNPJ, CPF<br/>Email, Money"]
            INTERFACES["Interfaces<br/>━━━━━━━━━━━<br/>IRepository<br/>IService"]
            EXCEPTIONS["Domain<br/>Exceptions"]
        end
        
        subgraph Infrastructure["🔧 Infrastructure Layer"]
            REPOS["Repositories<br/>━━━━━━━━━━━<br/>ClienteRepo<br/>CotacaoRepo<br/>PedidoRepo"]
            SERVICES["Services (24)<br/>━━━━━━━━━━━<br/>EmailService<br/>WhatsAppService<br/>BillingService"]
            CONTAINER["DI Container<br/>━━━━━━━━━━━<br/>Dependency<br/>Injection"]
            PERSIST["Persistence<br/>━━━━━━━━━━━<br/>Database<br/>SessionLocal"]
        end
        
        subgraph Models["📊 Data Models"]
            SQLMODELS["SQLAlchemy<br/>Models<br/>━━━━━━━━━━━<br/>User, Tenant<br/>Cliente, Pedido<br/>+ 25 models"]
        end
    end
    
    ROUTERS --> USECASES
    ROUTERS --> SERVICES
    MIDDLEWARE --> ROUTERS
    
    USECASES --> DTOS
    USECASES --> REPOS
    USECASES --> ENTITIES
    
    REPOS --> INTERFACES
    REPOS --> PERSIST
    REPOS --> SQLMODELS
    
    SERVICES --> PERSIST
    SERVICES --> SQLMODELS
    
    CONTAINER --> REPOS
    CONTAINER --> USECASES
    
    PERSIST --> DB[(PostgreSQL)]
    SERVICES --> REDIS[(Redis)]

    style Presentation fill:#e1f5fe
    style Application fill:#fff3e0
    style Domain fill:#f3e5f5
    style Infrastructure fill:#e8f5e9
```

---

## 2. Detalhamento por Camada

### 2.1 Presentation Layer

```mermaid
flowchart LR
    subgraph Routers["📡 Routers (32 módulos)"]
        direction TB
        R_AUTH["auth.py<br/>Login, JWT"]
        R_BILLING["billing.py<br/>Planos, Pagamentos"]
        R_COTACOES["cotacoes.py<br/>CRUD Cotações"]
        R_PEDIDOS["pedidos.py<br/>CRUD Pedidos"]
        R_MOTORISTAS["motoristas.py<br/>CRUD Motoristas"]
        R_FISCAL["fiscal.py<br/>CT-e, MDF-e"]
        R_WHATSAPP["whatsapp.py<br/>Mensagens"]
        R_GPS["gps_tracking.py<br/>Rastreamento"]
        R_OUTROS["+ 24 outros<br/>routers"]
    end
    
    subgraph Middlewares["🔒 Middlewares"]
        direction TB
        M_CORS["CORSMiddleware"]
        M_TENANT["TenantMiddleware"]
        M_RATE["RateLimitMiddleware"]
        M_CORR["CorrelationMiddleware"]
    end
    
    REQ[/"Request"/] --> M_CORS --> M_TENANT --> M_RATE --> M_CORR --> Routers
```

#### Componentes de Routers

| Componente | Arquivo | Responsabilidade |
|------------|---------|------------------|
| **Auth Router** | `auth.py` | Login, registro, JWT, refresh tokens |
| **Billing Router** | `billing.py` | Checkout, webhooks, planos |
| **Cotações Router** | `cotacoes.py` | CRUD de cotações de frete |
| **Pedidos Router** | `pedidos.py` | CRUD de pedidos confirmados |
| **Motoristas Router** | `motoristas.py` | CRUD de motoristas |
| **Fiscal Router** | `fiscal.py` | Emissão de CT-e, MDF-e, NF-e |
| **WhatsApp Router** | `whatsapp.py` | Envio de mensagens e chatbot |
| **GPS Router** | `gps_tracking.py` | Rastreamento em tempo real |
| **CRM Enterprise** | `crm_enterprise.py` | Módulo CRM nativo |

---

### 2.2 Application Layer

```mermaid
flowchart TB
    subgraph UseCases["⚙️ Use Cases"]
        direction TB
        subgraph Cliente["Cliente Use Cases"]
            UC_CRIAR_CLI["CriarClienteUseCase"]
            UC_ATUALIZAR_CLI["AtualizarClienteUseCase"]
            UC_BUSCAR_CLI["BuscarClienteUseCase"]
            UC_LISTAR_CLI["ListarClientesUseCase"]
        end
        
        subgraph Cotacao["Cotação Use Cases"]
            UC_CRIAR_COT["CriarCotacaoUseCase"]
            UC_ENVIAR_COT["EnviarCotacaoUseCase"]
            UC_APROVAR_COT["AprovarCotacaoUseCase"]
        end
    end
    
    subgraph DTOs["📦 DTOs"]
        DTO_CLI["ClienteCreateDTO<br/>ClienteUpdateDTO<br/>ClienteResponseDTO"]
        DTO_COT["CotacaoCreateDTO<br/>CotacaoResponseDTO"]
        DTO_PED["PedidoCreateDTO<br/>PedidoResponseDTO"]
    end
    
    Cliente --> DTO_CLI
    Cotacao --> DTO_COT
```

#### Use Cases Implementados

| Use Case | Descrição | Entrada | Saída |
|----------|-----------|---------|-------|
| `CriarClienteUseCase` | Cria novo cliente | ClienteCreateDTO | ClienteResponseDTO |
| `AtualizarClienteUseCase` | Atualiza cliente | ClienteUpdateDTO | ClienteResponseDTO |
| `BuscarClienteUseCase` | Busca por ID | UUID | ClienteResponseDTO |
| `ListarClientesUseCase` | Lista paginada | PaginationDTO | List[ClienteResponseDTO] |
| `CriarCotacaoUseCase` | Cria cotação | CotacaoCreateDTO | CotacaoResponseDTO |
| `EnviarCotacaoUseCase` | Envia ao cliente | UUID | CotacaoResponseDTO |
| `AprovarCotacaoUseCase` | Aprova cotação | UUID | PedidoResponseDTO |

---

### 2.3 Domain Layer

```mermaid
flowchart TB
    subgraph Entities["🏛️ Domain Entities"]
        direction LR
        E_CLI["Cliente<br/>━━━━━━━━━━━<br/>id, cnpj, razao_social<br/>endereco, contato"]
        E_COT["Cotacao<br/>━━━━━━━━━━━<br/>id, cliente_id, valor<br/>origem, destino, status"]
        E_PED["Pedido<br/>━━━━━━━━━━━<br/>id, cotacao_id<br/>data_coleta, status"]
    end
    
    subgraph ValueObjects["💎 Value Objects"]
        VO_CNPJ["CNPJ<br/>Validação automática"]
        VO_CPF["CPF<br/>Validação automática"]
        VO_EMAIL["Email<br/>Validação automática"]
        VO_MONEY["Money<br/>Precisão decimal"]
    end
    
    subgraph Interfaces["📋 Interfaces"]
        I_REPO["IRepository<br/>━━━━━━━━━━━<br/>get, list, create<br/>update, delete"]
        I_CLI_REPO["IClienteRepository"]
        I_COT_REPO["ICotacaoRepository"]
        I_PED_REPO["IPedidoRepository"]
    end
    
    E_CLI --> VO_CNPJ
    E_CLI --> VO_EMAIL
    E_COT --> VO_MONEY
    
    I_CLI_REPO --> I_REPO
    I_COT_REPO --> I_REPO
    I_PED_REPO --> I_REPO
```

#### Entidades de Domínio

| Entidade | Atributos Principais | Value Objects |
|----------|---------------------|---------------|
| **Cliente** | id, cnpj, razao_social, endereco, telefone, email | CNPJ, Email |
| **Cotacao** | id, cliente_id, origem, destino, peso, valor, status | Money |
| **Pedido** | id, cotacao_id, motorista_id, data_coleta, status | - |

---

### 2.4 Infrastructure Layer

```mermaid
flowchart TB
    subgraph Repositories["📚 Repositories"]
        direction TB
        REPO_CLI["ClienteRepository<br/>implements IClienteRepository"]
        REPO_COT["CotacaoRepository<br/>implements ICotacaoRepository"]
        REPO_PED["PedidoRepository<br/>implements IPedidoRepository"]
    end
    
    subgraph Services["🔧 Services (24)"]
        direction TB
        SVC_EMAIL["EmailService<br/>Envio de e-mails"]
        SVC_WA["WhatsAppService<br/>Integração WhatsApp"]
        SVC_MP["MercadoPagoService<br/>Pagamentos"]
        SVC_FISCAL["FiscalService<br/>CT-e, MDF-e, NF-e"]
        SVC_GPS["GPSService<br/>Rastreamento"]
        SVC_NPS["NPSService<br/>Pesquisas NPS/CSAT"]
        SVC_OUTROS["+ 18 outros services"]
    end
    
    subgraph DI["🔄 Dependency Injection"]
        CONTAINER["Container<br/>━━━━━━━━━━━<br/>get_db()<br/>get_repository()<br/>get_use_case()"]
    end
    
    subgraph Persistence["💾 Persistence"]
        DB_SESSION["SessionLocal<br/>SQLAlchemy Session"]
        DB_BASE["Base<br/>Declarative Base"]
    end
    
    Repositories --> Persistence
    Services --> Persistence
    CONTAINER --> Repositories
    CONTAINER --> Services
    
    Persistence --> DB[(PostgreSQL)]
    Services --> REDIS[(Redis)]
    Services --> EXT[/"External APIs"/]
```

#### Services Principais

| Service | Arquivo | Responsabilidade |
|---------|---------|------------------|
| **EmailService** | `email_service.py` | Envio de e-mails transacionais |
| **WhatsAppService** | `whatsapp_service.py` | Integração com WhatsApp Business |
| **MercadoPagoService** | `mercadopago_service.py` | Checkout e webhooks de pagamento |
| **FiscalService** | `fiscal_service.py` | Emissão de documentos fiscais |
| **NPSService** | `nps_service.py` | Pesquisas de satisfação |
| **HealthScoreService** | `health_score_service.py` | Cálculo de health score de clientes |
| **CacheService** | `cache_service.py` | Gerenciamento de cache Redis |
| **TenantProvisioningService** | `tenant_provisioning.py` | Provisionamento de novos tenants |

---

## 3. Frontend CRM - Componentes

```mermaid
flowchart TB
    subgraph Frontend["🌐 Vue.js Frontend"]
        subgraph Views["📄 Views (49)"]
            V_DASH["DashboardView"]
            V_CLI["ClientesView"]
            V_COT["CotacoesView"]
            V_PED["PedidosView"]
            V_MOT["MotoristasView"]
            V_OUTROS["+ 44 views"]
        end
        
        subgraph Components["🧩 Components (9)"]
            C_SIDEBAR["Sidebar"]
            C_NAVBAR["Navbar"]
            C_TABLE["DataTable"]
            C_FORM["FormComponents"]
            C_MODAL["ModalComponents"]
        end
        
        subgraph Stores["🗄️ Pinia Stores (3)"]
            S_AUTH["authStore<br/>JWT, User"]
            S_TENANT["tenantStore<br/>Tenant context"]
            S_UI["uiStore<br/>UI State"]
        end
        
        subgraph Services["🔌 API Services (2)"]
            API_SVC["api.js<br/>Axios instance"]
            AUTH_SVC["auth.js<br/>Auth helpers"]
        end
        
        subgraph Composables["♻️ Composables (2)"]
            COMP_1["useApi"]
            COMP_2["useAuth"]
        end
        
        subgraph Router["🛤️ Vue Router"]
            ROUTES["routes.js<br/>Route definitions"]
            GUARDS["Navigation Guards"]
        end
    end
    
    Views --> Components
    Views --> Stores
    Views --> Composables
    
    Stores --> Services
    Composables --> Services
    
    Router --> Views
    GUARDS --> S_AUTH
    
    Services --> API[/"Backend API"/]
```

---

## 4. Interações Entre Componentes

### 4.1 Fluxo de Criação de Cotação

```mermaid
sequenceDiagram
    participant V as CotacoesView
    participant S as apiService
    participant R as cotacoes.router
    participant UC as CriarCotacaoUseCase
    participant REPO as CotacaoRepository
    participant DB as PostgreSQL
    participant WA as WhatsAppService
    
    V->>S: createCotacao(data)
    S->>R: POST /cotacoes
    R->>UC: execute(CotacaoCreateDTO)
    UC->>UC: Validate business rules
    UC->>REPO: create(cotacao_entity)
    REPO->>DB: INSERT INTO cotacoes
    DB-->>REPO: Created
    REPO-->>UC: CotacaoEntity
    UC->>WA: notify(cotacao)
    WA-->>UC: Sent
    UC-->>R: CotacaoResponseDTO
    R-->>S: JSON Response
    S-->>V: Cotacao created
```

### 4.2 Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant U as User
    participant V as LoginView
    participant S as authStore
    participant R as auth.router
    participant M as TenantMiddleware
    participant DB as PostgreSQL
    
    U->>V: Submit credentials
    V->>S: login(email, password)
    S->>R: POST /auth/login
    R->>DB: Verify credentials
    DB-->>R: User + Tenant
    R->>R: Generate JWT
    R-->>S: {token, user, tenant}
    S->>S: Store in localStorage
    S-->>V: Authenticated
    
    Note over S,M: Subsequent Requests
    V->>R: Request + JWT Header
    M->>M: Extract tenant from JWT
    M->>R: Inject tenant_context
```

---

## 5. Dependências Entre Componentes

```mermaid
graph TD
    subgraph "Dependency Flow"
        ROUTER[Router] --> USECASE[Use Case]
        ROUTER --> SERVICE[Service]
        USECASE --> REPOSITORY[Repository]
        USECASE --> DTO[DTO]
        REPOSITORY --> ENTITY[Entity]
        REPOSITORY --> DATABASE[Database]
        SERVICE --> EXTERNAL[External API]
        SERVICE --> DATABASE
    end
    
    subgraph "Inversion of Control"
        USECASE -.->|depends on| INTERFACE[IRepository]
        REPOSITORY -.->|implements| INTERFACE
    end
```

---

## 6. Componentes por Módulo de Negócio

| Módulo | Router | Service | Use Cases | Entities |
|--------|--------|---------|-----------|----------|
| **Autenticação** | auth.py | - | - | User |
| **Clientes** | clientes.py | - | 4 | Cliente |
| **Cotações** | cotacoes.py | - | 3 | Cotacao |
| **Pedidos** | pedidos.py | - | - | Pedido |
| **Motoristas** | motoristas.py | - | - | Motorista |
| **Veículos** | veiculos.py | - | - | Veiculo |
| **Entregas** | entregas.py | - | - | Entrega |
| **Fiscal** | fiscal.py | FiscalService | - | CTe, MDFe |
| **WhatsApp** | whatsapp.py | WhatsAppService | - | Mensagem |
| **GPS** | gps_tracking.py | - | - | Localizacao |
| **Billing** | billing.py | MercadoPagoService | - | Subscription |
| **NPS** | nps.py | NPSService | - | Survey |

---

*Documento parte da documentação arquitetural do LogiFlow CRM - Modelo C4*
