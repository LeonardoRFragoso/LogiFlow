<template>
  <div class="nps-dashboard">
    <div class="page-header">
      <h1>⭐ NPS e Satisfação</h1>
      <p>Monitore a satisfação dos seus clientes em tempo real</p>
    </div>

    <!-- Cards de Resumo -->
    <div class="stats-grid">
      <div class="stat-card nps">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>NPS Atual</h3>
          <div class="stat-value" :class="npsClass">{{ dashboard.nps?.score || 0 }}</div>
          <p class="stat-label">{{ npsLabel }}</p>
        </div>
      </div>

      <div class="stat-card promotores">
        <div class="stat-icon">😊</div>
        <div class="stat-content">
          <h3>Promotores</h3>
          <div class="stat-value">{{ dashboard.nps?.promotores || 0 }}</div>
          <p class="stat-label">{{ promotoresPercentual }}% do total</p>
        </div>
      </div>

      <div class="stat-card neutros">
        <div class="stat-icon">😐</div>
        <div class="stat-content">
          <h3>Neutros</h3>
          <div class="stat-value">{{ dashboard.nps?.neutros || 0 }}</div>
          <p class="stat-label">{{ neutrosPercentual }}% do total</p>
        </div>
      </div>

      <div class="stat-card detratores">
        <div class="stat-icon">😞</div>
        <div class="stat-content">
          <h3>Detratores</h3>
          <div class="stat-value">{{ dashboard.nps?.detratores || 0 }}</div>
          <p class="stat-label">{{ detratoresPercentual }}% do total</p>
        </div>
      </div>

      <div class="stat-card csat">
        <div class="stat-icon">⭐</div>
        <div class="stat-content">
          <h3>CSAT Médio</h3>
          <div class="stat-value">{{ dashboard.csat?.media_score?.toFixed(1) || '0.0' }}</div>
          <p class="stat-label">de 5.0 estrelas</p>
        </div>
      </div>

      <div class="stat-card respostas">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>Respostas</h3>
          <div class="stat-value">{{ totalRespostas }}</div>
          <p class="stat-label">últimos 30 dias</p>
        </div>
      </div>
    </div>

    <!-- Alertas de Detratores -->
    <div v-if="alertas.length > 0" class="alertas-section">
      <h2>🚨 Alertas Ativos</h2>
      <div class="alertas-grid">
        <div v-for="alerta in alertas" :key="alerta.id" class="alerta-card">
          <div class="alerta-header">
            <span class="alerta-tipo">{{ alerta.tipo === 'nps' ? 'NPS Detrator' : 'CSAT Baixo' }}</span>
            <span class="alerta-data">{{ formatDate(alerta.data) }}</span>
          </div>
          <div class="alerta-body">
            <h4>{{ alerta.cliente_nome }}</h4>
            <p class="alerta-score">Score: {{ alerta.score }}</p>
            <p v-if="alerta.feedback" class="alerta-feedback">"{{ alerta.feedback }}"</p>
          </div>
          <div class="alerta-actions">
            <button @click="criarAcaoCS(alerta)" class="btn-action">Criar Ação CS</button>
            <button @click="marcarResolvido(alerta)" class="btn-secondary">Marcar Resolvido</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pesquisas Pendentes -->
    <div class="pesquisas-section">
      <div class="section-header">
        <h2>📋 Pesquisas Pendentes</h2>
        <button @click="agendarPesquisas" class="btn-primary">
          <span>➕</span> Agendar Novas Pesquisas
        </button>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Tipo</th>
              <th>Enviada em</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pesquisa in pesquisasPendentes" :key="pesquisa.id">
              <td>{{ pesquisa.cliente_nome }}</td>
              <td>
                <span class="badge" :class="pesquisa.tipo">
                  {{ pesquisa.tipo === 'nps' ? 'NPS' : 'CSAT' }}
                </span>
              </td>
              <td>{{ formatDate(pesquisa.data_envio) }}</td>
              <td>
                <span class="status" :class="pesquisa.status">
                  {{ statusLabel(pesquisa.status) }}
                </span>
              </td>
              <td>
                <button @click="reenviarPesquisa(pesquisa)" class="btn-icon" title="Reenviar">
                  📧
                </button>
                <button @click="cancelarPesquisa(pesquisa)" class="btn-icon" title="Cancelar">
                  ❌
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Gráfico de Tendência -->
    <div class="tendencia-section">
      <h2>📈 Tendência NPS (Últimos 6 Meses)</h2>
      <div class="chart-container">
        <div class="chart-placeholder">
          <p>Gráfico de tendência será renderizado aqui</p>
          <p class="chart-data">{{ tendenciaData }}</p>
        </div>
      </div>
    </div>

    <!-- Modal de Criar Pesquisa -->
    <div v-if="showCriarPesquisa" class="modal-overlay" @click="showCriarPesquisa = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Criar Nova Pesquisa</h3>
          <button @click="showCriarPesquisa = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Tipo de Pesquisa</label>
            <select v-model="novaPesquisa.tipo" class="form-control">
              <option value="nps">NPS (30 dias)</option>
              <option value="nps_90">NPS (90 dias)</option>
              <option value="csat">CSAT (Pós-Suporte)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Cliente</label>
            <input v-model="novaPesquisa.cliente_id" type="text" class="form-control" placeholder="ID do Cliente">
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCriarPesquisa = false" class="btn-secondary">Cancelar</button>
          <button @click="criarPesquisa" class="btn-primary">Criar Pesquisa</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const dashboard = ref({
  nps: null,
  csat: null,
  tendencia: []
})

