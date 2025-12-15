<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">🧑‍✈️ Motoristas</h1>
        <p class="page-subtitle">Gerencie sua equipe de motoristas</p>
      </div>
      <button @click="openModal()" class="btn-add">
        <span>+</span> Novo Motorista
      </button>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input v-model="search" placeholder="Buscar por nome ou CPF..." class="search-input" />
      </div>
      <span class="count-badge">{{ motoristas.length }} motoristas</span>
    </div>

    <div class="table-container">
      <table class="modern-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>CPF</th>
            <th>CNH</th>
            <th>Validade CNH</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in motoristas" :key="m.id">
            <td>
              <div class="driver-info">
                <span class="driver-avatar">{{ m.nome?.charAt(0) }}</span>
                <span class="driver-name">{{ m.nome }}</span>
              </div>
            </td>
            <td><span class="mono-text">{{ m.cpf }}</span></td>
            <td><span class="cnh-badge">{{ m.cnh_categoria }}</span></td>
            <td>
              <span :class="['cnh-date', m.cnh_vencida ? 'vencida' : m.cnh_vencendo ? 'vencendo' : '']">
                {{ formatDate(m.cnh_validade) }}
                <span v-if="m.cnh_vencida" class="cnh-alert">⚠️ Vencida</span>
                <span v-else-if="m.cnh_vencendo" class="cnh-warning">⏳ {{ m.dias_para_vencer_cnh }} dias</span>
              </span>
            </td>
            <td><span :class="['status-badge', 'status-' + m.status]">{{ statusLabel(m.status) }}</span></td>
            <td>
              <div class="action-buttons">
                <button @click="openModal(m)" class="btn-action btn-edit" title="Editar">✏️</button>
                <button class="btn-action btn-view" title="Ver entregas">📦</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="motoristas.length === 0" class="empty-state">
        <span class="empty-icon">🧑‍✈️</span>
        <h3>Nenhum motorista encontrado</h3>
        <p>Cadastre seu primeiro motorista.</p>
        <button @click="openModal()" class="btn-add">+ Novo Motorista</button>
      </div>
    </div>

    <MotoristaFormModal v-model="showModal" :motorista="selected" @saved="fetchData" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/services/api'
import MotoristaFormModal from './MotoristaFormModal.vue'

const motoristas = ref([])
const search = ref('')
const showModal = ref(false)
const selected = ref(null)

async function fetchData() {
  const response = await api.get('/motoristas')
  let data = response.data.data || response.data.results || response.data
  if (search.value) {
    data = data.filter(m => m.nome?.toLowerCase().includes(search.value.toLowerCase()) || m.cpf?.includes(search.value))
  }
  motoristas.value = data
}

function openModal(item = null) {
  selected.value = item
  showModal.value = true
}

const formatDate = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : ''
const statusLabel = (s) => ({ disponivel: 'Disponível', em_viagem: 'Em Viagem', ferias: 'Férias', inativo: 'Inativo' }[s] || s)

onMounted(fetchData)
watch(search, fetchData)
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
.filters-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; gap: 1rem; }
.search-box { display: flex; align-items: center; gap: 0.75rem; background: white; border: 1px solid #e5e7eb; border-radius: 0.75rem; padding: 0.75rem 1rem; min-width: 300px; transition: all 0.2s; }
.dark .search-box { background: #1f2937; border-color: #374151; }
.search-box:focus-within { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
.search-icon { font-size: 1rem; opacity: 0.5; }
.search-input { border: none; outline: none; background: transparent; font-size: 0.9rem; width: 100%; color: #1f2937; }
.dark .search-input { color: white; }
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
.driver-info { display: flex; align-items: center; gap: 0.75rem; }
.driver-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #8b5cf6, #6366f1); display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.9rem; }
.driver-name { font-weight: 500; }
.mono-text { font-family: 'Monaco', 'Consolas', monospace; font-size: 0.85rem; background: #f3f4f6; padding: 0.25rem 0.5rem; border-radius: 0.375rem; }
.dark .mono-text { background: #374151; }
.cnh-badge { background: #e0e7ff; color: #4338ca; padding: 0.25rem 0.75rem; border-radius: 0.375rem; font-weight: 600; font-size: 0.85rem; }
.dark .cnh-badge { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; }
.cnh-date { display: flex; align-items: center; gap: 0.5rem; }
.cnh-date.vencida { color: #dc2626; font-weight: 600; }
.cnh-date.vencendo { color: #d97706; }
.cnh-alert { font-size: 0.75rem; }
.cnh-warning { font-size: 0.75rem; }
.status-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-disponivel { background: #d1fae5; color: #059669; }
.status-em_viagem { background: #dbeafe; color: #1d4ed8; }
.status-ferias { background: #fef3c7; color: #d97706; }
.status-inativo { background: #f3f4f6; color: #6b7280; }
.dark .status-disponivel { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.dark .status-em_viagem { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.dark .status-ferias { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .status-inativo { background: rgba(107, 114, 128, 0.2); color: #9ca3af; }
.action-buttons { display: flex; gap: 0.5rem; }
.btn-action { width: 36px; height: 36px; border-radius: 0.5rem; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 1rem; }
.btn-edit { background: #eff6ff; color: #3b82f6; }
.btn-edit:hover { background: #dbeafe; transform: scale(1.1); }
.dark .btn-edit { background: rgba(59, 130, 246, 0.2); }
.btn-view { background: #f3e8ff; color: #9333ea; }
.btn-view:hover { background: #e9d5ff; transform: scale(1.1); }
.dark .btn-view { background: rgba(147, 51, 234, 0.2); }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 4rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3 { font-size: 1.25rem; font-weight: 600; color: #374151; margin: 0 0 0.5rem; }
.dark .empty-state h3 { color: #e5e7eb; }
.empty-state p { color: #9ca3af; margin-bottom: 1.5rem; }
</style>
