<template>
  <div class="listar-cte-container">
    <div class="header">
      <h1>CT-es Emitidos</h1>
      <button @click="$router.push('/pedidos')" class="btn btn-secondary">
        <i class="icon-arrow-left"></i> Voltar para Pedidos
      </button>
    </div>

    <div class="filters">
      <div class="filter-group">
        <label>Status</label>
        <select v-model="filtros.status" @change="carregarCTes">
          <option value="">Todos</option>
          <option value="autorizado">Autorizado</option>
          <option value="processando">Processando</option>
          <option value="cancelado">Cancelado</option>
          <option value="rejeitado">Rejeitado</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Data Início</label>
        <input type="date" v-model="filtros.data_inicio" @change="carregarCTes" />
      </div>

      <div class="filter-group">
        <label>Data Fim</label>
        <input type="date" v-model="filtros.data_fim" @change="carregarCTes" />
      </div>

      <div class="filter-group">
        <label>Pedido ID</label>
        <input type="text" v-model="filtros.pedido_id" @input="carregarCTes" placeholder="ID do pedido" />
      </div>

      <button @click="limparFiltros" class="btn btn-secondary">Limpar Filtros</button>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando CT-es...</p>
    </div>

    <div v-else-if="ctes.length === 0" class="empty-state">
      <p>Nenhum CT-e encontrado</p>
    </div>

    <div v-else class="table-container">
      <table class="cte-table">
        <thead>
          <tr>
            <th>Número</th>
            <th>Série</th>
            <th>Chave</th>
            <th>Status</th>
            <th>Data Emissão</th>
            <th>Tomador</th>
            <th>Valor</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cte in ctes" :key="cte.id">
            <td>{{ cte.numero }}</td>
            <td>{{ cte.serie }}</td>
            <td class="chave">{{ formatarChave(cte.chave) }}</td>
            <td>
              <span :class="['status-badge', `status-${cte.status}`]">
                {{ formatarStatus(cte.status) }}
              </span>
            </td>
            <td>{{ formatarData(cte.data_emissao) }}</td>
            <td>{{ cte.tomador_nome }}</td>
            <td>{{ formatarValor(cte.valor_total) }}</td>
            <td class="acoes">
              <button @click="verDetalhes(cte)" class="btn btn-sm btn-info" title="Ver detalhes">
                <i class="icon-eye"></i>
              </button>
              <button @click="downloadPDF(cte)" class="btn btn-sm btn-primary" title="Download PDF">
                <i class="icon-download"></i> PDF
              </button>
              <button @click="downloadXML(cte)" class="btn btn-sm btn-secondary" title="Download XML">
                <i class="icon-download"></i> XML
              </button>
              <button 
                v-if="cte.status === 'autorizado'" 
                @click="cancelarCTe(cte)" 
                class="btn btn-sm btn-danger"
                title="Cancelar CT-e"
              >
                <i class="icon-x"></i> Cancelar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pagination">
        <button @click="paginaAnterior" :disabled="paginaAtual === 1" class="btn btn-secondary">
          Anterior
        </button>
        <span>Página {{ paginaAtual }} de {{ totalPaginas }}</span>
        <button @click="proximaPagina" :disabled="paginaAtual === totalPaginas" class="btn btn-secondary">
          Próxima
        </button>
      </div>
    </div>

    <div v-if="showCancelModal" class="modal">
      <div class="modal-content">
        <h3>Cancelar CT-e {{ cteParaCancelar?.numero }}</h3>
        <p>Informe o motivo do cancelamento (mínimo 15 caracteres):</p>
        <textarea 
          v-model="motivoCancelamento" 
          rows="4" 
          placeholder="Ex: Emissão com dados incorretos..."
          class="form-control"
        ></textarea>
        <div class="modal-actions">
          <button @click="confirmarCancelamento" :disabled="motivoCancelamento.length < 15" class="btn btn-danger">
            Confirmar Cancelamento
          </button>
          <button @click="showCancelModal = false" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const ctes = ref([])
