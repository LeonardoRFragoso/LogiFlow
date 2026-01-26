# LogiFlow CRM - CI/CD Pipeline

## Visão Geral

O projeto utiliza **GitHub Actions** para CI/CD automatizado.

## Pipelines

### CI (Integração Contínua)

Arquivo: `.github/workflows/ci.yml`

Executado em: `push` e `pull_request` para branches `main` e `develop`

| Job | Descrição |
|-----|-----------|
| `backend-tests` | Testes unitários e integração com PostgreSQL e Redis |
| `backend-lint` | Análise de código com Ruff |
| `frontend-tests` | Build e lint do frontend Vue.js |
| `docker-build` | Validação do build Docker |
| `security-scan` | Scan de vulnerabilidades com Trivy |

### CD (Deploy Contínuo)

Arquivo: `.github/workflows/cd.yml`

| Trigger | Ambiente |
|---------|----------|
| Push para `main` | Staging |
| Tag `v*` | Production |
| Manual (`workflow_dispatch`) | Staging ou Production |

## Secrets Necessários

Configure os seguintes secrets no GitHub:

```
RENDER_API_KEY              # API Key do Render
RENDER_STAGING_SERVICE_ID   # ID do serviço staging
RENDER_PRODUCTION_SERVICE_ID # ID do serviço production
STAGING_DATABASE_URL        # URL do banco staging
```

## Executar Localmente

### Testes

```bash
cd "LogiFlow CRM/backend"

# Todos os testes unitários
pytest tests/unit/ -v

# Com cobertura
pytest tests/unit/ --cov=. --cov-report=html

# Testes específicos
pytest tests/unit/test_entities.py -v
```

### Lint

```bash
# Instalar ruff
pip install ruff

# Verificar erros
ruff check .

# Corrigir automaticamente
ruff check . --fix

# Verificar formatação
ruff format --check .
```

## Fluxo de Deploy

```
1. Developer cria branch feature/*
2. Push → CI executa testes
3. PR para develop → Code review
4. Merge para develop → CI executa
5. PR para main → Aprovação
6. Merge para main → Deploy Staging automático
7. Tag v1.x.x → Deploy Production
```

## Ambientes

| Ambiente | URL | Branch |
|----------|-----|--------|
| Development | localhost:8000 | feature/* |
| Staging | staging-api.logiflow.com.br | main |
| Production | api.logiflow.com.br | tags v* |

## Rollback

Para reverter um deploy:

1. **Via GitHub**: Reverta o merge/tag problemático
2. **Via Render**: Use o dashboard para deploy de versão anterior
3. **Manual**: `git revert <commit>` + push para main

## Monitoramento

Após deploy, verifique:

- [ ] Health check: `GET /health`
- [ ] Logs no Render Dashboard
- [ ] Métricas de erro
- [ ] Performance da API

## Troubleshooting

### CI falhou nos testes

```bash
# Verificar logs do job
# Reproduzir localmente:
docker-compose up -d db redis
pytest tests/unit/ -v --tb=long
```

### Deploy falhou

1. Verificar logs no Render
2. Verificar variáveis de ambiente
3. Verificar migrations pendentes
4. Rollback se necessário

### Build Docker falhou

```bash
# Build local para debug
docker build -t logiflow-api:test -f docker/api/Dockerfile .
docker run --rm logiflow-api:test python -c "import main"
```
