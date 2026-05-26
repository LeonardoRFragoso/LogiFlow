<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">🚚 Entregas</h1>
        <p class="page-subtitle">Acompanhe todas as entregas em tempo real</p>
      </div>
      <div class="header-actions">
        <button @click="toggleMapView" :class="['btn-toggle', viewMode === 'map' && 'active']">
          🗺️ Mapa
        </button>
        <button @click="openModal()" class="btn-add">
          <span>+</span> Nova Entrega
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card stat-total">
        <div class="stat-icon">📦</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.total }}</span>
          <span class="stat-label">Total</span>
        </div>
      </div>
      <div class="stat-card stat-transit">
        <div class="stat-icon">🚛</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.emTransito }}</span>
          <span class="stat-label">Em Trânsito</span>
        </div>
      </div>
      <div class="stat-card stat-delivered">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.entregues }}</span>
          <span class="stat-label">Entregues Hoje</span>
        </div>
      </div>
      <div class="stat-card stat-alert">
        <div class="stat-icon">⚠️</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.atrasadas }}</span>
          <span class="stat-label">Atrasadas</span>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="filters-left">
        <div class="filter-tabs">
          <button @click="filtroStatus = ''" :class="['filter-tab', !filtroStatus && 'active']">Todas</button>
          <button @click="filtroStatus = 'aguardando_coleta'" :class="['filter-tab', filtroStatus === 'aguardando_coleta' && 'active']">Aguardando</button>
          <button @click="filtroStatus = 'coletado'" :class="['filter-tab', filtroStatus === 'coletado' && 'active']">Coletado</button>
          <button @click="filtroStatus = 'em_transito'" :class="['filter-tab', filtroStatus === 'em_transito' && 'active']">Em Trânsito</button>
          <button @click="filtroStatus = 'saiu_para_entrega'" :class="['filter-tab', filtroStatus === 'saiu_para_entrega' && 'active']">Saiu p/ Entrega</button>
          <button @click="filtroStatus = 'entregue'" :class="['filter-tab', filtroStatus === 'entregue' && 'active']">Entregue</button>
        </div>
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input v-model="searchTerm" type="text" placeholder="Buscar por código, cliente..." class="search-input" />
        </div>
      </div>
      <div class="filters-right">
        <select v-model="filtroMotorista" class="filter-select">
          <option value="">Todos Motoristas</option>
          <option v-for="m in motoristas" :key="m.id" :value="m.id">{{ m.nome }}</option>
        </select>
        <span class="count-badge">{{ entregasFiltradas.length }} entregas</span>
      </div>
    </div>

    <!-- Map View -->
    <div v-if="viewMode === 'map'" class="map-container">
      <div class="map-placeholder">
        <span class="map-icon">🗺️</span>
        <h3>Mapa de Entregas</h3>
        <p>Visualização em tempo real das entregas</p>
        <div class="map-legend">
          <span class="legend-item"><span class="dot green"></span> Entregue</span>
          <span class="legend-item"><span class="dot blue"></span> Em Trânsito</span>
          <span class="legend-item"><span class="dot yellow"></span> Aguardando</span>
          <span class="legend-item"><span class="dot red"></span> Atrasada</span>
        </div>
      </div>
    </div>

    <!-- Table View -->
    <div v-else class="table-container">
      <table class="modern-table">
        <thead>
          <tr>
            <th>Código</th>
            <th>Cliente</th>
            <th>Endereço</th>
            <th>Motorista</th>
            <th>Status</th>
            <th>Previsão</th>
            <th>Progresso</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entrega in entregasFiltradas" :key="entrega.id" @click="openDetalhe(entrega)" class="clickable-row">
            <td>
              <span class="mono-text">{{ entrega.codigo }}</span>
            </td>
            <td>
              <div class="cliente-cell">
                <span class="cliente-nome">{{ entrega.cliente_nome }}</span>
                <span class="cliente-telefone">{{ entrega.cliente_telefone }}</span>
              </div>
            </td>
            <td>
              <div class="endereco-cell">
                <span class="endereco-rua">{{ entrega.endereco_rua }}</span>
                <span class="endereco-cidade">{{ entrega.endereco_cidade }} - {{ entrega.endereco_uf }}</span>
              </div>
            </td>
            <td>
              <span v-if="entrega.motorista_nome" class="driver-badge">
                🧑‍✈️ {{ entrega.motorista_nome }}
              </span>
              <span v-else class="no-driver">Não atribuído</span>
            </td>
            <td>
              <span :class="['status-badge', 'status-' + entrega.status]">
                {{ statusLabel(entrega.status) }}
              </span>
            </td>
            <td>
              <div class="previsao-cell">
                <span class="previsao-data">{{ formatDate(entrega.previsao_entrega) }}</span>
                <span :class="['previsao-hora', entrega.atrasada && 'atrasada']">
                  {{ formatTime(entrega.previsao_entrega) }}
                </span>
              </div>
            </td>
            <td>
              <div class="progress-cell">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: entrega.progresso + '%' }"></div>
                </div>
                <span class="progress-text">{{ entrega.progresso }}%</span>
              </div>
            </td>
            <td>
              <div class="action-buttons" @click.stop>
                <button @click="openModal(entrega)" class="btn-action btn-edit" title="Editar">✏️</button>
                <button @click="openTrack(entrega)" class="btn-action btn-track" title="Rastrear">📍</button>
                <button @click="sendWhatsApp(entrega)" class="btn-action btn-whatsapp" title="WhatsApp">💬</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="entregasFiltradas.length === 0" class="empty-state">
        <span class="empty-icon">🚚</span>
        <h3>Nenhuma entrega encontrada</h3>
        <p>Crie uma nova entrega ou ajuste os filtros.</p>
        <button @click="openModal()" class="btn-add">+ Nova Entrega</button>
      </div>
    </div>

    <!-- Timeline Section -->
    <div class="timeline-section">
      <h2 class="section-title">📅 Linha do Tempo - Hoje</h2>
      <div class="timeline">
        <div v-for="evento in eventosHoje" :key="evento.id" :class="['timeline-item', evento.tipo]">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <span class="timeline-time">{{ evento.hora }}</span>
            <span class="timeline-text">{{ evento.descricao }}</span>
          </div>
        </div>
      </div>
    </div>

    <EntregaFormModal v-model="showModal" :entrega="selected" @saved="fetchEntregas" />
    <EntregaDetalheModal v-model="showDetalhe" :entrega="selectedDetalhe" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/services/api'