const alertas = ref([])
const pesquisasPendentes = ref([])
const showCriarPesquisa = ref(false)
const novaPesquisa = ref({
  tipo: 'nps',
  cliente_id: ''
})

const npsClass = computed(() => {
  const score = dashboard.value.nps?.score || 0
  if (score >= 75) return 'excelente'
  if (score >= 50) return 'bom'
  if (score >= 0) return 'regular'
  return 'ruim'
})

const npsLabel = computed(() => {
  const score = dashboard.value.nps?.score || 0
  if (score >= 75) return 'Excelente'
  if (score >= 50) return 'Bom'
  if (score >= 0) return 'Regular'
  return 'Crítico'
})

const totalRespostas = computed(() => {
  return (dashboard.value.nps?.total_respostas || 0) + (dashboard.value.csat?.total_respostas || 0)
})

const promotoresPercentual = computed(() => {
  const total = dashboard.value.nps?.total_respostas || 0
  if (total === 0) return 0
  return Math.round((dashboard.value.nps?.promotores || 0) / total * 100)
})

const neutrosPercentual = computed(() => {
  const total = dashboard.value.nps?.total_respostas || 0
  if (total === 0) return 0
  return Math.round((dashboard.value.nps?.neutros || 0) / total * 100)
})

const detratoresPercentual = computed(() => {
  const total = dashboard.value.nps?.total_respostas || 0
  if (total === 0) return 0
  return Math.round((dashboard.value.nps?.detratores || 0) / total * 100)
})

const tendenciaData = computed(() => {
  return JSON.stringify(dashboard.value.tendencia || [])
})

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('pt-BR')
}

const statusLabel = (status) => {
  const labels = {
    'pendente': 'Pendente',
    'enviada': 'Enviada',
    'respondida': 'Respondida',
    'expirada': 'Expirada'
  }
  return labels[status] || status
}

const carregarDashboard = async () => {
  try {
    const response = await axios.get('/satisfacao/dashboard')
    if (response.data.success) {
      dashboard.value = response.data.data
    }
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  }
}

const carregarAlertas = async () => {
  try {
    const response = await axios.get('/satisfacao/alertas')
    if (response.data.success) {
      alertas.value = response.data.data
    }
  } catch (error) {
    console.error('Erro ao carregar alertas:', error)
  }
}

const agendarPesquisas = async () => {
  try {
    const response = await axios.post('/satisfacao/nps/agendar-automaticas')
    if (response.data.success) {
      alert(`${response.data.message}`)
      await carregarDashboard()
    }
  } catch (error) {
    console.error('Erro ao agendar pesquisas:', error)
  }
}

const criarPesquisa = async () => {
  try {
    const endpoint = novaPesquisa.value.tipo === 'csat' 
      ? '/satisfacao/csat/pesquisa/criar'
      : '/satisfacao/nps/pesquisa/criar'
    
    const response = await axios.post(endpoint, {
      cliente_id: novaPesquisa.value.cliente_id,
      tipo: novaPesquisa.value.tipo
    })
    
    if (response.data.success) {
      alert('Pesquisa criada com sucesso!')
      showCriarPesquisa.value = false
      await carregarDashboard()
    }
  } catch (error) {
    console.error('Erro ao criar pesquisa:', error)
    alert('Erro ao criar pesquisa')
  }
}

const criarAcaoCS = (alerta) => {
  alert(`Criar ação de Customer Success para: ${alerta.cliente_nome}`)
}

const marcarResolvido = (alerta) => {
  alert(`Marcar alerta como resolvido: ${alerta.id}`)
}

const reenviarPesquisa = (pesquisa) => {
  alert(`Reenviar pesquisa: ${pesquisa.id}`)
}

const cancelarPesquisa = (pesquisa) => {
  alert(`Cancelar pesquisa: ${pesquisa.id}`)
}

onMounted(() => {
  carregarDashboard()
  carregarAlertas()
})
</script>

<style scoped>
.nps-dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  gap: 1rem;
  align-items: center;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.stat-value.excelente { color: #10b981; }
.stat-value.bom { color: #3b82f6; }
.stat-value.regular { color: #f59e0b; }
.stat-value.ruim { color: #ef4444; }

.stat-label {
  font-size: 0.85rem;
  color: #999;
}

.alertas-section {
  margin-bottom: 2rem;
}

.alertas-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #ef4444;
}

.alertas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
}

.alerta-card {
  background: #fef2f2;
  border: 2px solid #fecaca;
  border-radius: 8px;
  padding: 1rem;
}

.alerta-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.alerta-tipo {
  background: #ef4444;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.alerta-data {
  color: #666;
  font-size: 0.85rem;
}

.alerta-body h4 {
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.alerta-score {
  font-weight: bold;
  color: #ef4444;
  margin-bottom: 0.5rem;
}

.alerta-feedback {
  font-style: italic;
  color: #666;
  margin-bottom: 1rem;
}

.alerta-actions {
  display: flex;
  gap: 0.5rem;
}

.pesquisas-section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 {
  font-size: 1.5rem;
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f3f4f6;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
}

.data-table td {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.nps {
  background: #dbeafe;
  color: #1e40af;
}

.badge.csat {
  background: #fef3c7;
  color: #92400e;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.status.pendente { background: #fef3c7; color: #92400e; }
.status.enviada { background: #dbeafe; color: #1e40af; }
.status.respondida { background: #d1fae5; color: #065f46; }
.status.expirada { background: #fee2e2; color: #991b1b; }

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-action {
  background: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-icon {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
}

.tendencia-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.tendencia-section h2 {
  margin-bottom: 1.5rem;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  border-radius: 8px;
}

.chart-placeholder {
  text-align: center;
  color: #9ca3af;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #9ca3af;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
</style>
