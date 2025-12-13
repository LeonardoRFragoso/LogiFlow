<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">⚠️ Ocorrências</h1>
        <p class="page-subtitle">Gerencie problemas e incidentes nas entregas</p>
      </div>
      <button @click="openModal()" class="btn-add">
        <span>+</span> Nova Ocorrência
      </button>
    </div>

    <div class="filters-bar">
      <div class="filters-left">
        <div class="filter-tabs">
          <button @click="filtroStatus = ''" :class="['filter-tab', !filtroStatus && 'active']">Todas</button>
          <button @click="filtroStatus = 'aberta'" :class="['filter-tab', filtroStatus === 'aberta' && 'active']">Abertas</button>
          <button @click="filtroStatus = 'em_analise'" :class="['filter-tab', filtroStatus === 'em_analise' && 'active']">Em Análise</button>
          <button @click="filtroStatus = 'resolvida'" :class="['filter-tab', filtroStatus === 'resolvida' && 'active']">Resolvidas</button>
        </div>
        <div class="priority-filters">
          <button @click="filtroPrioridade = ''" :class="['priority-btn', !filtroPrioridade && 'active']">🎯</button>
          <button @click="filtroPrioridade = 'critica'" :class="['priority-btn critica', filtroPrioridade === 'critica' && 'active']" title="Crítica">🔴</button>
          <button @click="filtroPrioridade = 'alta'" :class="['priority-btn alta', filtroPrioridade === 'alta' && 'active']" title="Alta">🟠</button>
          <button @click="filtroPrioridade = 'media'" :class="['priority-btn media', filtroPrioridade === 'media' && 'active']" title="Média">🟡</button>
          <button @click="filtroPrioridade = 'baixa'" :class="['priority-btn baixa', filtroPrioridade === 'baixa' && 'active']" title="Baixa">🟢</button>
        </div>
      </div>
      <span class="count-badge">{{ ocorrencias.length }} ocorrências</span>
    </div>

    <div class="table-container">
      <table class="modern-table">
        <thead>
          <tr>
            <th>Pedido</th>
            <th>Tipo</th>
            <th>Título</th>
            <th>Prioridade</th>
            <th>Status</th>
            <th>Data</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in ocorrencias" :key="o.id">
            <td><span class="mono-text">{{ o.pedido_numero }}</span></td>
            <td><span class="type-badge">{{ typeIcon(o.tipo) }} {{ o.tipo }}</span></td>
            <td>{{ o.titulo }}</td>
            <td><span :class="['priority-badge', 'priority-' + o.prioridade]">{{ prioridadeLabel(o.prioridade) }}</span></td>
            <td><span :class="['status-badge', 'status-' + o.status]">{{ statusLabel(o.status) }}</span></td>
            <td>{{ formatDate(o.data_ocorrencia) }}</td>
            <td>
              <div class="action-buttons">
                <button @click="openModal(o)" class="btn-action btn-edit" title="Editar">✏️</button>
                <button class="btn-action btn-resolve" title="Resolver">✅</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="ocorrencias.length === 0" class="empty-state">
        <span class="empty-icon">✅</span>
        <h3>Nenhuma ocorrência encontrada</h3>
        <p>Ótimo! Não há problemas registrados.</p>
      </div>
    </div>

    <OcorrenciaFormModal v-model="showModal" :ocorrencia="selected" @saved="fetchData" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/services/api'
import OcorrenciaFormModal from './OcorrenciaFormModal.vue'

const ocorrencias = ref([])
const filtroStatus = ref('')
const filtroPrioridade = ref('')
const showModal = ref(false)
const selected = ref(null)

async function fetchData() {
  const params = {}
  if (filtroStatus.value) params.status = filtroStatus.value
  if (filtroPrioridade.value) params.prioridade = filtroPrioridade.value
  const response = await api.get('/ocorrencias/', { params })
  ocorrencias.value = response.data.data || response.data.results || response.data || []
}

function openModal(ocorrencia = null) {
  selected.value = ocorrencia
  showModal.value = true
}

const formatDate = (d) => d ? new Date(d).toLocaleString('pt-BR') : ''
const statusLabel = (s) => ({ aberta: 'Aberta', em_analise: 'Em Análise', resolvida: 'Resolvida' }[s] || s)
const prioridadeLabel = (p) => ({ critica: 'Crítica', alta: 'Alta', media: 'Média', baixa: 'Baixa' }[p] || p)
const typeIcon = (t) => ({ atraso: '⏰', avaria: '📦', extravio: '❌', recusa: '🚫', outros: '📋' }[t] || '⚠️')

