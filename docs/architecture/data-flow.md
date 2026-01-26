# Diagrama de Fluxo de Dados (Data Flow)

## 1) Autenticação (login + uso de token)

```mermaid
sequenceDiagram
  autonumber
  participant U as Usuário (CRM/App)
  participant API as FastAPI API
  participant DB as Database

  U->>API: POST /api/v1/auth/login (email, senha)
  API->>DB: SELECT User by email
  DB-->>API: User + senha_hash
  API-->>U: access_token (JWT) + refresh_token

  U->>API: GET /api/v1/auth/me (Authorization: Bearer)
  API->>API: validar JWT / carregar usuário
  API-->>U: dados do usuário
```

## 2) Emissão de CT-e (Fiscal)

```mermaid
sequenceDiagram
  autonumber
  participant U as Usuário Interno
  participant API as FastAPI API
  participant T as TenantMiddleware
  participant DB as Database
  participant IM as integration_manager
  participant FN as Focus NFe

  U->>API: POST /api/v1/fiscal/cte/emitir (payload)
  API->>T: resolve tenant (JWT/header)
  T-->>API: tenant_id
  API->>IM: obter credencial FocusNFe por tenant
  IM->>DB: SELECT TenantCredentials
  DB-->>IM: token/config
  IM-->>API: client configurado
  API->>FN: emitir CT-e
  FN-->>API: ref + status
  API-->>U: resultado emissão
```

## 3) Cotação -> Pedido (fluxo operacional atual)

```mermaid
sequenceDiagram
  autonumber
  participant U as Usuário Interno
  participant API as FastAPI API
  participant C as Router Cotações
  participant P as Router Pedidos

  U->>API: POST /api/v1/cotacoes (CriarCotacaoRequest)
  API->>C: criar cotação
  C-->>U: cotação (status=rascunho)

  U->>API: POST /api/v1/cotacoes/{id}/enviar
  API->>C: enviar cotação
  C-->>U: cotação (status=enviada)

  U->>API: POST /api/v1/cotacoes/{id}/aprovar (criar_pedido=true)
  API->>C: aprovar cotação
  Note over C,P: Na implementação atual a criação do pedido é simulada
  C-->>U: cotação convertida + pedido_id simulado
```

## 4) Notificações assíncronas (Celery)

```mermaid
sequenceDiagram
  autonumber
  participant API as FastAPI API
  participant R as Redis
  participant W as Celery Worker
  participant WA as Evolution API

  API->>R: publica tarefa (ex: notificar status)
  W->>R: consome tarefa
  W->>WA: envia mensagem WhatsApp
  WA-->>W: status envio
```
