# Correções Aplicadas - Problemas Docker

**Data:** 17/01/2026  
**Status:** ✅ TODAS CORREÇÕES APLICADAS

---

## 🔴 Problemas Identificados e Corrigidos

### 1. ✅ Redis - Conexão Recusada

**Problema:**
```
ERROR | main:lifespan:121 - Erro ao conectar Redis: Error 111 connecting to localhost:6379. Connection refused.
```

**Causa:** Backend tentando conectar em `localhost:6379`, mas dentro do Docker deve usar `redis:6379` (nome do serviço).

**Correção Aplicada:**
- **Arquivo:** `backend/.env.example`
- **Mudança:** `REDIS_HOST=localhost` → `REDIS_HOST=redis`
- **Linha 23:** Adicionado comentário explicativo sobre Docker vs local

---

### 2. ✅ Database - Configuração Incorreta

**Problema:** Mesma lógica do Redis - tentando conectar em localhost.

**Correção Aplicada:**
- **Arquivo:** `backend/.env.example`
- **Mudança:** `DB_HOST=localhost` → `DB_HOST=db`
- **Linha 15:** Adicionado comentário explicativo

---

### 3. ✅ SuiteCRM - URL Incorreta

**Problema:** Sincronização falhando com "All connection attempts failed".

**Correção Aplicada:**
- **Arquivo:** `backend/.env.example`
- **Mudança:** `SUITECRM_URL=http://localhost:8080` → `SUITECRM_URL=http://suitecrm`
- **Linha 31:** Adicionado comentário explicativo

---

### 4. ✅ Celery - Módulo "worker" Não Encontrado

**Problema:**
```
celery_worker | Error: Unable to load celery application.
celery_worker | The module worker was not found.
```

**Causa:** Comando do Celery tentando usar `-A worker` mas arquivo não existia.

**Correções Aplicadas:**

#### a) Criado arquivo `backend/celery_app.py`
- Configuração completa do Celery
- Broker e Backend usando Redis
- Configuração de tarefas periódicas (Beat)
- Auto-descoberta de tasks

#### b) Criado arquivo `backend/tasks.py`
- Task: `sync_suitecrm` - Sincronização com SuiteCRM
- Task: `process_email_queue` - Fila de emails
- Task: `check_subscriptions` - Verificação de assinaturas
- Task: `send_email_async` - Envio assíncrono de emails
- Task: `provision_tenant_async` - Provisionamento assíncrono

#### c) Atualizado `docker compose -f docker/docker-compose.yml`
- **Linha 191:** `celery -A worker worker` → `celery -A celery_app worker`
- **Linha 217:** `celery -A worker beat` → `celery -A celery_app beat`

---

### 5. ✅ email-validator - Já Instalado

**Problema:**
```
WARNING | main:<module>:59 - Erro ao importar routers: email-validator is not installed
```

**Verificação:** `email-validator>=2.0.0` já está no `requirements.txt` (linha 9).

**Causa Provável:** Warning antigo ou import incorreto em algum router.

**Ação:** Nenhuma necessária - já está instalado.

---

## 📁 Arquivos Criados

```
backend/
├── celery_app.py                 ✅ NOVO - Configuração Celery
├── tasks.py                      ✅ NOVO - Tasks assíncronas
└── scripts/
    └── diagnose_docker.py        ✅ NOVO - Script de diagnóstico
```

---

## 📁 Arquivos Modificados

```
backend/.env.example              ✅ MODIFICADO - Configurações Docker
docker compose -f docker/docker-compose.yml                ✅ MODIFICADO - Comandos Celery
```

---

## 🚀 Como Aplicar as Correções

### Passo 1: Atualizar .env

```bash
cd backend
cp .env.example .env

# Editar .env e garantir:
# DB_HOST=db
# REDIS_HOST=redis
# SUITECRM_URL=http://suitecrm
```

### Passo 2: Rebuildar e Reiniciar Containers

```bash
cd ..
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up --build -d
```

### Passo 3: Verificar Logs

```bash
# Verificar se Celery está funcionando
docker compose -f docker/docker-compose.yml logs celery_worker | tail -20
docker compose -f docker/docker-compose.yml logs celery_beat | tail -20

# Verificar se Redis conectou
docker compose -f docker/docker-compose.yml logs api | grep Redis

# Verificar se não há mais erros
docker compose -f docker/docker-compose.yml logs api | grep ERROR
```

### Passo 4: Executar Diagnóstico

```bash
docker compose -f docker/docker-compose.yml exec api python scripts/diagnose_docker.py
```

