# 🚀 QUICK START GUIDE - LogiFlow CRM
## Comece em 30 Minutos!

**Data:** 4 de Março de 2026  
**Público:** Pessoas novas no projeto

---

## ⚡ Comece Aqui (< 5 min)

### O que é LogiFlow CRM?
**Um SaaS para transportadoras gerenciar cotações, pedidos, entregas e rastreamento GPS.**

### Stack in a Nutshell
| Layer | Tech |
|-------|------|
| API | FastAPI (Python) |
| Database | PostgreSQL |
| Cache | Redis |
| Frontend | Vue.js 3 |
| Mobile | PWA (app-motorista) |
| Deploy | Docker Compose |

### Usuários Principais
- 👔 **Admin**: configura tenants
- 📋 **Operador**: gerencia cotações, pedidos
- 🚛 **Motorista**: faz entregas (PWA mobile)
- 👥 **Cliente**: acompanha entrega (portal)

---

## 📚 Leia em 30 Min

### Arquivos Críticos a Saber

**Backend (Python)**
```
backend/
├── main.py                 ← Entrada da API
├── routers/               ← Endpoints HTTP
│   ├── clientes.py       ← GET/POST /clientes
│   ├── cotacoes.py       ← Cotações de frete
│   ├── pedidos.py        ← Pedidos
│   ├── gps_tracking.py   ← GPS real-time
│   └── billing.py        ← Pagamentos (MercadoPago)
├── models/               ← Estrutura do banco
├── domain/               ← Lógica de negócio
├── application/          ← Use cases
└── infrastructure/       ← Acesso a dados
```

**Frontend (Vue.js)**
```
frontend/
├── src/
│   ├── main.js           ← Entry point
│   ├── views/            ← Páginas
│   │   ├── clientes/
│   │   ├── cotacao/
│   │   ├── pedidos/
│   │   └── ... (outros módulos)
│   ├── stores/           ← Pinia state
│   ├── services/         ← API clients (Axios)
│   ├── components/       ← UI reusable
│   └── router/           ← Vue Router
```

---

## 🤔 5 Conceitos Principais

### 1️⃣ **Clean Architecture (4 Camadas)**
```
Domain    → Regras de negócio (Cliente, Cotação, etc)
Application → Orquestração (use cases)
Presentation → Endpoints HTTP (routers)
Infrastructure → Acesso a dados (repositories, APIs)
```
**Por que?** Fácil de testar, manter, e substituir tecnologias.

### 2️⃣ **Multi-tenancy**
```
Tenant A (TransportadoraA) → Dados isolados
Tenant B (TransportadoraB) → Dados isolados
(mesmo servidor, dados separados)
```
**Como funciona?** Middleware injeta `tenant_id` em cada requisição.
Todas as queries filtram por `tenant_id` automaticamente.

### 3️⃣ **JWT Tokens**
```
User faz login → Backend gera JWT
JWT contém: user_id + tenant_id + role (válido por 24h)
User envia JWT em cada requisição
Backend valida JWT → libera ou rejeita
```
**Benefício:** Stateless, escalável, seguro.

### 4️⃣ **MercadoPago SaaS**
```
Lead solicita demo → Paga no checkout → Webhook
Backend cria automaticamente:
├─ Novo Tenant
├─ Usuário admin
├─ Envia emails com credenciais
└─ Cliente faz login e usa sistema!
```
**Magic:** Provisioning 100% automático.

### 5️⃣ **GPS Real-Time**
```
App motorista coleta lat/lng a cada 5 seg
→ Envia para /gps/update
→ Backend persiste + publica em WebSocket
→ CRM/Portal recebem e mostram no mapa ao vivo
```
**Latência:** ~2-3 segundos.

---

## 🏃 Primeiros Passos (Prático)

### Setup Local (15 min)

