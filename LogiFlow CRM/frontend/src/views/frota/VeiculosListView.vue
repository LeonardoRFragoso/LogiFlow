<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">🚚 Veículos</h1>
        <p class="page-subtitle">Gerencie sua frota de veículos</p>
      </div>
      <button @click="openModal()" class="btn-add">
        <span>+</span> Novo Veículo
      </button>
    </div>

    <div class="filters-bar">
      <div class="filters-left">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input v-model="search" placeholder="Buscar por placa..." class="search-input" />
        </div>
        <div class="filter-tabs">
          <button @click="filtroStatus = ''" :class="['filter-tab', !filtroStatus && 'active']">Todos</button>
          <button @click="filtroStatus = 'disponivel'" :class="['filter-tab', filtroStatus === 'disponivel' && 'active']">Disponíveis</button>
          <button @click="filtroStatus = 'em_viagem'" :class="['filter-tab', filtroStatus === 'em_viagem' && 'active']">Em Viagem</button>
          <button @click="filtroStatus = 'manutencao'" :class="['filter-tab', filtroStatus === 'manutencao' && 'active']">Manutenção</button>
        </div>
      </div>
      <span class="count-badge">{{ veiculos.length }} veículos</span>
    </div>

    <div class="table-container">
      <table class="modern-table">
        <thead>
          <tr>
            <th>Placa</th>
            <th>Tipo</th>
            <th>Marca/Modelo</th>
            <th>KM Atual</th>
            <th>Status</th>
            <th>Motorista Fixo</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in veiculos" :key="v.id">
            <td><span class="plate-badge">{{ v.placa }}</span></td>
            <td><span class="type-icon">{{ typeIcon(v.tipo) }}</span> {{ v.tipo }}</td>
            <td>{{ v.marca }} {{ v.modelo }}</td>
            <td><span class="km-value">{{ v.km_atual?.toLocaleString() }} km</span></td>
            <td><span :class="['status-badge', 'status-' + v.status]">{{ statusLabel(v.status) }}</span></td>
            <td>
              <span v-if="v.motorista_fixo_nome" class="driver-badge">🧑‍✈️ {{ v.motorista_fixo_nome }}</span>
              <span v-else class="no-driver">-</span>
            </td>
            <td>
              <div class="action-buttons">
                <button @click="openModal(v)" class="btn-action btn-edit" title="Editar">✏️</button>
                <button class="btn-action btn-maintenance" title="Manutenção">🔧</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="veiculos.length === 0" class="empty-state">
        <span class="empty-icon">🚚</span>
        <h3>Nenhum veículo encontrado</h3>
        <p>Cadastre seu primeiro veículo.</p>
        <button @click="openModal()" class="btn-add">+ Novo Veículo</button>
      </div>
    </div>

    <VeiculoFormModal v-model="showModal" :veiculo="selected" @saved="fetchData" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/services/api'
import VeiculoFormModal from './VeiculoFormModal.vue'

const veiculos = ref([])
const search = ref('')
const filtroStatus = ref('')
const showModal = ref(false)
const selected = ref(null)

async function fetchData() {
  const params = { search: search.value }
  if (filtroStatus.value) params.status = filtroStatus.value
  const response = await api.get('/veiculos/', { params })
  veiculos.value = response.data.results || response.data
}

function openModal(item = null) {
  selected.value = item
  showModal.value = true
}

const statusLabel = (s) => ({ disponivel: 'Disponível', em_viagem: 'Em Viagem', manutencao: 'Manutenção' }[s] || s)
const typeIcon = (t) => ({ caminhao: '🚛', van: '🚐', carro: '🚗', moto: '🏍️' }[t] || '🚚')

onMounted(fetchData)
watch([search, filtroStatus], fetchData)
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
.search-box { display: flex; align-items: center; gap: 0.75rem; background: white; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 0.75rem 1rem; min-width: 220px; transition: all 0.2s; }
.dark .search-box { background: #1f2937; border-color: #374151; }
.search-box:focus-within { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
.search-icon { font-size: 1rem; opacity: 0.5; }
.search-input { border: none; outline: none; background: transparent; font-size: 0.9rem; width: 100%; color: #1f2937; }
.dark .search-input { color: white; }
.filter-tabs { display: flex; gap: 0.25rem; background: #f3f4f6; padding: 0.25rem; border-radius: 0.5rem; }
.dark .filter-tabs { background: #374151; }
.filter-tab { padding: 0.5rem 1rem; border: none; background: transparent; border-radius: 0.375rem; font-size: 0.875rem; cursor: pointer; color: #6b7280; transition: all 0.2s; }
.dark .filter-tab { color: #9ca3af; }
.filter-tab.active { background: white; color: #1f2937; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.dark .filter-tab.active { background: #1f2937; color: white; }
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
.plate-badge { font-family: 'Monaco', 'Consolas', monospace; font-size: 0.9rem; font-weight: 700; background: #1f2937; color: white; padding: 0.375rem 0.75rem; border-radius: 0.375rem; }
.dark .plate-badge { background: #374151; }
.type-icon { margin-right: 0.25rem; }
.km-value { font-family: 'Monaco', 'Consolas', monospace; font-size: 0.85rem; }
.driver-badge { font-size: 0.85rem; }
.no-driver { color: #9ca3af; }
.status-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-disponivel { background: #d1fae5; color: #059669; }
.status-em_viagem { background: #dbeafe; color: #1d4ed8; }
.status-manutencao { background: #fef3c7; color: #d97706; }
.dark .status-disponivel { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.dark .status-em_viagem { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.dark .status-manutencao { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.action-buttons { display: flex; gap: 0.5rem; }
.btn-action { width: 36px; height: 36px; border-radius: 0.5rem; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 1rem; }
.btn-edit { background: #eff6ff; color: #3b82f6; }
.btn-edit:hover { background: #dbeafe; transform: scale(1.1); }
.dark .btn-edit { background: rgba(59, 130, 246, 0.2); }
.btn-maintenance { background: #fef3c7; color: #d97706; }
.btn-maintenance:hover { background: #fde68a; transform: scale(1.1); }
.dark .btn-maintenance { background: rgba(245, 158, 11, 0.2); }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 4rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3 { font-size: 1.25rem; font-weight: 600; color: #374151; margin: 0 0 0.5rem; }
.dark .empty-state h3 { color: #e5e7eb; }
.empty-state p { color: #9ca3af; margin-bottom: 1.5rem; }
</style>
