# ⚡ Como Configurar Melhor Envio - Guia Rápido

## 📋 Checklist

- [ ] **Passo 1**: Obter token do Melhor Envio
- [ ] **Passo 2**: Configurar no `.env`
- [ ] **Passo 3**: Reiniciar backend
- [ ] **Passo 4**: Testar integração

---

## 🔑 Passo 1: Obter Token da API

### 1.1. Acesse o Painel do Melhor Envio

👉 **Link**: https://melhorenvio.com.br/painel

Faça login com sua conta do e-commerce.

### 1.2. Gerar Token de API

1. No menu lateral, procure por **"API"** ou **"Integrações"**
2. Clique em **"Criar novo token"** ou **"Gerar token"**
3. Dê um nome: `LogiFlow CRM`
4. **Selecione as permissões** (IMPORTANTE):
   - ✅ `shipping-calculate` (Calcular frete) - **OBRIGATÓRIO**
   - ✅ `companies-read` (Ler transportadoras)
   - ✅ `cart-read` (Ler carrinho)
   - ✅ `cart-write` (Escrever carrinho)
   - ✅ `agencies-read` (Ler agências - opcional)
   - ✅ `tracking-read` (Rastreamento - opcional)

5. Clique em **"Gerar"**
6. **⚠️ COPIE O TOKEN AGORA!** Ele só será exibido uma vez

**Token será parecido com:**
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTYiLCJqdGkiOiJhYmMxMjM...
```

---

## ⚙️ Passo 2: Configurar no Backend

### 2.1. Editar arquivo `.env`

Abra o arquivo:
```
LogiFlow CRM/backend/.env
```

### 2.2. Adicionar/Editar as linhas:

```env
# ===== MELHOR ENVIO =====
MELHOR_ENVIO_TOKEN=cole_seu_token_aqui
MELHOR_ENVIO_SANDBOX=false
```

**Exemplo real:**
```env
MELHOR_ENVIO_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTYiLCJqdGkiOiJhYmMxMjM...
MELHOR_ENVIO_SANDBOX=false
```

⚠️ **IMPORTANTE**: 
- `MELHOR_ENVIO_SANDBOX=false` = Produção (usa créditos reais)
- `MELHOR_ENVIO_SANDBOX=true` = Testes (ambiente sandbox)

### 2.3. Salvar o arquivo

---

## 🔄 Passo 3: Reiniciar o Backend

### Opção A: Docker (Recomendado)

```bash
cd "LogiFlow CRM"
docker-compose restart api
```

### Opção B: Sem Docker

```bash
cd "LogiFlow CRM/backend"
# Se estiver rodando, pare (Ctrl+C) e inicie novamente:
python -m uvicorn main:app --reload
```

---

## 🧪 Passo 4: Testar a Integração

### Opção 1: Script de Teste Automático (Recomendado)

```bash
cd "LogiFlow CRM/backend"
python scripts/test_melhor_envio.py
```

**Você verá:**
```
============================================================
🧪 TESTE MELHOR ENVIO - LogiFlow CRM
============================================================

✅ Token configurado: eyJ0eXAiOiJKV1QiLCJh...
✅ Sandbox: NÃO

============================================================
📦 TESTE 1: Cotação Simples
============================================================

📍 Origem: 01310100
📍 Destino: 04547130
⚖️  Peso: 5.0 kg

⏳ Calculando...

✅ 4 cotações encontradas:

1. ✅ Correios - PAC
   💰 R$ 25.50
   📅 8 dias úteis

2. ✅ Correios - SEDEX
   💰 45.80
   📅 3 dias úteis

3. ✅ Jadlog - Econômico
   💰 35.20
   📅 5 dias úteis

4. ✅ Azul Cargo - Azul
   💰 52.00
   📅 2 dias úteis

============================================================
```

### Opção 2: Testar via Swagger UI

1. Acesse: http://localhost:8000/docs
2. Encontre: `POST /api/v1/melhor-envio/cotacao-simples`
3. Clique em **"Try it out"**
4. Cole este JSON:
```json
{
  "origem_cep": "01310100",
  "destino_cep": "04547130",
  "peso_kg": 5,
  "valor_mercadoria": 100
}
```
5. Clique em **"Execute"**
6. Verifique a resposta (deve retornar cotações)

### Opção 3: Testar via Frontend

1. Acesse: http://localhost:3000/cotacao-automatica
2. Preencha:
   - **CEP Origem**: `01310-100`
   - **CEP Destino**: `04547-130`
   - **Peso**: `5` kg
   - ✅ Marque: **"Incluir Melhor Envio"**
3. Clique em **"Calcular Frete"**
4. Veja as cotações aparecerem

---

## ✅ Verificação de Sucesso

Se tudo funcionou, você deve ver:

✅ Cotações retornadas com valores reais
✅ Várias transportadoras (Correios, Jadlog, Azul Cargo)
✅ Prazos de entrega
✅ Preços diferentes para cada serviço

---

## ❌ Troubleshooting

### Erro: "Token inválido" ou "Unauthorized"

**Solução:**
1. Verifique se copiou o token completo (pode ser longo!)
2. Gere um novo token no painel Melhor Envio
3. Certifique-se de que selecionou a permissão `shipping-calculate`

### Erro: "CEP não encontrado"

**Solução:**
- Use CEPs válidos
- Remova caracteres especiais (apenas números: `01310100`)

### Erro: "No shipping options available"

**Solução:**
- Verifique se o peso não está muito alto (limite ~300kg)
- Teste com valores menores primeiro

### Erro: 429 (Too Many Requests)

**Solução:**
- Aguarde alguns minutos
- O sistema tem cache de 1 hora para cotações iguais

---

## 📊 Próximos Passos

Após configurar o Melhor Envio:

1. ✅ **Configurado!** Melhor Envio está funcionando
2. 🔄 Configure **Frenet** (cotação alternativa)
3. 📐 Implemente **Tabela Própria** (para comparar com sua frota)
4. 🚚 Integre com **Módulo de Pedidos** (cotação → pedido automático)

---

## 📞 Precisa de Ajuda?

- **Documentação Melhor Envio**: https://docs.melhorenvio.com.br/
- **Suporte Melhor Envio**: https://melhorenvio.com.br/suporte
- **Documentação LogiFlow**: Veja `docs/MELHOR_ENVIO_SETUP.md`

---

**Pronto! 🎉**

Sua integração com Melhor Envio está configurada!

