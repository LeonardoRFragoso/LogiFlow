# 🔄 Migração para Integration Manager Multi-Tenant

**Data:** 23 de Janeiro de 2026  
**Objetivo:** Migrar todas as integrações externas de variáveis de ambiente globais para configurações por tenant no banco de dados.

---

## ✅ Arquivos Modificados

### 1. **Backend - Modelo de Dados**

#### `backend/models.py`
**Modificação:** Adicionado modelo `TenantIntegration`
- Armazena credenciais criptografadas por tenant
- Campos: `api_key`, `access_token`, `config`, `environment`
- Tracking de uso: `request_count`, `last_request`
- Status de validação: `is_valid`, `validation_error`

---

### 2. **Backend - Serviços**

#### `backend/services/encryption_service.py` ✨ NOVO
**Criado:** Serviço de criptografia de credenciais
- Usa Fernet (AES-128) + PBKDF2
- Funções: `encrypt_api_key()`, `decrypt_api_key()`
- Requer variável `ENCRYPTION_KEY` no `.env`

#### `backend/services/integration_manager.py` ✨ NOVO
**Criado:** Gerenciador central de integrações
- `get_focusnfe_client(tenant_id, db)` → FocusNFeClient
- `get_melhor_envio_client(tenant_id, db)` → MelhorEnvioClient
- `get_frenet_client(tenant_id, db)` → FrenetClient
- `get_evolution_api_client(tenant_id, db)` → dict config
- `check_integration_configured(tenant_id, type, db)` → bool
- `get_integration_status(tenant_id, type, db)` → dict

#### `backend/services/whatsapp_service.py`
**Modificação:** Aceita config no construtor
- **Antes:** `WhatsAppService()` usava `settings` diretamente
- **Depois:** `WhatsAppService(api_url, api_key, instance_name)`
- Adicionado: `get_whatsapp_service_for_tenant(tenant_id, db)`

---

### 3. **Backend - Routers**

#### `backend/routers/integrations.py` ✨ NOVO
**Criado:** API REST para gerenciar integrações
- `POST /api/integrations` - Criar integração
- `GET /api/integrations` - Listar todas
- `GET /api/integrations/{type}` - Obter específica
- `PUT /api/integrations/{type}` - Atualizar
- `DELETE /api/integrations/{type}` - Deletar
- `POST /api/integrations/{type}/validate` - Testar conexão

#### `backend/routers/fiscal.py`
**Modificação:** Dependency `get_focusnfe_client` atualizada
- **Antes:** Buscava `settings.FOCUSNFE_TOKEN`
- **Depois:** Busca do banco via `get_tenant_focusnfe_client(current_user.tenant_id, db)`
- **Mensagem de erro:** "Focus NFe não configurado. Configure em Configurações > Integrações."

**Impacto:** Todos os 11 endpoints que usavam Focus NFe agora são multi-tenant:
- `/cte/emitir`, `/cte/{ref}`, `/cte/{ref}/pdf`, `/cte/{ref}/xml`
- `/mdfe/emitir`, `/mdfe/{ref}`, `/mdfe/{ref}/pdf`, `/mdfe/{ref}/xml`
- `/mdfe/{ref}/encerrar`, `/cte/{ref}` (DELETE), `/mdfe/{ref}` (DELETE)

#### `backend/routers/melhor_envio.py`
**Modificação:** Dependency `get_melhor_envio_client` atualizada
- **Antes:** Buscava `settings.MELHOR_ENVIO_TOKEN`
- **Depois:** Busca do banco via `get_tenant_melhor_envio_client(current_user.tenant_id, db)`
- **Mensagem de erro:** "Melhor Envio não configurado. Configure em Configurações > Integrações."

**Impacto:** Todos os endpoints de cotação são multi-tenant:
- `/calcular`, `/calcular-simples`, `/melhor-cotacao`, `/comparar-tabela`
- `/rastrear/{tracking_code}`, `/agencias`, `/status`

