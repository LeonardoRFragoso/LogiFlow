# 📦 Guia de Configuração - Melhor Envio

## 🎯 Objetivo

Configurar a integração do LogiFlow CRM com a API do Melhor Envio para cotação automática de frete.

---

## 📝 Passo 1: Obter Token da API

### 1.1. Acesse o Painel do Melhor Envio

1. Entre em: https://melhorenvio.com.br/painel
2. Faça login com sua conta

### 1.2. Gerar Token de Acesso

1. No menu lateral, clique em **"Integrações"** ou **"API"**
2. Clique em **"Criar Token"** ou **"Novo Token"**
3. Dê um nome ao token: `LogiFlow CRM`
4. Selecione as permissões necessárias:
   - ✅ `cart-read` - Ler carrinho
   - ✅ `cart-write` - Escrever no carrinho
   - ✅ `shipping-calculate` - **Calcular frete (OBRIGATÓRIO)**
   - ✅ `shipping-preview` - Visualizar envios
   - ✅ `companies-read` - Ler transportadoras
   - ✅ `agencies-read` - Ler agências
   - ✅ `tracking-read` - Rastrear pedidos (opcional)

5. Clique em **"Gerar Token"**
6. **⚠️ IMPORTANTE**: Copie o token gerado imediatamente, ele só será exibido uma vez!

**Exemplo de token:**
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTYiLCJqdGkiOiI...
```

---

## 🔧 Passo 2: Configurar no Backend

### 2.1. Editar arquivo `.env`

Abra o arquivo `LogiFlow CRM/backend/.env` e adicione:

```env
# Melhor Envio
MELHOR_ENVIO_TOKEN=seu_token_aqui
MELHOR_ENVIO_SANDBOX=false
```

**Para Produção:**
```env
MELHOR_ENVIO_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTYiLCJqdGkiOiI...
MELHOR_ENVIO_SANDBOX=false
```

**Para Testes (Sandbox):**
```env
MELHOR_ENVIO_TOKEN=seu_token_sandbox
MELHOR_ENVIO_SANDBOX=true
```

### 2.2. Verificar `config.py`

O arquivo `backend/config.py` já deve ter:

```python
MELHOR_ENVIO_TOKEN: str = os.getenv("MELHOR_ENVIO_TOKEN", "")
MELHOR_ENVIO_SANDBOX: bool = os.getenv("MELHOR_ENVIO_SANDBOX", "true").lower() == "true"
```

---

## 🏢 Passo 3: Configurar por Tenant (Multi-Tenancy)

### 3.1. Via Interface Web

1. Acesse: **Configurações → Integrações**
2. Clique em **"Adicionar Credencial"**
3. Preencha:
   - **Tipo de Integração**: `freight` (Frete)
   - **Provider**: `melhor_envio`
   - **Credenciais**:
     ```json
     {
       "token": "seu_token_melhor_envio",
       "sandbox": false
     }
     ```
4. Clique em **"Salvar"**

### 3.2. Via API (Postman/cURL)

```bash
POST /api/v1/tenant-credentials/credentials
Authorization: Bearer {seu_jwt_token}
X-Tenant-ID: {seu_tenant_id}
Content-Type: application/json

{
  "integration_type": "freight",
  "provider": "melhor_envio",
  "credentials": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
    "sandbox": false
  }
}
```

---

## 🧪 Passo 4: Testar a Integração

### 4.1. Teste Manual via Swagger

1. Acesse: http://localhost:8000/docs
2. Encontre o endpoint: `POST /api/v1/melhor-envio/cotacao-simples`
3. Clique em **"Try it out"**
4. Envie:
   ```json
   {
     "origem_cep": "01310100",
     "destino_cep": "04547130",
     "peso_kg": 5,
     "valor_mercadoria": 100
   }
   ```
5. Verifique a resposta (deve retornar cotações de Correios, Jadlog, Azul Cargo, etc.)

### 4.2. Teste via Frontend

1. Acesse: http://localhost:3000/cotacao-automatica
2. Preencha o formulário:
   - **CEP Origem**: 01310-100 (Av. Paulista, SP)
   - **CEP Destino**: 04547-130 (Itaim Bibi, SP)
   - **Peso**: 5 kg
   - **Altura**: 20 cm
   - **Largura**: 30 cm
   - **Comprimento**: 40 cm
   - ✅ Marque: **"Incluir Melhor Envio"**
3. Clique em **"Calcular Frete"**
4. Verifique as cotações retornadas

### 4.3. Teste via cURL

```bash
curl -X POST "http://localhost:8000/api/v1/melhor-envio/cotacao-simples" \
  -H "Authorization: Bearer {seu_token}" \
  -H "X-Tenant-ID: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "origem_cep": "01310100",
    "destino_cep": "04547130",
    "peso_kg": 5,
    "valor_mercadoria": 100
  }'
