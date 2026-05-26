# ADR-003: Escolha do PostgreSQL como Banco de Dados

## Status
**Aceita**

## Data
Janeiro 2026

## Contexto

O LogiFlow CRM requer um banco de dados que suporte:

- Multi-tenancy com isolamento de dados
- Transações ACID para operações financeiras
- Consultas complexas (relatórios, dashboards)
- Escalabilidade para milhares de tenants
- Dados geoespaciais (GPS tracking)
- JSON para dados semi-estruturados

### Volume Estimado
- 100+ tenants iniciais
- ~1M registros/tenant/ano
- Picos de 1000 req/s em horário comercial

## Decisão

Escolhemos **PostgreSQL 15** como banco de dados principal.

```yaml
# docker compose -f docker/docker-compose.yml
db:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: logiflow
    POSTGRES_USER: logiflow
    POSTGRES_PASSWORD: ${DB_PASSWORD}
```

## Consequências

### Positivas

- **ACID compliance**: Transações confiáveis para dados financeiros
- **Multi-tenancy**: Row-Level Security (RLS) nativo
- **Performance**: Excelente para leitura e escrita concorrentes
- **JSON/JSONB**: Flexibilidade para dados semi-estruturados
- **PostGIS**: Extensão para dados geoespaciais (GPS)
- **Full-text search**: Busca textual sem ElasticSearch
- **Partitioning**: Tabelas particionadas por tenant/data
- **Replicação**: Read replicas para escalabilidade
- **Ecossistema**: Ferramentas maduras (pgAdmin, Adminer)
- **Cloud support**: Disponível em todos os clouds (RDS, Cloud SQL, etc)

### Negativas

- **Complexidade**: Mais configuração que SQLite/MySQL
- **Recursos**: Consome mais memória que alternativas
- **Curva de aprendizado**: Features avançadas requerem conhecimento

### Riscos Mitigados

| Risco | Mitigação |
|-------|-----------|
| Performance em escala | Índices otimizados + connection pooling |
| Complexidade | Alembic para migrations + documentação |
| Lock-in | SQLAlchemy abstrai diferenças de DB |

## Alternativas Consideradas

### MySQL/MariaDB
- ✅ Popular e bem documentado
- ✅ Performance para leituras simples
- ❌ JSON support inferior
- ❌ Transações menos robustas (MyISAM)
- ❌ Sem RLS nativo

**Descartado por**: PostgreSQL oferece features mais avançadas.

### MongoDB
- ✅ Flexibilidade de schema
- ✅ Escalabilidade horizontal
- ❌ Sem ACID completo (pre-4.0)
- ❌ Joins complexos são difíceis
- ❌ Consistência eventual

**Descartado por**: Dados relacionais são predominantes no domínio.

### SQLite
- ✅ Zero configuração
- ✅ Embedded, sem servidor
- ❌ Não suporta concorrência
- ❌ Sem features avançadas
- ❌ Não escala

**Descartado por**: Não adequado para produção multi-tenant.

## Estratégia de Multi-Tenancy

```sql
-- Todas as tabelas têm tenant_id
CREATE TABLE clientes (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    -- ... outros campos
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- Índice para queries por tenant
CREATE INDEX idx_clientes_tenant ON clientes(tenant_id);

-- Row Level Security (futuro)
ALTER TABLE clientes ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON clientes
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Configuração de Performance

```ini
# postgresql.conf (recomendado para produção)
shared_buffers = 256MB
effective_cache_size = 768MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 4
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
max_parallel_maintenance_workers = 2
```

## Validação

1. **Testes de carga**: 10k requests/min sem degradação
2. **Multi-tenancy**: Isolamento verificado em testes
3. **Backup/Restore**: Procedimento validado

## Referências

- [PostgreSQL 15 Documentation](https://www.postgresql.org/docs/15/)
- [Multi-tenancy with PostgreSQL](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [SQLAlchemy 2.0 + PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
