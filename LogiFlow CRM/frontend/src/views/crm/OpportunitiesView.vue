<template>
  <div class="opportunities-container">
    <!-- Header -->
    <div class="header">
      <div>
        <h1 class="title">Pipeline de Oportunidades</h1>
        <p class="subtitle">Acompanhe suas oportunidades de negócio</p>
      </div>
      <button @click="openCreateModal" class="btn btn-primary">
        ➕ Nova Oportunidade
      </button>
    </div>

    <!-- Estatísticas -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <p class="stat-label">Valor Total</p>
          <p class="stat-value">R$ {{ formatCurrency(stats.total_pipeline_value) }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <p class="stat-label">Valor Ponderado</p>
          <p class="stat-value">R$ {{ formatCurrency(stats.weighted_pipeline_value) }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-content">
          <p class="stat-label">Total Oportunidades</p>
          <p class="stat-value">{{ stats.total_opportunities }}</p>
        </div>
      </div>
    </div>

    <!-- Kanban Board -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando pipeline...</p>
    </div>

    <div v-else class="kanban-board">
      <div 
        v-for="stage in stages" 
        :key="stage.value"
        class="kanban-column"
      >
        <div class="column-header">
          <h3>{{ stage.label }}</h3>
          <span class="count-badge">{{ getStageCount(stage.value) }}</span>
        </div>
        
        <div class="column-content">
          <div 
            v-for="opportunity in getOpportunitiesByStage(stage.value)" 
            :key="opportunity.id"
            class="opportunity-card"
            @click="editOpportunity(opportunity)"
          >
            <h4 class="opportunity-name">{{ opportunity.name }}</h4>
            
            <div class="opportunity-details">
              <div v-if="opportunity.account_name" class="detail-row">
                <span class="icon">🏢</span>
                <span>{{ opportunity.account_name }}</span>
              </div>
              
              <div class="detail-row">
                <span class="icon">💵</span>
                <span class="amount">R$ {{ formatCurrency(opportunity.amount) }}</span>
              </div>
              
              <div v-if="opportunity.probability" class="detail-row">
                <span class="icon">📈</span>
                <span>{{ opportunity.probability }}% de chance</span>
              </div>
              
              <div v-if="opportunity.date_closed" class="detail-row">
                <span class="icon">📅</span>
                <span>{{ formatDate(opportunity.date_closed) }}</span>
              </div>
            </div>

            <div v-if="opportunity.next_step" class="next-step">
              <strong>Próximo passo:</strong> {{ opportunity.next_step }}
            </div>
          </div>

          <div v-if="getOpportunitiesByStage(stage.value).length === 0" class="empty-column">
            <span>Nenhuma oportunidade</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Criar/Editar -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Editar Oportunidade' : 'Nova Oportunidade' }}</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <form @submit.prevent="saveOpportunity" class="modal-body">
          <div class="form-group">
            <label>Nome da Oportunidade *</label>
            <input v-model="formData.name" type="text" required placeholder="Ex: Contrato Logística 2025" />
          </div>

          <div class="form-group">
            <label>Cliente</label>
            <select v-model="formData.account_id">
              <option value="">Selecione um cliente</option>
              <option v-for="client in clients" :key="client.id" :value="client.id">
                {{ client.nome }}
              </option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Valor Estimado</label>
              <input v-model.number="formData.amount" type="number" step="0.01" placeholder="0.00" />
            </div>
            <div class="form-group">
              <label>Probabilidade (%)</label>
              <input v-model.number="formData.probability" type="number" min="0" max="100" />
            </div>
          </div>

          <div class="form-group">
            <label>Estágio *</label>
            <select v-model="formData.sales_stage" required>
              <option v-for="stage in stages" :key="stage.value" :value="stage.value">
                {{ stage.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Data Prevista de Fechamento</label>
            <input v-model="formData.date_closed" type="date" />
          </div>

          <div class="form-group">
            <label>Próximo Passo</label>
            <input v-model="formData.next_step" type="text" placeholder="Ex: Enviar proposta comercial" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Origem do Lead</label>
              <select v-model="formData.lead_source">
                <option value="">Selecione</option>
                <option value="Website">Website</option>
                <option value="Phone">Telefone</option>
                <option value="Email">Email</option>
                <option value="Referral">Indicação</option>
                <option value="Social Media">Redes Sociais</option>
              </select>
            </div>
            <div class="form-group">
              <label>Tipo</label>
              <select v-model="formData.opportunity_type">
                <option value="">Selecione</option>
                <option value="New Business">Novo Negócio</option>
                <option value="Existing Business">Cliente Existente</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Descrição</label>
            <textarea v-model="formData.description" rows="3" placeholder="Detalhes sobre a oportunidade..."></textarea>
          </div>

          <div class="modal-actions">
            <button 
              v-if="isEditing" 
              type="button" 
              @click="deleteOpportunity" 
              class="btn btn-danger"
              :disabled="saving"
            >
              🗑️ Excluir
            </button>
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? 'Salvando...' : 'Salvar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const opportunities = ref([])
const clients = ref([])
const stages = ref([])
const stats = ref({
  total_opportunities: 0,
  total_pipeline_value: 0,
  weighted_pipeline_value: 0
})
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const editingId = ref(null)

const formData = ref({
  name: '',
  account_id: '',
  amount: null,
  sales_stage: '',
  probability: null,
  date_closed: '',
  next_step: '',
  description: '',
  lead_source: '',
  opportunity_type: ''
})

const loadOpportunities = async () => {
  loading.value = true
  try {
    const response = await api.get('/opportunities')
    opportunities.value = response.data || []
  } catch (error) {
    console.error('Erro ao carregar oportunidades:', error)
    alert('Erro ao carregar oportunidades')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await api.get('/opportunities/stats/pipeline')
    stats.value = response.data
  } catch (error) {
    console.error('Erro ao carregar estatísticas:', error)
  }
}

const loadStages = async () => {
  try {
    const response = await api.get('/opportunities/sales-stages/list')
    stages.value = response.data.stages
  } catch (error) {
    console.error('Erro ao carregar estágios:', error)
  }
}

const loadClients = async () => {
  try {
    const response = await api.get('/clientes')
    clients.value = response.data.data || response.data
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
  }
}

const getOpportunitiesByStage = (stage) => {
  return opportunities.value.filter(opp => opp.sales_stage === stage)
}

const getStageCount = (stage) => {
  return getOpportunitiesByStage(stage).length
}

const formatCurrency = (value) => {
  if (!value) return '0,00'
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR')
}

const openCreateModal = () => {
  isEditing.value = false
  editingId.value = null
  formData.value = {
    name: '',
    account_id: '',
    amount: null,
    sales_stage: stages.value[0]?.value || '',
    probability: null,
    date_closed: '',
    next_step: '',
    description: '',
    lead_source: '',
    opportunity_type: ''
  }
  showModal.value = true
}

const editOpportunity = (opportunity) => {
  isEditing.value = true
  editingId.value = opportunity.id
  formData.value = {
    name: opportunity.name || '',
    account_id: opportunity.account_id || '',
    amount: opportunity.amount || null,
    sales_stage: opportunity.sales_stage || '',
    probability: opportunity.probability || null,
    date_closed: opportunity.date_closed || '',
    next_step: opportunity.next_step || '',
    description: opportunity.description || '',
    lead_source: opportunity.lead_source || '',
    opportunity_type: opportunity.opportunity_type || ''
  }
  showModal.value = true
}

const saveOpportunity = async () => {
  saving.value = true
  try {
    if (isEditing.value) {
      await api.put(`/opportunities/${editingId.value}`, formData.value)
      alert('Oportunidade atualizada com sucesso!')
    } else {
      await api.post('/opportunities', formData.value)
      alert('Oportunidade criada com sucesso!')
    }
    closeModal()
    await Promise.all([loadOpportunities(), loadStats()])
  } catch (error) {
    console.error('Erro ao salvar oportunidade:', error)
    alert('Erro ao salvar oportunidade')
  } finally {
    saving.value = false
  }
}

const deleteOpportunity = async () => {
  if (!confirm('Deseja realmente excluir esta oportunidade?')) return

  saving.value = true
  try {
    await api.delete(`/opportunities/${editingId.value}`)
    alert('Oportunidade excluída com sucesso!')
    closeModal()
    await Promise.all([loadOpportunities(), loadStats()])
  } catch (error) {
    console.error('Erro ao excluir oportunidade:', error)
    alert('Erro ao excluir oportunidade')
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  showModal.value = false
}

onMounted(async () => {
  await Promise.all([
    loadStages(),
    loadClients()
  ])
  await Promise.all([
    loadOpportunities(),
    loadStats()
  ])
})
</script>

<style scoped>
.opportunities-container {
  padding: 2rem;
  max-width: 100%;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.subtitle {
  color: #6b7280;
  margin: 0.5rem 0 0 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content {
  flex: 1;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0 0 0.25rem 0;
}

.stat-value {
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.kanban-board {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 1rem;
}

.kanban-column {
  flex: 0 0 320px;
  background: #f9fafb;
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  max-height: 70vh;
}

.column-header {
  padding: 1rem 1.25rem;
  background: white;
  border-radius: 0.75rem 0.75rem 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e5e7eb;
}

.column-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.count-badge {
  background: #e5e7eb;
  color: #374151;
  padding: 0.25rem 0.625rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.column-content {
  padding: 1rem;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.opportunity-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s;
}

.opportunity-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.opportunity-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.75rem 0;
}

.opportunity-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.detail-row .icon {
  font-size: 1rem;
}

.detail-row .amount {
  color: #10b981;
  font-weight: 600;
}

.next-step {
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
  font-size: 0.75rem;
  color: #6b7280;
}

.next-step strong {
  color: #374151;
}

.empty-column {
  text-align: center;
  padding: 2rem 1rem;
  color: #9ca3af;
  font-size: 0.875rem;
}

.btn {
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  background: #d1d5db;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.spinner {
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 0.75rem;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  line-height: 1;
}

.close-btn:hover {
  color: #1f2937;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 500;
  font-size: 0.875rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}
</style>
