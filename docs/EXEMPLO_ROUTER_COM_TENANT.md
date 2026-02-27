# 📝 Exemplo: Router com Filtragem por Tenant

## 🎯 Padrão para Atualizar Routers

Todos os routers devem filtrar dados por `tenant_id`. Aqui está o padrão:

### ❌ ANTES (Sem isolamento)
```python
@router.get("/clientes")
async def listar_clientes(db: Session = Depends(get_db)):
    # ❌ Retorna clientes de TODOS os tenants
    clientes = db.query(Cliente).all()
    return clientes
```

### ✅ DEPOIS (Com isolamento)
```python
from fastapi import Request
from middleware.tenant import get_current_tenant_id

@router.get("/clientes")
async def listar_clientes(
    request: Request,
    db: Session = Depends(get_db)
):
    # ✅ Obtém tenant_id do contexto
    tenant_id = get_current_tenant_id(request)
    
    # ✅ Filtra clientes apenas do tenant
    clientes = db.query(Cliente).filter(
        Cliente.tenant_id == tenant_id
    ).all()
    return clientes
```

## 📋 Padrão Completo para CRUD

```python
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from middleware.tenant import get_current_tenant_id

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# ========================================
# GET - Listar
# ========================================

@router.get("")
async def listar_clientes(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Lista clientes do tenant atual"""
    tenant_id = get_current_tenant_id(request)
    
    clientes = db.query(Cliente).filter(
        Cliente.tenant_id == tenant_id
    ).offset(skip).limit(limit).all()
    
    return clientes


# ========================================
# GET - Obter por ID
# ========================================

@router.get("/{cliente_id}")
async def obter_cliente(
    cliente_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém cliente específico do tenant atual"""
    tenant_id = get_current_tenant_id(request)
    
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.tenant_id == tenant_id  # ✅ Validar tenant
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente


# ========================================
# POST - Criar
# ========================================

@router.post("")
async def criar_cliente(
    cliente_data: ClienteCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria novo cliente para o tenant atual"""
    tenant_id = get_current_tenant_id(request)
    
    # ✅ Adicionar tenant_id ao criar
    cliente = Cliente(
        **cliente_data.dict(),
        tenant_id=tenant_id  # ✅ IMPORTANTE
    )
    
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    
    return cliente


# ========================================
# PUT - Atualizar
# ========================================

@router.put("/{cliente_id}")
async def atualizar_cliente(
    cliente_id: str,
    cliente_data: ClienteUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza cliente do tenant atual"""
    tenant_id = get_current_tenant_id(request)
    
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.tenant_id == tenant_id  # ✅ Validar tenant
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Atualizar campos
    for key, value in cliente_data.dict(exclude_unset=True).items():
        setattr(cliente, key, value)
    
    db.commit()
    db.refresh(cliente)
    
    return cliente


# ========================================
# DELETE - Deletar
# ========================================

@router.delete("/{cliente_id}")
async def deletar_cliente(
    cliente_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Deleta cliente do tenant atual"""
    tenant_id = get_current_tenant_id(request)
    
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id,
        Cliente.tenant_id == tenant_id  # ✅ Validar tenant
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(cliente)
    db.commit()
    
    return {"message": "Cliente deletado com sucesso"}
```

## 🔐 Checklist de Segurança

Para cada endpoint, verificar:

- [ ] Obtém `tenant_id` do contexto
- [ ] Filtra dados por `tenant_id`
- [ ] Valida que recurso pertence ao tenant
- [ ] Não retorna dados de outros tenants
- [ ] Não permite modificar dados de outros tenants

## 📊 Routers a Atualizar

Prioridade Alta:
- [ ] `/clientes` - Listar, criar, atualizar, deletar
- [ ] `/pedidos` - Listar, criar, atualizar, deletar
- [ ] `/motoristas` - Listar, criar, atualizar, deletar
- [ ] `/veiculos` - Listar, criar, atualizar, deletar
- [ ] `/entregas` - Listar, criar, atualizar, deletar

Prioridade Média:
- [ ] `/cotacoes` - Listar, criar, atualizar, deletar
- [ ] `/ocorrencias` - Listar, criar, atualizar, deletar
- [ ] `/dashboard` - Filtrar dados por tenant
- [ ] `/relatorios` - Filtrar dados por tenant

Prioridade Baixa:
- [ ] `/fiscal` - Filtrar por tenant
- [ ] `/rastreamento` - Filtrar por tenant
- [ ] `/whatsapp` - Filtrar por tenant

---

**Status:** Padrão Definido - Pronto para Implementação
