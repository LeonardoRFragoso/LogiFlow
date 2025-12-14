<template>
  <div class="p-6">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Gestão de Leads</h1>
          <p class="text-gray-600 mt-1">Gerencie suas solicitações de demonstração e leads</p>
        </div>
        <button @click="refreshLeads" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          Atualizar
        </button>
      </div>

      <!-- Estatísticas -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="text-blue-100">Total de Leads</span>
            <svg class="w-8 h-8 text-blue-200" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
            </svg>
          </div>
          <div class="text-3xl font-bold">{{ stats.total }}</div>
        </div>

        <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="text-green-100">Novos</span>
            <svg class="w-8 h-8 text-green-200" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="text-3xl font-bold">{{ stats.novo }}</div>
        </div>

        <div class="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl p-6 text-white shadow-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="text-yellow-100">Em Contato</span>
            <svg class="w-8 h-8 text-yellow-200" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
            </svg>
          </div>
          <div class="text-3xl font-bold">{{ stats.contato }}</div>
        </div>

        <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="text-purple-100">Convertidos</span>
            <svg class="w-8 h-8 text-purple-200" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="text-3xl font-bold">{{ stats.convertido }}</div>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Buscar</label>
          <input v-model="filters.search" type="text" placeholder="Nome, email ou empresa..."
                 class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Status</label>
          <select v-model="filters.status"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">Todos</option>
            <option value="novo">Novo</option>
            <option value="contato">Em Contato</option>
            <option value="qualificado">Qualificado</option>
            <option value="convertido">Convertido</option>
            <option value="perdido">Perdido</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Origem</label>
          <select v-model="filters.source"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">Todas</option>
            <option value="site">Site</option>
            <option value="indicacao">Indicação</option>
            <option value="google">Google</option>
            <option value="redes_sociais">Redes Sociais</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Ordenar por</label>
          <select v-model="filters.sortBy"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="created_at">Data (mais recente)</option>
            <option value="name">Nome (A-Z)</option>
            <option value="company">Empresa (A-Z)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Tabela de Leads -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Lead</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Empresa</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Contato</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Veículos</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Status</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Data</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-if="loading" class="text-center">
              <td colspan="7" class="px-6 py-12">
                <div class="flex items-center justify-center">
                  <svg class="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span class="ml-3 text-gray-600">Carregando leads...</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredLeads.length === 0" class="text-center">
              <td colspan="7" class="px-6 py-12 text-gray-500">
                Nenhum lead encontrado
              </td>
            </tr>
            <tr v-else v-for="lead in filteredLeads" :key="lead.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center text-white font-bold">
                    {{ lead.name.charAt(0).toUpperCase() }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-semibold text-gray-900">{{ lead.name }}</div>
                    <div class="text-sm text-gray-500">{{ lead.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ lead.company || '-' }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ lead.phone || '-' }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">{{ lead.vehicles || '-' }}</div>
              </td>
              <td class="px-6 py-4">
                <span :class="getStatusClass(lead.status)" class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ getStatusLabel(lead.status) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ formatDate(lead.created_at) }}
              </td>
              <td class="px-6 py-4 text-sm font-medium">
                <div class="flex items-center gap-2">
                  <button @click="viewLead(lead)" class="text-blue-600 hover:text-blue-900 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  </button>
                  <button @click="editLead(lead)" class="text-green-600 hover:text-green-900 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button @click="deleteLead(lead)" class="text-red-600 hover:text-red-900 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de Detalhes -->
    <div v-if="selectedLead" class="fixed inset-0 z-50 overflow-y-auto" @click.self="selectedLead = null">
      <div class="flex items-center justify-center min-h-screen p-4">
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-8">
          <button @click="selectedLead = null" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>

          <h2 class="text-2xl font-bold text-gray-900 mb-6">Detalhes do Lead</h2>

          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-600 mb-1">Nome</label>
                <p class="text-gray-900">{{ selectedLead.name }}</p>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-600 mb-1">Email</label>
                <p class="text-gray-900">{{ selectedLead.email }}</p>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-600 mb-1">Telefone</label>
                <p class="text-gray-900">{{ selectedLead.phone || '-' }}</p>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-600 mb-1">Empresa</label>
                <p class="text-gray-900">{{ selectedLead.company || '-' }}</p>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-600 mb-1">Veículos</label>
                <p class="text-gray-900">{{ selectedLead.vehicles || '-' }}</p>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-600 mb-1">Status</label>
                <span :class="getStatusClass(selectedLead.status)" class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ getStatusLabel(selectedLead.status) }}
                </span>
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-600 mb-1">Mensagem</label>
              <p class="text-gray-900 bg-gray-50 p-4 rounded-lg">{{ selectedLead.message || 'Sem mensagem' }}</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-600 mb-1">Data de Criação</label>
              <p class="text-gray-900">{{ formatDate(selectedLead.created_at) }}</p>
            </div>

            <div class="pt-4 border-t border-gray-200">
              <label class="block text-sm font-semibold text-gray-600 mb-2">Alterar Status</label>
              <select v-model="selectedLead.status" @change="updateLeadStatus"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option value="novo">Novo</option>
                <option value="contato">Em Contato</option>
                <option value="qualificado">Qualificado</option>
                <option value="convertido">Convertido</option>
                <option value="perdido">Perdido</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const leads = ref([])
