# 🔧 Instruções para Executar Migrations

## Status Atual

As migrations foram criadas e estão prontas para serem executadas. O erro ao tentar executar é devido ao banco de dados local não estar acessível.

## ⚠️ Erro Encontrado

```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed
FATAL: password authentication failed for user "logiflow"
```

## ✅ Solução

### Opção 1: Executar Migrations Localmente (Desenvolvimento)

1. **Verificar se PostgreSQL está rodando:**
   ```bash
   sudo systemctl status postgresql
   ```

2. **Se não estiver rodando, iniciar:**
   ```bash
   sudo systemctl start postgresql
   ```

3. **Verificar credenciais do banco:**
   - Arquivo: `LogiFlow CRM/backend/.env`
   - Verificar: `DATABASE_URL=postgresql://logiflow:senha@localhost:5432/logiflow`

4. **Resetar senha do usuário PostgreSQL:**
   ```bash
   sudo -u postgres psql
   ALTER USER logiflow WITH PASSWORD 'nova_senha';
   \q
   ```

5. **Atualizar `.env` com a nova senha:**
   ```
   DATABASE_URL=postgresql://logiflow:nova_senha@localhost:5432/logiflow
   ```

6. **Executar migrations:**
   ```bash
   cd "LogiFlow CRM/backend"
   alembic upgrade head
   ```

### Opção 2: Executar Migrations em Produção (Railway)

1. **Conectar ao Railway:**
   ```bash
   railway login
   ```

2. **Selecionar projeto:**
   ```bash
   railway project select
   ```

3. **Executar migrations no Railway:**
   ```bash
   cd "LogiFlow CRM/backend"
   railway run alembic upgrade head
   ```

### Opção 3: Usar Script Python

```bash
cd "LogiFlow CRM/backend"
python run_migrations.py
```

## 📋 Migrations Criadas

### Migration 007: Adicionar tenant_id aos Modelos Principais

**Arquivo:** `alembic/versions/007_add_tenant_id_to_main_models.py`

**Alterações:**
- Adiciona coluna `tenant_id` em:
  - `users`
  - `clientes`
  - `motoristas`
  - `veiculos`
  - `pedidos`
  - `entregas`
  - `leads`

- Cria índices para performance:
  - `idx_users_tenant_id`
  - `idx_clientes_tenant_id`
  - `idx_motoristas_tenant_id`
  - `idx_veiculos_tenant_id`
  - `idx_pedidos_tenant_id`
  - `idx_entregas_tenant_id`
  - `idx_leads_tenant_id`

- Adiciona constraints de foreign key:
  - Relacionamento com tabela `tenants`

## 🔍 Verificar Status das Migrations

```bash
cd "LogiFlow CRM/backend"
alembic current
alembic history
```

## ✅ Após Executar as Migrations

1. **Verificar que as colunas foram criadas:**
   ```sql
   SELECT column_name FROM information_schema.columns 
   WHERE table_name = 'users' AND column_name = 'tenant_id';
   ```

2. **Verificar índices:**
   ```sql
   SELECT indexname FROM pg_indexes 
   WHERE tablename = 'users' AND indexname LIKE 'idx_%tenant%';
   ```

3. **Testar fluxo completo:**
   - Criar lead via `/api/leads`
   - Aprovar lead via `/api/leads/{id}/approve`
   - Verificar que tenant foi criado
   - Verificar que user foi criado
   - Fazer login com novo user
   - Verificar isolamento de dados

## 📝 Checklist de Execução

- [ ] PostgreSQL está rodando
- [ ] Credenciais do banco estão corretas
- [ ] Arquivo `.env` foi atualizado
- [ ] Migrations foram executadas com sucesso
- [ ] Colunas `tenant_id` foram criadas em todas as tabelas
- [ ] Índices foram criados
- [ ] Fluxo completo foi testado

## 🚀 Próximos Passos

1. Executar migrations
2. Testar fluxo completo
3. Deploy em produção (Railway)
4. Validar que isolamento de dados funciona

## 📞 Suporte

Se encontrar erros ao executar as migrations:

1. Verifique a conexão com o banco:
   ```bash
   psql postgresql://logiflow:senha@localhost:5432/logiflow
   ```

2. Verifique o arquivo `.env`:
   ```bash
   cat "LogiFlow CRM/backend/.env" | grep DATABASE
   ```

3. Verifique logs do alembic:
   ```bash
   cd "LogiFlow CRM/backend"
   alembic upgrade head --sql
   ```

---

**Status:** Pronto para executar migrations
**Data:** 27 de Fevereiro de 2026
**Próximo Passo:** Executar migrations quando banco estiver disponível
