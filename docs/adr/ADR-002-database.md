# ADR-002: Banco de Dados Principal

## Status
Aceita

## Contexto
Atualmente há inconsistência entre ambientes:

- `docker-compose.yml`: MariaDB 10.6
- `render.yaml`: PostgreSQL (managed)
- `backend/config.py` + `backend/database.py`: constrói URL de MySQL (`mysql+pymysql://...`)

Isso aumenta risco de:

- divergência de schema/migrations
- queries incompatíveis entre engines
- falhas em deploy

## Decisão
Padronizar o banco principal em **PostgreSQL** para produção e desenvolvimento.

O `docker-compose.yml` local e o backend (`config.py`/`database.py`) devem ser alinhados para Postgres, reduzindo divergências entre ambientes.

## Consequências
### Positivas
- Alinha com o ambiente de produção já descrito em `render.yaml`
- Melhor suporte a recursos avançados (JSONB, índices, etc.)
- Reduz risco de “works on my machine”

### Negativas
- Exige ajustes no `docker-compose.yml` e no `database.py`/config
- Pode exigir pequenas adaptações de tipos/DDL nas migrations existentes

## Alternativas Consideradas
- **MariaDB/MySQL como padrão**: descartado porque conflita com o blueprint atual do Render e adiciona risco operacional (ajustes de infra e conexão).
- **SQLite em dev, Postgres em prod**: descartado porque aumenta divergência e dificulta testes de integração realistas.
