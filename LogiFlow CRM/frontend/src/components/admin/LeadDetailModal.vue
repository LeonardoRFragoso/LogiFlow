<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header">
        <h2 class="modal-title">Detalhes do Lead #{{ lead.id }}</h2>
        <button @click="$emit('close')" class="btn-close">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <!-- Body -->
      <div class="modal-body">
        <!-- Informações Principais -->
        <div class="info-section">
          <h3 class="section-title">Informações de Contato</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Nome</label>
              <p>{{ lead.name }}</p>
            </div>
            <div class="info-item">
              <label>Email</label>
              <p>{{ lead.email }}</p>
            </div>
            <div class="info-item">
              <label>Telefone</label>
              <p>{{ lead.phone }}</p>
            </div>
            <div class="info-item">
              <label>Empresa</label>
              <p>{{ lead.company }}</p>
            </div>
            <div class="info-item">
              <label>Veículos</label>
              <p>{{ lead.vehicles || 'Não informado' }}</p>
            </div>
            <div class="info-item">
              <label>Origem</label>
              <p class="capitalize">{{ lead.source }}</p>
            </div>
          </div>
        </div>

        <!-- Mensagem -->
        <div class="info-section" v-if="lead.message">
          <h3 class="section-title">Mensagem</h3>
          <p class="message-text">{{ lead.message }}</p>
        </div>

        <!-- Status Atual -->
        <div class="info-section">
          <h3 class="section-title">Status e Datas</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Status Atual</label>
              <span :class="getStatusClass(lead.status)" class="status-badge-large">
                {{ getStatusLabel(lead.status) }}
              </span>
            </div>
            <div class="info-item">
              <label>Criado em</label>
              <p>{{ formatDate(lead.created_at) }}</p>
            </div>
            <div class="info-item">
              <label>Atualizado em</label>
              <p>{{ formatDate(lead.updated_at) }}</p>
            </div>
            <div class="info-item" v-if="lead.converted_at">
              <label>Convertido em</label>
              <p>{{ formatDate(lead.converted_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Atualizar Status -->
        <div class="info-section">
          <h3 class="section-title">Atualizar Status</h3>
          <div class="status-actions">
            <button
              v-for="status in availableStatuses"
              :key="status.value"
              @click="updateStatus(status.value)"
              :class="['status-btn', status.class]"
              :disabled="lead.status === status.value"
            >
              <i :class="status.icon"></i>
              {{ status.label }}
            </button>
          </div>
        </div>

        <!-- Atribuir Vendedor -->
        <div class="info-section">
          <h3 class="section-title">Atribuir a Vendedor</h3>
          <div class="assign-section">
            <select v-model="selectedUser" class="user-select">
              <option value="">Selecione um vendedor...</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.nome }} ({{ user.email }})
              </option>
            </select>
            <button
              @click="assignLead"
              :disabled="!selectedUser"
              class="btn-assign"
            >
              <i class="fas fa-user-check"></i>
              Atribuir
            </button>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <button @click="$emit('close')" class="btn-secondary">
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'LeadDetailModal',
  props: {
    lead: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'updated'],
  setup(props, { emit }) {
    const authStore = useAuthStore();
    const selectedUser = ref('');
    const users = ref([]);

    const availableStatuses = computed(() => {
      const statuses = [
        { value: 'novo', label: 'Novo', icon: 'fas fa-star', class: 'status-novo' },
        { value: 'contatado', label: 'Contatado', icon: 'fas fa-phone', class: 'status-contatado' },
        { value: 'qualificado', label: 'Qualificado', icon: 'fas fa-check', class: 'status-qualificado' },
        { value: 'convertido', label: 'Convertido', icon: 'fas fa-check-circle', class: 'status-convertido' },
        { value: 'perdido', label: 'Perdido', icon: 'fas fa-times-circle', class: 'status-perdido' }
      ];
      return statuses.filter(s => s.value !== props.lead.status);
    });

    const updateStatus = async (newStatus) => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/${props.lead.id}/status`,
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
          emit('updated');
          emit('close');
        }
      } catch (error) {
        console.error('Erro ao atualizar status:', error);
        alert('Erro ao atualizar status');
      }
    };

    const assignLead = async () => {
      if (!selectedUser.value) return;

      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/admin/leads/${props.lead.id}/assign`,
          {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${authStore.token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: parseInt(selectedUser.value) })
          }
        );

        if (response.ok) {
          alert('Lead atribuído com sucesso!');
          emit('updated');
          emit('close');
        }
      } catch (error) {
        console.error('Erro ao atribuir lead:', error);
        alert('Erro ao atribuir lead');
      }
    };

    const fetchUsers = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/v1/auth/usuarios`,
          {
            headers: {
              'Authorization': `Bearer ${authStore.token}`
            }
          }
        );

        if (response.ok) {
          const data = await response.json();
          users.value = data.data || [];
        }
      } catch (error) {
        console.error('Erro ao carregar usuários:', error);
      }
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

    fetchUsers();

    return {
      selectedUser,
      users,
      availableStatuses,
      updateStatus,
      assignLead,
      getStatusClass,
      getStatusLabel,
      formatDate
    };
  }
};
</script>

<style scoped>
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
  border-radius: 1rem;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.btn-close {
  padding: 0.5rem;
  background: #f3f4f6;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #e5e7eb;
  color: #111827;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.info-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.info-item p {
  font-size: 0.875rem;
  color: #111827;
  font-weight: 500;
}

.message-text {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.6;
}

.status-badge-large {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.status-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.status-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-novo {
  background: #dbeafe;
  color: #1e40af;
}

.status-novo:hover:not(:disabled) {
  background: #bfdbfe;
}

.status-contatado {
  background: #fef3c7;
  color: #92400e;
}

.status-contatado:hover:not(:disabled) {
  background: #fde68a;
}

.status-qualificado {
  background: #e9d5ff;
  color: #6b21a8;
}

.status-qualificado:hover:not(:disabled) {
  background: #d8b4fe;
}

.status-convertido {
  background: #d1fae5;
  color: #065f46;
}

.status-convertido:hover:not(:disabled) {
  background: #a7f3d0;
}

.status-perdido {
  background: #fee2e2;
  color: #991b1b;
}

.status-perdido:hover:not(:disabled) {
  background: #fecaca;
}

.assign-section {
  display: flex;
  gap: 1rem;
}

.user-select {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.btn-assign {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
}

.btn-assign:hover:not(:disabled) {
  background: #2563eb;
}

.btn-assign:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.capitalize {
  text-transform: capitalize;
}
</style>