#### `backend/routers/cotacao_automatica.py`
**Modificação:** Endpoints principais atualizados
- **Antes:** Verificava `settings.MELHOR_ENVIO_TOKEN` e `settings.FRENET_TOKEN`
- **Depois:** Usa `check_integration_configured()` e `get_*_client()`
- **Mensagem de erro:** "Configure Melhor Envio ou Frenet em Configurações > Integrações."

**Impacto:** Endpoints multi-tenant:
- `POST /cotar` - Cotação consolidada
- `GET /frenet/cotar` - Cotação Frenet
- `GET /frenet/rastrear/{codigo}` - Rastreamento Frenet
- `GET /comparar` - Comparação de opções

**Nota:** Google Maps Distance Matrix ainda usa variável global (comentário TODO adicionado para migração futura)

---

### 4. **Frontend - Vue**

#### `frontend/src/views/configuracoes/IntegracoesView.vue`
**Modificação:** Atualizada para usar nova API `/api/integrations`
- Adicionado Focus NFe na aba "Frete"
- Select de ambiente (Homologação/Produção, Sandbox/Production)
- Links diretos para painéis dos serviços
- Validação em tempo real com botão "Testar"
- Funções atualizadas: `saveCredentials()`, `loadCredentials()`, `testConnection()`

**Novos providers configuráveis:**
- 📄 Focus NFe (CT-e/MDF-e)
- 📦 Melhor Envio (Cotação de frete)
- 🚚 Frenet (Cotação de frete)

---

## 🔐 Segurança Implementada

1. **Criptografia:** Todas as chaves são criptografadas com Fernet antes de salvar
2. **Isolamento:** Cada tenant vê apenas suas próprias credenciais
3. **Validação:** Sistema testa credenciais antes de aceitar
4. **Auditoria:** Registra quando e quantas vezes foi usado
5. **Permissões:** Apenas admins do tenant podem configurar

---

## 📋 Próximos Passos (Checklist)

### 1. Criar Migration ⚠️ OBRIGATÓRIO
```bash
cd backend
alembic revision --autogenerate -m "Add tenant_integrations table"
alembic upgrade head
```

### 2. Adicionar Variável de Ambiente ⚠️ OBRIGATÓRIO
```bash
# backend/.env
ENCRYPTION_KEY=seu-segredo-ultra-secreto-minimo-32-caracteres-aleatorios
```

**Gerar chave segura:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 3. Registrar Router ⚠️ OBRIGATÓRIO
```python
# backend/main.py
from routers import integrations

app.include_router(integrations.router)
```

### 4. Instalar Dependência (se necessário)
```bash
pip install cryptography
```

### 5. Atualizar Documentação para Usuários
- Compartilhar `GUIA_USUARIO_INTEGRACOES.md` com time de suporte
- Criar vídeo tutorial (opcional)

---

## 🔄 Compatibilidade com Código Legado

### Durante a Transição

As integrações mantêm compatibilidade com o código antigo:

```python
# ✅ FUNCIONA - Código antigo (usando settings)
from config import settings
token = settings.FOCUSNFE_TOKEN

# ✅ FUNCIONA - Código novo (multi-tenant)
from services.integration_manager import get_focusnfe_client
client = get_focusnfe_client(tenant_id, db)
```

### Comportamento

1. **Se integração configurada no banco:** Usa credenciais do tenant
2. **Se NÃO configurada no banco:** 
   - Retorna `None`
   - Endpoint retorna erro 400: "Configure em Configurações > Integrações"

### Migração Gradual

Não é necessário migrar tudo de uma vez. Você pode:
1. Rodar a migration
2. Configurar integrações por tenant gradualmente
3. Código legado continua funcionando (se `settings` tiver valor)

---

## 🧪 Testando a Migração

### Teste 1: Criar Integração
```bash
curl -X POST http://localhost:8000/api/integrations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "integration_type": "focusnfe",
    "api_token": "homologacao_abc123",
    "environment": "homologacao",
    "is_active": true
  }'
```

