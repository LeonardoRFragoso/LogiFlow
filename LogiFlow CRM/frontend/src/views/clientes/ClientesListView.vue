<template>
  <div class="page-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">👥 Clientes</h1>
        <p class="page-subtitle">Gerencie sua carteira de clientes</p>
      </div>
      <button @click="openModal()" class="btn-add">
        <span>+</span> Novo Cliente
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input v-model="search" placeholder="Buscar por nome, CNPJ ou cidade..." class="search-input" />
      </div>
      <div class="filter-info">
        <span class="count-badge">{{ clientes.length }} clientes</span>
      </div>
    </div>

    <!-- Table -->
    <div class="table-container">
      <table class="modern-table">
        <thead>
          <tr>
            <th>Razão Social</th>
            <th>CNPJ</th>
            <th>Cidade/UF</th>
            <th>Telefone</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cliente in clientes" :key="cliente.id">
            <td>
              <div class="cell-main">{{ cliente.nome_fantasia || cliente.razao_social }}</div>
              <div class="cell-sub" v-if="cliente.nome_fantasia">{{ cliente.razao_social }}</div>
            </td>
            <td><span class="mono-text">{{ cliente.cnpj }}</span></td>
            <td>{{ cliente.cidade }}/{{ cliente.uf }}</td>
            <td>{{ cliente.telefone || '-' }}</td>
            <td>
              <div class="action-buttons">
                <button @click="openModal(cliente)" class="btn-action btn-edit" title="Editar">✏️</button>
                <button @click="deleteCliente(cliente.id)" class="btn-action btn-delete" title="Excluir">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="clientes.length === 0" class="empty-state">
        <span class="empty-icon">👥</span>
        <h3>Nenhum cliente encontrado</h3>
        <p>Cadastre seu primeiro cliente para começar.</p>
        <button @click="openModal()" class="btn-add">+ Novo Cliente</button>
      </div>
    </div>

    <ClienteFormModal v-model="showModal" :cliente="selectedCliente" @saved="onSaved" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/services/api'
import ClienteFormModal from './ClienteFormModal.vue'

const clientes = ref([])
const search = ref('')
const showModal = ref(false)
const selectedCliente = ref(null)

async function fetchClientes() {
  const response = await api.get('/clientes')
  let data = response.data.data || response.data.results || response.data
  if (search.value) {
    const s = search.value.toLowerCase()
    data = data.filter(c => c.razao_social?.toLowerCase().includes(s) || c.nome_fantasia?.toLowerCase().includes(s) || c.cnpj?.includes(s) || c.cidade?.toLowerCase().includes(s))
  }
  clientes.value = data
}

function openModal(cliente = null) {
  selectedCliente.value = cliente
  showModal.value = true
}

function onSaved() {
  fetchClientes()
}

async function deleteCliente(id) {
  if (confirm('Tem certeza que deseja excluir este cliente?')) {
    await api.delete(`/clientes/${id}/`)
    fetchClientes()
  }
}

onMounted(fetchClientes)
watch(search, fetchClientes)
</script>

<style scoped>
.page-container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.dark .page-title {
  color: white;
}

.page-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.dark .page-subtitle {
  color: #9ca3af;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn-add span {
  font-size: 1.25rem;
  font-weight: 300;
}

/* Filters */
.filters-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 0.75rem 1rem;
  flex: 1;
  max-width: 400px;
  transition: all 0.2s;
}

.dark .search-box {
  background: #1f2937;
  border-color: #374151;
}

.search-box:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  font-size: 1rem;
  opacity: 0.5;
}

.search-input {
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.9rem;
  width: 100%;
  color: #1f2937;
}

.dark .search-input {
  color: white;
}

.count-badge {
  background: #f3f4f6;
  color: #6b7280;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.dark .count-badge {
  background: #374151;
  color: #9ca3af;
}

/* Table */
.table-container {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.dark .table-container {
  background: #1f2937;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table thead {
  background: #f8fafc;
}

.dark .modern-table thead {
  background: #111827;
}

.modern-table th {
  text-align: left;
  padding: 1rem 1.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
  border-bottom: 1px solid #e5e7eb;
}

.dark .modern-table th {
  color: #9ca3af;
  border-color: #374151;
}

.modern-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f3f4f6;
  color: #374151;
}

.dark .modern-table td {
  border-color: #1f2937;
  color: #e5e7eb;
}

.modern-table tbody tr {
  transition: background 0.15s;
}

.modern-table tbody tr:hover {
  background: #f8fafc;
}

.dark .modern-table tbody tr:hover {
  background: #111827;
}

.cell-main {
  font-weight: 500;
  color: #1f2937;
}

.dark .cell-main {
  color: white;
}

.cell-sub {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 0.125rem;
}

.mono-text {
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 0.85rem;
  background: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
}

.dark .mono-text {
  background: #374151;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  width: 36px;
  height: 36px;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 1rem;
}

.btn-edit {
  background: #eff6ff;
  color: #3b82f6;
}

.btn-edit:hover {
  background: #dbeafe;
  transform: scale(1.1);
}

.dark .btn-edit {
  background: rgba(59, 130, 246, 0.2);
}

.btn-delete {
  background: #fef2f2;
  color: #ef4444;
}

.btn-delete:hover {
  background: #fee2e2;
  transform: scale(1.1);
}

.dark .btn-delete {
  background: rgba(239, 68, 68, 0.2);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.5rem;
}

.dark .empty-state h3 {
  color: #e5e7eb;
}

.empty-state p {
  color: #9ca3af;
  margin-bottom: 1.5rem;
}
</style>