import EntregaFormModal from './EntregaFormModal.vue'
import EntregaDetalheModal from './EntregaDetalheModal.vue'

const entregas = ref([])
const motoristas = ref([])
const filtroStatus = ref('')
const filtroMotorista = ref('')
const searchTerm = ref('')
const viewMode = ref('list')
const showModal = ref(false)
const showDetalhe = ref(false)
const selected = ref(null)
const selectedDetalhe = ref(null)

const stats = computed(() => ({
  total: entregas.value.length,
  emTransito: entregas.value.filter(e => e.status === 'em_transito' || e.status === 'saiu_para_entrega').length,
  entregues: entregas.value.filter(e => e.status === 'entregue' && isToday(e.data_entrega)).length,
  atrasadas: entregas.value.filter(e => e.atrasada).length,
}))

const entregasFiltradas = computed(() => {
  let result = entregas.value
  if (filtroStatus.value) {
    result = result.filter(e => e.status === filtroStatus.value)
  }
  if (filtroMotorista.value) {
    result = result.filter(e => e.motorista_id === filtroMotorista.value)
  }
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(e => 
      e.codigo?.toLowerCase().includes(term) ||
      e.cliente_nome?.toLowerCase().includes(term) ||
      e.endereco_rua?.toLowerCase().includes(term)
    )
  }
  return result
})

