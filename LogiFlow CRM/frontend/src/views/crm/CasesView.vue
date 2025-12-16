<template>
  <div class="cases-container">
    <!-- Header -->
    <div class="header">
      <div>
        <h1 class="title">Casos de Suporte</h1>
        <p class="subtitle">Gerencie tickets e atendimento ao cliente</p>
      </div>
      <button @click="openCreateModal" class="btn btn-primary">
        ➕ Novo Caso
      </button>
    </div>

    <!-- Estatísticas -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">🎫</div>
        <div class="stat-content">
          <p class="stat-label">Total de Casos</p>
          <p class="stat-value">{{ stats.total_cases }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📂</div>
        <div class="stat-content">
          <p class="stat-label">Casos Abertos</p>
          <p class="stat-value">{{ stats.open_cases }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <p class="stat-label">Casos Fechados</p>
          <p class="stat-value">{{ stats.closed_cases }}</p>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="filters-card">
      <div class="filters">
        <select v-model="filters.status" @change="loadCases" class="filter-select">
          <option value="">Todos os status</option>
          <option v-for="status in statuses" :key="status.value" :value="status.value">
            {{ status.label }}
          </option>
        </select>
        <select v-model="filters.priority" @change="loadCases" class="filter-select">
          <option value="">Todas as prioridades</option>
          <option v-for="priority in priorities" :key="priority.value" :value="priority.value">
            {{ priority.label }}
          </option>
        </select>
        <select v-model="filters.account_id" @change="loadCases" class="filter-select">
          <option value="">Todos os clientes</option>
          <option v-for="client in clients" :key="client.id" :value="client.id">
            {{ client.nome }}
          </option>
        </select>
      </div>
    </div>

    <!-- Lista de Casos -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando casos...</p>
    </div>

    <div v-else-if="cases.length === 0" class="empty-state">
      <span class="empty-icon">🎫</span>
      <h3>Nenhum caso encontrado</h3>
      <p>Crie seu primeiro caso de suporte</p>
    </div>

    <div v-else class="cases-list">
      <div v-for="caseItem in cases" :key="caseItem.id" class="case-card">
        <div class="case-header">
          <div class="case-info">
            <div class="case-title-row">
              <span v-if="caseItem.case_number" class="case-number">#{{ caseItem.case_number }}</span>
              <h3 class="case-name">{{ caseItem.name }}</h3>
            </div>
            <p v-if="caseItem.account_name" class="case-account">
              🏢 {{ caseItem.account_name }}
            </p>
          </div>
          <div class="case-badges">
            <span :class="['badge', 'badge-' + getStatusClass(caseItem.status)]">
              {{ getStatusLabel(caseItem.status) }}
            </span>
            <span :class="['badge', 'badge-' + getPriorityClass(caseItem.priority)]">
              {{ getPriorityLabel(caseItem.priority) }}
            </span>
          </div>
        </div>

        <div v-if="caseItem.description" class="case-description">
          {{ truncate(caseItem.description, 150) }}
        </div>

        <div class="case-footer">
          <div class="case-meta">
            <span v-if="caseItem.type" class="meta-item">
              📋 {{ caseItem.type }}
            </span>
            <span v-if="caseItem.assigned_user_name" class="meta-item">
              👤 {{ caseItem.assigned_user_name }}
            </span>
            <span v-if="caseItem.created_at" class="meta-item">
              📅 {{ formatDate(caseItem.created_at) }}
            </span>
          </div>
          <div class="case-actions">
            <button @click="editCase(caseItem)" class="btn btn-sm btn-secondary">
              ✏️ Editar
            </button>
            <button @click="deleteCase(caseItem)" class="btn btn-sm btn-danger">
              🗑️ Excluir
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Criar/Editar -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Editar Caso' : 'Novo Caso' }}</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <form @submit.prevent="saveCase" class="modal-body">
          <div class="form-group">
            <label>Assunto *</label>
            <input v-model="formData.name" type="text" required placeholder="Ex: Problema com entrega" />
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
              <label>Status *</label>
              <select v-model="formData.status" required>
                <option v-for="status in statuses" :key="status.value" :value="status.value">
                  {{ status.label }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Prioridade *</label>
              <select v-model="formData.priority" required>
                <option v-for="priority in priorities" :key="priority.value" :value="priority.value">
                  {{ priority.label }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Tipo</label>
            <select v-model="formData.type">
              <option value="">Selecione</option>
              <option value="User">Usuário</option>
              <option value="Administration">Administração</option>
              <option value="Product">Produto</option>
            </select>
          </div>

          <div class="form-group">
            <label>Descrição</label>
            <textarea v-model="formData.description" rows="4" placeholder="Descreva o problema em detalhes..."></textarea>
          </div>

          <div class="form-group">
            <label>Resolução</label>
            <textarea v-model="formData.resolution" rows="3" placeholder="Como o caso foi resolvido..."></textarea>
          </div>

          <div class="modal-actions">
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

const cases = ref([])
const clients = ref([])
const statuses = ref([])
const priorities = ref([])
const stats = ref({
  total_cases: 0,
  open_cases: 0,
  closed_cases: 0
})
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const editingId = ref(null)

const filters = ref({
  status: '',
  priority: '',
  account_id: ''
})

const formData = ref({
  name: '',
  account_id: '',
  status: 'New',
  priority: 'P3',
  type: '',
  description: '',
  resolution: ''
})

const loadCases = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.priority) params.priority = filters.value.priority
    if (filters.value.account_id) params.account_id = filters.value.account_id

    const response = await api.get('/cases', { params })
    cases.value = response.data || []
  } catch (error) {
    console.error('Erro ao carregar casos:', error)
    alert('Erro ao carregar casos')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await api.get('/cases/stats/summary')
    stats.value = response.data
  } catch (error) {
    console.error('Erro ao carregar estatísticas:', error)
  }
}

const loadStatuses = async () => {
  try {
    const response = await api.get('/cases/options/status')
    statuses.value = response.data.statuses
  } catch (error) {
    console.error('Erro ao carregar status:', error)
  }
}

const loadPriorities = async () => {
  try {
    const response = await api.get('/cases/options/priority')
    priorities.value = response.data.priorities
  } catch (error) {
    console.error('Erro ao carregar prioridades:', error)
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

const getStatusClass = (status) => {
  const classes = {
    'New': 'info',
    'Assigned': 'warning',
    'Closed': 'success',
    'Pending Input': 'warning',
    'Rejected': 'danger',
    'Duplicate': 'secondary'
  }
  return classes[status] || 'secondary'
}

const getStatusLabel = (status) => {
  return statuses.value.find(s => s.value === status)?.label || status
}

const getPriorityClass = (priority) => {
  const classes = {
    'P1': 'danger',
    'P2': 'warning',
    'P3': 'info',
    'Low': 'secondary'
  }
  return classes[priority] || 'secondary'
}

const getPriorityLabel = (priority) => {
  return priorities.value.find(p => p.value === priority)?.label || priority
}

const truncate = (text, length) => {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openCreateModal = () => {
  isEditing.value = false
  editingId.value = null
  formData.value = {
    name: '',
    account_id: '',
    status: 'New',
    priority: 'P3',
    type: '',
    description: '',
    resolution: ''
  }
  showModal.value = true
}

const editCase = (caseItem) => {
  isEditing.value = true
  editingId.value = caseItem.id
  formData.value = {
    name: caseItem.name || '',
    account_id: caseItem.account_id || '',
    status: caseItem.status || 'New',
    priority: caseItem.priority || 'P3',
    type: caseItem.type || '',
    description: caseItem.description || '',
    resolution: caseItem.resolution || ''
  }
  showModal.value = true
}

const saveCase = async () => {
  saving.value = true
  try {
    if (isEditing.value) {
      await api.put(`/cases/${editingId.value}`, formData.value)
      alert('Caso atualizado com sucesso!')
    } else {
      await api.post('/cases', formData.value)
      alert('Caso criado com sucesso!')
    }
    closeModal()
    await Promise.all([loadCases(), loadStats()])
  } catch (error) {
    console.error('Erro ao salvar caso:', error)
    alert('Erro ao salvar caso')
  } finally {
    saving.value = false
  }
}

const deleteCase = async (caseItem) => {
  if (!confirm(`Deseja realmente excluir o caso "${caseItem.name}"?`)) return

  try {
    await api.delete(`/cases/${caseItem.id}`)
    alert('Caso excluído com sucesso!')
    await Promise.all([loadCases(), loadStats()])
  } catch (error) {
    console.error('Erro ao excluir caso:', error)
    alert('Erro ao excluir caso')
  }
}

const closeModal = () => {
  showModal.value = false
}

onMounted(async () => {
  await Promise.all([
    loadStatuses(),
    loadPriorities(),
    loadClients()
  ])
  await Promise.all([
    loadCases(),
    loadStats()
  ])
})
</script>

<style scoped>
.cases-container {
  padding: 2rem;
  max-width: 1400px;
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

.filters-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  min-width: 200px;
}

.cases-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.case-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.case-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.case-info {
  flex: 1;
}

.case-title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.case-number {
  background: #e5e7eb;
  color: #374151;
  padding: 0.25rem 0.625rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.case-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.case-account {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.case-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.badge-info {
  background: #dbeafe;
  color: #1e40af;
}

.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

.badge-success {
  background: #d1fae5;
  color: #065f46;
}

.badge-danger {
  background: #fee2e2;
  color: #991b1b;
}

.badge-secondary {
  background: #e5e7eb;
  color: #374151;
}

.case-description {
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.case-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.case-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.meta-item {
  color: #6b7280;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.case-actions {
  display: flex;
  gap: 0.5rem;
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

.btn-danger:hover {
  background: #dc2626;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading, .empty-state {
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

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
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
