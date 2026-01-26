<template>
  <div class="emitir-mdfe-container">
    <div class="header">
      <h1>Emitir MDF-e</h1>
      <button @click="$router.push('/fiscal/mdfe')" class="btn btn-secondary">
        <i class="icon-arrow-left"></i> Voltar
      </button>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando CT-es disponíveis...</p>
    </div>

    <form v-else @submit.prevent="emitirMDFe" class="mdfe-form">
      <div class="section">
        <h2>1. Selecionar CT-es</h2>
        <p class="hint">Selecione os CT-es que serão incluídos neste MDF-e</p>
        
        <div v-if="ctesDisponiveis.length === 0" class="alert alert-warning">
          Nenhum CT-e autorizado disponível para vinculação ao MDF-e
        </div>
        
        <div v-else class="ctes-list">
          <div v-for="cte in ctesDisponiveis" :key="cte.id" class="cte-item">
            <label class="checkbox-container">
              <input 
                type="checkbox" 
                :value="cte.id" 
                v-model="ctesSelecionados"
                @change="atualizarTotalizadores"
              />
              <div class="cte-info">
                <div class="cte-header">
                  <strong>CT-e {{ cte.numero }}/{{ cte.serie }}</strong>
                  <span class="badge">{{ cte.chave?.substring(0, 8) }}...</span>
                </div>
                <div class="cte-details">
                  <span>{{ cte.remetente_nome }} → {{ cte.destinatario_nome }}</span>
                  <span>{{ cte.remetente_dados?.uf }} → {{ cte.destinatario_dados?.uf }}</span>
                  <span>R$ {{ formatarValor(cte.valor_total) }}</span>
                  <span>{{ cte.peso_kg }} kg</span>
                </div>
              </div>
            </label>
          </div>
        </div>

        <div v-if="ctesSelecionados.length > 0" class="totalizadores">
          <div class="total-item">
            <strong>Total de CT-es:</strong>
            <span>{{ ctesSelecionados.length }}</span>
          </div>
          <div class="total-item">
            <strong>Valor Total:</strong>
            <span>R$ {{ formatarValor(totalizadores.valor_total) }}</span>
          </div>
          <div class="total-item">
            <strong>Peso Total:</strong>
            <span>{{ totalizadores.peso_total }} kg</span>
          </div>
        </div>
      </div>

      <div class="section">
        <h2>2. Dados do MDF-e</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label>Número *</label>
            <input 
              type="number" 
              v-model.number="formData.numero" 
              class="form-control"
              placeholder="Deixe vazio para gerar automaticamente"
            />
          </div>

          <div class="form-group">
            <label>Série *</label>
            <input 
              type="text" 
              v-model="formData.serie" 
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label>Modal *</label>
            <select v-model="formData.modal" class="form-control" required>
              <option value="1">Rodoviário</option>
              <option value="2">Aéreo</option>
              <option value="3">Aquaviário</option>
              <option value="4">Ferroviário</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Percurso (UFs) *</label>
          <div class="percurso-selector">
            <div v-for="uf in ufs" :key="uf" class="uf-checkbox">
              <label>
                <input type="checkbox" :value="uf" v-model="formData.percurso" />
                {{ uf }}
              </label>
            </div>
          </div>
          <p class="hint">Selecione todas as UFs do percurso</p>
        </div>
      </div>

      <div class="section">
        <h2>3. Veículo</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label>Placa *</label>
            <input 
              type="text" 
              v-model="formData.veiculo.placa" 
              class="form-control"
              placeholder="ABC-1234"
              required
            />
          </div>

          <div class="form-group">
            <label>UF *</label>
            <select v-model="formData.veiculo.uf" class="form-control" required>
              <option value="">Selecione</option>
              <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
            </select>
          </div>

          <div class="form-group">
            <label>RENAVAM</label>
            <input 
              type="text" 
              v-model="formData.veiculo.renavam" 
              class="form-control"
              placeholder="Opcional"
            />
          </div>

          <div class="form-group">
            <label>Tipo *</label>
            <select v-model="formData.veiculo.tipo" class="form-control" required>
              <option value="01">Truck</option>
              <option value="02">Toco</option>
              <option value="03">Cavalo Mecânico</option>
              <option value="04">VAN</option>
              <option value="05">Utilitário</option>
              <option value="06">Outros</option>
            </select>
          </div>
        </div>
      </div>

      <div class="section">
        <h2>4. Condutores</h2>
        
        <div v-for="(condutor, index) in formData.condutores" :key="index" class="condutor-item">
          <div class="condutor-header">
            <h3>Condutor {{ index + 1 }}</h3>
            <button 
              v-if="formData.condutores.length > 1" 
              type="button" 
              @click="removerCondutor(index)" 
              class="btn btn-sm btn-danger"
            >
              <i class="icon-trash"></i> Remover
            </button>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input 
                type="text" 
                v-model="condutor.nome" 
                class="form-control"
                required
              />
            </div>

            <div class="form-group">
              <label>CPF *</label>
              <input 
                type="text" 
                v-model="condutor.cpf" 
                class="form-control"
                placeholder="000.000.000-00"
                required
              />
            </div>
          </div>
        </div>

        <button type="button" @click="adicionarCondutor" class="btn btn-secondary">
          <i class="icon-plus"></i> Adicionar Condutor
        </button>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="!isFormValid || emitindo" class="btn btn-primary btn-lg">
          <span v-if="emitindo">Emitindo MDF-e...</span>
          <span v-else>Emitir MDF-e</span>
        </button>
        <button type="button" @click="$router.push('/fiscal/mdfe')" class="btn btn-secondary btn-lg">
          Cancelar
        </button>
      </div>
    </form>

    <div v-if="showSuccessModal" class="modal">
      <div class="modal-content success">
        <div class="success-icon">✓</div>
        <h2>MDF-e Emitido com Sucesso!</h2>
        
        <div class="mdfe-info">
          <div class="info-item">
            <label>Número:</label>
            <strong>{{ mdfeEmitido.numero }}</strong>
          </div>
          <div class="info-item">
            <label>Série:</label>
            <strong>{{ mdfeEmitido.serie }}</strong>
          </div>
          <div class="info-item">
            <label>Chave:</label>
            <strong class="chave-completa">{{ mdfeEmitido.chave }}</strong>
          </div>
          <div class="info-item">
            <label>Protocolo:</label>
            <strong>{{ mdfeEmitido.protocolo }}</strong>
          </div>
        </div>

        <div class="success-actions">
          <button @click="downloadPDF" class="btn btn-primary">
            <i class="icon-download"></i> Baixar DAMDFE (PDF)
          </button>
          <button @click="downloadXML" class="btn btn-secondary">
            <i class="icon-download"></i> Baixar XML
          </button>
          <button @click="closeSuccessModal" class="btn btn-secondary">
            Fechar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const loading = ref(true)