const loading = ref(false)
const selectedLead = ref(null)

const filters = ref({
  search: '',
  status: '',
  source: '',
  sortBy: 'created_at'
})

const stats = computed(() => {
  return {
    total: leads.value.length,
    novo: leads.value.filter(l => l.status === 'novo').length,
    contato: leads.value.filter(l => l.status === 'contato').length,
    convertido: leads.value.filter(l => l.status === 'convertido').length
  }
})

const filteredLeads = computed(() => {
  let result = [...leads.value]

  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    result = result.filter(l => 
      l.name.toLowerCase().includes(search) ||
      l.email.toLowerCase().includes(search) ||
      (l.company && l.company.toLowerCase().includes(search))
    )
  }

  if (filters.value.status) {
    result = result.filter(l => l.status === filters.value.status)
  }

  if (filters.value.source) {
    result = result.filter(l => l.source === filters.value.source)
  }

  result.sort((a, b) => {
    if (filters.value.sortBy === 'created_at') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (filters.value.sortBy === 'name') {
      return a.name.localeCompare(b.name)
    } else if (filters.value.sortBy === 'company') {
      return (a.company || '').localeCompare(b.company || '')
    }
    return 0
  })

  return result
})

const fetchLeads = async () => {
  loading.value = true
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/leads/`)
    const data = await response.json()
    leads.value = data.leads || []
  } catch (error) {
    console.error('Erro ao buscar leads:', error)
  } finally {
    loading.value = false
  }
}

const refreshLeads = () => {
  fetchLeads()
}

const viewLead = (lead) => {
  selectedLead.value = { ...lead }
}

const editLead = (lead) => {
  selectedLead.value = { ...lead }
}

const deleteLead = async (lead) => {
  if (!confirm(`Deseja realmente excluir o lead ${lead.name}?`)) return

  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    await fetch(`${apiUrl}/api/leads/${lead.id}`, { method: 'DELETE' })
    await fetchLeads()
  } catch (error) {
    console.error('Erro ao excluir lead:', error)
  }
}

const updateLeadStatus = async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    await fetch(`${apiUrl}/api/leads/${selectedLead.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: selectedLead.value.status })
    })
    await fetchLeads()
  } catch (error) {
    console.error('Erro ao atualizar status:', error)
  }
}

const getStatusClass = (status) => {
  const classes = {
    novo: 'bg-green-100 text-green-800',
    contato: 'bg-yellow-100 text-yellow-800',
    qualificado: 'bg-blue-100 text-blue-800',
    convertido: 'bg-purple-100 text-purple-800',
    perdido: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusLabel = (status) => {
  const labels = {
    novo: 'Novo',
    contato: 'Em Contato',
    qualificado: 'Qualificado',
    convertido: 'Convertido',
    perdido: 'Perdido'
  }
  return labels[status] || status
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchLeads()
})
</script>