const eventosHoje = computed(() => {
  return entregas.value
    .filter(e => e.eventos?.length)
    .flatMap(e => e.eventos.map(ev => ({ ...ev, entrega: e.codigo })))
    .sort((a, b) => new Date(b.data) - new Date(a.data))
    .slice(0, 10)
})

const statusLabel = (s) => ({
  aguardando_coleta: 'Aguardando Coleta',
  coletado: 'Coletado',
  em_transito: 'Em Trânsito',
  saiu_para_entrega: 'Saiu p/ Entrega',
  entregue: 'Entregue',
  devolvido: 'Devolvido',
  cancelado: 'Cancelado',
}[s] || s)

const formatDate = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : ''
const formatTime = (d) => d ? new Date(d).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) : ''
const isToday = (d) => d && new Date(d).toDateString() === new Date().toDateString()

async function fetchEntregas() {
  try {
    const params = {}
    if (filtroStatus.value) params.status = filtroStatus.value
    const response = await api.get('/entregas/', { params })
    entregas.value = response.data.results || response.data?.data || response.data || []
  } catch (e) {
    console.error('Erro ao carregar entregas:', e)
    entregas.value = []
  }
}

async function fetchMotoristas() {
  try {
    const response = await api.get('/motoristas/')
    motoristas.value = response.data.results || response.data || []
  } catch (e) {
    motoristas.value = []
  }
}


function openModal(entrega = null) {
  selected.value = entrega
  showModal.value = true
}

function openDetalhe(entrega) {
  selectedDetalhe.value = entrega
  showDetalhe.value = true
}

function openTrack(entrega) {
  window.open(`/tracking/${entrega.codigo}`, '_blank')
}

function sendWhatsApp(entrega) {
  const phone = entrega.cliente_telefone?.replace(/\D/g, '')
  const msg = encodeURIComponent(`Olá ${entrega.cliente_nome}! Sua entrega ${entrega.codigo} está ${statusLabel(entrega.status).toLowerCase()}. Previsão: ${formatDate(entrega.previsao_entrega)}`)
  window.open(`https://wa.me/55${phone}?text=${msg}`, '_blank')
}

function toggleMapView() {
  viewMode.value = viewMode.value === 'map' ? 'list' : 'map'
}

onMounted(() => {
  fetchEntregas()
  fetchMotoristas()
})

watch([filtroStatus, filtroMotorista], fetchEntregas)
</script>