onMounted(fetchData)
watch([filtroStatus, filtroPrioridade], fetchData)
</script>

<style scoped>
.page-container { max-width: 1400px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #1f2937; margin: 0; }
.dark .page-title { color: white; }
.page-subtitle { color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem; }
.dark .page-subtitle { color: #9ca3af; }
.btn-add { display: flex; align-items: center; gap: 0.5rem; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 0.75rem 1.25rem; border-radius: 0.75rem; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
.btn-add:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4); }
.btn-add span { font-size: 1.25rem; font-weight: 300; }
.filters-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; gap: 1rem; flex-wrap: wrap; }
.filters-left { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.filter-tabs { display: flex; gap: 0.25rem; background: #f3f4f6; padding: 0.25rem; border-radius: 0.5rem; }
.dark .filter-tabs { background: #374151; }
.filter-tab { padding: 0.5rem 1rem; border: none; background: transparent; border-radius: 0.375rem; font-size: 0.875rem; cursor: pointer; color: #6b7280; transition: all 0.2s; }
.dark .filter-tab { color: #9ca3af; }
.filter-tab.active { background: white; color: #1f2937; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.dark .filter-tab.active { background: #1f2937; color: white; }
.priority-filters { display: flex; gap: 0.25rem; }
.priority-btn { width: 36px; height: 36px; border: none; border-radius: 0.5rem; cursor: pointer; font-size: 1rem; background: #f3f4f6; transition: all 0.2s; }
.dark .priority-btn { background: #374151; }
.priority-btn.active { transform: scale(1.1); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.count-badge { background: #f3f4f6; color: #6b7280; padding: 0.5rem 1rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 500; }
.dark .count-badge { background: #374151; color: #9ca3af; }
.table-container { background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); overflow: hidden; }
.dark .table-container { background: #1f2937; }
.modern-table { width: 100%; border-collapse: collapse; }
.modern-table thead { background: #f8fafc; }
.dark .modern-table thead { background: #111827; }
.modern-table th { text-align: left; padding: 1rem 1.25rem; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #6b7280; border-bottom: 1px solid #e5e7eb; }
.dark .modern-table th { color: #9ca3af; border-color: #374151; }
.modern-table td { padding: 1rem 1.25rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
.dark .modern-table td { border-color: #1f2937; color: #e5e7eb; }
.modern-table tbody tr { transition: background 0.15s; }
.modern-table tbody tr:hover { background: #f8fafc; }
.dark .modern-table tbody tr:hover { background: #111827; }
.mono-text { font-family: 'Monaco', 'Consolas', monospace; font-size: 0.85rem; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 0.375rem; }
.dark .mono-text { background: #374151; }
.type-badge { font-size: 0.85rem; }
.priority-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.priority-critica { background: #dc2626; color: white; }
.priority-alta { background: #fee2e2; color: #dc2626; }
.priority-media { background: #fef3c7; color: #d97706; }
.priority-baixa { background: #d1fae5; color: #059669; }
.dark .priority-critica { background: #dc2626; }
.dark .priority-alta { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.dark .priority-media { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .priority-baixa { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.status-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-aberta { background: #fee2e2; color: #dc2626; }
.status-em_analise { background: #fef3c7; color: #d97706; }
.status-resolvida { background: #d1fae5; color: #059669; }
.dark .status-aberta { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.dark .status-em_analise { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .status-resolvida { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.action-buttons { display: flex; gap: 0.5rem; }
.btn-action { width: 36px; height: 36px; border-radius: 0.5rem; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 1rem; }
.btn-edit { background: #eff6ff; color: #3b82f6; }
.btn-edit:hover { background: #dbeafe; transform: scale(1.1); }
.dark .btn-edit { background: rgba(59, 130, 246, 0.2); }
.btn-resolve { background: #d1fae5; color: #059669; }
.btn-resolve:hover { background: #a7f3d0; transform: scale(1.1); }
.dark .btn-resolve { background: rgba(16, 185, 129, 0.2); }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 4rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3 { font-size: 1.25rem; font-weight: 600; color: #374151; margin: 0 0 0.5rem; }
.dark .empty-state h3 { color: #e5e7eb; }
.empty-state p { color: #9ca3af; margin-bottom: 1.5rem; }
</style>
