# 🔐 Configurar OAuth2 no SuiteCRM - Guia Passo a Passo

## 📋 Pré-requisitos

- ✅ SuiteCRM 8.6.1 instalado e rodando
- ✅ Acesso admin ao SuiteCRM
- ✅ Backend FastAPI instalado

---

## 🚀 Passo 1: Criar OAuth2 Client no SuiteCRM

### 1.1. Acessar Admin Panel

1. Faça login no SuiteCRM como **Admin**
2. Clique no menu **Admin** (canto superior direito)
3. Role até a seção **System**
4. Clique em **OAuth2 Clients and Tokens**

```
URL: http://localhost:8080/index.php?module=OAuth2Clients&action=index
```

### 1.2. Criar Novo Client

1. Clique no botão **Create OAuth2 Client**
2. Preencha os campos:

```
Name: LogiFlow Backend API
Client Type: Confidential
```

3. **IMPORTANTE:** Anote as credenciais geradas:
   - **Client ID** (UUID, ex: `123e4567-e89b-12d3-a456-426614174000`)
   - **Client Secret** (String longa, ex: `abc123def456...`)

4. Clique em **Save**

### 1.3. Configurar Permissões (Opcional)

Se quiser restringir permissões:
1. Vá em **Roles** 
2. Crie uma role específica para API
3. Associe ao OAuth2 Client

**Recomendação:** Para desenvolvimento, use permissões de admin.

---

## 🔧 Passo 2: Configurar Backend FastAPI

### 2.1. Editar arquivo `.env`

Navegue até:
```
C:\Users\leona\OneDrive\Documentos\Projetos\LogiFlow\LogiFlow CRM\backend\.env
```

Se não existir, copie de `.env.example`:
```bash
cd "C:\Users\leona\OneDrive\Documentos\Projetos\LogiFlow\LogiFlow CRM\backend"
copy .env.example .env
```

### 2.2. Adicionar Credenciais OAuth2

Edite o arquivo `.env` e adicione:

```env
# SuiteCRM OAuth2
SUITECRM_URL=http://localhost:8080
SUITECRM_CLIENT_ID=seu_client_id_aqui
SUITECRM_CLIENT_SECRET=seu_client_secret_aqui
```

**Exemplo real:**
```env
SUITECRM_URL=http://localhost:8080
SUITECRM_CLIENT_ID=123e4567-e89b-12d3-a456-426614174000
SUITECRM_CLIENT_SECRET=abc123def456ghi789jkl012mno345pqr678stu901vwx234
```

### 2.3. Salvar e Verificar

```bash
# Verificar se .env está correto
cat .env | grep SUITECRM
```

---

## ✅ Passo 3: Testar Integração

### 3.1. Executar Script de Teste

```bash
cd "C:\Users\leona\OneDrive\Documentos\Projetos\LogiFlow\LogiFlow CRM\backend"

python tests/test_suitecrm_integration.py
```

### 3.2. Resultado Esperado

```
🧪 INICIANDO TESTES DE INTEGRAÇÃO SUITECRM
================================================================================
✅ PASSOU | Teste 01 - Conexão - Conectado em http://localhost:8080
✅ PASSOU | Teste 02 - Listar Cotacoes - Encontradas 0 cotações
✅ PASSOU | Teste 03 - Criar Cotacao - Cotação criada com ID: abc-123
...

📊 RELATÓRIO FINAL DE TESTES
================================================================================
Total de Testes: 12
✅ Sucessos: 12
❌ Falhas: 0
📈 Taxa de Sucesso: 100.0%
================================================================================

🎉 TODOS OS TESTES PASSARAM! Integração 100% funcional!
```

### 3.3. Se Houver Erro

**Erro comum 1:** `401 Unauthorized`
```
Solução: Verifique Client ID e Secret no .env
```

**Erro comum 2:** `Connection refused`
```
Solução: Verifique se SuiteCRM está rodando em http://localhost:8080
```

**Erro comum 3:** `Module not found`
```
Solução: Execute Quick Repair no SuiteCRM Admin
Admin → Repair → Quick Repair and Rebuild
```

---

## 🧪 Passo 4: Testar Manualmente via API

### 4.1. Obter Token

```bash
curl -X POST http://localhost:8080/Api/access_token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=SEU_CLIENT_ID" \
  -d "client_secret=SEU_CLIENT_SECRET"
```