<style scoped>
.page-container { max-width: 1600px; margin: 0 auto; padding: 0 1rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 1.75rem; font-weight: 700; color: #1f2937; margin: 0; }
.dark .page-title { color: white; }
.page-subtitle { color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem; }
.dark .page-subtitle { color: #9ca3af; }
.header-actions { display: flex; gap: 0.75rem; }
.btn-toggle { display: flex; align-items: center; gap: 0.5rem; background: #f3f4f6; color: #374151; padding: 0.75rem 1.25rem; border-radius: 0.75rem; font-weight: 500; border: none; cursor: pointer; transition: all 0.2s; }
.dark .btn-toggle { background: #374151; color: #e5e7eb; }
.btn-toggle.active { background: #3b82f6; color: white; }
.btn-add { display: flex; align-items: center; gap: 0.5rem; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 0.75rem 1.25rem; border-radius: 0.75rem; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
.btn-add:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }
.btn-add span { font-size: 1.25rem; font-weight: 300; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card { display: flex; align-items: center; gap: 1rem; background: white; padding: 1.25rem; border-radius: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.dark .stat-card { background: #1f2937; }
.stat-icon { font-size: 2rem; }
.stat-info { display: flex; flex-direction: column; }
.stat-value { font-size: 1.75rem; font-weight: 700; color: #1f2937; }
.dark .stat-value { color: white; }
.stat-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
.dark .stat-label { color: #9ca3af; }
.stat-transit .stat-value { color: #3b82f6; }
.stat-delivered .stat-value { color: #10b981; }
.stat-alert .stat-value { color: #ef4444; }

/* Filters */
.filters-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; gap: 1rem; flex-wrap: wrap; }
.filters-left { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.filters-right { display: flex; align-items: center; gap: 1rem; }
.filter-tabs { display: flex; gap: 0.25rem; background: #f3f4f6; padding: 0.25rem; border-radius: 0.5rem; flex-wrap: wrap; }
.dark .filter-tabs { background: #374151; }
.filter-tab { padding: 0.5rem 0.75rem; border: none; background: transparent; border-radius: 0.375rem; font-size: 0.8rem; cursor: pointer; color: #6b7280; transition: all 0.2s; white-space: nowrap; }
.dark .filter-tab { color: #9ca3af; }
.filter-tab.active { background: white; color: #1f2937; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.dark .filter-tab.active { background: #1f2937; color: white; }
.search-box { display: flex; align-items: center; background: #f3f4f6; border-radius: 0.5rem; padding: 0 0.75rem; }
.dark .search-box { background: #374151; }
.search-icon { color: #9ca3af; }
.search-input { border: none; background: transparent; padding: 0.5rem; font-size: 0.875rem; width: 200px; color: #1f2937; }
.dark .search-input { color: white; }
.search-input::placeholder { color: #9ca3af; }
.filter-select { padding: 0.5rem 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 0.875rem; background: white; color: #374151; }
.dark .filter-select { background: #374151; border-color: #4b5563; color: white; }
.count-badge { background: #f3f4f6; color: #6b7280; padding: 0.5rem 1rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 500; }
.dark .count-badge { background: #374151; color: #9ca3af; }

/* Map */
.map-container { background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); overflow: hidden; margin-bottom: 1.5rem; }
.dark .map-container { background: #1f2937; }
.map-placeholder { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); min-height: 400px; }
.dark .map-placeholder { background: linear-gradient(135deg, #1e3a5f 0%, #1e293b 100%); }
.map-icon { font-size: 4rem; margin-bottom: 1rem; }
.map-placeholder h3 { font-size: 1.25rem; font-weight: 600; color: #1f2937; margin: 0 0 0.5rem; }
.dark .map-placeholder h3 { color: white; }
.map-placeholder p { color: #6b7280; margin-bottom: 1.5rem; }
.dark .map-placeholder p { color: #9ca3af; }
.map-legend { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #6b7280; }
.dark .legend-item { color: #9ca3af; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot.green { background: #10b981; }
.dot.blue { background: #3b82f6; }
.dot.yellow { background: #f59e0b; }
.dot.red { background: #ef4444; }

/* Table */
.table-container { background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); overflow: hidden; margin-bottom: 1.5rem; }
.dark .table-container { background: #1f2937; }
.modern-table { width: 100%; border-collapse: collapse; }
.modern-table thead { background: #f8fafc; }
.dark .modern-table thead { background: #111827; }
.modern-table th { text-align: left; padding: 1rem; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #6b7280; border-bottom: 1px solid #e5e7eb; }
.dark .modern-table th { color: #9ca3af; border-color: #374151; }
.modern-table td { padding: 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
.dark .modern-table td { border-color: #1f2937; color: #e5e7eb; }
.clickable-row { cursor: pointer; transition: background 0.15s; }
.clickable-row:hover { background: #f8fafc; }
.dark .clickable-row:hover { background: #111827; }
.mono-text { font-family: 'Monaco', 'Consolas', monospace; font-size: 0.85rem; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 0.375rem; }
.dark .mono-text { background: #374151; }
.cliente-cell, .endereco-cell, .previsao-cell { display: flex; flex-direction: column; }
.cliente-nome, .endereco-rua { font-weight: 500; }
.cliente-telefone, .endereco-cidade { font-size: 0.75rem; color: #9ca3af; }
.previsao-data { font-weight: 500; }
.previsao-hora { font-size: 0.75rem; color: #6b7280; }
.previsao-hora.atrasada { color: #ef4444; font-weight: 600; }
.driver-badge { font-size: 0.85rem; }
.no-driver { font-size: 0.8rem; color: #9ca3af; font-style: italic; }

/* Status Badges */
.status-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 600; white-space: nowrap; }
.status-aguardando_coleta { background: #fef3c7; color: #d97706; }
.status-coletado { background: #e0e7ff; color: #4338ca; }
.status-em_transito { background: #dbeafe; color: #1d4ed8; }
.status-saiu_para_entrega { background: #cffafe; color: #0891b2; }
.status-entregue { background: #d1fae5; color: #059669; }
.status-devolvido { background: #fee2e2; color: #dc2626; }
.status-cancelado { background: #f3f4f6; color: #6b7280; }
.dark .status-aguardando_coleta { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .status-coletado { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; }
.dark .status-em_transito { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.dark .status-saiu_para_entrega { background: rgba(6, 182, 212, 0.2); color: #22d3ee; }
.dark .status-entregue { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.dark .status-devolvido { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.dark .status-cancelado { background: rgba(107, 114, 128, 0.2); color: #9ca3af; }

/* Progress */
.progress-cell { display: flex; align-items: center; gap: 0.75rem; }
.progress-bar { flex: 1; height: 6px; background: #e5e7eb; border-radius: 3px; overflow: hidden; min-width: 80px; }
.dark .progress-bar { background: #374151; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981); border-radius: 3px; transition: width 0.3s; }
.progress-text { font-size: 0.75rem; font-weight: 600; color: #6b7280; min-width: 35px; }
.dark .progress-text { color: #9ca3af; }

/* Actions */
.action-buttons { display: flex; gap: 0.5rem; }
.btn-action { width: 32px; height: 32px; border-radius: 0.5rem; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 0.9rem; }
.btn-edit { background: #eff6ff; color: #3b82f6; }
.btn-edit:hover { background: #dbeafe; transform: scale(1.1); }
.dark .btn-edit { background: rgba(59, 130, 246, 0.2); }
.btn-track { background: #fef3c7; color: #d97706; }
.btn-track:hover { background: #fde68a; transform: scale(1.1); }
.dark .btn-track { background: rgba(245, 158, 11, 0.2); }
.btn-whatsapp { background: #d1fae5; color: #059669; }
.btn-whatsapp:hover { background: #a7f3d0; transform: scale(1.1); }
.dark .btn-whatsapp { background: rgba(16, 185, 129, 0.2); }

/* Timeline */
.timeline-section { margin-top: 2rem; }
.section-title { font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem; }
.dark .section-title { color: white; }
.timeline { display: flex; flex-direction: column; gap: 0.5rem; background: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.dark .timeline { background: #1f2937; }
.timeline-item { display: flex; align-items: center; gap: 1rem; padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6; }
.dark .timeline-item { border-color: #374151; }
.timeline-item:last-child { border-bottom: none; }
.timeline-dot { width: 10px; height: 10px; border-radius: 50%; background: #3b82f6; flex-shrink: 0; }
.timeline-item.entrega .timeline-dot { background: #10b981; }
.timeline-item.coleta .timeline-dot { background: #f59e0b; }
.timeline-item.ocorrencia .timeline-dot { background: #ef4444; }
.timeline-content { display: flex; gap: 1rem; flex: 1; }
.timeline-time { font-size: 0.75rem; color: #6b7280; font-weight: 500; min-width: 50px; }
.dark .timeline-time { color: #9ca3af; }
.timeline-text { font-size: 0.875rem; color: #374151; }
.dark .timeline-text { color: #e5e7eb; }

/* Empty State */
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 4rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3 { font-size: 1.25rem; font-weight: 600; color: #374151; margin: 0 0 0.5rem; }
.dark .empty-state h3 { color: #e5e7eb; }
.empty-state p { color: #9ca3af; margin-bottom: 1.5rem; }
</style>
