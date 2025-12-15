# 📘 LogiFlow CRM - Contrato de API

## 📋 Visão Geral

Este documento define o contrato oficial da API do LogiFlow CRM, incluindo:
- Estrutura de URLs e versionamento
- Autenticação e autorização
- Headers obrigatórios e opcionais
- Formatos de requisição/resposta
- Códigos de status e tratamento de erros
- Rate limiting e quotas
- Integrações externas

---

## 🔗 URLs e Versionamento

### Base URL

```
[PRODUÇÃO]  https://api.logiflow.com.br
[STAGING]   https://staging-api.logiflow.com.br
[LOCAL]     http://localhost:8000
```

### Estrutura de Endpoints

Todos os endpoints seguem o padrão:

```
{BASE_URL}/api/{version}/{resource}
```

**Exemplo:**
```
GET https://api.logiflow.com.br/api/v1/entregas
POST https://api.logiflow.com.br/api/v1/cotacao-automatica/cotar
```

### Versionamento

- **Versão Atual**: `v1`
- **Formato**: Semântico (Major)
- **Header Alternativo**: `Accept: application/vnd.logiflow.v1+json` (opcional)

**Política de Versionamento:**
- Breaking changes → nova versão major (`v2`, `v3`)
- Novas features não-breaking → mesma versão
- Depreciação → 6 meses de aviso prévio
- Suporte → versões N e N-1

---

## 🔐 Autenticação

### JWT Bearer Token

Todos os endpoints (exceto públicos) requerem autenticação via JWT.

**Header:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Endpoints de Autenticação

#### 1. Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@empresa.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "dGhpc19pc19y...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### 2. Refresh Token

```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh": "dGhpc19pc19y..."
}
```

#### 3. Logout

```http
POST /api/v1/auth/logout
Authorization: Bearer {token}
```

### Endpoints Públicos (Sem Autenticação)

- `GET /health` - Healthcheck
- `GET /ready` - Readiness check
- `GET /api/v1/plans` - Listar planos disponíveis
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro

---

## 📝 Headers Obrigatórios

### Para Requisições Autenticadas

```http
Authorization: Bearer {jwt_token}
X-Tenant-ID: {tenant_id}
Content-Type: application/json
```

### Para Requisições Públicas

```http
Content-Type: application/json
```

### Headers Opcionais (Recomendados)

```http
X-Correlation-ID: {uuid}        # Rastreamento de requisições
Accept-Language: pt-BR          # Idioma preferido
User-Agent: LogiFlow-Client/1.0 # Identificação do cliente
```

---

## 🔑 Multi-Tenancy

### Identificação de Tenant

O tenant pode ser identificado de 3 formas (prioridade):

1. **JWT Claim** (recomendado)
   ```json
   {
     "tenant_id": 123,
     "user_id": 456,
     "role": "admin"
   }
   ```

2. **Subdomínio**
   ```
   https://empresa-abc.logiflow.com.br/api/v1/entregas
   → tenant_id extraído do subdomínio
   ```

3. **Header X-Tenant-ID** (fallback)
   ```http
   X-Tenant-ID: 123
   ```

### Isolamento de Dados

- **Todos** os recursos são isolados por tenant
- Tentativa de acessar dados de outro tenant → `403 Forbidden`
- Queries automáticas filtram por `tenant_id`

---

## 📊 Formatos de Requisição/Resposta

### Formato Padrão: JSON

```http
Content-Type: application/json
```

### Estrutura de Resposta de Sucesso

```json
{
  "success": true,
  "data": { ... },
  "message": "Operação realizada com sucesso",
  "timestamp": "2025-12-15T10:30:00Z",
  "correlation_id": "uuid-1234"
}
```

