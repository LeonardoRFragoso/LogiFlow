# Integrações ERP - LogiFlow CRM

## Visão Geral

O LogiFlow CRM oferece integração nativa com os principais ERPs do mercado brasileiro, permitindo sincronização automática de clientes, pedidos e dados financeiros.

## ERPs Suportados

### 1. Omie ERP

**Prioridade:** Alta (Market share PME)  
**Complexidade:** Baixa (API REST bem documentada)

#### Configuração

1. Obtenha as credenciais no painel Omie:
   - Acesse: Configurações > Integrações > API
   - Gere um novo App Key e App Secret

2. Configure no `.env`:
```env
OMIE_APP_KEY=seu_app_key_aqui
OMIE_APP_SECRET=seu_app_secret_aqui
```

#### Funcionalidades

- ✅ Sincronização de clientes (bidirecional)
- ✅ Criação de pedidos de venda
- ✅ Consulta de serviços cadastrados
- ✅ Criação de ordens de serviço
- ✅ Mapeamento automático de campos

#### Endpoints Disponíveis

```
GET  /erp/omie/clientes              - Lista clientes do Omie
POST /erp/omie/clientes/sincronizar  - Sincroniza cliente LogiFlow → Omie
GET  /erp/omie/pedidos               - Lista pedidos do Omie
POST /erp/omie/pedidos/sincronizar   - Sincroniza pedido LogiFlow → Omie
```

#### Exemplo de Uso

```python
import requests

# Sincronizar cliente
response = requests.post(
    "http://localhost:8000/erp/omie/clientes/sincronizar",
    json={
        "cliente_id": "abc123",
        "nome": "Transportadora XYZ Ltda",
        "cnpj": "12345678000190",
        "ie": "123456789",
        "telefone": "11999999999",
        "email": "contato@xyz.com.br",
        "endereco": "Rua Exemplo",
        "numero": "100",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "uf": "SP",
        "cep": "01310100"
    }
)
```

---

### 2. Bling ERP

**Prioridade:** Alta (E-commerce e PME)  
**Complexidade:** Baixa (API REST v3)

#### Configuração

1. Obtenha o token OAuth2 no painel Bling:
   - Acesse: Configurações > API > Aplicações
   - Crie uma nova aplicação e gere o Access Token

2. Configure no `.env`:
```env
BLING_ACCESS_TOKEN=seu_access_token_aqui
```

#### Funcionalidades

- ✅ Sincronização de contatos (clientes/fornecedores)
- ✅ Criação de pedidos de venda
- ✅ Gestão de produtos/serviços
- ✅ Emissão de NFS-e
- ✅ Mapeamento automático de campos

#### Endpoints Disponíveis

```
GET  /erp/bling/contatos              - Lista contatos do Bling
POST /erp/bling/contatos/sincronizar  - Sincroniza cliente LogiFlow → Bling
GET  /erp/bling/pedidos               - Lista pedidos do Bling
POST /erp/bling/pedidos/sincronizar   - Sincroniza pedido LogiFlow → Bling
```

#### Exemplo de Uso

```python
import requests

# Sincronizar cliente
response = requests.post(
    "http://localhost:8000/erp/bling/contatos/sincronizar",
    json={
        "cliente_id": "abc123",
        "nome": "Transportadora ABC Ltda",
        "cnpj": "12345678000190",
        "telefone": "11999999999",
        "email": "contato@abc.com.br",
        "endereco": "Av. Paulista",
        "numero": "1000",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "uf": "SP",
        "cep": "01310100"
    }
)
```

---

## Fluxos de Sincronização

### LogiFlow → ERP

**Quando sincronizar:**
- Novo cliente cadastrado no LogiFlow
- Pedido aprovado e convertido
- Atualização de dados cadastrais

**Processo:**
1. Cliente/Pedido criado no LogiFlow
2. Webhook dispara sincronização
3. Dados são mapeados para formato do ERP
4. API do ERP é chamada (upsert)
5. ID do ERP é armazenado no LogiFlow

