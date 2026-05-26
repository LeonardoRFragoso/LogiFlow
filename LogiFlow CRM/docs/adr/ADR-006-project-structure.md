# ADR-006: Estrutura de Pastas do Projeto

## Status
**Aceita**

## Data
Janeiro 2026

## Contexto

O LogiFlow CRM é um projeto com múltiplas aplicações:

- Backend API (FastAPI)
- Frontend CRM (Vue.js)
- App Motorista (Vue.js PWA)
- Portal Cliente (Vue.js)
- Site de Divulgação (Vue.js)

Precisamos de uma estrutura que:
- Permita desenvolvimento independente de cada aplicação
- Facilite o deploy separado ou conjunto
- Mantenha código compartilhado organizado
- Suporte Docker e CI/CD

## Decisão

Adotamos uma estrutura **monorepo** com separação clara por aplicação:

```
LogiFlow CRM/
├── backend/              # API FastAPI
├── frontend/             # CRM principal (Vue.js)
├── app-motorista/        # App do motorista (Vue.js PWA)
├── portal-cliente/       # Portal do cliente (Vue.js)
├── site-divulgacao/      # Landing page (Vue.js)
├── docker/               # Dockerfiles e configs
├── docs/                 # Documentação
├── scripts/              # Scripts de automação
├── .github/              # GitHub Actions
└── docker compose -f docker/docker-compose.yml    # Orquestração local
```

## Consequências

### Positivas

- **Visibilidade**: Todo o código em um lugar
- **Refatoração**: Mudanças cross-cutting facilitadas
- **CI/CD**: Pipeline unificado
- **Versionamento**: Versão única para todo o sistema
- **Code review**: Contexto completo em PRs
- **Dependências**: Compartilhamento facilitado

### Negativas

- **Tamanho do repo**: Clone inicial maior
- **Builds**: Pode rebuildar mais do que necessário
- **Conflitos**: Mais chances de conflitos de merge
- **Permissões**: Todos veem todo o código

### Riscos Mitigados

| Risco | Mitigação |
|-------|-----------|
| Build lento | CI com caching + builds incrementais |
| Conflitos | Branches curtas + trunk-based development |
| Tamanho | Git LFS para arquivos grandes |

## Estrutura Detalhada

### Backend

```
backend/
├── alembic/              # Migrations
├── domain/               # Clean Architecture - Domain
├── application/          # Clean Architecture - Application
├── infrastructure/       # Clean Architecture - Infrastructure
├── presentation/         # Clean Architecture - Presentation
├── routers/              # API endpoints (legado)
├── services/             # Business services
├── models/               # SQLAlchemy models
├── middleware/           # HTTP middlewares
├── integrations/         # External API clients
├── tests/                # Testes
├── main.py               # Entry point
├── config.py             # Configurações
├── database.py           # DB connection
└── requirements.txt      # Dependencies
```

### Frontend (Vue.js Apps)

```
frontend/                 # ou app-motorista/, portal-cliente/
├── public/               # Static assets
├── src/
│   ├── assets/           # Images, fonts
│   ├── components/       # Reusable components
│   ├── composables/      # Vue composables
│   ├── layouts/          # Page layouts
│   ├── router/           # Vue Router config
│   ├── services/         # API services
│   ├── stores/           # Pinia stores
│   ├── views/            # Page components
│   ├── App.vue           # Root component
│   └── main.js           # Entry point
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

### Docker

```
docker/
├── api/
│   └── Dockerfile        # Backend image
├── frontend/
│   └── Dockerfile        # Frontend image
├── site/
│   └── Dockerfile        # Site image
├── nginx/
│   └── nginx.conf        # Reverse proxy
└── celery/
    └── start-worker.sh   # Celery startup
```

### Documentação

```
docs/
├── analysis/             # Análises técnicas
├── architecture/         # Diagramas C4
├── adr/                  # Architecture Decision Records
├── guides/               # Guias de uso
├── patterns/             # Padrões implementados
├── deployment/           # Guias de deploy
├── security/             # Documentação de segurança
└── api/                  # Documentação da API
```

### CI/CD

```
.github/
├── workflows/
│   ├── ci.yml            # Continuous Integration
│   ├── cd.yml            # Continuous Deployment
│   └── deploy.yml        # Manual deploy
└── agents/               # Copilot/AI configs
```

## Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Arquivos Python | snake_case | `cliente_repository.py` |
| Classes Python | PascalCase | `ClienteRepository` |
| Arquivos Vue | PascalCase | `ClienteForm.vue` |
| Componentes Vue | PascalCase | `<ClienteForm />` |
| Arquivos JS | camelCase | `apiService.js` |
| Funções | camelCase | `createCliente()` |
| Constantes | UPPER_SNAKE | `API_BASE_URL` |
| Diretórios | kebab-case | `app-motorista/` |
| Env vars | UPPER_SNAKE | `DB_PASSWORD` |

## Alternativas Consideradas

### Multi-repo (Polyrepo)
- ✅ Repos independentes
- ✅ Builds isolados
- ❌ Sincronização de versões difícil
- ❌ Mudanças cross-cutting complexas
- ❌ Múltiplos repos para gerenciar

**Descartado por**: Complexidade de gerenciamento para equipe pequena.

### Monolito Puro
- ✅ Simplicidade máxima
- ❌ Backend e frontend acoplados
- ❌ Deploy conjunto obrigatório
- ❌ Difícil escalar equipe

**Descartado por**: Necessidade de deploys independentes.

### Turborepo/Nx Monorepo
- ✅ Builds inteligentes
- ✅ Caching distribuído
- ❌ Overhead de configuração
- ❌ Curva de aprendizado

**Considerado para futuro**: Quando escalar a equipe.

## Validação

1. **Build time**: < 5 min para CI completo
2. **Clone time**: < 2 min (sem node_modules)
3. **Onboarding**: Novo dev produtivo em 1 dia

## Referências

- [Monorepo vs Polyrepo](https://www.atlassian.com/git/tutorials/monorepos)
- [Vue.js Style Guide](https://vuejs.org/style-guide/)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)
