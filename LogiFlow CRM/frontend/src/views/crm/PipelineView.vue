<template>
  <div class="pipeline-view">
    <div class="pipeline-header">
      <div class="header-left">
        <h1 class="page-title">Pipeline de Vendas</h1>
        <p class="page-subtitle">Gerencie suas oportunidades por estágio</p>
      </div>
      
      <div class="header-actions">
        <div class="view-toggle">
          <button 
            class="toggle-btn"
            :class="{ active: viewMode === 'kanban' }"
            @click="viewMode = 'kanban'"
          >
            Kanban
          </button>
          <button 
            class="toggle-btn"
            :class="{ active: viewMode === 'list' }"
            @click="viewMode = 'list'"
          >
            Lista
          </button>
        </div>
        
        <button @click="handleNewOpportunity" class="new-opp-btn">
          + Nova Oportunidade
        </button>
      </div>
    </div>
    
    <div v-if="loading && !opportunities.length" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando pipeline...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p class="error-message">{{ error }}</p>
      <button @click="loadOpportunities" class="retry-btn">Tentar Novamente</button>
    </div>
    
    <div v-else class="pipeline-content">
      <!-- Kanban View -->
      <PipelineKanban
        v-if="viewMode === 'kanban'"
        :opportunities="opportunities"
        @move-stage="handleMoveStage"
        @open-details="handleOpenDetails"
      />
      
      <!-- List View -->
      <div v-else class="list-view">
        <div class="list-filters">
          <select v-model="filters.stage" class="filter-select">
            <option value="">Todos os estágios</option>
            <option value="lead">Lead</option>
            <option value="qualificado">Qualificado</option>
            <option value="proposta">Proposta</option>
            <option value="negociacao">Negociação</option>
            <option value="ganho">Ganho</option>
            <option value="perdido">Perdido</option>
          </select>
          
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar oportunidades..."
            class="search-input"
          />
        </div>
        
        <div class="opportunities-table">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Cliente</th>
                <th>Valor</th>
                <th>Estágio</th>
                <th>Probabilidade</th>
                <th>Responsável</th>
                <th>Criada em</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="opp in filteredOpportunities"
                :key="opp.id"
                class="table-row"
                @click="handleOpenDetails(opp)"
              >
                <td class="cell-name">{{ opp.nome }}</td>
                <td>{{ opp.cliente_nome }}</td>
                <td class="cell-value">R$ {{ formatCurrency(opp.valor_estimado) }}</td>
                <td>
                  <span class="stage-badge" :class="`stage-${opp.sales_stage}`">
                    {{ formatStage(opp.sales_stage) }}
                  </span>
                </td>
                <td class="cell-probability">{{ opp.probabilidade }}%</td>
                <td>{{ opp.responsavel_nome || '-' }}</td>
                <td class="cell-date">{{ formatDate(opp.criado_em) }}</td>
                <td class="cell-actions">
                  <button class="action-icon-btn" @click.stop="handleEdit(opp)">✏️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <!-- Modal de Detalhes (simplificado) -->
    <div v-if="selectedOpportunity" class="modal-overlay" @click="closeDetails">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedOpportunity.nome }}</h2>
          <button class="close-btn" @click="closeDetails">×</button>
        </div>
        <div class="modal-body">
          <p><strong>Cliente:</strong> {{ selectedOpportunity.cliente_nome }}</p>
          <p><strong>Valor:</strong> R$ {{ formatCurrency(selectedOpportunity.valor_estimado) }}</p>
          <p><strong>Estágio:</strong> {{ formatStage(selectedOpportunity.sales_stage) }}</p>
          <p><strong>Probabilidade:</strong> {{ selectedOpportunity.probabilidade }}%</p>
          <p v-if="selectedOpportunity.descricao"><strong>Descrição:</strong> {{ selectedOpportunity.descricao }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCRMStore } from '../../stores/crmStore'
import PipelineKanban from '../../components/crm/PipelineKanban.vue'
import dayjs from 'dayjs'

const router = useRouter()
const crmStore = useCRMStore()

const viewMode = ref('kanban')
const searchQuery = ref('')
const filters = ref({
  stage: ''
})
const selectedOpportunity = ref(null)

const opportunities = computed(() => crmStore.opportunities)
const loading = computed(() => crmStore.loading)
const error = computed(() => crmStore.error)

const filteredOpportunities = computed(() => {
  let result = opportunities.value
  
  if (filters.value.stage) {
    result = result.filter(o => o.sales_stage === filters.value.stage)
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(o =>
      o.nome.toLowerCase().includes(query) ||
      o.cliente_nome?.toLowerCase().includes(query)
    )
  }
  
  return result
})

onMounted(() => {
  loadOpportunities()
})

async function loadOpportunities() {
  try {
    await crmStore.loadOpportunities()
  } catch (err) {
    console.error('Erro ao carregar oportunidades:', err)
  }
}

async function handleMoveStage({ opportunityId, newStage }) {
  try {
    await crmStore.moveOpportunityStage(opportunityId, newStage)
  } catch (err) {
    console.error('Erro ao mover oportunidade:', err)
    alert('Erro ao atualizar estágio da oportunidade')
  }
}

function handleOpenDetails(opp) {
  selectedOpportunity.value = opp
}

function closeDetails() {
  selectedOpportunity.value = null
}

function handleEdit(opp) {
  router.push(`/crm/opportunities/${opp.id}/edit`)
}

function handleNewOpportunity() {
  router.push('/crm/opportunities/new')
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR').format(value || 0)
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

function formatDate(date) {
  return dayjs(date).format('DD/MM/YYYY')
}
</script>

<style scoped>
.pipeline-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.pipeline-header {
  background: white;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 4px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.view-toggle {
  display: flex;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 4px;
}

.toggle-btn {
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active {
  background: white;
  color: #111827;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.new-opp-btn {
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.new-opp-btn:hover {
  background: #2563eb;
}

.pipeline-content {
  flex: 1;
  min-height: 0;
  overflow: auto;
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

.list-view {
  padding: 24px;
}

.list-filters {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.filter-select,
.search-input {
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.opportunities-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f9fafb;
}

th {
  padding: 12px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e5e7eb;
}

.table-row {
  cursor: pointer;
  transition: background 0.2s;
}

.table-row:hover {
  background: #f9fafb;
}

td {
  padding: 16px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid #f3f4f6;
}

.cell-name {
  font-weight: 600;
  color: #111827;
}

.cell-value {
  color: #10b981;
  font-weight: 600;
}

.stage-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.stage-lead { background: #f3f4f6; color: #6b7280; }
.stage-qualificado { background: #dbeafe; color: #1e40af; }
.stage-proposta { background: #fed7aa; color: #92400e; }
.stage-negociacao { background: #e9d5ff; color: #6b21a8; }
.stage-ganho { background: #d1fae5; color: #065f46; }
.stage-perdido { background: #fee2e2; color: #991b1b; }

.cell-probability {
  font-weight: 500;
}

.cell-date {
  color: #9ca3af;
  font-size: 13px;
}

.action-icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.action-icon-btn:hover {
  background: #f3f4f6;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  color: #9ca3af;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  margin: 0 0 12px 0;
  font-size: 14px;
  line-height: 1.6;
}
</style>
