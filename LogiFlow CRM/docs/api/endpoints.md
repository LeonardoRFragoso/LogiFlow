# LogiFlow CRM API - Endpoints Reference

> Documentação completa de todos os endpoints da API

## Sumário

1. [Autenticação](#autenticação)
2. [Clientes](#clientes)
3. [Cotações](#cotações)
4. [Pedidos](#pedidos)
5. [Motoristas](#motoristas)
6. [Veículos](#veículos)
7. [Entregas](#entregas)
8. [Rastreamento GPS](#rastreamento-gps)
9. [Fiscal (CT-e/MDF-e)](#fiscal)
10. [WhatsApp](#whatsapp)
11. [Billing](#billing)
12. [Dashboard](#dashboard)

---

## Autenticação

### POST /auth/login
Autentica usuário e retorna tokens.

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "string",
    "nome": "string",
    "tipo": "admin|operador|motorista"
  }
}
```

### POST /auth/refresh
Renova access token.

### POST /auth/logout
Invalida refresh token.

### POST /auth/register
Registra novo usuário (requer admin).

---

## Clientes

### GET /clientes
Lista clientes do tenant.

**Query Parameters:**
- `skip` (int): Registros a pular (default: 0)
- `limit` (int): Limite por página (default: 100)
- `search` (string): Busca por nome/CNPJ

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "cnpj": "12.345.678/0001-90",
      "razao_social": "string",
      "email": "string",
      "telefone": "string",
      "ativo": true,
      "created_at": "datetime"
    }
  ],
  "total": 100,
  "skip": 0,
  "limit": 100,
  "has_more": false
}
```

### GET /clientes/{id}
Busca cliente por ID.

### POST /clientes
Cria novo cliente.

**Request:**
```json
{
  "cnpj": "12345678000190",
  "razao_social": "string (required)",
  "nome_fantasia": "string",
  "email": "email",
  "telefone": "string",
  "endereco": "string"
}
```

### PATCH /clientes/{id}
Atualiza cliente (campos parciais).

### DELETE /clientes/{id}
Remove cliente (soft delete).

---

## Cotações

### GET /cotacoes
Lista cotações.

**Query Parameters:**
- `status`: pendente|enviada|aprovada|recusada|expirada
- `cliente_id`: Filtrar por cliente

### GET /cotacoes/{id}
Busca cotação por ID.

### POST /cotacoes
Cria nova cotação.

**Request:**
```json
{
  "cliente_id": "uuid",
  "origem": {
    "cep": "01310100",
    "logradouro": "string",
    "numero": "string",
    "complemento": "string",
    "bairro": "string",
    "cidade": "string",
    "uf": "SP"
  },
  "destino": { ... },
  "peso_kg": 10.5,
  "volumes": 1,
  "valor_mercadoria": 1000.00,
  "observacoes": "string"
}
```

### PATCH /cotacoes/{id}/aprovar
Aprova cotação (cria pedido automaticamente).

### PATCH /cotacoes/{id}/recusar
Recusa cotação.

### PATCH /cotacoes/{id}/enviar
Envia cotação para cliente (email/WhatsApp).

---

## Pedidos

### GET /pedidos
Lista pedidos.

### GET /pedidos/{id}
Busca pedido.

### PATCH /pedidos/{id}/status
Atualiza status do pedido.

**Request:**
```json
{
  "status": "aguardando|em_separacao|coletado|em_transito|entregue|cancelado"
}
```

### PATCH /pedidos/{id}/atribuir
Atribui motorista e veículo.

**Request:**
```json
{
  "motorista_id": "uuid",
  "veiculo_id": "uuid",
  "data_coleta": "datetime"
}
```

---

## Motoristas

### GET /motoristas
Lista motoristas.

### GET /motoristas/disponiveis
Lista motoristas disponíveis.

### GET /motoristas/cnh-vencendo
Lista motoristas com CNH próxima do vencimento.

### POST /motoristas
Cria motorista.

**Request:**
```json
{
  "nome": "string",
  "cpf": "string",
  "cnh": "string",
  "cnh_categoria": "A|B|C|D|E",
  "cnh_validade": "date",
  "telefone": "string",
  "email": "string"
}
```

### PATCH /motoristas/{id}/status
Atualiza status (disponivel|em_rota|indisponivel|ferias).

---

## Veículos

### GET /veiculos
Lista veículos.

### GET /veiculos/disponiveis
Lista veículos disponíveis.

### POST /veiculos
Cria veículo.

**Request:**
```json
{
  "placa": "ABC1D23",
  "tipo": "van|truck|carreta",
  "marca": "string",
  "modelo": "string",
  "ano": 2024,
  "capacidade_kg": 1000,
  "capacidade_m3": 10
}
```

---

## Entregas

### GET /entregas
Lista entregas.

### GET /entregas/{id}
Busca entrega.

### PATCH /entregas/{id}/status
Atualiza status da entrega.

**Request:**
```json
{
  "status": "aguardando_coleta|coletado|em_transito|saiu_para_entrega|entregue|devolvido",
  "observacao": "string",
  "foto_comprovante": "base64"
}
```

---

## Rastreamento GPS

### GET /rastreamento/{codigo}
Rastreia entrega por código público.

**Response:**
```json
{
  "codigo": "LF1234567890",
  "status": "em_transito",
  "origem": "São Paulo/SP",
  "destino": "Rio de Janeiro/RJ",
  "previsao": "2026-01-27T14:00:00Z",
  "historico": [
    {
      "status": "coletado",
      "data": "2026-01-26T10:00:00Z",
      "local": "São Paulo/SP"
    }
  ],
  "localizacao_atual": {
    "latitude": -23.5505,
    "longitude": -46.6333,
    "atualizado_em": "2026-01-26T12:30:00Z"
  }
}
```

### POST /gps/tracking
Atualiza localização GPS (App Motorista).

**Request:**
```json
{
  "latitude": -23.5505,
  "longitude": -46.6333,
  "velocidade_kmh": 60,
  "precisao_metros": 10
}
```

---

## Fiscal

### POST /fiscal/cte
Emite CT-e.

### POST /fiscal/mdfe
Emite MDF-e.

### GET /fiscal/cte/{chave}
Consulta CT-e por chave.

### POST /fiscal/cte/{chave}/cancelar
Cancela CT-e.

---

## WhatsApp

### POST /whatsapp/send
Envia mensagem WhatsApp.

**Request:**
```json
{
  "to": "5511999998888",
  "message": "string",
  "template": "cotacao_enviada|pedido_confirmado|entrega_realizada"
}
```

### POST /whatsapp/webhook
Webhook para receber mensagens.

---

## Billing

### GET /billing/plans
Lista planos disponíveis.

### POST /billing/checkout
Cria checkout de pagamento.

### POST /billing/webhook
Webhook MercadoPago.

### GET /billing/subscription
Consulta assinatura atual.

---

## Dashboard

### GET /dashboard/stats
Estatísticas gerais.

**Response:**
```json
{
  "cotacoes_mes": 150,
  "pedidos_mes": 120,
  "entregas_mes": 115,
  "faturamento_mes": 45000.00,
  "taxa_conversao": 0.80,
  "nps_score": 72
}
```

### GET /dashboard/graficos
Dados para gráficos.

---

## Health Checks

### GET /health
Liveness probe.

### GET /ready
Readiness probe.

### GET /metrics
Métricas Prometheus (se habilitado).
