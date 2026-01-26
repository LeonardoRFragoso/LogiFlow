<template>
  <div class="listar-mdfe-container">
    <div class="header">
      <h1>MDF-es Emitidos</h1>
      <div class="header-actions">
        <button @click="$router.push('/fiscal/mdfe/emitir')" class="btn btn-primary">
          <i class="icon-plus"></i> Emitir MDF-e
        </button>
        <button @click="$router.push('/fiscal/cte')" class="btn btn-secondary">
          Ver CT-es
        </button>
      </div>
    </div>

    <div class="filters">
      <div class="filter-group">
        <label>Status</label>
        <select v-model="filtros.status" @change="carregarMDFes">
          <option value="">Todos</option>
          <option value="autorizado">Autorizado</option>
          <option value="encerrado">Encerrado</option>
          <option value="processando">Processando</option>
          <option value="cancelado">Cancelado</option>
          <option value="rejeitado">Rejeitado</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Data Início</label>
        <input type="date" v-model="filtros.data_inicio" @change="carregarMDFes" />
      </div>

      <div class="filter-group">
        <label>Data Fim</label>
        <input type="date" v-model="filtros.data_fim" @change="carregarMDFes" />
      </div>

      <button @click="limparFiltros" class="btn btn-secondary">Limpar Filtros</button>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando MDF-es...</p>
    </div>

    <div v-else-if="mdfes.length === 0" class="empty-state">
      <p>Nenhum MDF-e encontrado</p>
      <button @click="$router.push('/fiscal/mdfe/emitir')" class="btn btn-primary">
        Emitir Primeiro MDF-e
      </button>
    </div>

    <div v-else class="table-container">
      <table class="mdfe-table">
        <thead>
          <tr>
            <th>Número</th>
            <th>Série</th>
            <th>Chave</th>
            <th>Status</th>
            <th>Data Emissão</th>
            <th>CT-es</th>
            <th>Percurso</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="mdfe in mdfes" :key="mdfe.id">
            <td>{{ mdfe.numero }}</td>
            <td>{{ mdfe.serie }}</td>
            <td class="chave">{{ formatarChave(mdfe.chave) }}</td>
            <td>
              <span :class="['status-badge', `status-${mdfe.status}`]">
                {{ formatarStatus(mdfe.status) }}
              </span>
            </td>
            <td>{{ formatarData(mdfe.data_emissao) }}</td>
            <td>
              <span class="badge">{{ mdfe.quantidade_ctes }} CT-es</span>
            </td>
            <td>
              <div class="percurso">
                <span v-for="uf in mdfe.percurso" :key="uf" class="uf-badge">{{ uf }}</span>
              </div>
            </td>
            <td class="acoes">
              <button @click="verDetalhes(mdfe)" class="btn btn-sm btn-info" title="Ver detalhes">
                <i class="icon-eye"></i>
              </button>
              <button @click="downloadPDF(mdfe)" class="btn btn-sm btn-primary" title="Download PDF">
                <i class="icon-download"></i> PDF
              </button>
              <button @click="downloadXML(mdfe)" class="btn btn-sm btn-secondary" title="Download XML">
                <i class="icon-download"></i> XML
              </button>
              <button 
                v-if="mdfe.status === 'autorizado'" 
                @click="encerrarMDFe(mdfe)" 
                class="btn btn-sm btn-success"
                title="Encerrar MDF-e"
              >
                <i class="icon-check"></i> Encerrar
              </button>
              <button 
                v-if="mdfe.status === 'autorizado'" 
                @click="cancelarMDFe(mdfe)" 
                class="btn btn-sm btn-danger"
                title="Cancelar MDF-e"
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

    <div v-if="showEncerrarModal" class="modal">
      <div class="modal-content">
        <h3>Encerrar MDF-e {{ mdfeParaEncerrar?.numero }}</h3>
        <p>Informe os dados do encerramento:</p>
        <div class="form-group">
          <label>UF de Encerramento</label>
          <select v-model="dadosEncerramento.uf" class="form-control">
            <option value="">Selecione a UF</option>
            <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Código IBGE da Cidade</label>
          <input 
            v-model="dadosEncerramento.cidade_codigo" 
            type="text" 
            class="form-control"
            placeholder="Ex: 3550308 (São Paulo)"
          />
        </div>
        <div class="modal-actions">
          <button @click="confirmarEncerramento" :disabled="!dadosEncerramento.uf || !dadosEncerramento.cidade_codigo" class="btn btn-success">
            Confirmar Encerramento
          </button>
          <button @click="showEncerrarModal = false" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </div>
    </div>

    <div v-if="showCancelModal" class="modal">
      <div class="modal-content">
        <h3>Cancelar MDF-e {{ mdfeParaCancelar?.numero }}</h3>
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

