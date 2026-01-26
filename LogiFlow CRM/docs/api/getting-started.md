# LogiFlow CRM API - Quick Start Guide

> **Base URL:** `https://api.logiflow.com.br/api/v1`  
> **Swagger:** `https://api.logiflow.com.br/api/v1/docs`  
> **Versão:** 1.0.0

## Autenticação

A API usa **JWT Bearer Token** para autenticação.

### 1. Obter Token

```bash
curl -X POST "https://api.logiflow.com.br/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@empresa.com",
    "password": "sua_senha"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### 2. Usar Token nas Requisições

```bash
curl -X GET "https://api.logiflow.com.br/api/v1/clientes" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### 3. Refresh Token

```bash
curl -X POST "https://api.logiflow.com.br/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }'
```

---

## Endpoints Principais

### Clientes

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/clientes` | Listar clientes |
| `GET` | `/clientes/{id}` | Buscar cliente por ID |
| `POST` | `/clientes` | Criar cliente |
| `PATCH` | `/clientes/{id}` | Atualizar cliente |
| `DELETE` | `/clientes/{id}` | Remover cliente |

### Cotações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/cotacoes` | Listar cotações |
| `GET` | `/cotacoes/{id}` | Buscar cotação |
| `POST` | `/cotacoes` | Criar cotação |
| `PATCH` | `/cotacoes/{id}/aprovar` | Aprovar cotação |
| `PATCH` | `/cotacoes/{id}/recusar` | Recusar cotação |

### Pedidos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/pedidos` | Listar pedidos |
| `GET` | `/pedidos/{id}` | Buscar pedido |
| `PATCH` | `/pedidos/{id}/status` | Atualizar status |

### Rastreamento

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/rastreamento/{codigo}` | Rastrear entrega |
| `POST` | `/gps/tracking` | Atualizar localização GPS |

---

## Exemplos de Uso

### Criar Cliente

```bash
curl -X POST "https://api.logiflow.com.br/api/v1/clientes" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "cnpj": "12345678000190",
    "razao_social": "Empresa Exemplo LTDA",
    "email": "contato@empresa.com",
    "telefone": "11999998888",
    "endereco": "Rua Exemplo, 123 - São Paulo/SP"
  }'
```

**Resposta (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "cnpj": "12.345.678/0001-90",
  "razao_social": "Empresa Exemplo LTDA",
  "email": "contato@empresa.com",
  "telefone": "(11) 99999-8888",
  "created_at": "2026-01-26T10:00:00Z"
}
```

### Criar Cotação

```bash
curl -X POST "https://api.logiflow.com.br/api/v1/cotacoes" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "550e8400-e29b-41d4-a716-446655440000",
    "origem": {
      "cep": "01310100",
      "logradouro": "Av. Paulista",
      "numero": "1000",
      "bairro": "Bela Vista",
      "cidade": "São Paulo",
      "uf": "SP"
    },
    "destino": {
      "cep": "22041080",
      "logradouro": "Av. Atlântica",
      "numero": "500",
      "bairro": "Copacabana",
      "cidade": "Rio de Janeiro",
      "uf": "RJ"
    },
    "peso_kg": 10.5,
    "volumes": 2,
    "valor_mercadoria": 1500.00
  }'
```

### Aprovar Cotação

```bash
curl -X PATCH "https://api.logiflow.com.br/api/v1/cotacoes/{id}/aprovar" \
  -H "Authorization: Bearer {token}"
```

---

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| `200` | Sucesso |
| `201` | Criado com sucesso |
| `400` | Dados inválidos |
| `401` | Não autenticado |
| `403` | Sem permissão |
| `404` | Não encontrado |
| `422` | Erro de validação |
| `429` | Rate limit excedido |
| `500` | Erro interno |

## Rate Limiting

- **Limite:** 100 requests/minuto por IP
- **Header:** `X-RateLimit-Remaining` indica requests restantes
- **Resposta 429:** Aguarde `Retry-After` segundos

## Paginação

```bash
GET /clientes?skip=0&limit=100
```

**Resposta:**
```json
{
  "items": [...],
  "total": 250,
  "skip": 0,
  "limit": 100,
  "has_more": true
}
```

---

## Swagger UI

Acesse a documentação interativa em:
- **Desenvolvimento:** `http://localhost:8000/api/v1/docs`
- **Produção:** `https://api.logiflow.com.br/api/v1/docs`

## Suporte

- **Email:** suporte@logiflow.com.br
- **Docs:** https://docs.logiflow.com.br
