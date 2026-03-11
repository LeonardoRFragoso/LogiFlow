<template>
  <div class="admin-leads-view">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Gestão de Leads</h1>
        <p class="text-gray-600 mt-1">Gerencie solicitações de demonstração e converta em clientes</p>
      </div>
      <button @click="fetchLeads" class="btn-refresh">
        <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
        Atualizar
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid" v-if="stats">
      <div class="stat-card">
        <div class="stat-icon bg-blue-100 text-blue-600">
          <i class="fas fa-users"></i>
        </div>
        <div>
          <p class="stat-label">Total de Leads</p>
          <p class="stat-value">{{ stats.total }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon bg-green-100 text-green-600">
          <i class="fas fa-user-plus"></i>
        </div>
        <div>
          <p class="stat-label">Novos</p>
          <p class="stat-value">{{ stats.por_status?.novos || 0 }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon bg-purple-100 text-purple-600">
          <i class="fas fa-check-circle"></i>
        </div>
        <div>
          <p class="stat-label">Convertidos</p>
          <p class="stat-value">{{ stats.por_status?.convertidos || 0 }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon bg-yellow-100 text-yellow-600">
          <i class="fas fa-percentage"></i>
        </div>
        <div>
          <p class="stat-label">Taxa de Conversão</p>
          <p class="stat-value">{{ stats.taxa_conversao }}%</p>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-card">
      <div class="filters-grid">
        <div class="filter-group">
          <label>Buscar</label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Nome, email ou empresa..."
            class="filter-input"
            @input="debouncedSearch"
          />
        </div>

        <div class="filter-group">
          <label>Status</label>
          <select v-model="filters.status" @change="fetchLeads" class="filter-select">
            <option value="">Todos</option>
            <option value="novo">Novo</option>
            <option value="contatado">Contatado</option>
            <option value="qualificado">Qualificado</option>
            <option value="convertido">Convertido</option>
            <option value="perdido">Perdido</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Origem</label>
          <select v-model="filters.source" @change="fetchLeads" class="filter-select">
            <option value="">Todas</option>
            <option value="site">Site</option>
            <option value="indicacao">Indicação</option>
            <option value="google">Google</option>
            <option value="facebook">Facebook</option>
          </select>
        </div>

        <div class="filter-group">
          <button @click="clearFilters" class="btn-clear-filters">
            <i class="fas fa-times"></i>
            Limpar Filtros
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-spin text-4xl text-blue-500"></i>
        <p class="mt-4 text-gray-600">Carregando leads...</p>
      </div>

      <div v-else-if="leads.length === 0" class="empty-state">
        <i class="fas fa-inbox text-6xl text-gray-300"></i>
        <p class="mt-4 text-gray-600 text-lg">Nenhum lead encontrado</p>
        <p class="text-gray-500 text-sm">Ajuste os filtros ou aguarde novas solicitações</p>
      </div>

      <table v-else class="leads-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Empresa</th>
            <th>Email</th>
            <th>Telefone</th>
            <th>Veículos</th>
            <th>Status</th>
            <th>Origem</th>
            <th>Data</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lead in leads" :key="lead.id" class="lead-row">
            <td class="font-mono text-sm">{{ lead.id }}</td>
            <td class="font-medium">{{ lead.name }}</td>
            <td>{{ lead.company }}</td>
            <td class="text-sm">{{ lead.email }}</td>
            <td class="text-sm">{{ lead.phone }}</td>
            <td class="text-center">{{ lead.vehicles || '-' }}</td>
            <td>
              <span :class="getStatusClass(lead.status)" class="status-badge">
                {{ getStatusLabel(lead.status) }}
              </span>
            </td>
            <td>
              <span class="source-badge">{{ lead.source }}</span>
            </td>
            <td class="text-sm text-gray-600">
              {{ formatDate(lead.created_at) }}
            </td>
            <td>
              <div class="action-buttons">
                <button
                  @click="viewLead(lead)"
                  class="btn-action btn-view"
                  title="Ver detalhes"
                >
                  <i class="fas fa-eye"></i>
                </button>
                <button
                  v-if="lead.status === 'novo'"
                  @click="updateStatus(lead.id, 'contatado')"
                  class="btn-action btn-contact"
                  title="Marcar como contatado"
                >
                  <i class="fas fa-phone"></i>
                </button>
                <button
                  v-if="lead.status !== 'convertido'"
                  @click="openConvertModal(lead)"
                  class="btn-action btn-convert"
                  title="Converter em cliente"
                >
                  <i class="fas fa-check-circle"></i>
                </button>
                <button
                  @click="deleteLead(lead.id)"
                  class="btn-action btn-delete"
                  title="Deletar"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Lead Detail Modal -->
    <LeadDetailModal
      v-if="selectedLead"
      :lead="selectedLead"
      @close="selectedLead = null"
      @updated="fetchLeads"
    />

    <!-- Convert Lead Modal -->
    <ConvertLeadModal
      v-if="leadToConvert"
      :lead="leadToConvert"
      @close="leadToConvert = null"
      @converted="handleLeadConverted"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import LeadDetailModal from '@/components/admin/LeadDetailModal.vue';
import ConvertLeadModal from '@/components/admin/ConvertLeadModal.vue';

export default {
  name: 'AdminLeadsView',
  components: {
    LeadDetailModal,
    ConvertLeadModal
  },
  setup() {
    const authStore = useAuthStore();
    const leads = ref([]);
    const stats = ref(null);
    const loading = ref(false);
    const selectedLead = ref(null);
    const leadToConvert = ref(null);
    
    const filters = reactive({
      search: '',
      status: '',
      source: '',
      assigned_to: null
    });

    let searchTimeout = null;

    const fetchLeads = async () => {
      loading.value = true;
      try {
        const params = new URLSearchParams();
        if (filters.status) params.append('status', filters.status);
        if (filters.source) params.append('source', filters.source);
        if (filters.search) params.append('search', filters.search);
        if (filters.assigned_to) params.append('assigned_to', filters.assigned_to);

        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/?${params}`,
          {
            headers: {
              'Authorization': `Bearer ${authStore.token}`
            }
          }
        );

        if (response.ok) {
          leads.value = await response.json();
        }
      } catch (error) {
        console.error('Erro ao carregar leads:', error);
        alert('Erro ao carregar leads');
      } finally {
        loading.value = false;
      }
    };

    const fetchStats = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/stats`,
          {
            headers: {
              'Authorization': `Bearer ${authStore.token}`
            }
          }
        );

        if (response.ok) {
          const data = await response.json();
          stats.value = data.data;
        }
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
      }
    };

    const debouncedSearch = () => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        fetchLeads();
      }, 500);
    };

    const clearFilters = () => {
      filters.search = '';
      filters.status = '';
      filters.source = '';
      filters.assigned_to = null;
      fetchLeads();
    };

    const updateStatus = async (leadId, newStatus) => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/${leadId}/status`,
          {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${authStore.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
          }
        );

        if (response.ok) {
          alert('Status atualizado com sucesso!');
          fetchLeads();
          fetchStats();
        }
      } catch (error) {
        console.error('Erro ao atualizar status:', error);
        alert('Erro ao atualizar status');
      }
    };

    const deleteLead = async (leadId) => {
      if (!confirm('Tem certeza que deseja deletar este lead?')) return;

      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/${leadId}`,
          {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${authStore.token}`
            }
          }
        );

        if (response.ok) {
          alert('Lead deletado com sucesso!');
          fetchLeads();
          fetchStats();
        }
      } catch (error) {
        console.error('Erro ao deletar lead:', error);
        alert('Erro ao deletar lead');
      }
    };

    const viewLead = (lead) => {
      selectedLead.value = lead;
    };

    const openConvertModal = (lead) => {
      leadToConvert.value = lead;
    };

    const handleLeadConverted = () => {
      leadToConvert.value = null;
      fetchLeads();
      fetchStats();
    };

    const getStatusClass = (status) => {
      const classes = {
        'novo': 'bg-blue-100 text-blue-800',
        'contatado': 'bg-yellow-100 text-yellow-800',
        'qualificado': 'bg-purple-100 text-purple-800',
        'convertido': 'bg-green-100 text-green-800',
        'perdido': 'bg-red-100 text-red-800'
      };
      return classes[status] || 'bg-gray-100 text-gray-800';
    };

    const getStatusLabel = (status) => {
      const labels = {
        'novo': 'Novo',
        'contatado': 'Contatado',
        'qualificado': 'Qualificado',
        'convertido': 'Convertido',
        'perdido': 'Perdido'
      };
      return labels[status] || status;
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    onMounted(() => {
      fetchLeads();
      fetchStats();
    });

    return {
      leads,
      stats,
      loading,
      filters,
      selectedLead,
      leadToConvert,
      fetchLeads,
      debouncedSearch,
      clearFilters,
      updateStatus,
      deleteLead,
      viewLead,
      openConvertModal,
      handleLeadConverted,
      getStatusClass,
      getStatusLabel,
      formatDate
    };
  }
};
</script>

<style scoped>
.admin-leads-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-refresh:hover {
  background: #2563eb;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
}

.filters-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.filter-input,
.filter-select {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.filter-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  ring: 2px;
  ring-color: #3b82f620;
}

.btn-clear-filters {
  width: 100%;
  padding: 0.625rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.6rem;
}

.btn-clear-filters:hover {
  background: #e5e7eb;
}

.table-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.loading-state,
.empty-state {
  padding: 4rem;
  text-align: center;
}

.leads-table {
  width: 100%;
  border-collapse: collapse;
}

.leads-table thead {
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.leads-table th {
  padding: 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.lead-row {
  border-bottom: 1px solid #e5e7eb;
  transition: background 0.2s;
}

.lead-row:hover {
  background: #f9fafb;
}

.leads-table td {
  padding: 1rem;
  font-size: 0.875rem;
  color: #111827;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.source-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f3f4f6;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b7280;
  text-transform: capitalize;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  padding: 0.5rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.btn-view {
  background: #eff6ff;
  color: #3b82f6;
}

.btn-view:hover {
  background: #dbeafe;
}

.btn-contact {
  background: #fef3c7;
  color: #f59e0b;
}

.btn-contact:hover {
  background: #fde68a;
}

.btn-convert {
  background: #d1fae5;
  color: #10b981;
}

.btn-convert:hover {
  background: #a7f3d0;
}

.btn-delete {
  background: #fee2e2;
  color: #ef4444;
}

.btn-delete:hover {
  background: #fecaca;
}
</style>
