<template>
  <div class="cotacoes-view">
    <div class="header">
      <h1>Cotações</h1>
      <button @click="novaCotacao" class="btn-primary">
        + Nova Cotação
      </button>
    </div>

    <!-- Filtros -->
    <div class="filters">
      <input 
        v-model="filtros.busca" 
        type="text" 
        placeholder="Buscar cotação..."
        class="search-input"
      />
      <select v-model="filtros.status" class="filter-select">
        <option value="">Todos os status</option>
        <option value="aberta">Aberta</option>
        <option value="aprovada">Aprovada</option>
        <option value="perdida">Perdida</option>
        <option value="expirada">Expirada</option>
      </select>
    </div>

    <!-- Lista de Cotações -->
    <div class="cotacoes-list">
      <div 
        v-for="cotacao in cotacoesFiltradas" 
        :key="cotacao.id"
        class="cotacao-card"
        @click="abrirCotacao(cotacao.id)"
      >
        <div class="cotacao-header">
          <span class="cotacao-numero">{{ cotacao.numero }}</span>
          <span :class="['status-badge', `status-${cotacao.status}`]">
            {{ statusLabel(cotacao.status) }}
          </span>
        </div>
        
        <div class="cotacao-body">
          <div class="cliente">
            <strong>{{ cotacao.cliente_nome }}</strong>
          </div>
          <div class="rota">
            <span>{{ cotacao.origem_cidade }}/{{ cotacao.origem_uf }}</span>
            <span class="arrow">→</span>
            <span>{{ cotacao.destino_cidade }}/{{ cotacao.destino_uf }}</span>
          </div>
          <div class="detalhes">
            <span>{{ cotacao.tipo_carga }}</span>
            <span>{{ cotacao.peso_kg }} kg</span>
            <span class="valor">R$ {{ formatarValor(cotacao.valor_proposta) }}</span>
          </div>
        </div>
        
        <div class="cotacao-footer">
          <span class="data">{{ formatarData(cotacao.data_criacao) }}</span>
          <span class="validade">Válida até {{ formatarData(cotacao.validade) }}</span>
        </div>
      </div>
    </div>

    <!-- Modal Nova Cotação -->
    <div v-if="modalNovaCotacao" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Nova Cotação</h2>
          <button @click="modalNovaCotacao = false" class="btn-close">×</button>
        </div>
        
        <form @submit.prevent="salvarCotacao" class="cotacao-form">
          <div class="form-group">
            <label>Cliente *</label>
            <select v-model="novaCotacaoForm.cliente_id" required>
              <option value="">Selecione o cliente</option>
              <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                {{ cliente.nome }}
              </option>
            </select>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Origem - Cidade *</label>
              <input v-model="novaCotacaoForm.origem_cidade" type="text" required />
            </div>
            <div class="form-group">
              <label>UF *</label>
              <input v-model="novaCotacaoForm.origem_uf" type="text" maxlength="2" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Destino - Cidade *</label>
              <input v-model="novaCotacaoForm.destino_cidade" type="text" required />
            </div>
            <div class="form-group">
              <label>UF *</label>
              <input v-model="novaCotacaoForm.destino_uf" type="text" maxlength="2" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Tipo de Carga *</label>
              <select v-model="novaCotacaoForm.tipo_carga" required>
                <option value="geral">Geral</option>
                <option value="refrigerada">Refrigerada</option>
                <option value="perigosa">Perigosa</option>
                <option value="fragil">Frágil</option>
              </select>
            </div>
            <div class="form-group">
              <label>Peso (kg) *</label>
              <input v-model.number="novaCotacaoForm.peso_kg" type="number" step="0.01" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Valor Proposta (R$) *</label>
              <input v-model.number="novaCotacaoForm.valor_proposta" type="number" step="0.01" required />
            </div>
            <div class="form-group">
              <label>Prazo Estimado (dias) *</label>
              <input v-model.number="novaCotacaoForm.prazo_estimado" type="number" required />
            </div>
          </div>

          <div class="form-group">
            <label>Observações</label>
            <textarea v-model="novaCotacaoForm.observacoes" rows="3"></textarea>
          </div>

          <div class="form-actions">
            <button type="button" @click="modalNovaCotacao = false" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary">
              Salvar Cotação
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