const emitindo = ref(false)
const ctesDisponiveis = ref([])
const ctesSelecionados = ref([])
const showSuccessModal = ref(false)
const mdfeEmitido = ref(null)

const formData = ref({
  numero: null,
  serie: '1',
  modal: '1',
  percurso: [],
  veiculo: {
    placa: '',
    uf: '',
    renavam: '',
    tipo: '02'
  },
  condutores: [
    {
      nome: '',
      cpf: ''
    }
  ]
})

const totalizadores = ref({
  valor_total: 0,
  peso_total: 0
})

const ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

const isFormValid = computed(() => {
  return (
    ctesSelecionados.value.length > 0 &&
    formData.value.serie &&
    formData.value.percurso.length > 0 &&
    formData.value.veiculo.placa &&
    formData.value.veiculo.uf &&
    formData.value.condutores.length > 0 &&
    formData.value.condutores.every(c => c.nome && c.cpf)
  )
})

async function carregarCTesDisponiveis() {
  loading.value = true
  try {
    const response = await api.get('/fiscal/cte', {
      params: {
        status: 'autorizado',
        limit: 100
      }
    })
    
    ctesDisponiveis.value = response.data.data.filter(cte => !cte.mdfe_id)
  } catch (error) {
    console.error('Erro ao carregar CT-es:', error)
    alert('Erro ao carregar CT-es disponíveis')
  } finally {
    loading.value = false
  }
}

function atualizarTotalizadores() {
  const ctesSelecionadosObj = ctesDisponiveis.value.filter(
    cte => ctesSelecionados.value.includes(cte.id)
  )
  
  totalizadores.value.valor_total = ctesSelecionadosObj.reduce(
    (sum, cte) => sum + cte.valor_total, 0
  )
  totalizadores.value.peso_total = ctesSelecionadosObj.reduce(
    (sum, cte) => sum + cte.peso_kg, 0
  )

  const ufsPercurso = new Set()
  ctesSelecionadosObj.forEach(cte => {
    if (cte.remetente_dados?.uf) ufsPercurso.add(cte.remetente_dados.uf)
    if (cte.destinatario_dados?.uf) ufsPercurso.add(cte.destinatario_dados.uf)
  })
  
  formData.value.percurso = Array.from(ufsPercurso)
}