```bash
# 1. Clone e entre no diretório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd LogiFlow/LogiFlow\ CRM

# 2. Copie arquivo de configuração
cp .env.example .env

# 3. Start com Docker Compose
docker-compose up -d

# 4. Aguarde os containers
# Backend estará em: http://localhost:8000
# Frontend estará em: http://localhost:3000
# API Docs em: http://localhost:8000/api/v1/docs
```

### Acesse o Sistema

```
Frontend CRM:    http://localhost:3000
API Docs:        http://localhost:8000/api/v1/docs
Adminer (DB):    http://localhost:8080
```

### Primeiro Teste

```bash
# 1. Abra http://localhost:8000/api/v1/docs
# 2. Clique em "Authorize"
# 3. Faça login com admin/admin
# 4. Teste endpoint GET /clientes
# 5. Resposta mostra clientes do seu tenant
```

---

## 📖 Entenda Seu Papel

### Se você é **Backend Developer**
```
1. Estude: /docs/ANALISE_ARQUITETURA_COMPLETA_2026.md
2. Foco: domain/ ← entities, value_objects
3. Foco: application/ ← use cases
4. Foco: routers/ ← endpoints
5. Foco: models/ ← banco de dados
6. Teste: pytest backend/tests/
```

### Se você é **Frontend Developer**
```
1. Estude: /docs/ANALISE_ARQUITETURA_COMPLETA_2026.md
2. Foco: frontend/src/views/ ← páginas
3. Foco: frontend/src/stores/ ← Pinia state
4. Foco: frontend/src/services/ ← API calls
5. Foco: frontend/src/components/ ← UI components
6. Teste: npm run dev → http://localhost:3000
```

### Se você é **DevOps/Infra**
```
1. Estude: docker-compose.yml
2. Verificar: ./docs/ para deployment guides
3. Setup: Environment variables (.env)
4. Scale: Adicionar replicas, load balancer
5. Monitor: Setup Prometheus (não existe ainda!)
```

---

## 🔥 Atalhos para Fazer Tudo Rápido

### Adicionar Nova Feat no Backend (30 min)

**Step 1: Crie entidade no domínio**
```python
# domain/entities/novo_modelo.py
@dataclass
class NovoModelo(Entity):
    nome: str
    descricao: str
    tenant_id: str
```

**Step 2: Crie repository interface**
```python
# domain/interfaces/repositories.py
class INovoModeloRepository(ABC):
    def adicionar(self, modelo: NovoModelo) -> None: pass
    def buscar(self, id: str) -> NovoModelo: pass
```

**Step 3: Implemente repository**
```python
# infrastructure/repositories/novo_modelo_repository.py
class NovoModeloRepository(INovoModeloRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def adicionar(self, modelo):
        db_model = DBNovoModelo(...)
        self.db.add(db_model)
        self.db.commit()
```

**Step 4: Crie use case**
```python
# application/use_cases/novo_modelo_use_cases.py
class CriarNovoModeloUseCase:
    def __init__(self, repo: INovoModeloRepository):
        self.repo = repo
    
    def execute(self, dados):
        modelo = NovoModelo.criar(dados)
        self.repo.adicionar(modelo)
        return modelo
```

**Step 5: Crie router**
```python
# routers/novo_modelo.py
router = APIRouter(prefix="/novo-modelo")

@router.post("/")
async def criar(dados: Create DTO, db = Depends(get_db)):
    use_case = CriarNovoModeloUseCase(NovoModeloRepository(db))
    resultado = use_case.execute(dados)
    return resultado
```

**Step 6: Inclua router no main.py**
```python
# main.py
from routers import novo_modelo
app.include_router(novo_modelo.router)
```

✅ Pronto!

### Adicionar Nova Tela no Frontend (20 min)

**Step 1: Crie o serviço HTTP**
```javascript
// services/novo_modelo.service.js
import api from './api'

export const novoModeloService = {
  list: () => api.get('/novo-modelo'),
  create: (data) => api.post('/novo-modelo', data),
  getById: (id) => api.get(`/novo-modelo/${id}`),
  update: (id, data) => api.put(`/novo-modelo/${id}`, data),
  delete: (id) => api.delete(`/novo-modelo/${id}`)
}
```