**Resposta esperada:**
```json
{
  "token_type": "Bearer",
  "expires_in": 3600,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4.2. Listar Cotações

```bash
curl -X GET http://localhost:8080/Api/V8/module/Cotacoes \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/vnd.api+json"
```

### 4.3. Criar Cotação

```bash
curl -X POST http://localhost:8080/Api/V8/module/Cotacoes \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "Cotacoes",
      "attributes": {
        "name": "Teste API",
        "status": "aberta"
      }
    }
  }'
```

---

## 📊 Passo 5: Testar via Backend FastAPI

### 5.1. Iniciar Backend

```bash
cd "C:\Users\leona\OneDrive\Documentos\Projetos\LogiFlow\LogiFlow CRM\backend"

uvicorn main:app --reload
```

### 5.2. Testar Endpoint de Status

```bash
curl http://localhost:8000/api/suitecrm/status
```

**Resposta esperada:**
```json
{
  "success": true,
  "data": {
    "success": true,
    "message": "Conexão estabelecida com sucesso",
    "base_url": "http://localhost:8080",
    "token_valid": true
  },
  "timestamp": "2025-12-15T22:00:00"
}
```

### 5.3. Testar Listagem de Módulos

```bash
# Listar cotações
curl http://localhost:8000/api/suitecrm/modules/Cotacoes

# Listar pedidos
curl http://localhost:8000/api/suitecrm/modules/PedidosFrete

# Listar motoristas
curl http://localhost:8000/api/suitecrm/modules/Motoristas
```

---

## 🔒 Segurança - Boas Práticas

### ✅ DO (Faça):

1. **Nunca commite o `.env`**
   - Adicione ao `.gitignore`
   - Use `.env.example` como template

2. **Use HTTPS em produção**
   ```env
   SUITECRM_URL=https://crm.seudominio.com
   ```

3. **Rotacione credenciais periodicamente**
   - A cada 90 dias
   - Ou se suspeitar de vazamento

4. **Use variáveis de ambiente**
   - No Render/Heroku/AWS
   - Nunca hardcode credenciais

### ❌ DON'T (Não faça):

1. ❌ Compartilhar Client Secret
2. ❌ Commitar credenciais no Git
3. ❌ Usar HTTP em produção
4. ❌ Deixar OAuth2 Client sem nome claro

---

## 🐛 Troubleshooting

### Problema: Token expira muito rápido

**Solução:** O token JWT tem validade de 1h por padrão. O service renova automaticamente.

### Problema: Rate limiting (429)

**Solução:** SuiteCRM tem limite de requisições. Adicione delay entre chamadas:
```python
await asyncio.sleep(0.1)  # 100ms delay
```

### Problema: Módulo não encontrado

**Solução:**
1. Verificar se módulos estão habilitados:
   ```
   Admin → Display Modules and Subpanels
   ```

2. Executar Quick Repair:
   ```
   Admin → Repair → Quick Repair and Rebuild
   ```

3. Verificar nome exato do módulo:
   ```python
   # CERTO:
   module="Cotacoes"
   
   # ERRADO:
   module="LF_Cotacoes"
   module="cotacoes"
   ```

---

## 📚 Referências

### Documentação Oficial

- [SuiteCRM API V8](https://docs.suitecrm.com/developer/api/api-v8/)
- [OAuth2 SuiteCRM](https://docs.suitecrm.com/admin/administration-panel/oauth2/)

### Arquivos do Projeto

- **Service:** `backend/services/suitecrm_service.py`
- **Endpoints:** `backend/routers/suitecrm.py`
- **Config:** `backend/config.py`
- **Testes:** `backend/tests/test_suitecrm_integration.py`

---

## ✅ Checklist Final

Antes de considerar a integração completa:

- [ ] OAuth2 Client criado no SuiteCRM
- [ ] Credenciais adicionadas no `.env`
- [ ] `.env` adicionado ao `.gitignore`
- [ ] Script de teste executado com sucesso
- [ ] Teste manual via cURL funcionando
- [ ] Backend FastAPI conectando ao SuiteCRM
- [ ] Todos os 6 módulos acessíveis
- [ ] Criar/Editar/Deletar funcionando

---

## 🎉 Próximos Passos

Após configurar OAuth2:

1. ✅ **Testar CRUD completo**
   - Criar, Ler, Atualizar, Deletar

2. ✅ **Configurar Sincronização**
   - Schedulers para sync periódico
   - Webhooks para eventos em tempo real

3. ✅ **Integrar com Frontend Vue**
   - Consumir endpoints do FastAPI
   - Exibir dados do SuiteCRM na UI

4. ✅ **Monitorar Performance**
   - Logs de requisições
   - Tempo de resposta
   - Taxa de erro

---

**Tempo estimado para configuração completa: 15-20 minutos** ⏱️

**Dificuldade: Fácil** 👍