### Estrutura de Resposta de Erro

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "CEP inválido",
    "details": {
      "field": "origem_cep",
      "reason": "Formato esperado: 12345-678"
    }
  },
  "timestamp": "2025-12-15T10:30:00Z",
  "correlation_id": "uuid-1234"
}
```

---

## 🚦 Códigos de Status HTTP

### Sucesso (2xx)

- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado
- `202 Accepted` - Processamento assíncrono iniciado
- `204 No Content` - Sucesso sem corpo de resposta (DELETE)

### Erro do Cliente (4xx)

- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Não autorizado (sem permissão)
- `404 Not Found` - Recurso não encontrado
- `409 Conflict` - Conflito (ex: duplicata)
- `422 Unprocessable Entity` - Validação falhou
- `429 Too Many Requests` - Rate limit excedido

### Erro do Servidor (5xx)

- `500 Internal Server Error` - Erro interno
- `502 Bad Gateway` - Erro em integração externa
- `503 Service Unavailable` - Serviço temporariamente indisponível
- `504 Gateway Timeout` - Timeout em integração externa

---

## ⏱️ Rate Limiting

### Limites por Endpoint

| Endpoint | Limite | Janela |
|----------|--------|--------|
| `/auth/login` | 5 req | 5 min |
| `/auth/refresh` | 10 req | 5 min |
| `/auth/register` | 3 req | 1 hora |
| `/gps/*` | 100 req | 1 min |
| `/cotacao-automatica/*` | 30 req | 1 min |
| **Geral** | 100 req | 1 min |

### Headers de Rate Limit

Toda resposta inclui:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1671105000
```

### Quando Limite Excedido

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Limite de 5 requisições por 5 minutos excedido",
    "retry_after_seconds": 60
  }
}
```

---

## 🔌 Integrações Externas

### APIs Integradas

1. **Google Maps Distance Matrix**
   - Cálculo de distâncias e rotas
   - Quota: 1000 req/dia, 30k/mês
   - Custo: ~$0.005/req

2. **Melhor Envio**
   - Cotação de frete (Correios, Jadlog, Azul)
   - Credenciais por tenant

3. **Frenet**
   - Cotação de frete alternativa
   - Credenciais por tenant

4. **GPS Providers**
   - Sascar, Autotrac, Onixsat
   - Credenciais por tenant, criptografadas

5. **ERPs**
   - Omie, Bling
   - Credenciais por tenant

6. **Mercado Pago**
   - Pagamentos e assinaturas
   - Access token global + por tenant

7. **Evolution API**
   - WhatsApp Business
   - Credenciais por tenant

### Políticas de Integração

**Produção:**
- Integrações SEM credenciais → `400 Bad Request`
- Não é permitido usar mocks/simulações
- Monitoramento de quotas ativo

**Desenvolvimento:**
- Simulação permitida se `DEBUG=true`
- Avisos nos logs quando em mock

---

## 🔒 Segurança

### Headers de Segurança

```http
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; ...
```

### CORS

```http
Access-Control-Allow-Origin: https://app.logiflow.com.br
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH
Access-Control-Allow-Headers: Authorization, Content-Type, X-Tenant-ID
Access-Control-Allow-Credentials: true
```

### Criptografia

- **Em trânsito**: TLS 1.3
- **Senhas**: bcrypt (12 rounds)
- **Credenciais de integração**: Fernet (AES-128)
- **Tokens JWT**: HS256 (dev), RS256 (prod)

---

## 🛡️ RBAC (Controle de Acesso Baseado em Roles)

### Roles Disponíveis

- **admin** - Acesso total
- **manager** - Gerenciamento de recursos
- **user** - Uso padrão
- **motorista** - Apenas app do motorista
- **cliente** - Apenas portal do cliente

### Endpoints Protegidos

```http
GET /api/v1/admin/quotas
→ Requer role: admin
→ Requer permissão: admin:view_quotas
```

```http
DELETE /api/v1/tenant-credentials/{id}
→ Requer role: admin ou manager
→ Requer permissão: credentials:delete
```

---

## 📋 Melhores Práticas

### 1. Idempotência

**Use IDs únicos para operações críticas:**

```http
POST /api/v1/pedidos
X-Idempotency-Key: {uuid}
```

### 2. Paginação

**Para listas grandes:**

```http
GET /api/v1/entregas?page=1&per_page=50
```

**Resposta:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 1234,
    "total_pages": 25
  }
}
```

### 3. Filtros e Ordenação

```http
GET /api/v1/entregas?status=entregue&sort=-created_at&cliente_id=123
```

### 4. Campos Parciais (Field Selection)

```http
GET /api/v1/entregas?fields=id,numero_pedido,status
```

### 5. Webhooks

**Para eventos assíncronos:**

```http
POST /api/v1/webhooks/register

{
  "url": "https://empresa.com/webhook",
  "events": ["pedido.criado", "entrega.finalizada"]
}
```

---

## 🧪 Ambientes

### Desenvolvimento

```
BASE_URL=http://localhost:8000
DEBUG=true
SIMULATION_MODE=true
```

### Staging

```
BASE_URL=https://staging-api.logiflow.com.br
DEBUG=false
SIMULATION_MODE=false
```

### Produção

```
BASE_URL=https://api.logiflow.com.br
DEBUG=false
SIMULATION_MODE=false
REQUIRE_HTTPS=true
```

---

## 📚 Variáveis de Ambiente Obrigatórias

```env
# Aplicação
API_PREFIX=/api
API_VERSION=v1
SECRET_KEY=<strong-random-key>
DEBUG=false

# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost/logiflow
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET_KEY=<strong-jwt-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Integrações (Opcionais, mas recomendadas)
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=<api-key>
MELHOR_ENVIO_TOKEN=<token>
FRENET_TOKEN=<token>
MERCADOPAGO_ACCESS_TOKEN=<token>

# Multi-Tenancy
ENABLE_TENANT_ISOLATION=true
TENANT_RESOLUTION_METHOD=jwt,subdomain,header
```

---

## 📞 Suporte

- **Documentação Interativa**: `/docs` (Swagger UI)
- **Redoc**: `/redoc`
- **Status da API**: `GET /health`
- **Suporte Técnico**: suporte@logiflow.com.br

---

## 📝 Changelog

### v1 (Atual)

- ✅ API REST completa
- ✅ Autenticação JWT
- ✅ Multi-tenancy
- ✅ RBAC
- ✅ Rate limiting
- ✅ Monitoramento de quotas
- ✅ Integrações externas

---

**Última Atualização**: 15/12/2025
**Versão do Documento**: 1.0.0

