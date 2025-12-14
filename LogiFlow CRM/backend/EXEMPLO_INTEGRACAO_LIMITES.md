# 🔒 Exemplo de Integração de Validação de Limites

## 📋 Como Integrar Validação nos Endpoints

### Padrão de Implementação

```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Tenant, Veiculo
from middleware.plan_limits import check_vehicle_limit

router = APIRouter()

@router.post("/veiculos")
def criar_veiculo(
    veiculo_data: VeiculoCreate,
    db: Session = Depends(get_db),
    tenant_id: int = 1  # TODO: Obter do token JWT
):
    """
    Cria um novo veículo com validação de limites
    """
    # 1. Obter tenant
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")
    
    # 2. VALIDAR LIMITE ANTES DE CRIAR
    check_vehicle_limit(tenant, db)
    
    # 3. Se passou, criar o veículo
    novo_veiculo = Veiculo(**veiculo_data.dict())
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)
    
    return novo_veiculo
```

---

## 🚗 Exemplo: Endpoint de Veículos

### Arquivo: `routers/veiculos.py`

```python
from middleware.plan_limits import check_vehicle_limit

@router.post("/veiculos", response_model=VeiculoResponse)
def criar_veiculo(
    veiculo: VeiculoCreate,
    db: Session = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Cria novo veículo com validação de limite"""
    
    # Validar limite do plano
    check_vehicle_limit(current_tenant, db)
    
    # Criar veículo
    novo_veiculo = Veiculo(
        placa=veiculo.placa,
        modelo=veiculo.modelo,
        # ... outros campos
    )
    
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)
    
    return novo_veiculo
```

**Resposta se exceder limite**:
```json
{
  "detail": "Limite de veículos atingido (10). Faça upgrade do seu plano."
}
```
Status: `403 Forbidden`

---

## 👤 Exemplo: Endpoint de Motoristas/Usuários

### Arquivo: `routers/motoristas.py`

```python
from middleware.plan_limits import check_user_limit

@router.post("/motoristas", response_model=MotoristaResponse)
def criar_motorista(
    motorista: MotoristaCreate,
    db: Session = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Cria novo motorista com validação de limite"""
    
    # Validar limite de usuários
    check_user_limit(current_tenant, db)
    
    # Criar motorista
    novo_motorista = Motorista(
        nome=motorista.nome,
        cpf=motorista.cpf,
        # ... outros campos
    )
    
    db.add(novo_motorista)
    db.commit()
    db.refresh(novo_motorista)
    
    return novo_motorista
```

---

## 📦 Exemplo: Endpoint de Pedidos

### Arquivo: `routers/pedidos.py`

```python
from middleware.plan_limits import check_order_limit

@router.post("/pedidos", response_model=PedidoResponse)
def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    current_tenant: Tenant = Depends(get_current_tenant)
):
    """Cria novo pedido com validação de limite mensal"""
    
    # Validar limite de pedidos do mês
    check_order_limit(current_tenant, db)
    
    # Criar pedido
    novo_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        origem=pedido.origem,
        destino=pedido.destino,
        # ... outros campos
    )
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    
    return novo_pedido
```

**Resposta se exceder limite**:
```json
{
  "detail": "Limite de pedidos do mês atingido (500). Faça upgrade do seu plano."
}
```

---

## 🔐 Dependency para Obter Tenant Atual

### Arquivo: `dependencies.py` (criar)

```python
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import Tenant

def get_current_tenant(
    tenant_id: int = Header(..., alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
) -> Tenant:
    """
    Obtém o tenant atual baseado no header X-Tenant-ID
    
    Em produção, isso deve vir do token JWT decodificado
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")
    
    if tenant.status == "cancelled":
        raise HTTPException(status_code=403, detail="Assinatura cancelada")
    
    return tenant
```

**Uso nos endpoints**:
```python
@router.post("/veiculos")
def criar_veiculo(
    veiculo: VeiculoCreate,
    db: Session = Depends(get_db),
    tenant: Tenant = Depends(get_current_tenant)  # ← Injeta automaticamente
):
    check_vehicle_limit(tenant, db)
    # ...
```

---

## 📊 Endpoint de Estatísticas de Uso

### Arquivo: `routers/tenants.py`

```python
from middleware.plan_limits import get_usage_stats

@router.get("/tenants/{tenant_id}/usage")
def get_usage(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """Retorna estatísticas de uso do tenant"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")
    
    return get_usage_stats(tenant, db)
```

