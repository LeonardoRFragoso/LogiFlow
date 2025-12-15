# 🔒 Guia de Proteção de Rotas por Plano

Este documento mostra como proteger rotas do backend baseado no plano do cliente.

---

## 📋 Como Usar o Middleware

### 1. Importar o Middleware

```python
from fastapi import Depends
from middleware.plan_authorization import require_feature, require_plan
```

### 2. Proteger Rota por Funcionalidade

```python
@router.get(
    "/cotacao-automatica/comparar",
    dependencies=[Depends(require_feature("cotacao_automatica"))]
)
async def comparar_cotacoes():
    """
    Esta rota só funciona para clientes Pro e Enterprise
    """
    return {"message": "Comparação de cotações"}
```

### 3. Proteger Rota por Plano Mínimo

```python
@router.get(
    "/gps/rastreamento",
    dependencies=[Depends(require_plan("enterprise"))]
)
async def rastreamento_gps():
    """
    Esta rota só funciona para clientes Enterprise
    """
    return {"message": "Rastreamento GPS"}
```

---

## 🎯 Exemplos de Aplicação

### Router: cotacao_automatica.py

```python
from fastapi import APIRouter, Depends
from middleware.plan_authorization import require_feature

router = APIRouter()

# ✅ PROTEGIDO - Apenas Pro e Enterprise
@router.post(
    "/comparar",
    dependencies=[Depends(require_feature("cotacao_automatica"))]
)
async def comparar_cotacoes(data: CotacaoRequest):
    """Compara cotações de múltiplas fontes"""
    # Lógica da cotação
    pass

# ✅ PROTEGIDO - Apenas Pro e Enterprise
@router.get(
    "/historico",
    dependencies=[Depends(require_feature("cotacao_automatica"))]
)
async def historico_cotacoes():
    """Histórico de cotações automáticas"""
    pass
```

### Router: gps_tracking.py

```python
from fastapi import APIRouter, Depends
from middleware.plan_authorization import require_plan

router = APIRouter()

# ✅ PROTEGIDO - Apenas Enterprise
@router.get(
    "/posicoes",
    dependencies=[Depends(require_plan("enterprise"))]
)
async def obter_posicoes():
    """Posições em tempo real da frota"""
    pass

# ✅ PROTEGIDO - Apenas Enterprise
@router.get(
    "/historico/{veiculo_id}",
    dependencies=[Depends(require_plan("enterprise"))]
)
async def historico_rotas(veiculo_id: str):
    """Histórico de rotas de um veículo"""
    pass
```

### Router: nps.py

```python
from fastapi import APIRouter, Depends
from middleware.plan_authorization import require_feature

router = APIRouter()

# ✅ PROTEGIDO - Apenas Pro e Enterprise
@router.get(
    "/dashboard",
    dependencies=[Depends(require_feature("nps_satisfacao"))]
)
async def dashboard_nps():
    """Dashboard de NPS e satisfação"""
    pass

# ✅ PROTEGIDO - Apenas Pro e Enterprise
@router.post(
    "/pesquisa",
    dependencies=[Depends(require_feature("nps_satisfacao"))]
)
async def criar_pesquisa(data: PesquisaRequest):
    """Cria nova pesquisa NPS"""
    pass
```

### Router: tenant_credentials.py

```python
from fastapi import APIRouter, Depends
from middleware.plan_authorization import require_plan

router = APIRouter()

# ✅ PROTEGIDO - Apenas Pro e Enterprise (para ERP/Frete)
@router.post(
    "/credentials",
    dependencies=[Depends(require_plan("pro"))]
)
async def criar_credencial(data: CredentialCreate):
    """
    Criar credenciais de integração
    Requer plano Pro ou superior
    """
    # Validação adicional por tipo
    if data.integration_type == "gps":
        # GPS requer Enterprise
        # TODO: Adicionar verificação específica
        pass
    
    pass
```

