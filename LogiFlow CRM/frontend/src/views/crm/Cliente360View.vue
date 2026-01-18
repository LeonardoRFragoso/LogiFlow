<template>
  <div class="cliente-360-view">
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando informações do cliente...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p class="error-message">{{ error }}</p>
      <button @click="loadData" class="retry-btn">Tentar Novamente</button>
    </div>
    
    <div v-else-if="cliente360" class="cliente-360-content">
      <!-- Header do Cliente -->
      <div class="cliente-header">
        <div class="header-main">
          <div class="cliente-avatar">
            {{ getInitials(cliente360.cliente.razao_social) }}
          </div>
          <div class="cliente-info">
            <h1 class="cliente-nome">{{ cliente360.cliente.razao_social }}</h1>
            <p v-if="cliente360.cliente.nome_fantasia" class="cliente-fantasia">
              {{ cliente360.cliente.nome_fantasia }}
            </p>
            <div class="cliente-meta">
              <span class="meta-badge">{{ cliente360.cliente.segmento || 'Sem segmento' }}</span>
              <span class="meta-badge">{{ cliente360.cliente.porte || 'Porte não definido' }}</span>
              <span class="meta-badge" :class="`status-${cliente360.cliente.status_comercial}`">
                {{ cliente360.cliente.status_comercial }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="header-actions">
          <button @click="handleNewInteraction" class="action-btn primary">
            Nova Interação
          </button>
          <button @click="handleNewOpportunity" class="action-btn secondary">
            Nova Oportunidade
          </button>
        </div>
      </div>
      
      <!-- Grid Principal -->
      <div class="main-grid">
        <!-- Health Score -->
        <div class="grid-item health-score-section">
          <HealthScoreCard
            :score="cliente360.health_score.score"
            :variacao="cliente360.health_score.variacao"
            :categoria="cliente360.health_score.categoria"
            :fatores="cliente360.health_score.fatores"
            :show-factors="true"
          />
        </div>
        
        <!-- Métricas Rápidas -->
        <div class="grid-item metrics-section">
          <h3 class="section-title">Métricas Principais</h3>
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="metric-label">Valor Total Gasto</div>
              <div class="metric-value">R$ {{ formatCurrency(cliente360.metricas.valor_total_gasto) }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Ticket Médio</div>
              <div class="metric-value">R$ {{ formatCurrency(cliente360.metricas.ticket_medio) }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Total Pedidos</div>
              <div class="metric-value">{{ cliente360.metricas.total_pedidos }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Oportunidades</div>
              <div class="metric-value">{{ cliente360.metricas.total_oportunidades }}</div>
            </div>
          </div>
        </div>
        
        <!-- Informações de Contato -->
        <div class="grid-item contact-section">
          <h3 class="section-title">Informações de Contato</h3>
          <div class="contact-list">
            <div v-if="cliente360.cliente.email" class="contact-item">
              <span class="contact-label">Email:</span>
              <a :href="`mailto:${cliente360.cliente.email}`" class="contact-value link">
                {{ cliente360.cliente.email }}
              </a>
            </div>
            <div v-if="cliente360.cliente.telefone" class="contact-item">
              <span class="contact-label">Telefone:</span>
              <span class="contact-value">{{ cliente360.cliente.telefone }}</span>
            </div>
            <div v-if="cliente360.cliente.cnpj" class="contact-item">
              <span class="contact-label">CNPJ:</span>
              <span class="contact-value">{{ formatCNPJ(cliente360.cliente.cnpj) }}</span>
            </div>
            <div v-if="cliente360.cliente.cidade" class="contact-item">
              <span class="contact-label">Localização:</span>
              <span class="contact-value">{{ cliente360.cliente.cidade }}/{{ cliente360.cliente.uf }}</span>
            </div>
            <div v-if="cliente360.cliente.responsavel_comercial" class="contact-item">
              <span class="contact-label">Responsável Comercial:</span>
              <span class="contact-value">{{ cliente360.cliente.responsavel_comercial }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Tabs -->
      <div class="tabs-section">
        <div class="tabs-header">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            class="tab-btn"
            :class="{ active: activeTab === tab.value }"
            @click="activeTab = tab.value"
          >
            {{ tab.label }}
            <span class="tab-count">{{ getTabCount(tab.value) }}</span>
          </button>
        </div>
        
        <div class="tabs-content">
          <!-- Timeline -->
          <div v-show="activeTab === 'timeline'" class="tab-panel">
            <div v-if="cliente360.timeline && cliente360.timeline.length > 0" class="timeline-container">
              <TimelineEvent
                v-for="(event, index) in cliente360.timeline"
                :key="index"
                :event="event"
                :is-last="index === cliente360.timeline.length - 1"
              />
            </div>
            <div v-else class="empty-state">
              <p>Nenhum evento no histórico ainda</p>
            </div>
          </div>
          
          <!-- Oportunidades -->
          <div v-show="activeTab === 'oportunidades'" class="tab-panel">
            <div v-if="cliente360.oportunidades_recentes && cliente360.oportunidades_recentes.length > 0" class="opportunities-list">
              <div
                v-for="opp in cliente360.oportunidades_recentes"
                :key="opp.id"
                class="opportunity-item"
                @click="handleOpenOpportunity(opp)"
              >
                <div class="opp-header">
                  <h4 class="opp-name">{{ opp.nome }}</h4>
                  <span class="opp-stage" :class="`stage-${opp.sales_stage}`">
                    {{ formatStage(opp.sales_stage) }}
                  </span>
                </div>
                <div class="opp-details">
                  <span class="opp-value">R$ {{ formatCurrency(opp.valor_estimado) }}</span>
                  <span v-if="opp.probabilidade" class="opp-probability">{{ opp.probabilidade }}% prob.</span>
                  <span class="opp-date">{{ formatDate(opp.criado_em) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>Nenhuma oportunidade cadastrada</p>
              <button @click="handleNewOpportunity" class="empty-action-btn">
                Criar Primeira Oportunidade
              </button>
            </div>
          </div>
          
          <!-- Interações -->
          <div v-show="activeTab === 'interacoes'" class="tab-panel">
            <div v-if="cliente360.interacoes_recentes && cliente360.interacoes_recentes.length > 0" class="interactions-list">
              <div
                v-for="inter in cliente360.interacoes_recentes"
                :key="inter.id"
                class="interaction-item"
              >
                <div class="inter-icon" :class="`type-${inter.tipo}`">
                  {{ getInteractionIcon(inter.tipo) }}
                </div>
                <div class="inter-content">
                  <div class="inter-header">
                    <h4 class="inter-subject">{{ inter.assunto }}</h4>
                    <span class="inter-date">{{ formatDate(inter.data_interacao) }}</span>
                  </div>
                  <div class="inter-meta">
                    <span class="inter-type">{{ formatInteractionType(inter.tipo) }}</span>
                    <span v-if="inter.responsavel" class="inter-responsible">{{ inter.responsavel }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>Nenhuma interação registrada</p>
              <button @click="handleNewInteraction" class="empty-action-btn">
                Registrar Primeira Interação
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCRMStore } from '../../stores/crmStore'
import HealthScoreCard from '../../components/crm/HealthScoreCard.vue'
import TimelineEvent from '../../components/crm/TimelineEvent.vue'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const crmStore = useCRMStore()

const loading = ref(false)
const error = ref(null)
const cliente360 = ref(null)
const activeTab = ref('timeline')

const tabs = [
  { value: 'timeline', label: 'Timeline' },
  { value: 'oportunidades', label: 'Oportunidades' },
  { value: 'interacoes', label: 'Interações' }
]

onMounted(() => {
  loadData()
})

async function loadData() {
  const clienteId = route.params.id
  if (!clienteId) {
    error.value = 'ID do cliente não fornecido'
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    const data = await crmStore.loadCliente360(clienteId)
    cliente360.value = data
  } catch (err) {
    error.value = 'Erro ao carregar dados do cliente'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function getTabCount(tabValue) {
  if (!cliente360.value) return 0
  
  switch (tabValue) {
    case 'timeline':
      return cliente360.value.timeline?.length || 0
    case 'oportunidades':
      return cliente360.value.oportunidades_recentes?.length || 0
    case 'interacoes':
      return cliente360.value.interacoes_recentes?.length || 0
    default:
      return 0
  }
}

function getInitials(name) {
  return name?.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() || 'CL'
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR').format(value || 0)
}

function formatCNPJ(cnpj) {
  return cnpj?.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5') || cnpj
}

function formatDate(date) {
  return dayjs(date).format('DD/MM/YYYY')
}

function formatStage(stage) {
  const stages = {
    lead: 'Lead',
    qualificado: 'Qualificado',
    proposta: 'Proposta',
    negociacao: 'Negociação',
    ganho: 'Ganho',
    perdido: 'Perdido'
  }
  return stages[stage] || stage
}

function formatInteractionType(type) {
  const types = {
    call: 'Ligação',
    email: 'E-mail',
    meeting: 'Reunião',
    whatsapp: 'WhatsApp',
    follow_up: 'Follow-up',
    note: 'Nota'
  }
  return types[type] || type
}

function getInteractionIcon(type) {
  const icons = {
    call: '📞',
    email: '✉️',
    meeting: '👥',
    whatsapp: '💬',
    follow_up: '🔔',
    note: '📝'
  }
  return icons[type] || '📌'
}

function handleNewInteraction() {
  router.push(`/crm/interactions/new?cliente_id=${route.params.id}`)
}

function handleNewOpportunity() {
  router.push(`/crm/opportunities/new?cliente_id=${route.params.id}`)
}

function handleOpenOpportunity(opp) {
  router.push(`/crm/opportunities/${opp.id}`)
}
</script>

<style scoped>
.cliente-360-view {
  min-height: 100vh;
  background: #f9fafb;
  padding: 24px;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #ef4444;
  margin-bottom: 16px;
}

.retry-btn {
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.cliente-header {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-main {
  display: flex;
  gap: 20px;
}

.cliente-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  flex-shrink: 0;
}

.cliente-nome {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px 0;
}

.cliente-fantasia {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 12px 0;
}

.cliente-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.meta-badge {
  padding: 4px 12px;
  background: #f3f4f6;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.meta-badge.status-ativo {
  background: #d1fae5;
  color: #065f46;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
}

.action-btn.secondary {
  background: white;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.grid-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 16px 0;
}

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.metric-card {
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.metric-label {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
}

.contact-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.contact-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
}

.contact-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.contact-value {
  font-size: 14px;
  color: #111827;
}

.contact-value.link {
  color: #3b82f6;
  text-decoration: none;
}

.contact-value.link:hover {
  text-decoration: underline;
}

.tabs-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabs-header {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.tab-btn {
  flex: 1;
  padding: 16px 24px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.tab-btn:hover {
  color: #3b82f6;
  background: white;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: white;
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: #e5e7eb;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.tab-btn.active .tab-count {
  background: #dbeafe;
  color: #1e40af;
}

.tabs-content {
  padding: 24px;
}

.tab-panel {
  min-height: 400px;
}

.timeline-container {
  max-width: 900px;
}

.opportunities-list,
.interactions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.opportunity-item {
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.opportunity-item:hover {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.opp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.opp-name {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.opp-stage {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.opp-details {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #6b7280;
}

.opp-value {
  color: #10b981;
  font-weight: 600;
}

.interaction-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.inter-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: white;
  border: 2px solid #e5e7eb;
  flex-shrink: 0;
}

.inter-content {
  flex: 1;
}

.inter-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.inter-subject {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.inter-date {
  font-size: 13px;
  color: #9ca3af;
}

.inter-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #6b7280;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #9ca3af;
}

.empty-action-btn {
  margin-top: 16px;
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.empty-action-btn:hover {
  background: #2563eb;
}
</style>
