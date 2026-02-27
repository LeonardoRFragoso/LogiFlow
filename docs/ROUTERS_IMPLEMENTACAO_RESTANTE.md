# 🔧 Implementação dos Routers Restantes com Tenant

## Estratégia

Os routers de pedidos, motoristas, veiculos e entregas atualmente usam mock data (dicts em memória).
Precisam ser convertidos para usar o banco de dados com filtragem por `tenant_id`.

## Padrão de Conversão

### Antes (Mock Data)
```python
pedidos_db: dict = {}

@router.get("")
async def listar_pedidos():
    pedidos = list(pedidos_db.values())
    return pedidos
```

### Depois (DB com Tenant)
```python
from middleware.tenant import get_current_tenant_id

@router.get("")
async def listar_pedidos(request: Request, db: Session = Depends(get_db)):
    tenant_id = get_current_tenant_id(request)
    pedidos = db.query(Pedido).filter(Pedido.tenant_id == tenant_id).all()
    return pedidos
```

## Routers a Atualizar

### 1. `/pedidos` (routers/pedidos.py)
- Converter `pedidos_db` para queries do banco
- Adicionar `tenant_id` a todas as queries
- Endpoints: GET, POST, PUT, DELETE, PATCH

### 2. `/motoristas` (routers/motoristas.py)
- Converter `motoristas_db` para queries do banco
- Adicionar `tenant_id` a todas as queries
- Endpoints: GET, POST, PUT, PATCH, DELETE

### 3. `/veiculos` (routers/veiculos.py)
- Converter `veiculos_db` para queries do banco
- Converter `manutencoes_db` para queries do banco
- Adicionar `tenant_id` a todas as queries
- Endpoints: GET, POST, PUT, DELETE

### 4. `/entregas` (routers/entregas.py)
- Converter `entregas_mock` para queries do banco
- Adicionar `tenant_id` a todas as queries
- Endpoints: GET, POST, PATCH, DELETE

## Checklist de Implementação

### Imports Necessários
- [x] `from fastapi import Request`
- [x] `from middleware.tenant import get_current_tenant_id`
- [x] `from models import Pedido, Motorista, Veiculo, Entrega`
- [x] `from loguru import logger`

### Cada Endpoint
- [ ] Adicionar `request: Request` ao parâmetro
- [ ] Chamar `tenant_id = get_current_tenant_id(request)`
- [ ] Filtrar com `.filter(Model.tenant_id == tenant_id)`
- [ ] Adicionar `tenant_id=tenant_id` ao criar registros
- [ ] Adicionar try/except com logging

## Ordem de Implementação

1. **Pedidos** - Mais crítico, usado por motoristas e clientes
2. **Motoristas** - Necessário para atribuir a pedidos
3. **Veículos** - Necessário para atribuir a pedidos
4. **Entregas** - Menos crítico, pode ser feito por último

## Tempo Estimado

- Pedidos: 1-2 horas
- Motoristas: 1-2 horas
- Veículos: 1-2 horas
- Entregas: 30 min - 1 hora
- **Total: 4-7 horas**

## Próximas Etapas Após Routers

1. Executar migrations: `alembic upgrade head`
2. Implementar email com credenciais
3. Testar fluxo completo
4. Deploy em produção

---

**Status:** Pronto para implementação
**Próximo Passo:** Começar com `/pedidos`