**Step 2: Crie o store (Pinia)**
```javascript
// stores/novo_modelo.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { novoModeloService } from '@/services/novo_modelo.service'

export const useNovoModeloStore = defineStore('novoModelo', () => {
  const items = ref([])
  
  const carregar = async () => {
    const res = await novoModeloService.list()
    items.value = res.data
  }
  
  const criar = async (dados) => {
    const res = await novoModeloService.create(dados)
    items.value.push(res.data)
  }
  
  return { items, carregar, criar }
})
```

**Step 3: Crie a view**
```vue
<!-- views/novo-modelo/ListaView.vue -->
<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold">Novo Modelo</h1>
    
    <div v-for="item in store.items" :key="item.id" class="border p-4">
      <p>{{ item.nome }}</p>
      <p>{{ item.descricao }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useNovoModeloStore } from '@/stores/novo_modelo'

const store = useNovoModeloStore()

onMounted(() => store.carregar())
</script>
```

**Step 4: Adicione rota**
```javascript
// router/index.js
{
  path: '/novo-modelo',
  component: () => import('@/views/novo-modelo/ListaView.vue'),
  meta: { requiresAuth: true }
}
```

✅ Pronto!

---

## 🐛 Debug & Troubleshooting

### Como ver logs?
```bash
# Backend
docker-compose logs -f api

# Frontend (no console do browser)
Ctrl+Shift+J (ou F12 → Console)
```

### Como resetar database?
```bash
# Parar containers
docker-compose down

# Remover volume (database)
docker volume rm logiflow_crm_db_data

# Reiniciar
docker-compose up -d
```

### API retorna 401?
- [ ] JWT inválido/expirado → Faça login novamente
- [ ] Tenant_id incorreto → Verifique header X-Tenant-ID
- [ ] Usuario inativo → Verifique is_active no banco

### Frontend não carrega?
- [ ] Porta 3000 ocupada → `kill -9 $(lsof -ti:3000)`
- [ ] Node modules corrompido → `rm -rf node_modules && npm install`
- [ ] Cache do browser → Ctrl+Shift+Delete

---

## 📊 Dashboard Rápido (Status)

| Aspecto | Status | Ação |
|---------|--------|------|
| **API** | ✅ 100% | Pronta para produção |
| **Frontend** | ✅ 100% | Pronta para produção |
| **Mobile** | ✅ 100% | PWA funcional |
| **Testes** | ⚠️ 30% | +Aumentar cobertura |
| **Seg** | ⚠️ 70% | +Rate limiting |
| **Deploy** | ⚠️ 70% | +K8s, Helm |
| **Monitoring** | ❌ 0% | +Prometheus |

---

## 💡 Dicas Pro

### 1. Entenda Pinia
Pinia é o "storage" centralizado do frontend:
```javascript
// Store = "app state"
const store = useClienteStore()
store.clientes  // dados
store.criar()   // ações
store.total     // computed
```

### 2. Entenda Routers
Backend routers = endpoints HTTP:
```python
# GET /api/v1/clientes
@router.get("/")
async def listar_clientes(): ...

# POST /api/v1/clientes
@router.post("/")
async def criar_cliente(): ...

# PUT /api/v1/clientes/{id}
@router.put("/{id}")
async def atualizar_cliente(): ...
```

### 3. Middleware injeta tenant_id
```python
# Toda requisição automaticamente:
# 1. Valida JWT token
# 2. Extrai user_id + tenant_id
# 3. Injeta em `request.state.tenant_id`
# 4. Todas queries filtram por tenant_id
# → Multi-tenancy funciona automático!
```