const loading = ref(false)
const paginaAtual = ref(1)
const totalPaginas = ref(1)
const limit = ref(50)

const filtros = ref({
  status: '',
  data_inicio: '',
  data_fim: '',
  pedido_id: ''
})

const showCancelModal = ref(false)
const cteParaCancelar = ref(null)
const motivoCancelamento = ref('')

async function carregarCTes() {
  loading.value = true
  try {
    const params = {
      page: paginaAtual.value,
      limit: limit.value,
      ...filtros.value
    }

    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })

    const response = await api.get('/fiscal/cte', { params })
    ctes.value = response.data.data
    totalPaginas.value = response.data.pages
  } catch (error) {
    console.error('Erro ao carregar CT-es:', error)
    alert('Erro ao carregar CT-es')
  } finally {
    loading.value = false
  }
}

function limparFiltros() {
  filtros.value = {
    status: '',
    data_inicio: '',
    data_fim: '',
    pedido_id: ''
  }
  paginaAtual.value = 1
  carregarCTes()
}

function paginaAnterior() {
  if (paginaAtual.value > 1) {
    paginaAtual.value--
    carregarCTes()
  }
}

function proximaPagina() {
  if (paginaAtual.value < totalPaginas.value) {
    paginaAtual.value++
    carregarCTes()
  }
}

function verDetalhes(cte) {
  router.push(`/fiscal/cte/${cte.ref}`)
}

async function downloadPDF(cte) {
  try {
    const response = await api.get(`/fiscal/cte/${cte.ref}/pdf`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `DACTE_${cte.numero}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar PDF:', error)
    alert('Erro ao baixar PDF')
  }
}

async function downloadXML(cte) {
  try {
    const response = await api.get(`/fiscal/cte/${cte.ref}/xml`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `CTE_${cte.numero}.xml`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar XML:', error)
    alert('Erro ao baixar XML')
  }
}

function cancelarCTe(cte) {
  cteParaCancelar.value = cte
  motivoCancelamento.value = ''
  showCancelModal.value = true
}

async function confirmarCancelamento() {
  try {
    await api.delete(`/fiscal/cte/${cteParaCancelar.value.ref}`, {
      data: { justificativa: motivoCancelamento.value }
    })
    alert('CT-e cancelado com sucesso!')
    showCancelModal.value = false
    carregarCTes()
  } catch (error) {
    console.error('Erro ao cancelar CT-e:', error)
    alert(error.response?.data?.detail || 'Erro ao cancelar CT-e')
  }
}

function formatarChave(chave) {
  if (!chave) return '-'
  return chave.substring(0, 8) + '...' + chave.substring(chave.length - 8)
}

function formatarStatus(status) {
  const statusMap = {
    autorizado: 'Autorizado',
    processando: 'Processando',
    cancelado: 'Cancelado',
    rejeitado: 'Rejeitado',
    rascunho: 'Rascunho'
  }
  return statusMap[status] || status
}

function formatarData(data) {
  if (!data) return '-'
  return new Date(data).toLocaleDateString('pt-BR')
}

function formatarValor(valor) {
  if (!valor) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor)
}

onMounted(() => {
  carregarCTes()
})
</script>

<style scoped>
.listar-cte-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #333;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-size: 12px;
  font-weight: 600;
  color: #666;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.cte-table {
  width: 100%;
  border-collapse: collapse;
}

.cte-table thead {
  background: #f8f9fa;
}

.cte-table th,
.cte-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.cte-table th {
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.cte-table td {
  font-size: 14px;
  color: #212529;
}

.chave {
  font-family: monospace;
  font-size: 12px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-autorizado {
  background: #d4edda;
  color: #155724;
}

.status-processando {
  background: #fff3cd;
  color: #856404;
}

.status-cancelado {
  background: #f8d7da;
  color: #721c24;
}

.status-rejeitado {
  background: #f8d7da;
  color: #721c24;
}

.acoes {
  display: flex;
  gap: 5px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border-top: 1px solid #dee2e6;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-content h3 {
  margin-bottom: 20px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  margin: 15px 0;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
