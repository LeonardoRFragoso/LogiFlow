# LogiFlow CRM - Guia de Migrations

## Visão Geral

O LogiFlow CRM utiliza **Alembic** para gerenciamento de migrations do banco de dados PostgreSQL.

## Pré-requisitos

```bash
# Variáveis de ambiente necessárias
DATABASE_URL=postgresql://logiflow:logiflow123@localhost:5432/logiflow

# Ou variáveis separadas
DB_HOST=localhost
DB_PORT=5432
DB_NAME=logiflow
DB_USER=logiflow
DB_PASSWORD=logiflow123
```

## Comandos Básicos

### Via Script Helper

```bash
cd backend

# Aplicar todas as migrations
python scripts/run_migrations.py upgrade

# Reverter última migration
python scripts/run_migrations.py downgrade

# Ver versão atual
python scripts/run_migrations.py current

# Ver histórico
python scripts/run_migrations.py history

# Gerar nova migration (autogenerate)
python scripts/run_migrations.py generate "descricao da migration"
```

### Via Alembic Diretamente

```bash
cd backend

# Aplicar todas as migrations
alembic upgrade head

# Aplicar até versão específica
alembic upgrade 006_clean_architecture

# Reverter última migration
alembic downgrade -1

# Reverter para versão específica
alembic downgrade 005_create_gps_tables

# Ver status atual
alembic current

# Ver histórico
alembic history --verbose
```

## Migrations Existentes

| Versão | Descrição | Tabelas |
|--------|-----------|---------|
| 001 | CRM Enterprise Tables | Tabelas base do CRM |
| 002 | Add Tenant ID | Multi-tenancy |
| 003 | Create Tenants Table | Gerenciamento de tenants |
| 004 | NPS/CSAT Tables | Pesquisas de satisfação |
| 005 | GPS Tables | Rastreamento GPS |
| **006** | **Clean Architecture** | `clientes`, `cotacoes`, `pedidos` (v2) |

## Criando Nova Migration

### Autogenerate (Recomendado)

```bash
# 1. Modifique os models em infrastructure/persistence/models.py
# 2. Gere a migration automaticamente
python scripts/run_migrations.py generate "add campo xyz to clientes"

# 3. Revise o arquivo gerado em alembic/versions/
# 4. Aplique a migration
python scripts/run_migrations.py upgrade
```

### Manual

```bash
# Criar arquivo de migration vazio
alembic revision -m "descricao"
```

Edite o arquivo gerado em `alembic/versions/`:

```python
def upgrade() -> None:
    op.add_column('clientes', sa.Column('novo_campo', sa.String(100)))

def downgrade() -> None:
    op.drop_column('clientes', 'novo_campo')
```

## Estrutura das Tabelas v2

### clientes
```
- id: UUID (PK)
- razao_social: String(200)
- nome_fantasia: String(200)
- documento: String(14) UNIQUE
- email: String(255)
- telefone: String(20)
- inscricao_estadual: String(20)
- ativo: Boolean
- observacoes: Text
- endereco: JSON
- created_at: DateTime
- updated_at: DateTime
```

### cotacoes
```
- id: UUID (PK)
- numero: String(50) UNIQUE
- cliente_id: UUID (FK -> clientes)
- origem: JSON
- destino: JSON
- itens: JSON
- tipo_frete: String(10)
- tipo_carga: String(20)
- status: String(20)
- valor_frete: Numeric(12,2)
- valor_seguro: Numeric(12,2)
- valor_outros: Numeric(12,2)
- desconto: Numeric(12,2)
- validade: Date
- observacoes: Text
- criado_por: String(100)
- created_at: DateTime
- updated_at: DateTime
```

### pedidos
```
- id: UUID (PK)
- numero: String(50) UNIQUE
- cliente_id: UUID (FK -> clientes)
- cotacao_id: UUID (FK -> cotacoes)
- origem: JSON
- destino: JSON
- status: String(30)
- peso_kg: Numeric(12,3)
- volume_m3: Numeric(12,3)
- valor_mercadoria: Numeric(12,2)
- descricao_carga: Text
- valor_frete: Numeric(12,2)
- valor_seguro: Numeric(12,2)
- valor_total: Numeric(12,2)
- data_coleta_prevista: DateTime
- data_coleta_realizada: DateTime
- data_entrega_prevista: DateTime
- data_entrega_realizada: DateTime
- motorista_id: UUID
- veiculo_id: UUID
- cte_numero: String(50)
- cte_chave: String(50)
- nfe_chave: String(50)
- observacoes: Text
- created_at: DateTime
- updated_at: DateTime
```

## Troubleshooting

### Erro: "Target database is not up to date"

```bash
# Verificar versão atual
alembic current

# Aplicar migrations pendentes
alembic upgrade head
```

### Erro: "Can't locate revision"

```bash
# Verificar histórico
alembic history

# Marcar versão manualmente (cuidado!)
alembic stamp <revision_id>
```

### Resetar Banco de Desenvolvimento

```bash
# ATENÇÃO: Isso apaga todos os dados!
# 1. Dropar banco
psql -U postgres -c "DROP DATABASE logiflow;"

# 2. Recriar banco
psql -U postgres -c "CREATE DATABASE logiflow OWNER logiflow;"

# 3. Rodar todas as migrations
alembic upgrade head
```

## Boas Práticas

1. **Sempre revise** migrations geradas automaticamente
2. **Nunca edite** migrations já aplicadas em produção
3. **Teste migrations** em ambiente de desenvolvimento primeiro
4. **Faça backup** antes de aplicar em produção
5. **Documente** alterações significativas no schema