---

## 🚫 Resposta de Erro

Quando um cliente tenta acessar uma funcionalidade sem permissão:

```json
{
  "detail": {
    "error": "Funcionalidade não disponível no seu plano",
    "feature": "cotacao_automatica",
    "current_plan": "Starter",
    "required_plan": "Pro",
    "upgrade_url": "/checkout"
  }
}
```

Status Code: **403 Forbidden**

---

## 📊 Mapeamento Completo

### Funcionalidades por Plano

| Funcionalidade | Starter | Pro | Enterprise |
|----------------|---------|-----|------------|
| Cotações | ✅ | ✅ | ✅ |
| Pedidos | ✅ | ✅ | ✅ |
| CT-e/MDF-e | ✅ | ✅ | ✅ |
| WhatsApp | ✅ | ✅ | ✅ |
| **Cotação Automática** | ❌ | ✅ | ✅ |
| **Integração Frete** | ❌ | ✅ | ✅ |
| **Integração ERP** | ❌ | ✅ | ✅ |
| **NPS/Satisfação** | ❌ | ✅ | ✅ |
| **Health Score** | ❌ | ✅ | ✅ |
| **Rastreamento GPS** | ❌ | ❌ | ✅ |
| **BI Analytics** | ❌ | ❌ | ✅ |

### Routers a Proteger

```python
# ✅ LIVRE (Todos os planos)
/cotacoes
/pedidos
/entregas
/motoristas
/veiculos
/clientes
/ocorrencias
/fiscal
/whatsapp
/dashboard

# 🔒 PRO+ (Requer Pro ou Enterprise)
/cotacao-automatica
/melhor-envio
/erp
/nps
/health-score
/customer-success
/tenant-credentials (para ERP/Frete)

# 🔐 ENTERPRISE (Requer Enterprise)
/gps
/tenant-credentials (para GPS)
/analytics
```

---

## ✅ Checklist de Implementação

### Backend
- [x] Criar middleware `plan_authorization.py`
- [x] Criar router `plan_info.py`
- [ ] Aplicar `require_feature()` em rotas Pro+
- [ ] Aplicar `require_plan("enterprise")` em rotas Enterprise
- [ ] Testar respostas 403 com Postman

### Frontend
- [ ] Criar composable `usePlanFeatures.js`
- [ ] Ocultar menus de features não disponíveis
- [ ] Mostrar badge "Upgrade" em features bloqueadas
- [ ] Redirecionar para /checkout ao clicar em feature bloqueada

---

## 🎨 Exemplo Frontend (Vue)

```vue
<template>
  <div>
    <!-- Sempre visível -->
    <router-link to="/cotacoes">Cotações</router-link>
    
    <!-- Apenas Pro+ -->
    <router-link 
      v-if="hasFeature('cotacao_automatica')" 
      to="/cotacao-automatica"
    >
      Cotação Automática
    </router-link>
    
    <!-- Bloqueado com badge -->
    <div v-else class="feature-locked">
      <span>Cotação Automática</span>
      <span class="badge-pro">Pro</span>
    </div>
    
    <!-- Apenas Enterprise -->
    <router-link 
      v-if="hasFeature('rastreamento_gps')" 
      to="/gps"
    >
      Rastreamento GPS
    </router-link>
  </div>
</template>

<script setup>
import { usePlanFeatures } from '@/composables/usePlanFeatures'

const { hasFeature, currentPlan } = usePlanFeatures()
</script>
```

---

## 🔧 Próximos Passos

1. **Aplicar proteção em todos os routers** (cotacao_automatica, gps_tracking, nps, etc)
2. **Criar composable Vue** para verificar features no frontend
3. **Atualizar menu lateral** para mostrar/ocultar itens por plano
4. **Adicionar badges** "Pro" e "Enterprise" em features bloqueadas
5. **Testar fluxo completo** de upgrade de plano