// Estado
const cotacoes = ref([])
const clientes = ref([])
const modalNovaCotacao = ref(false)
const filtros = ref({
  busca: '',
  status: ''
})

const novaCotacaoForm = ref({
  cliente_id: '',
  origem_cidade: '',
  origem_uf: '',
  destino_cidade: '',
  destino_uf: '',
  tipo_carga: 'geral',
  peso_kg: 0,
  valor_proposta: 0,
  prazo_estimado: 3,
  observacoes: ''
})

// Computed
const cotacoesFiltradas = computed(() => {
  let resultado = cotacoes.value

  if (filtros.value.busca) {
    const busca = filtros.value.busca.toLowerCase()
    resultado = resultado.filter(c => 
      c.numero.toLowerCase().includes(busca) ||
      c.cliente_nome.toLowerCase().includes(busca) ||
      c.origem_cidade.toLowerCase().includes(busca) ||
      c.destino_cidade.toLowerCase().includes(busca)
    )
  }

  if (filtros.value.status) {
    resultado = resultado.filter(c => c.status === filtros.value.status)
  }

  return resultado
})

// Métodos
const carregarCotacoes = async () => {
  try {
    const response = await api.get('/cotacoes')
    cotacoes.value = response.data.data || []
  } catch (error) {
    console.error('Erro ao carregar cotações:', error)
  }
}

const carregarClientes = async () => {
  try {
    const response = await api.get('/clientes')
    clientes.value = response.data.data || []
  } catch (error) {
    console.error('Erro ao carregar clientes:', error)
  }
}

const novaCotacao = () => {
  modalNovaCotacao.value = true
}

const salvarCotacao = async () => {
  try {
    await api.post('/cotacoes', novaCotacaoForm.value)
    modalNovaCotacao.value = false
    await carregarCotacoes()
    // Resetar formulário
    novaCotacaoForm.value = {
      cliente_id: '',
      origem_cidade: '',
      origem_uf: '',
      destino_cidade: '',
      destino_uf: '',
      tipo_carga: 'geral',
      peso_kg: 0,
      valor_proposta: 0,
      prazo_estimado: 3,
      observacoes: ''
    }
  } catch (error) {
    console.error('Erro ao salvar cotação:', error)
    alert('Erro ao salvar cotação. Tente novamente.')
  }
}

const abrirCotacao = (id) => {
  router.push(`/cotacoes/${id}`)
}

const statusLabel = (status) => {
  const labels = {
    aberta: 'Aberta',
    aprovada: 'Aprovada',
    perdida: 'Perdida',
    expirada: 'Expirada'
  }
  return labels[status] || status
}

const formatarValor = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(valor)
}

const formatarData = (data) => {
  if (!data) return '-'
  return new Date(data).toLocaleDateString('pt-BR')
}

// Lifecycle
onMounted(() => {
  carregarCotacoes()
  carregarClientes()
})
</script>

<style scoped>
.cotacoes-view {
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  min-width: 200px;
}

.cotacoes-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.cotacao-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.cotacao-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.cotacao-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.cotacao-numero {
  font-weight: 600;
  color: #1f2937;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-aberta { background: #dbeafe; color: #1e40af; }
.status-aprovada { background: #d1fae5; color: #065f46; }
.status-perdida { background: #fee2e2; color: #991b1b; }
.status-expirada { background: #f3f4f6; color: #6b7280; }

.cotacao-body {
  margin-bottom: 1rem;
}

.cliente {
  margin-bottom: 0.5rem;
}

.rota {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.arrow {
  color: #3b82f6;
}

.detalhes {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.valor {
  color: #059669;
  font-weight: 600;
  margin-left: auto;
}

.cotacao-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: #9ca3af;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

/* Modal */
.modal {
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #6b7280;
}

.cotacao-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: white;
  color: #6b7280;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #f9fafb;
}
</style>