### 4. DTOs (Pydantic) validam entrAdA
```python
# Definição
class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr  # ← Valida email!
    idade: int = Field(gt=0)  # ← Deve ser > 0

# Uso
@router.post("/")
async def criar(cliente: ClienteCreate):
    # FastAPI valida automaticamente
    # Se inválido: HTTP 422
    pass
```

### 5. Vue Router lazy load
```javascript
{
  path: '/clientes',
  component: () => import('@/views/clientes/ListaView.vue')
  // ↑ Carrega só quando o user navegará
}
```

---

## 📚 Referências Rápidas

### Links Importantes
- **API Docs**: http://localhost:8000/api/v1/docs
- **Frontend**: http://localhost:3000
- **GitHub**: https://github.com/LeonardoRFragoso/LogiFlow
- **Análise Completa**: [/docs/ANALISE_ARQUITETURA_COMPLETA_2026.md](ANALISE_ARQUITETURA_COMPLETA_2026.md)

### Comandos Úteis
```bash
# Backend
cd backend
pytest                           # Run tests
python -m pytest -v tests/       # Verbose
coverage run -m pytest           # Test coverage

# Frontend
cd frontend
npm run dev                      # Dev server
npm run build                    # Build production
npm run lint                     # Lint code

# Docker
docker-compose up -d             # Start
docker-compose down              # Stop
docker-compose ps                # Status
docker-compose logs -f api       # Logs
```

### Estrutura de Pasta
```
backend/
├── routers/        ← Adicione aqui novos endpoints
├── models/         ← SQLAlchemy models
├── domain/         ← Lógica de negócio pura
├── application/    ← Use cases
└── infrastructure/ ← Acesso a dados

frontend/
├── src/views/      ← Adicione aqui novas páginas
├── src/stores/     ← State management
├── src/services/   ← API clients
├── src/components/ ← Componentes reutilizáveis
└── src/router/     ← Rotas
```

---

## ✅ Checklist: Você está pronto quando...

- [x] Entende o que é LogiFlow CRM
- [x] Sabe rodar `docker-compose up -d`
- [x] Acessa http://localhost:3000 e http://localhost:8000/api/v1/docs
- [x] Entende os 5 conceitos principais (clean arch, multi-tenancy, etc)
- [x] Sabe onde está cada tipo de código (backend/frontend/mobile)
- [x] Consegue adicionar um endpoint simples
- [x] Consegue adicionar uma tela simples no frontend
- [x] Conhece os comandos básicos (docker, npm, pytest)
- [x] Sabe onde encontrar logs
- [x] Baixou a Análise Completa para referência

---

## 🎓 Próximo Passo

Escolha seu caminho:

### 👨‍💻 Backend Developer
→ Estude `domain/` e `application/`  
→ Leia [ANALISE_ARQUITETURA_COMPLETA_2026.md](ANALISE_ARQUITETURA_COMPLETA_2026.md#️-backend---fastapi)

### 🎨 Frontend Developer
→ Estude `frontend/src/stores/` e `views/`  
→ Leia [ANALISE_ARQUITETURA_COMPLETA_2026.md](ANALISE_ARQUITETURA_COMPLETA_2026.md#️-frontend---vuejs-3-crm)

### 🚀 DevOps / Infra
→ Estude `docker-compose.yml`  
→ Leia roadmap de [Scalability](DIAGRAMAS_ARQUITETURA_2026.md#-10-tendências-de-crescimento-e-escalabilidade)

### 📊 Project Manager
→ Leia [SUMARIO_EXECUTIVO](SUMARIO_EXECUTIVO_ANALISE_TECNICA.md)  
→ Entenda [Roadmap](SUMARIO_EXECUTIVO_ANALISE_TECNICA.md#-roadmap-de-12-meses)

---

**Parabéns! Você agora entende LogiFlow CRM!** 🎉

**Dúvidas?** Abra uma issue no GitHub ou leia a [Documentação Completa](INDICE_NAVEGAVEL.md).