### Teste 2: Validar Integração
```bash
curl -X POST http://localhost:8000/api/integrations/focusnfe/validate \
  -H "Authorization: Bearer $TOKEN"
```

### Teste 3: Emitir CT-e (usando integração do tenant)
```bash
curl -X POST http://localhost:8000/api/fiscal/cte/emitir \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @cte_payload.json
```

---

## ⚠️ Erros Comuns e Soluções

### Erro: "Focus NFe não configurado"
**Causa:** Tenant não tem integração configurada  
**Solução:** Configure em **Configurações > Integrações** no frontend

### Erro: "ENCRYPTION_KEY não definida"
**Causa:** Variável não existe no `.env`  
**Solução:** Adicione `ENCRYPTION_KEY` com valor aleatório de 32+ caracteres

### Erro: Table 'tenant_integrations' doesn't exist
**Causa:** Migration não foi rodada  
**Solução:** Execute `alembic upgrade head`

### Erro: Import 'auth' not found
**Causa:** Falta módulo de autenticação  
**Solução:** Verifique se `backend/auth.py` existe e exporta `get_current_user`

---

## 📊 Resumo de Impacto

### Endpoints Atualizados
- ✅ **11 endpoints** Focus NFe (fiscal.py)
- ✅ **7 endpoints** Melhor Envio (melhor_envio.py)
- ✅ **4 endpoints** Cotação Automática (cotacao_automatica.py)
- ✅ **1 router novo** Integrations (integrations.py)
- **Total:** 23+ endpoints migrados

### Integrações Disponíveis
- ✅ Focus NFe (CT-e/MDF-e)
- ✅ Melhor Envio (Correios, Jadlog, Azul)
- ✅ Frenet (Cotação de frete)
- ✅ Evolution API (WhatsApp)
- 🔜 Google Maps (TODO futuro)
- 🔜 ERPs - Bling, Omie, Tiny (futuro)
- 🔜 GPS - Sascar, Autotrac, Onixsat (futuro)

### Arquivos Criados
- ✨ `backend/models.py` (modificado - +43 linhas)
- ✨ `backend/services/encryption_service.py` (+93 linhas)
- ✨ `backend/services/integration_manager.py` (+229 linhas)
- ✨ `backend/routers/integrations.py` (+475 linhas)
- ✨ `GUIA_USUARIO_INTEGRACOES.md` (+447 linhas)
- ✨ `MIGRACAO_INTEGRATION_MANAGER.md` (este arquivo)

### Arquivos Modificados
- ✏️ `backend/routers/fiscal.py` (dependency atualizada)
- ✏️ `backend/routers/melhor_envio.py` (dependency atualizada)
- ✏️ `backend/routers/cotacao_automatica.py` (múltiplas dependencies)
- ✏️ `backend/services/whatsapp_service.py` (construtor flexível)
- ✏️ `frontend/src/views/configuracoes/IntegracoesView.vue` (nova API)

---

## 🎯 Benefícios da Migração

1. **Escalabilidade:** Cada cliente tem suas próprias credenciais
2. **Segurança:** Criptografia + isolamento por tenant
3. **Flexibilidade:** Fácil adicionar novas integrações
4. **Auditoria:** Logs de uso por integração
5. **UX:** Interface intuitiva para configurar (sem mexer no código)
6. **Manutenção:** Não precisa reiniciar servidor para mudar credenciais

---

## 📞 Suporte

**Problemas com a migração?**
- Verifique os logs do backend: `tail -f backend/logs/app.log`
- Teste a API diretamente: `curl` ou Postman
- Consulte `GUIA_USUARIO_INTEGRACOES.md` para instruções de uso

**Dúvidas técnicas?**
- Revise este documento
- Verifique comentários no código
- Contate o time de desenvolvimento

---

**Última atualização:** 23 de Janeiro de 2026  
**Versão:** 1.0.0  
**Status:** ✅ Pronto para Produção (após rodar migration)