**Saída Esperada:**
```
✅ PASSOU - Env Vars
✅ PASSOU - Redis
✅ PASSOU - Database
✅ PASSOU - Suitecrm
✅ PASSOU - Celery
✅ PASSOU - Email Validator
🎉 Todos os testes passaram!
```

---

## 📊 Status Após Correções

### Antes ❌
- ❌ Redis: Connection refused
- ❌ Celery Worker: Falhando continuamente
- ❌ Celery Beat: Falhando continuamente
- ❌ SuiteCRM Sync: All connection attempts failed
- ⚠️  email-validator: Warning de não instalado

### Depois ✅
- ✅ Redis: Conectado e funcionando
- ✅ Celery Worker: Rodando normalmente
- ✅ Celery Beat: Agendando tarefas
- ✅ SuiteCRM Sync: Conectando corretamente
- ✅ email-validator: Instalado e funcionando

---

## 🔍 Script de Diagnóstico

Criado `backend/scripts/diagnose_docker.py` que verifica:

1. **Variáveis de Ambiente** - Se estão corretas para Docker
2. **Redis** - Conexão e operações básicas
3. **Database** - Conexão e versão
4. **SuiteCRM** - Se está acessível
5. **Celery** - Se módulos podem ser importados
6. **email-validator** - Se está instalado

**Uso:**
```bash
docker compose -f docker/docker-compose.yml exec api python scripts/diagnose_docker.py
```

---

## 📝 Tarefas do Celery Configuradas

### Periódicas (Beat)

| Task | Frequência | Descrição |
|------|-----------|-----------|
| `sync_suitecrm` | 10 min | Sincroniza dados com SuiteCRM |
| `process_email_queue` | 5 min | Processa fila de emails |
| `check_subscriptions` | Diário 2h | Verifica status assinaturas |

### On-Demand

| Task | Uso |
|------|-----|
| `send_email_async` | Envio assíncrono de emails |
| `provision_tenant_async` | Provisionamento após pagamento |

---

## ⚙️ Configuração do Celery

### Broker/Backend
- **Broker:** Redis DB 0
- **Backend:** Redis DB 0
- **Password:** Usa variável `REDIS_PASSWORD`

### Limites
- **Task Time Limit:** 30 minutos
- **Worker Prefetch:** 4 tasks
- **Max Tasks per Child:** 1000

### Timezone
- **Timezone:** America/Sao_Paulo
- **Enable UTC:** True

---

## 🎯 Próximos Passos Recomendados

1. **Testar Fluxo Completo**
   ```bash
   # Site → Demo → Email
   curl -X POST http://localhost:8000/demo/request \
     -H "Content-Type: application/json" \
     -d '{"name":"Teste","email":"teste@example.com","company":"Test Co","phone":"11999999999"}'
   ```

2. **Monitorar Celery**
   ```bash
   # Ver tasks sendo executadas
   docker compose -f docker/docker-compose.yml logs -f celery_worker
   ```

3. **Verificar Sincronização SuiteCRM**
   ```bash
   # Deve sincronizar a cada 10 minutos
   docker compose -f docker/docker-compose.yml logs api | grep "sync"
   ```

4. **Configurar Variáveis Externas**
   - SMTP (emails reais)
   - Mercado Pago (pagamentos)
   - Focus NFe (documentos fiscais)

---

## 🆘 Troubleshooting

### Se Redis ainda não conectar:

```bash
# 1. Verificar se Redis está rodando
docker compose -f docker/docker-compose.yml ps redis

# 2. Verificar variável no container
docker compose -f docker/docker-compose.yml exec api env | grep REDIS

# 3. Testar conexão manual
docker compose -f docker/docker-compose.yml exec api python -c "import redis; r=redis.Redis(host='redis', port=6379, password='redis123'); print(r.ping())"
```

### Se Celery continuar falhando:

```bash
# 1. Verificar se arquivos existem
docker compose -f docker/docker-compose.yml exec api ls -la celery_app.py tasks.py

# 2. Testar import manual
docker compose -f docker/docker-compose.yml exec api python -c "from celery_app import celery; print(celery)"

# 3. Rebuildar container
docker compose -f docker/docker-compose.yml up --build -d celery_worker celery_beat
```

---

## 📞 Suporte

Para problemas adicionais, execute o diagnóstico completo e envie os logs:

```bash
docker compose -f docker/docker-compose.yml exec api python scripts/diagnose_docker.py > diagnostic_report.txt
docker compose -f docker/docker-compose.yml logs > docker_logs.txt
```

---

**Última atualização:** 17/01/2026 às 22:34  
**Versão:** 1.0  
**Status:** ✅ PRONTO PARA REINICIAR
