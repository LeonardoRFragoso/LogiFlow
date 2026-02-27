# 🗄️ Arquitetura de Conexões ao Banco de Dados

## ✅ Resposta: SIM, Múltiplas Conexões

Você está correto! O sistema deve ter **múltiplas conexões** do mesmo banco de dados PostgreSQL.

## 📊 Arquitetura Atual

```
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL (logiflow-db)                       │
│  - 1 banco de dados compartilhado                           │
│  - Isolamento por tenant_id (aplicação)                     │
│  - Máximo de conexões: 100 (padrão PostgreSQL)              │
└─────────────────────────────────────────────────────────────┘
         ↑         ↑         ↑         ↑
         │         │         │         │
    ┌────┴─┐  ┌────┴─┐  ┌────┴─┐  ┌────┴─┐
    │      │  │      │  │      │  │      │
   API   Jobs Scripts Webhooks ...
  (via connection pool)
```

## 🔄 Connection Pool (Pool de Conexões)

### Configuração Atual (Otimizada)

```python
# Produção (Railway)
poolclass = QueuePool
pool_size = 10              # Conexões permanentes
max_overflow = 20           # Conexões adicionais
pool_timeout = 30           # Timeout para obter conexão
pool_recycle = 3600         # Reciclar a cada 1 hora
pool_pre_ping = True        # Verificar conexão antes de usar

# Total: até 30 conexões simultâneas
```

### Como Funciona

1. **Pool Inicial**: 10 conexões criadas e mantidas abertas
2. **Overflow**: Se precisar de mais, cria até 20 adicionais
3. **Reutilização**: Conexões são reutilizadas entre requisições
4. **Limpeza**: Conexões inativas são fechadas automaticamente
5. **Validação**: Cada conexão é testada antes de usar (`pool_pre_ping`)

## 📈 Escalabilidade

### Cenários de Uso

| Cenário | Conexões | Status |
|---------|----------|--------|
| 1 requisição | 1 | ✅ OK |
| 10 requisições simultâneas | 10 | ✅ OK |
| 20 requisições simultâneas | 20 | ✅ OK |
| 30 requisições simultâneas | 30 | ✅ OK (máximo) |
| 31+ requisições | Fila de espera | ⚠️ Aguarda liberação |

## 🔐 Isolamento de Dados

### Nível de Banco de Dados
- ✅ 1 banco PostgreSQL compartilhado
- ✅ Todas as tabelas no mesmo banco
- ✅ Sem isolamento a nível de BD

### Nível de Aplicação
- ✅ Coluna `tenant_id` em todas as tabelas
- ✅ Middleware valida `tenant_id` do JWT
- ✅ Queries filtram por `tenant_id`
- ✅ Usuário só vê dados do seu tenant

### Segurança
```python
# ❌ ERRADO - Sem isolamento
clientes = db.query(Cliente).all()

# ✅ CORRETO - Com isolamento
tenant_id = request.state.tenant_id
clientes = db.query(Cliente).filter(Cliente.tenant_id == tenant_id).all()
```

## 🚀 Múltiplos Serviços Conectados

### Exemplo: Arquitetura Futura

```
┌──────────────────────────────────────────────────────────┐
│                  PostgreSQL (logiflow-db)                │
└──────────────────────────────────────────────────────────┘
    ↑           ↑           ↑           ↑           ↑
    │           │           │           │           │
┌───┴──┐   ┌────┴──┐   ┌────┴──┐   ┌───┴──┐   ┌───┴──┐
│ API  │   │ Jobs  │   │Reports│   │Webhks│   │Cache │
│(FastA│   │(Celery│   │(Panda │   │(Fast │   │(Redis│
│PI)   │   │)      │   │S)     │   │API)  │   │)     │
└──────┘   └───────┘   └───────┘   └──────┘   └──────┘
```

Cada serviço:
- ✅ Usa sua própria sessão do pool
- ✅ Compartilha o mesmo banco de dados
- ✅ Respeita isolamento por `tenant_id`
- ✅ Não interfere com outros serviços

## 📋 Checklist de Implementação

- [x] Configurar QueuePool com limites apropriados
- [x] Implementar pool_pre_ping para validação
- [x] Implementar pool_recycle para limpeza
- [x] Adicionar tenant_id a todos os modelos
- [x] Implementar middleware de tenant
- [x] Atualizar queries para filtrar por tenant
- [ ] Testar com múltiplas conexões simultâneas
- [ ] Monitorar uso de conexões em produção
- [ ] Configurar alertas se pool ficar saturado

## 🔍 Monitoramento

### Verificar Conexões Ativas

```sql
-- Conectar ao PostgreSQL e executar:
SELECT datname, count(*) as connections
FROM pg_stat_activity
GROUP BY datname;

-- Ver detalhes de cada conexão
SELECT pid, usename, application_name, state, query
FROM pg_stat_activity
WHERE datname = 'logiflow';
```

### Logs do SQLAlchemy

```python
# Ativar logs para debug (development apenas)
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
```

## ⚙️ Configuração por Ambiente

### Desenvolvimento
- Pool: NullPool (sem limite)
- Conexões: Criadas/destruídas por requisição
- Vantagem: Simples, sem deadlocks
- Desvantagem: Mais lento

### Produção (Railway)
- Pool: QueuePool (com limite)
- Conexões: Reutilizadas
- Vantagem: Rápido, eficiente
- Desvantagem: Requer monitoramento

## 🎯 Resultado Final

✅ **1 Banco de Dados PostgreSQL**
- Compartilhado entre todos os serviços
- Isolamento por `tenant_id` (aplicação)
- Múltiplas conexões simultâneas (até 30)
- Seguro e escalável

✅ **Múltiplos Serviços**
- API (FastAPI)
- Jobs (Celery - futuro)
- Webhooks (FastAPI - futuro)
- Scripts (Alembic, etc.)
- Todos compartilham o mesmo pool

✅ **Segurança**
- Usuários isolados por tenant
- Dados isolados por tenant
- Sem acesso cruzado entre tenants

---

**Status:** ✅ Configuração Otimizada e Pronta para Produção
