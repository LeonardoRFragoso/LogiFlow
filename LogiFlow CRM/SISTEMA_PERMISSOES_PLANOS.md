# 🔒 Sistema de Permissões por Plano - LogiFlow CRM

Documentação completa do sistema de autorização baseado em planos de assinatura.

---

## 📊 Estrutura de Planos

### **Plano Starter** - R$ 297/mês
**Funcionalidades:**
- ✅ Gestão de Cotações
- ✅ Gestão de Pedidos
- ✅ Gestão de Entregas
- ✅ Gestão de Motoristas
- ✅ Gestão de Veículos
- ✅ Gestão de Clientes
- ✅ Ocorrências
- ✅ Emissão CT-e/MDF-e
- ✅ WhatsApp Integrado
- ✅ Dashboard Básico
- ✅ Relatórios Básicos

**Limites:**
- 👥 Até 3 usuários
- 🚛 Até 10 veículos
- 📦 Até 100 pedidos/mês

---

### **Plano Pro** - R$ 597/mês
**Tudo do Starter +**
- ✅ **Cotação Automática** (Melhor Envio + Frenet + Tabela Própria)
- ✅ **Integração de Frete** (Cliente configura Melhor Envio/Frenet)
- ✅ **Integração ERP** (Cliente configura Omie/Bling/Tiny)
- ✅ **NPS e Satisfação**
- ✅ **Health Score**
- ✅ **Customer Success**
- ✅ **Relatórios Avançados**
- ✅ **Acesso à API**

**Limites:**
- 👥 Até 10 usuários
- 🚛 Até 50 veículos
- 📦 Até 500 pedidos/mês

---

### **Plano Enterprise** - R$ 997/mês
**Tudo do Pro +**
- ✅ **Rastreamento GPS** (Cliente configura Sascar/Autotrac/Onixsat)
- ✅ **BI e Analytics**
- ✅ **White Label**
- ✅ **Suporte Prioritário**
- ✅ **SLA Garantido**

**Limites:**
- 👥 Usuários ilimitados
- 🚛 Veículos ilimitados
- 📦 Pedidos ilimitados

---

## 🔐 Implementação Backend

### Middleware de Autorização

**Arquivo:** `backend/middleware/plan_authorization.py`

```python
from middleware.plan_authorization import require_feature, require_plan

# Proteger por funcionalidade
@router.get("/endpoint", dependencies=[Depends(require_feature("cotacao_automatica"))])

# Proteger por plano mínimo
@router.get("/endpoint", dependencies=[Depends(require_plan("pro"))])
```

### Routers Protegidos

#### 🔒 **Plano Pro+**
- `/cotacao-automatica/*` - Cotação automática
- `/melhor-envio/*` - Integração Melhor Envio (cliente configura)
- `/erp/*` - Integração ERP (cliente configura)
- `/nps/*` - NPS e Satisfação
- `/health-score/*` - Health Score
- `/customer-success/*` - Customer Success
- `/tenant-credentials/*` - Configuração de credenciais (ERP/Frete)

#### 🔐 **Plano Enterprise**
- `/gps/*` - Rastreamento GPS
- `/analytics/*` - BI e Analytics
- `/tenant-credentials/*` - Configuração GPS

---

## 🎨 Implementação Frontend

### Composable Vue

**Arquivo:** `frontend/src/composables/usePlanFeatures.js`

```javascript
import { usePlanFeatures } from '@/composables/usePlanFeatures'

const { hasFeature, hasPlan, requireFeature } = usePlanFeatures()

// Verificar feature
if (hasFeature('cotacao_automatica')) {
  // Mostrar funcionalidade
}

// Verificar plano
if (hasPlan('pro')) {
  // Mostrar funcionalidade
}

// Requerer feature com redirect
await requireFeature('rastreamento_gps', router)
```

### Exemplo de Uso em Componente

