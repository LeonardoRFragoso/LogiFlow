<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">📦 Pedidos</h1>
        <p class="page-subtitle">Acompanhe suas entregas em tempo real</p>
      </div>
      <button @click="openModal()" class="btn-add">
        <span>+</span> Novo Pedido
      </button>
    </div>

    <div class="filters-bar">
      <div class="filters-left">
        <div class="filter-tabs">
          <button @click="filtroStatus = ''" :class="['filter-tab', !filtroStatus && 'active']">Todos</button>
          <button @click="filtroStatus = 'em_planejamento'" :class="['filter-tab', filtroStatus === 'em_planejamento' && 'active']">Planejamento</button>
          <button @click="filtroStatus = 'em_transito'" :class="['filter-tab', filtroStatus === 'em_transito' && 'active']">Em Trânsito</button>
          <button @click="filtroStatus = 'entregue'" :class="['filter-tab', filtroStatus === 'entregue' && 'active']">Entregue</button>
        </div>
        <div class="sla-filters">
          <button @click="filtroSla = ''" :class="['sla-btn', !filtroSla && 'active']">🎯 SLA</button>
          <button @click="filtroSla = 'verde'" :class="['sla-btn sla-verde', filtroSla === 'verde' && 'active']">🟢</button>
          <button @click="filtroSla = 'amarelo'" :class="['sla-btn sla-amarelo', filtroSla === 'amarelo' && 'active']">🟡</button>
          <button @click="filtroSla = 'vermelho'" :class="['sla-btn sla-vermelho', filtroSla === 'vermelho' && 'active']">🔴</button>
        </div>
      </div>
      <span class="count-badge">{{ pedidos.length }} pedidos</span>
    </div>

    <div class="table-container">
      <table class="modern-table">
        <thead>
          <tr>
            <th>Nº</th>
            <th>Cliente</th>
            <th>Rota</th>
            <th>Motorista</th>
            <th>Status</th>
            <th>SLA</th>
            <th>Previsão</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pedido in pedidos" :key="pedido.id">
            <td><span class="mono-text">{{ pedido.numero }}</span></td>
            <td>{{ pedido.cliente_nome }}</td>
            <td><span class="route-badge">{{ pedido.rota }}</span></td>
            <td>
              <span v-if="pedido.motorista_nome" class="driver-badge">🧑‍✈️ {{ pedido.motorista_nome }}</span>
              <span v-else class="no-driver">Não atribuído</span>
            </td>
            <td><span :class="['status-badge', 'status-' + pedido.status]">{{ statusLabel(pedido.status) }}</span></td>
            <td><span :class="['sla-badge', 'sla-' + pedido.sla_status]">{{ slaLabel[pedido.sla_status] }}</span></td>
            <td>{{ formatDate(pedido.previsao_entrega) }}</td>
            <td>
              <div class="action-buttons">
                <button @click="openModal(pedido)" class="btn-action btn-edit" title="Editar">✏️</button>
                <button class="btn-action btn-track" title="Rastrear">📍</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="pedidos.length === 0" class="empty-state">
        <span class="empty-icon">📦</span>
        <h3>Nenhum pedido encontrado</h3>
        <p>Crie um novo pedido ou ajuste os filtros.</p>
        <button @click="openModal()" class="btn-add">+ Novo Pedido</button>
      </div>
    </div>

    <PedidoFormModal v-model="showModal" :pedido="selected" @saved="fetchPedidos" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/services/api'
import PedidoFormModal from './PedidoFormModal.vue'

const pedidos = ref([])
const filtroStatus = ref('')
const filtroSla = ref('')
const showModal = ref(false)
const selected = ref(null)

const slaLabel = { verde: 'No Prazo', amarelo: 'Atenção', vermelho: 'Atrasado' }
const statusLabel = (s) => ({ em_planejamento: 'Planejamento', em_transito: 'Em Trânsito', entregue: 'Entregue', aguardando_coleta: 'Aguardando', coletado: 'Coletado' }[s] || s)

async function fetchPedidos() {
  const params = {}
  if (filtroStatus.value) params.status = filtroStatus.value
  if (filtroSla.value) params.sla_status = filtroSla.value
  const response = await api.get('/pedidos/', { params })
  pedidos.value = response.data.data || response.data.results || response.data || []
}

function openModal(pedido = null) {
  selected.value = pedido
  showModal.value = true
}

const formatDate = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : ''

onMounted(fetchPedidos)
watch([filtroStatus, filtroSla], fetchPedidos)
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
.sla-filters { display: flex; gap: 0.25rem; }
.sla-btn { width: 36px; height: 36px; border: none; border-radius: 0.5rem; cursor: pointer; font-size: 1rem; background: #f3f4f6; transition: all 0.2s; }
.dark .sla-btn { background: #374151; }
.sla-btn.active { transform: scale(1.1); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
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
.route-badge { font-size: 0.85rem; color: #6b7280; }
.dark .route-badge { color: #9ca3af; }
.driver-badge { font-size: 0.85rem; }
.no-driver { font-size: 0.8rem; color: #9ca3af; font-style: italic; }
.status-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-em_planejamento { background: #e0e7ff; color: #4338ca; }
.status-em_transito { background: #dbeafe; color: #1d4ed8; }
.status-entregue { background: #d1fae5; color: #059669; }
.dark .status-em_planejamento { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; }
.dark .status-em_transito { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.dark .status-entregue { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.sla-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.sla-verde { background: #d1fae5; color: #059669; }
.sla-amarelo { background: #fef3c7; color: #d97706; }
.sla-vermelho { background: #fee2e2; color: #dc2626; }
.dark .sla-verde { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.dark .sla-amarelo { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .sla-vermelho { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.action-buttons { display: flex; gap: 0.5rem; }
.btn-action { width: 36px; height: 36px; border-radius: 0.5rem; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 1rem; }
.btn-edit { background: #eff6ff; color: #3b82f6; }
.btn-edit:hover { background: #dbeafe; transform: scale(1.1); }
.dark .btn-edit { background: rgba(59, 130, 246, 0.2); }
.btn-track { background: #fef3c7; color: #d97706; }
.btn-track:hover { background: #fde68a; transform: scale(1.1); }
.dark .btn-track { background: rgba(245, 158, 11, 0.2); }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 4rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3 { font-size: 1.25rem; font-weight: 600; color: #374151; margin: 0 0 0.5rem; }
.dark .empty-state h3 { color: #e5e7eb; }
.empty-state p { color: #9ca3af; margin-bottom: 1.5rem; }
</style>