### ERP → LogiFlow

**Quando sincronizar:**
- Pagamento recebido no ERP
- Novo cliente cadastrado no ERP
- Atualização de status financeiro

**Processo:**
1. Webhook do ERP notifica LogiFlow
2. Dados são consultados via API
3. Mapeamento reverso é aplicado
4. Registro é atualizado no LogiFlow

---

## Mapeamento de Campos

### Cliente LogiFlow → Omie

| LogiFlow | Omie |
|----------|------|
| `id` | `codigo_cliente_integracao` |
| `nome` | `razao_social` |
| `nome_fantasia` | `nome_fantasia` |
| `cnpj/cpf` | `cnpj_cpf` |
| `ie` | `inscricao_estadual` |
| `telefone` | `telefone1_numero` |
| `email` | `email` |
| `endereco` | `endereco` |
| `numero` | `endereco_numero` |
| `bairro` | `bairro` |
| `cidade` | `cidade` |
| `uf` | `estado` |
| `cep` | `cep` |

### Cliente LogiFlow → Bling

| LogiFlow | Bling |
|----------|-------|
| `id` | `codigo` |
| `nome` | `nome` |
| `cnpj/cpf` | `numeroDocumento` |
| `ie` | `ie.inscricaoEstadual` |
| `telefone` | `telefone` |
| `celular` | `celular` |
| `email` | `email` |
| `endereco` | `endereco.endereco` |
| `numero` | `endereco.numero` |
| `bairro` | `endereco.bairro` |
| `cidade` | `endereco.municipio` |
| `uf` | `endereco.uf` |
| `cep` | `endereco.cep` |

---

## Webhooks

### Configurar Webhook no Omie

1. Acesse: Configurações > Integrações > Webhooks
2. Adicione a URL: `https://api.logiflow.com.br/webhooks/omie`
3. Selecione eventos:
   - Cliente incluído/alterado
   - Pedido incluído/alterado
   - Pagamento recebido

### Configurar Webhook no Bling

1. Acesse: Configurações > API > Webhooks
2. Adicione a URL: `https://api.logiflow.com.br/webhooks/bling`
3. Selecione eventos:
   - Contato criado/atualizado
   - Pedido criado/atualizado
   - Pagamento recebido

---

## Verificar Status das Integrações

```bash
curl http://localhost:8000/erp/status
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "omie": {
      "configurado": true,
      "ativo": true
    },
    "bling": {
      "configurado": true,
      "ativo": true
    }
  }
}
```

---

## Tratamento de Erros

### Erros Comuns

**1. Credenciais inválidas**
```json
{
  "success": false,
  "error": "Token inválido ou expirado"
}
```
**Solução:** Verifique as credenciais no `.env`

**2. Cliente já existe**
```json
{
  "success": false,
  "error": "Cliente com este CNPJ já cadastrado"
}
```
**Solução:** Use o método de atualização ou upsert

**3. Campos obrigatórios faltando**
```json
{
  "success": false,
  "error": "Campo 'cnpj_cpf' é obrigatório"
}
```
**Solução:** Preencha todos os campos obrigatórios

---

## Logs e Monitoramento

Todos os eventos de sincronização são registrados em:
```
backend/logs/api_{date}.log
```

Exemplo de log:
```
2024-12-14 14:30:15 | INFO | Cliente sincronizado com Omie: Transportadora XYZ
2024-12-14 14:30:20 | INFO | Pedido sincronizado com Bling: PED-2024-00123
```

---

## Roadmap

### Próximas Integrações

- [ ] TOTVS Protheus (Q1 2025)
- [ ] Tiny ERP (Q2 2025)
- [ ] Sankhya (Q2 2025)
- [ ] SAP Business One (Q3 2025)

---

## Suporte

Para dúvidas sobre as integrações ERP:
- Email: suporte@logiflow.com.br
- Documentação: https://docs.logiflow.com.br/integracoes/erp
- API Reference: https://api.logiflow.com.br/docs
