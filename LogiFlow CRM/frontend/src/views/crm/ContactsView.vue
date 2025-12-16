<template>
  <div class="contacts-container">
    <!-- Header -->
    <div class="header">
      <div>
        <h1 class="title">Contatos</h1>
        <p class="subtitle">Gerencie os contatos dos seus clientes</p>
      </div>
      <button @click="openCreateModal" class="btn btn-primary">
        ➕ Novo Contato
      </button>
    </div>

    <!-- Filtros -->
    <div class="filters-card">
      <div class="filters">
        <input 
          v-model="filters.search" 
          type="text" 
          placeholder="🔍 Buscar por nome ou email..."
          class="search-input"
          @input="loadContacts"
        />
        <select v-model="filters.account_id" @change="loadContacts" class="filter-select">
          <option value="">Todos os clientes</option>
          <option v-for="client in clients" :key="client.id" :value="client.id">
            {{ client.nome }}
          </option>
        </select>
      </div>
    </div>

    <!-- Lista de Contatos -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando contatos...</p>
    </div>

    <div v-else-if="contacts.length === 0" class="empty-state">
      <span class="empty-icon">📇</span>
      <h3>Nenhum contato encontrado</h3>
      <p>Crie seu primeiro contato clicando no botão acima</p>
    </div>

    <div v-else class="contacts-grid">
      <div v-for="contact in contacts" :key="contact.id" class="contact-card">
        <div class="contact-header">
          <div class="contact-avatar">
            {{ getInitials(contact.full_name) }}
          </div>
          <div class="contact-info">
            <h3 class="contact-name">{{ contact.full_name }}</h3>
            <p v-if="contact.title" class="contact-title">{{ contact.title }}</p>
          </div>
        </div>

        <div class="contact-details">
          <div v-if="contact.email" class="detail-item">
            <span class="icon">📧</span>
            <a :href="`mailto:${contact.email}`">{{ contact.email }}</a>
          </div>
          <div v-if="contact.phone_mobile" class="detail-item">
            <span class="icon">📱</span>
            <a :href="`tel:${contact.phone_mobile}`">{{ contact.phone_mobile }}</a>
          </div>
          <div v-if="contact.phone_work" class="detail-item">
            <span class="icon">☎️</span>
            <a :href="`tel:${contact.phone_work}`">{{ contact.phone_work }}</a>
          </div>
          <div v-if="contact.department" class="detail-item">
            <span class="icon">🏢</span>
            <span>{{ contact.department }}</span>
          </div>
        </div>

        <div class="contact-actions">
          <button @click="editContact(contact)" class="btn btn-sm btn-secondary">
            ✏️ Editar
          </button>
          <button @click="deleteContact(contact)" class="btn btn-sm btn-danger">
            🗑️ Excluir
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Criar/Editar -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Editar Contato' : 'Novo Contato' }}</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <form @submit.prevent="saveContact" class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input v-model="formData.first_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Sobrenome *</label>
              <input v-model="formData.last_name" type="text" required />
            </div>
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

          <div class="form-group">
            <label>Email</label>
            <input v-model="formData.email" type="email" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Telefone Celular</label>
              <input v-model="formData.phone_mobile" type="tel" />
            </div>
            <div class="form-group">
              <label>Telefone Comercial</label>
              <input v-model="formData.phone_work" type="tel" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Cargo</label>
              <input v-model="formData.title" type="text" />
            </div>
            <div class="form-group">
              <label>Departamento</label>
              <input v-model="formData.department" type="text" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Cidade</label>
              <input v-model="formData.primary_address_city" type="text" />
            </div>
            <div class="form-group">
              <label>Estado</label>
              <input v-model="formData.primary_address_state" type="text" maxlength="2" />
            </div>
          </div>

          <div class="form-group">
            <label>Observações</label>
            <textarea v-model="formData.description" rows="3"></textarea>
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

const contacts = ref([])
const clients = ref([])
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const editingId = ref(null)

const filters = ref({
  search: '',
  account_id: ''
})

const formData = ref({
  first_name: '',
  last_name: '',
  account_id: '',
  email: '',
  phone_mobile: '',
  phone_work: '',
  title: '',
  department: '',
  primary_address_city: '',
  primary_address_state: '',
  description: ''
})

const loadContacts = async () => {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.account_id) params.account_id = filters.value.account_id

    const response = await api.get('/contacts', { params })
    contacts.value = response.data
  } catch (error) {
    console.error('Erro ao carregar contatos:', error)
    alert('Erro ao carregar contatos')
  } finally {
    loading.value = false
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

const getInitials = (name) => {
  if (!name) return '??'
  const parts = name.trim().split(' ')
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

const openCreateModal = () => {
  isEditing.value = false
  editingId.value = null
  formData.value = {
    first_name: '',
    last_name: '',
    account_id: '',
    email: '',
    phone_mobile: '',
    phone_work: '',
    title: '',
    department: '',
    primary_address_city: '',
    primary_address_state: '',
    description: ''
  }
  showModal.value = true
}

const editContact = (contact) => {
  isEditing.value = true
  editingId.value = contact.id
  formData.value = {
    first_name: contact.first_name || '',
    last_name: contact.last_name || '',
    account_id: contact.account_id || '',
    email: contact.email || '',
    phone_mobile: contact.phone_mobile || '',
    phone_work: contact.phone_work || '',
    title: contact.title || '',
    department: contact.department || '',
    primary_address_city: contact.primary_address_city || '',
    primary_address_state: contact.primary_address_state || '',
    description: contact.description || ''
  }
  showModal.value = true
}

const saveContact = async () => {
  saving.value = true
  try {
    if (isEditing.value) {
      await api.put(`/contacts/${editingId.value}`, formData.value)
      alert('Contato atualizado com sucesso!')
    } else {
      await api.post('/contacts', formData.value)
      alert('Contato criado com sucesso!')
    }
    closeModal()
    await loadContacts()
  } catch (error) {
    console.error('Erro ao salvar contato:', error)
    alert('Erro ao salvar contato')
  } finally {
    saving.value = false
  }
}

const deleteContact = async (contact) => {
  if (!confirm(`Deseja realmente excluir o contato ${contact.full_name}?`)) return

  try {
    await api.delete(`/contacts/${contact.id}`)
    alert('Contato excluído com sucesso!')
    await loadContacts()
  } catch (error) {
    console.error('Erro ao excluir contato:', error)
    alert('Erro ao excluir contato')
  }
}

const closeModal = () => {
  showModal.value = false
}

onMounted(async () => {
  await Promise.all([loadContacts(), loadClients()])
})
</script>

<style scoped>
.contacts-container {
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
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  min-width: 200px;
}

.contacts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.contact-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.contact-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.contact-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.contact-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.125rem;
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.contact-title {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0.25rem 0 0 0;
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4b5563;
  font-size: 0.875rem;
}

.detail-item .icon {
  font-size: 1rem;
}

.detail-item a {
  color: #3b82f6;
  text-decoration: none;
}

.detail-item a:hover {
  text-decoration: underline;
}

.contact-actions {
  display: flex;
  gap: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
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

.btn-primary:hover {
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
  flex: 1;
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
