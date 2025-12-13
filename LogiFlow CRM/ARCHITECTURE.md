# LogiFlow CRM - Arquitetura Integrada

## Visão Geral

O LogiFlow CRM utiliza uma **arquitetura híbrida** onde:

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                   │
│                     Vue 3 + Vite                                  │
│            (SPA - Single Page Application)                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/REST
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND ORQUESTRADOR                           │
│                   FastAPI (Python)                                │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │ Autenticação│   Billing   │   Regras    │   Cache     │      │
│  │    JWT      │   Asaas     │  Negócio    │   Redis     │      │
│  └─────────────┴─────────────┴─────────────┴─────────────┘      │
└─────────────────────┬───────────────────────────────────────────┘
                      │ API V8 (JSON:API)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SUITECRM 8.x                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   MÓDULOS CUSTOM                         │    │
│  │  Cotacoes │ PedidosFrete │ Entregas │ Motoristas │ ...  │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              FUNCIONALIDADES NATIVAS                     │    │
│  │  ACL │ Workflows │ Relatórios │ API V8 │ Logic Hooks    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BANCO DE DADOS                                 │
│                   MariaDB 10.6                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes

### 1. Frontend (Vue 3)
- **Localização:** `/frontend/`
- **Tecnologias:** Vue 3, Vite, Pinia, Vue Router, TailwindCSS
- **Responsabilidade:** Interface do usuário, não acessa SuiteCRM diretamente

### 2. Backend Orquestrador (FastAPI)
- **Localização:** `/backend/`
- **Tecnologias:** FastAPI, Python 3.11, httpx, Redis, Celery
- **Responsabilidade:**
  - Autenticação de usuários (JWT)
  - Orquestração de chamadas para SuiteCRM
  - Regras de negócio adicionais
  - Integrações externas (CT-e, WhatsApp, etc.)
  - Cache de tokens e dados

### 3. SuiteCRM
- **Localização:** `/suitecrm/`
- **Versão:** 8.4.0
- **Responsabilidade:**
  - Armazenamento de dados (módulos custom)
  - ACL (controle de acesso)
  - Workflows automatizados
  - Logic Hooks
  - API V8 (JSON:API)

## Módulos Custom do SuiteCRM

| Módulo | Tabela | Descrição |
|--------|--------|-----------|
| Cotacoes | cotacoes | Cotações de frete |
| PedidosFrete | pedidos_frete | Pedidos confirmados |
| Entregas | entregas | Registro de entregas |
| Motoristas | motoristas | Cadastro de motoristas |
| Veiculos | veiculos | Cadastro de veículos |
| Ocorrencias | ocorrencias | Ocorrências operacionais |

## Fluxo de Dados

### Criar Cotação
```
Vue → POST /api/cotacoes → FastAPI → SuiteCRM API V8 → MySQL
```

### Aprovar Cotação (cria Pedido automaticamente)
```
Vue → PATCH /api/cotacoes/{id}/aprovar → FastAPI → SuiteCRM API V8
                                                        │
                                                        ▼
                                               Logic Hook dispara
                                                        │
                                                        ▼
                                               Cria PedidoFrete
```

## Arquivos de Configuração

### Docker
- `docker-compose.yml` - Orquestração de todos os containers
- `docker/suitecrm/Dockerfile` - Imagem PHP-FPM para SuiteCRM
- `docker/nginx/sites/default.conf` - Proxy reverso

### SuiteCRM Custom
```
suitecrm/custom/
├── modules/
│   ├── Cotacoes/
│   │   ├── metadata/vardefs.php
│   │   ├── language/pt_BR.lang.php
│   │   ├── logic_hooks.php
│   │   └── CriarPedidoHook.php
│   ├── PedidosFrete/
│   ├── Entregas/
│   ├── Motoristas/
│   ├── Veiculos/
│   └── Ocorrencias/
├── themes/LogiFlow/
│   ├── css/style.css
│   └── themedef.php
└── Extension/application/Ext/Language/
    └── pt_BR.logiflow_dropdowns.php
```

## Configuração OAuth2 (SuiteCRM API V8)

Após instalar o SuiteCRM, configure as credenciais OAuth2:

1. Acesse Admin → OAuth2 Clients
2. Crie um novo client:
   - Name: `logiflow_api`
   - Grant Type: `client_credentials`
   - Scope: `*`
3. Copie `client_id` e `client_secret` para o `.env`

## Comandos Úteis

```bash
# Subir ambiente de desenvolvimento
docker-compose up -d

# Ver logs
docker-compose logs -f suitecrm
docker-compose logs -f django

# Rebuild após mudanças
docker-compose up -d --build

# Acessar container SuiteCRM
docker exec -it logiflow_suitecrm bash

# Limpar cache do SuiteCRM
docker exec logiflow_suitecrm php bin/console cache:clear
```

## Endpoints da API

### Cotações
- `GET /api/cotacoes` - Listar
- `GET /api/cotacoes/{id}` - Detalhe
- `POST /api/cotacoes` - Criar
- `PATCH /api/cotacoes/{id}/aprovar` - Aprovar (cria pedido)
- `PATCH /api/cotacoes/{id}/perder` - Marcar como perdida

### Pedidos
- `GET /api/pedidos` - Listar
- `GET /api/pedidos/{id}` - Detalhe
- `PATCH /api/pedidos/{id}/status` - Atualizar status

### Motoristas
- `GET /api/motoristas` - Listar
- `GET /api/motoristas/disponiveis` - Disponíveis
- `GET /api/motoristas/cnh-vencendo` - CNH vencendo
- `POST /api/motoristas` - Criar

### Veículos
- `GET /api/veiculos` - Listar
- `GET /api/veiculos/disponiveis` - Disponíveis
- `POST /api/veiculos` - Criar

## Próximos Passos

1. [ ] Instalar SuiteCRM no container
2. [ ] Configurar OAuth2 credentials
3. [ ] Executar Quick Repair no SuiteCRM (criar tabelas)
4. [ ] Testar integração end-to-end