**Resposta**:
```json
{
  "plan": "starter",
  "limits": {
    "users": {
      "max": 5,
      "current": 3,
      "available": 2
    },
    "vehicles": {
      "max": 10,
      "current": 7,
      "available": 3
    },
    "orders_per_month": {
      "max": 500,
      "current": 245,
      "available": 255
    }
  },
  "trial_ends_at": "2025-12-28T12:00:00",
  "is_trial": false
}
```

---

## 🎯 Checklist de Integração

### Para cada endpoint de criação:

- [ ] Importar função de validação do middleware
- [ ] Obter tenant atual (via dependency ou header)
- [ ] Chamar função de validação ANTES de criar recurso
- [ ] Tratar exceção HTTP 403 no frontend
- [ ] Mostrar mensagem de upgrade ao usuário

### Endpoints que precisam de validação:

#### Alta Prioridade:
- [ ] `POST /api/veiculos` - Validar `check_vehicle_limit`
- [ ] `POST /api/motoristas` - Validar `check_user_limit`
- [ ] `POST /api/pedidos` - Validar `check_order_limit`

#### Média Prioridade:
- [ ] `POST /api/clientes` - Pode adicionar limite futuro
- [ ] `POST /api/cotacoes` - Pode adicionar limite futuro

---

## 🚨 Tratamento de Erros no Frontend

### Exemplo em Vue.js:

```javascript
async function criarVeiculo(veiculoData) {
  try {
    const response = await api.post('/veiculos', veiculoData, {
      headers: {
        'X-Tenant-ID': tenantId
      }
    })
    
    // Sucesso
    showSuccess('Veículo criado com sucesso!')
    return response.data
    
  } catch (error) {
    if (error.response?.status === 403) {
      // Limite atingido
      showUpgradeModal({
        title: 'Limite Atingido',
        message: error.response.data.detail,
        currentPlan: 'starter',
        suggestedPlan: 'professional'
      })
    } else {
      showError('Erro ao criar veículo')
    }
  }
}
```

---

## 📈 Benefícios da Implementação

### Para o Negócio:
- ✅ **Monetização**: Força upgrade de plano
- ✅ **Controle**: Limita uso por plano
- ✅ **Previsibilidade**: Custos controlados

### Para o Usuário:
- ✅ **Transparência**: Sabe seus limites
- ✅ **Flexibilidade**: Pode fazer upgrade
- ✅ **Justiça**: Paga pelo que usa

---

## 🔄 Fluxo Completo

```
1. Usuário tenta criar veículo
   ↓
2. Frontend envia POST /api/veiculos
   ↓
3. Backend obtém tenant do header/JWT
   ↓
4. Middleware conta veículos atuais
   ↓
5. Compara com limite do plano
   ↓
6a. Se OK: Cria veículo → Retorna 201
6b. Se LIMITE: Retorna 403 com mensagem
   ↓
7. Frontend mostra modal de upgrade
```

---

## 🎨 Modal de Upgrade (Frontend)

```vue
<template>
  <div v-if="showUpgradeModal" class="modal">
    <div class="modal-content">
      <h2>🚀 Limite Atingido!</h2>
      <p>{{ upgradeMessage }}</p>
      
      <div class="plans-comparison">
        <div class="current-plan">
          <h3>Plano Atual: Starter</h3>
          <ul>
            <li>✅ 5 usuários</li>
            <li>❌ 10 veículos (limite atingido)</li>
            <li>✅ 500 pedidos/mês</li>
          </ul>
        </div>
        
        <div class="suggested-plan">
          <h3>Plano Professional</h3>
          <ul>
            <li>✅ 15 usuários</li>
            <li>✅ 30 veículos</li>
            <li>✅ Pedidos ilimitados</li>
          </ul>
          <button @click="upgradeNow">
            Fazer Upgrade - R$ 599/mês
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
```

---

## ✅ Status da Implementação

| Componente | Status |
|------------|--------|
| Middleware de validação | ✅ Completo |
| Contagem real de recursos | ✅ Completo |
| Endpoint de estatísticas | ✅ Completo |
| Exemplos de integração | ✅ Documentado |
| Integração em endpoints | ⏳ Pendente |
| Frontend - Modal upgrade | ⏳ Pendente |

---

## 📝 Próximos Passos

1. Criar `dependencies.py` com `get_current_tenant`
2. Atualizar endpoints existentes com validação
3. Criar componente de modal de upgrade no frontend
4. Testar fluxo completo de limite atingido
5. Adicionar analytics para rastrear upgrades

---

**🎉 Com essa implementação, o sistema terá controle completo de limites por plano!**