```

**Resposta Esperada:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "PAC",
      "price": 25.50,
      "delivery_time": 8,
      "company": {
        "id": 1,
        "name": "Correios",
        "picture": "https://..."
      },
      "error": null
    },
    {
      "id": 2,
      "name": "SEDEX",
      "price": 45.80,
      "delivery_time": 3,
      "company": {
        "id": 1,
        "name": "Correios",
        "picture": "https://..."
      },
      "error": null
    }
  ]
}
```

---

## 📊 Passo 5: Verificar Uso e Limites

### 5.1. Dashboard Melhor Envio

- Acesse: https://melhorenvio.com.br/painel/estatisticas
- Verifique:
  - ✅ Número de cotações realizadas
  - ✅ Limites da conta
  - ✅ Custos (se aplicável)

### 5.2. Logs do Sistema

```bash
# No terminal do backend
docker-compose logs -f api | grep "melhor_envio"
```

---

## 🔍 Troubleshooting

### Erro: "Token inválido"

**Causa**: Token expirado ou incorreto

**Solução**:
1. Gere um novo token no painel Melhor Envio
2. Atualize o `.env`
3. Reinicie o backend: `docker-compose restart api`

### Erro: "Unauthorized"

**Causa**: Token sem permissões necessárias

**Solução**:
1. No painel Melhor Envio, edite o token
2. Marque a permissão `shipping-calculate`
3. Salve e use o novo token

### Erro: "CEP não encontrado"

**Causa**: CEP inválido ou fora da área de cobertura

**Solução**:
- Verifique se o CEP está correto
- Teste com CEPs conhecidos (ex: 01310-100)

### Erro: "No shipping options available"

**Causa**: Nenhuma transportadora atende a rota

**Solução**:
- Verifique peso e dimensões (podem estar fora dos limites)
- Teste com valores menores

### Erro: 429 (Rate Limit)

**Causa**: Muitas requisições em curto período

**Solução**:
- Aguarde alguns minutos
- Implemente cache de cotações (já está no código)

---

## 💡 Dicas de Uso

### 1. Cache de Cotações

O sistema já implementa cache de 1 hora para cotações idênticas. Aproveite!

### 2. Comparação com Tabela Própria

Use o endpoint `/comparar-tabela` para comparar preços do Melhor Envio com sua frota:

```json
{
  "origem_cep": "01310100",
  "destino_cep": "04547130",
  "peso_kg": 50,
  "valor_tabela_propria": 150.00
}
```

Resposta mostra se vale mais a pena terceirizar ou usar frota própria.

### 3. Prioridade por Preço ou Prazo

Use `/melhor-cotacao` para obter automaticamente a melhor opção:

```json
{
  "origem_cep": "01310100",
  "destino_cep": "04547130",
  "peso_kg": 10,
  "prioridade": "preco"  // ou "prazo"
}
```

---

## 📚 Documentação Oficial

- **API Melhor Envio**: https://docs.melhorenvio.com.br/
- **Painel**: https://melhorenvio.com.br/painel
- **Sandbox**: https://sandbox.melhorenvio.com.br/

---

## ✅ Checklist de Configuração

- [ ] Token gerado no painel Melhor Envio
- [ ] Permissão `shipping-calculate` habilitada
- [ ] Token adicionado ao `.env`
- [ ] Backend reiniciado
- [ ] Teste via Swagger executado com sucesso
- [ ] Teste via frontend executado com sucesso
- [ ] Credenciais salvas no tenant (se multi-tenancy)
- [ ] Logs verificados (sem erros)

---

## 🚀 Próximos Passos

Após configurar o Melhor Envio:

1. **Configurar Frenet** (cotação alternativa)
2. **Implementar cálculo de tabela própria** (comparação)
3. **Configurar webhooks** (rastreamento automático)
4. **Integrar com módulo de pedidos** (cotação → pedido)

---

**Configuração concluída!** 🎉

Agora o LogiFlow CRM está pronto para cotar fretes automaticamente via Melhor Envio.