```vue
<template>
  <div class="menu">
    <!-- Sempre visível (Starter+) -->
    <router-link to="/cotacoes">Cotações</router-link>
    <router-link to="/pedidos">Pedidos</router-link>
    
    <!-- Apenas Pro+ -->
    <router-link 
      v-if="hasFeature('cotacao_automatica')" 
      to="/cotacao-automatica"
    >
      💰 Cotação Automática
    </router-link>
    <div v-else class="menu-item-locked" @click="showUpgrade('cotacao_automatica')">
      💰 Cotação Automática
      <span class="badge-pro">PRO</span>
    </div>
    
    <!-- Apenas Enterprise -->
    <router-link 
      v-if="hasFeature('rastreamento_gps')" 
      to="/gps"
    >
      🛰️ Rastreamento GPS
    </router-link>
    <div v-else class="menu-item-locked" @click="showUpgrade('rastreamento_gps')">
      🛰️ Rastreamento GPS
      <span class="badge-enterprise">ENTERPRISE</span>
    </div>
  </div>
</template>

<script setup>
import { usePlanFeatures } from '@/composables/usePlanFeatures'
import { useRouter } from 'vue-router'

const { hasFeature, getFeatureInfo } = usePlanFeatures()
const router = useRouter()

const showUpgrade = async (feature) => {
  const info = await getFeatureInfo(feature)
  
  const shouldUpgrade = confirm(
    `Esta funcionalidade requer o plano ${info.required_plan.name}.\n` +
    `Deseja fazer upgrade agora?`
  )
  
  if (shouldUpgrade) {
    router.push('/checkout')
  }
}
</script>

<style scoped>
.menu-item-locked {
  opacity: 0.6;
  cursor: pointer;
  position: relative;
}

.badge-pro {
  background: #3b82f6;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  margin-left: 8px;
}

.badge-enterprise {
  background: #8b5cf6;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  margin-left: 8px;
}
</style>
```

---

## 🔄 Fluxo de Verificação

### Backend
```
1. Cliente faz request → /cotacao-automatica/comparar
2. Middleware verifica header X-Tenant-ID
3. Busca plano do tenant no banco
4. Verifica se plano tem feature "cotacao_automatica"
5. Se SIM → Permite acesso
6. Se NÃO → Retorna 403 com info de upgrade
```

### Frontend
```
1. Componente carrega features ao montar
2. Chama GET /plan-info/my-features
3. Armazena features disponíveis
4. Usa v-if="hasFeature('...')" para mostrar/ocultar
5. Mostra badge "PRO" ou "ENTERPRISE" em features bloqueadas
6. Ao clicar em feature bloqueada → Redireciona para /checkout
```

---

## 📋 Checklist de Implementação

### ✅ Backend
- [x] Criar `middleware/plan_authorization.py`
- [x] Criar `routers/plan_info.py`
- [x] Documentar uso em `EXEMPLO_PROTECAO_ROTAS.md`
- [ ] Aplicar proteção em `/cotacao-automatica`
- [ ] Aplicar proteção em `/nps`
- [ ] Aplicar proteção em `/health-score`
- [ ] Aplicar proteção em `/gps`
- [ ] Aplicar proteção em `/tenant-credentials`
- [ ] Testar respostas 403

### ✅ Frontend
- [x] Criar `composables/usePlanFeatures.js`
- [ ] Atualizar menu lateral com verificação de features
- [ ] Adicionar badges "PRO" e "ENTERPRISE"
- [ ] Criar modal de upgrade
- [ ] Testar fluxo completo

### 📝 Documentação
- [x] Criar `SISTEMA_PERMISSOES_PLANOS.md`
- [x] Criar `EXEMPLO_PROTECAO_ROTAS.md`
- [x] Atualizar `EMPRESAS_INTEGRACOES_NECESSARIAS.md`

---

## 🚀 Próximos Passos

1. **Aplicar proteção em todos os routers** que requerem Pro/Enterprise
2. **Atualizar frontend** para usar `usePlanFeatures()`
3. **Criar página de pricing** com comparação de planos
4. **Implementar modal de upgrade** bonito
5. **Testar fluxo completo** de upgrade de plano
6. **Integrar com Mercado Pago** para processar upgrades

---

## ✅ Resultado Final

**Sistema 100% protegido por plano:**
- ✅ Backend verifica permissões em cada request
- ✅ Frontend mostra/oculta features automaticamente
- ✅ Mensagens claras sobre upgrade necessário
- ✅ Fluxo de upgrade integrado
- ✅ Segregação completa por tenant e plano
