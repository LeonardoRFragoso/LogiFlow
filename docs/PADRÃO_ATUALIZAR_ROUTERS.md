# 📝 Padrão para Atualizar Routers com Filtragem por Tenant

## 🎯 Objetivo
Todos os routers devem filtrar dados por `tenant_id` para garantir isolamento de dados.

## 📋 Checklist de Routers a Atualizar

### 🔴 CRÍTICOS (Hoje)
- [x] `/clientes` - ✅ COMPLETO
- [ ] `/pedidos` - ⏳ Pendente
- [ ] `/motoristas` - ⏳ Pendente
- [ ] `/veiculos` - ⏳ Pendente
- [ ] `/entregas` - ⏳ Pendente

### 🟡 IMPORTANTES (Amanhã)
- [ ] `/dashboard` - Filtrar dados por tenant
- [ ] `/cotacoes` - Filtrar por tenant
- [ ] `/ocorrencias` - Filtrar por tenant

### 🟢 SECUNDÁRIOS (Próxima Semana)
- [ ] `/rastreamento` - Filtrar por tenant
- [ ] `/fiscal` - Filtrar por tenant
- [ ] `/whatsapp` - Filtrar por tenant

## 🔧 Padrão de Implementação

### 1. Imports Necessários
```python
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import SeuModelo
from middleware.tenant import get_current_tenant_id
from loguru import logger
```

### 2. GET - Listar com Filtragem por Tenant
```python
@router.get("")
async def listar_items(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista items do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        items = db.query(SeuModelo).filter(
            SeuModelo.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()
        
        logger.info(f"✅ Listados {len(items)} items do tenant {tenant_id}")
        return items
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao listar items: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. GET by ID - Obter com Validação de Tenant
```python
@router.get("/{item_id}")
async def obter_item(
    item_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém item específico do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        item = db.query(SeuModelo).filter(
            SeuModelo.id == item_id,
            SeuModelo.tenant_id == tenant_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        logger.info(f"✅ Item {item_id} obtido do tenant {tenant_id}")
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao obter item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 4. POST - Criar com tenant_id Automático
```python
@router.post("", status_code=201)
async def criar_item(
    item_data: ItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria novo item para o tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        novo_item = SeuModelo(
            **item_data.dict(),
            tenant_id=tenant_id  # ✅ IMPORTANTE
        )
        
        db.add(novo_item)
        db.commit()
        db.refresh(novo_item)
        
        logger.info(f"✅ Item {novo_item.id} criado para tenant {tenant_id}")
        return novo_item
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 5. PUT - Atualizar com Validação de Tenant
```python
@router.put("/{item_id}")
async def atualizar_item(
    item_id: str,
    item_data: ItemUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Atualiza item do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        item = db.query(SeuModelo).filter(
            SeuModelo.id == item_id,
            SeuModelo.tenant_id == tenant_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        for key, value in item_data.dict(exclude_unset=True).items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        
        logger.info(f"✅ Item {item_id} atualizado no tenant {tenant_id}")
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao atualizar item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 6. DELETE - Deletar com Validação de Tenant
```python
@router.delete("/{item_id}", status_code=204)
async def deletar_item(
    item_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Deleta item do tenant atual"""
    try:
        tenant_id = get_current_tenant_id(request)
        
        item = db.query(SeuModelo).filter(
            SeuModelo.id == item_id,
            SeuModelo.tenant_id == tenant_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        db.delete(item)
        db.commit()
        
        logger.info(f"✅ Item {item_id} deletado do tenant {tenant_id}")
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao deletar item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

## ✅ Checklist para Cada Router

- [ ] Adicionar `Request` ao import do FastAPI
- [ ] Adicionar `from middleware.tenant import get_current_tenant_id`
- [ ] Adicionar `from loguru import logger`
- [ ] Adicionar `request: Request` a todos os endpoints
- [ ] Chamar `tenant_id = get_current_tenant_id(request)` em cada endpoint
- [ ] Filtrar queries com `.filter(Model.tenant_id == tenant_id)`
- [ ] Adicionar `tenant_id=tenant_id` ao criar novos registros
- [ ] Adicionar try/except com logging
- [ ] Testar endpoint com JWT contendo tenant_id

## 📊 Routers Restantes

### Pedidos (`routers/pedidos.py`)
- GET `/pedidos` - Listar pedidos do tenant
- GET `/pedidos/{id}` - Obter pedido específico
- POST `/pedidos` - Criar pedido
- PUT `/pedidos/{id}` - Atualizar pedido
- DELETE `/pedidos/{id}` - Deletar pedido

### Motoristas (`routers/motoristas.py`)
- GET `/motoristas` - Listar motoristas do tenant
- GET `/motoristas/{id}` - Obter motorista específico
- POST `/motoristas` - Criar motorista
- PUT `/motoristas/{id}` - Atualizar motorista
- DELETE `/motoristas/{id}` - Deletar motorista

### Veículos (`routers/veiculos.py`)
- GET `/veiculos` - Listar veículos do tenant
- GET `/veiculos/{id}` - Obter veículo específico
- POST `/veiculos` - Criar veículo
- PUT `/veiculos/{id}` - Atualizar veículo
- DELETE `/veiculos/{id}` - Deletar veículo

### Entregas (`routers/entregas.py`)
- GET `/entregas` - Listar entregas do tenant
- GET `/entregas/{id}` - Obter entrega específica
- POST `/entregas` - Criar entrega
- PUT `/entregas/{id}` - Atualizar entrega
- DELETE `/entregas/{id}` - Deletar entrega

---

**Status:** Padrão Definido - Pronto para Implementação em Massa