const mdfes = ref([])
const loading = ref(false)
const paginaAtual = ref(1)
const totalPaginas = ref(1)
const limit = ref(50)

const filtros = ref({
  status: '',
  data_inicio: '',
  data_fim: ''
})

const showEncerrarModal = ref(false)
const showCancelModal = ref(false)
const mdfeParaEncerrar = ref(null)
const mdfeParaCancelar = ref(null)
const motivoCancelamento = ref('')
const dadosEncerramento = ref({
  uf: '',
  cidade_codigo: ''
})

const ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

async function carregarMDFes() {
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

    const response = await api.get('/fiscal/mdfe', { params })
    mdfes.value = response.data.data
    totalPaginas.value = response.data.pages
  } catch (error) {
    console.error('Erro ao carregar MDF-es:', error)
    alert('Erro ao carregar MDF-es')
  } finally {
    loading.value = false
  }
}

function limparFiltros() {
  filtros.value = {
    status: '',
    data_inicio: '',
    data_fim: ''
  }
  paginaAtual.value = 1
  carregarMDFes()
}

function paginaAnterior() {
  if (paginaAtual.value > 1) {
    paginaAtual.value--
    carregarMDFes()
  }
}

function proximaPagina() {
  if (paginaAtual.value < totalPaginas.value) {
    paginaAtual.value++
    carregarMDFes()
  }
}

function verDetalhes(mdfe) {
  router.push(`/fiscal/mdfe/${mdfe.ref}`)
}

async function downloadPDF(mdfe) {
  try {
    const response = await api.get(`/fiscal/mdfe/${mdfe.ref}/pdf`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `DAMDFE_${mdfe.numero}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar PDF:', error)
    alert('Erro ao baixar PDF')
  }
}

async function downloadXML(mdfe) {
  try {
    const response = await api.get(`/fiscal/mdfe/${mdfe.ref}/xml`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `MDFE_${mdfe.numero}.xml`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar XML:', error)
    alert('Erro ao baixar XML')
  }
}

function encerrarMDFe(mdfe) {
  mdfeParaEncerrar.value = mdfe
  dadosEncerramento.value = {
    uf: '',
    cidade_codigo: ''
  }
  showEncerrarModal.value = true
}

async function confirmarEncerramento() {
  try {
    await api.patch(`/fiscal/mdfe/${mdfeParaEncerrar.value.ref}/encerrar`, dadosEncerramento.value)
    alert('MDF-e encerrado com sucesso!')
    showEncerrarModal.value = false
    carregarMDFes()
  } catch (error) {
    console.error('Erro ao encerrar MDF-e:', error)
    alert(error.response?.data?.detail || 'Erro ao encerrar MDF-e')
  }
}

function cancelarMDFe(mdfe) {
  mdfeParaCancelar.value = mdfe
  motivoCancelamento.value = ''
  showCancelModal.value = true
}

async function confirmarCancelamento() {
  try {
    await api.delete(`/fiscal/mdfe/${mdfeParaCancelar.value.ref}`, {
      data: { justificativa: motivoCancelamento.value }
    })
    alert('MDF-e cancelado com sucesso!')
    showCancelModal.value = false
    carregarMDFes()
  } catch (error) {
    console.error('Erro ao cancelar MDF-e:', error)
    alert(error.response?.data?.detail || 'Erro ao cancelar MDF-e')
  }
}

function formatarChave(chave) {
  if (!chave) return '-'
  return chave.substring(0, 8) + '...' + chave.substring(chave.length - 8)
}

function formatarStatus(status) {
  const statusMap = {
    autorizado: 'Autorizado',
    encerrado: 'Encerrado',
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

onMounted(() => {
  carregarMDFes()
})
</script>

<style scoped>
.listar-mdfe-container {
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

.header-actions {
  display: flex;
  gap: 10px;
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

.mdfe-table {
  width: 100%;
  border-collapse: collapse;
}

.mdfe-table thead {
  background: #f8f9fa;
}

.mdfe-table th,
.mdfe-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.mdfe-table th {
  font-weight: 600;
  color: #495057;
  font-size: 14px;
}

.mdfe-table td {
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

.status-encerrado {
  background: #cce5ff;
  color: #004085;
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

.badge {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.percurso {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.uf-badge {
  background: #007bff;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.acoes {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  white-space: nowrap;
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

.btn-success {
  background: #28a745;
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

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #495057;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