function adicionarCondutor() {
  formData.value.condutores.push({
    nome: '',
    cpf: ''
  })
}

function removerCondutor(index) {
  formData.value.condutores.splice(index, 1)
}

async function emitirMDFe() {
  if (!isFormValid.value) {
    alert('Por favor, preencha todos os campos obrigatórios')
    return
  }
  
  try {
    emitindo.value = true
    
    const ctesSelecionadosObj = ctesDisponiveis.value.filter(
      cte => ctesSelecionados.value.includes(cte.id)
    )
    
    const payload = {
      numero: formData.value.numero,
      serie: formData.value.serie,
      modal: formData.value.modal,
      percurso: formData.value.percurso,
      veiculo: formData.value.veiculo,
      condutores: formData.value.condutores,
      documentos: ctesSelecionadosObj.map(cte => ({
        chave: cte.chave,
        tipo: 'CTE'
      }))
    }
    
    const response = await api.post('/fiscal/mdfe/emitir', payload)
    
    mdfeEmitido.value = response.data.data
    showSuccessModal.value = true
  } catch (err) {
    console.error('Erro ao emitir MDF-e:', err)
    alert(err.response?.data?.detail || 'Erro ao emitir MDF-e')
  } finally {
    emitindo.value = false
  }
}

function downloadPDF() {
  if (mdfeEmitido.value.url_damdfe) {
    window.open(mdfeEmitido.value.url_damdfe, '_blank')
  }
}

function downloadXML() {
  if (mdfeEmitido.value.xml) {
    window.open(mdfeEmitido.value.xml, '_blank')
  }
}

function closeSuccessModal() {
  showSuccessModal.value = false
  router.push('/fiscal/mdfe')
}

function formatarValor(valor) {
  if (!valor) return '0,00'
  return valor.toFixed(2).replace('.', ',')
}

onMounted(() => {
  carregarCTesDisponiveis()
})
</script>

<style scoped>
.emitir-mdfe-container {
  padding: 20px;
  max-width: 1200px;
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

.mdfe-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section {
  padding: 30px;
  border-bottom: 1px solid #e9ecef;
}

.section:last-child {
  border-bottom: none;
}

.section h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
}

.hint {
  color: #6c757d;
  font-size: 14px;
  margin-bottom: 15px;
}

.alert {
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.alert-warning {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.ctes-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.cte-item {
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 15px;
  transition: all 0.2s;
}

.cte-item:hover {
  background: #f8f9fa;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
}

.checkbox-container input[type="checkbox"] {
  margin-top: 4px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.cte-info {
  flex: 1;
}

.cte-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.cte-details {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #6c757d;
}

.badge {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-family: monospace;
}

.totalizadores {
  background: #e7f3ff;
  padding: 15px;
  border-radius: 6px;
  display: flex;
  gap: 30px;
}

.total-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.total-item strong {
  font-size: 12px;
  color: #6c757d;
}

.total-item span {
  font-size: 18px;
  font-weight: 600;
  color: #007bff;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.form-control {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #007bff;
}

.percurso-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 10px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
}

.uf-checkbox label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  cursor: pointer;
}

.condutor-item {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 15px;
}

.condutor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.condutor-header h3 {
  font-size: 16px;
  color: #495057;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding: 30px;
  background: #f8f9fa;
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

.btn-lg {
  padding: 12px 32px;
  font-size: 16px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  padding: 40px;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  text-align: center;
}

.modal-content.success {
  border-top: 4px solid #28a745;
}

.success-icon {
  width: 80px;
  height: 80px;
  background: #28a745;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  margin: 0 auto 20px;
}

.modal-content h2 {
  color: #333;
  margin-bottom: 30px;
}

.mdfe-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  text-align: left;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #dee2e6;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item label {
  color: #6c757d;
  font-size: 14px;
}

.info-item strong {
  color: #333;
  font-size: 14px;
}

.chave-completa {
  font-family: monospace;
  font-size: 11px;
  word-break: break-all;
}

.success-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
