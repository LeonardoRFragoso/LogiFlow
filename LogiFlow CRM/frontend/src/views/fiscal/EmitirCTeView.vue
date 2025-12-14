<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">📄 Emissão de CT-e</h1>
        <p class="page-subtitle">Conhecimento de Transporte Eletrônico</p>
      </div>
      <button @click="voltarPedidos" class="btn-secondary">
        ← Voltar para Pedidos
      </button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando dados do pedido...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <span class="error-icon">⚠️</span>
      <h3>Erro ao carregar pedido</h3>
      <p>{{ error }}</p>
      <button @click="voltarPedidos" class="btn-primary">Voltar</button>
    </div>

    <div v-else class="cte-form-container">
      <div class="form-sections">
        <!-- Informações do Pedido -->
        <div class="form-section">
          <div class="section-header">
            <h2>📦 Informações do Pedido</h2>
            <span v-if="pedido.cte_numero" class="cte-badge">CT-e: {{ pedido.cte_numero }}</span>
          </div>
          <div class="info-grid">
            <div class="info-item">
              <label>Número do Pedido</label>
              <span class="mono-text">{{ pedido.numero }}</span>
            </div>
            <div class="info-item">
              <label>Cliente</label>
              <span>{{ pedido.cliente_nome }}</span>
            </div>
            <div class="info-item">
              <label>Valor Total</label>
              <span class="value-text">R$ {{ formatMoney(pedido.valor_total) }}</span>
            </div>
            <div class="info-item">
              <label>Peso</label>
              <span>{{ pedido.peso_kg }} kg</span>
            </div>
          </div>
        </div>

        <!-- Dados do Tomador -->
        <div class="form-section">
          <div class="section-header">
            <h2>👤 Tomador do Serviço</h2>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>Tipo de Tomador *</label>
              <select v-model="formData.tomador.tipo" required>
                <option value="0">Remetente</option>
                <option value="1">Expedidor</option>
                <option value="2">Recebedor</option>
                <option value="3">Destinatário</option>
                <option value="4">Outros</option>
              </select>
            </div>
            <div class="form-group">
              <label>CNPJ/CPF *</label>
              <input v-model="formData.tomador.documento" type="text" placeholder="00.000.000/0000-00" required />
            </div>
            <div class="form-group">
              <label>Razão Social/Nome *</label>
              <input v-model="formData.tomador.nome" type="text" placeholder="Nome do tomador" required />
            </div>
            <div class="form-group">
              <label>Inscrição Estadual</label>
              <input v-model="formData.tomador.ie" type="text" placeholder="000.000.000.000" />
            </div>
            <div class="form-group full-width">
              <label>Endereço *</label>
              <input v-model="formData.tomador.endereco" type="text" placeholder="Rua, Avenida..." required />
            </div>
            <div class="form-group">
              <label>Número *</label>
              <input v-model="formData.tomador.numero" type="text" placeholder="123" required />
            </div>
            <div class="form-group">
              <label>Complemento</label>
              <input v-model="formData.tomador.complemento" type="text" placeholder="Apto, Sala..." />
            </div>
            <div class="form-group">
              <label>Bairro *</label>
              <input v-model="formData.tomador.bairro" type="text" placeholder="Centro" required />
            </div>
            <div class="form-group">
              <label>Cidade *</label>
              <input v-model="formData.tomador.cidade" type="text" placeholder="São Paulo" required />
            </div>
            <div class="form-group">
              <label>UF *</label>
              <select v-model="formData.tomador.uf" required>
                <option value="">Selecione</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>CEP *</label>
              <input v-model="formData.tomador.cep" type="text" placeholder="00000-000" required />
            </div>
            <div class="form-group">
              <label>Telefone</label>
              <input v-model="formData.tomador.telefone" type="text" placeholder="(11) 3333-4444" />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="formData.tomador.email" type="email" placeholder="contato@empresa.com.br" />
            </div>
          </div>
        </div>

        <!-- Dados do Remetente -->
        <div class="form-section">
          <div class="section-header">
            <h2>📤 Remetente</h2>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>CNPJ/CPF *</label>
              <input v-model="formData.remetente.documento" type="text" placeholder="00.000.000/0000-00" required />
            </div>
            <div class="form-group">
              <label>Razão Social/Nome *</label>
              <input v-model="formData.remetente.nome" type="text" placeholder="Nome do remetente" required />
            </div>
            <div class="form-group">
              <label>Inscrição Estadual</label>
              <input v-model="formData.remetente.ie" type="text" placeholder="000.000.000.000" />
            </div>
            <div class="form-group full-width">
              <label>Endereço *</label>
              <input v-model="formData.remetente.endereco" type="text" placeholder="Rua, Avenida..." required />
            </div>
            <div class="form-group">
              <label>Número *</label>
              <input v-model="formData.remetente.numero" type="text" placeholder="123" required />
            </div>
            <div class="form-group">
              <label>Bairro *</label>
              <input v-model="formData.remetente.bairro" type="text" placeholder="Centro" required />
            </div>
            <div class="form-group">
              <label>Cidade *</label>
              <input v-model="formData.remetente.cidade" type="text" placeholder="São Paulo" required />
            </div>
            <div class="form-group">
              <label>UF *</label>
              <select v-model="formData.remetente.uf" required>
                <option value="">Selecione</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>CEP *</label>
              <input v-model="formData.remetente.cep" type="text" placeholder="00000-000" required />
            </div>
          </div>
        </div>

        <!-- Dados do Destinatário -->
        <div class="form-section">
          <div class="section-header">
            <h2>📥 Destinatário</h2>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>CNPJ/CPF *</label>
              <input v-model="formData.destinatario.documento" type="text" placeholder="00.000.000/0000-00" required />
            </div>
            <div class="form-group">
              <label>Razão Social/Nome *</label>
              <input v-model="formData.destinatario.nome" type="text" placeholder="Nome do destinatário" required />
            </div>
            <div class="form-group">
              <label>Inscrição Estadual</label>
              <input v-model="formData.destinatario.ie" type="text" placeholder="000.000.000.000" />
            </div>
            <div class="form-group full-width">
              <label>Endereço *</label>
              <input v-model="formData.destinatario.endereco" type="text" placeholder="Rua, Avenida..." required />
            </div>
            <div class="form-group">
              <label>Número *</label>
              <input v-model="formData.destinatario.numero" type="text" placeholder="123" required />
            </div>
            <div class="form-group">
              <label>Bairro *</label>
              <input v-model="formData.destinatario.bairro" type="text" placeholder="Centro" required />
            </div>
            <div class="form-group">
              <label>Cidade *</label>
              <input v-model="formData.destinatario.cidade" type="text" placeholder="São Paulo" required />
            </div>
            <div class="form-group">
              <label>UF *</label>
              <select v-model="formData.destinatario.uf" required>
                <option value="">Selecione</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>CEP *</label>
              <input v-model="formData.destinatario.cep" type="text" placeholder="00000-000" required />
            </div>
          </div>
        </div>

        <!-- Valores e Carga -->
        <div class="form-section">
          <div class="section-header">
            <h2>💰 Valores e Carga</h2>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>Valor Total do Serviço *</label>
              <input v-model="formData.valores.valor_total" type="number" step="0.01" placeholder="0.00" required />
            </div>
            <div class="form-group">
              <label>Valor a Receber *</label>
              <input v-model="formData.valores.valor_receber" type="number" step="0.01" placeholder="0.00" required />
            </div>
            <div class="form-group">
              <label>Valor da Carga</label>
              <input v-model="formData.valores.valor_carga" type="number" step="0.01" placeholder="0.00" />
            </div>
            <div class="form-group">
              <label>Peso (kg) *</label>
              <input v-model="formData.valores.peso_kg" type="number" step="0.01" placeholder="0.00" required />
            </div>
            <div class="form-group full-width">
              <label>Produto Predominante</label>
              <input v-model="formData.valores.produto_predominante" type="text" placeholder="MERCADORIA" />
            </div>
          </div>
        </div>

        <!-- Dados do Veículo -->
        <div class="form-section">
          <div class="section-header">
            <h2>🚚 Veículo</h2>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>Placa *</label>
              <input v-model="formData.veiculo.placa" type="text" placeholder="ABC-1234" required />
            </div>
            <div class="form-group">
              <label>UF *</label>
              <select v-model="formData.veiculo.uf" required>
                <option value="">Selecione</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>RENAVAM</label>
              <input v-model="formData.veiculo.renavam" type="text" placeholder="00000000000" />
            </div>
            <div class="form-group">
              <label>Tipo de Veículo</label>
              <select v-model="formData.veiculo.tipo">
                <option value="02">Caminhão</option>
                <option value="03">Caminhão Trator</option>
                <option value="04">Carreta</option>
                <option value="05">Semi-reboque</option>
                <option value="06">Van</option>
              </select>
            </div>
            <div class="form-group">
              <label>RNTRC</label>
              <input v-model="formData.rntrc" type="text" placeholder="00000000" />
            </div>
            <div class="form-group">
              <label>CIOT</label>
              <input v-model="formData.ciot" type="text" placeholder="000000000000" />
            </div>
          </div>
        </div>

        <!-- Dados Fiscais -->
        <div class="form-section">
          <div class="section-header">
            <h2>📋 Dados Fiscais</h2>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>Natureza da Operação *</label>
              <input v-model="formData.natureza_operacao" type="text" placeholder="PRESTACAO DE SERVICO DE TRANSPORTE" required />
            </div>
            <div class="form-group">
              <label>Série *</label>
              <input v-model="formData.serie" type="text" placeholder="1" required />
            </div>
            <div class="form-group">
              <label>Modal</label>
              <select v-model="formData.modal">
                <option value="01">Rodoviário</option>
                <option value="02">Aéreo</option>
                <option value="03">Aquaviário</option>
                <option value="04">Ferroviário</option>
                <option value="05">Dutoviário</option>
              </select>
            </div>
            <div class="form-group">
              <label>Situação Tributária ICMS</label>
              <select v-model="formData.icms_situacao">
                <option value="00">Tributação Normal</option>
                <option value="20">Com Redução de Base de Cálculo</option>
                <option value="40">Isenta</option>
                <option value="41">Não Tributada</option>
                <option value="51">Diferimento</option>
                <option value="90">Outros</option>
              </select>
            </div>
            <div class="form-group">
              <label>Alíquota ICMS (%)</label>
              <input v-model="formData.icms_aliquota" type="number" step="0.01" placeholder="0.00" />
            </div>
            <div class="form-group">
              <label>Valor ICMS</label>
              <input v-model="formData.icms_valor" type="number" step="0.01" placeholder="0.00" />
            </div>
          </div>
        </div>
      </div>

      <!-- Botões de Ação -->
      <div class="form-actions">
        <button @click="voltarPedidos" class="btn-secondary" :disabled="emitindo">
          Cancelar
        </button>
        <button @click="emitirCTe" class="btn-primary" :disabled="emitindo || !isFormValid">
          <span v-if="emitindo" class="spinner-small"></span>
          {{ emitindo ? 'Emitindo CT-e...' : '📄 Emitir CT-e' }}
        </button>
      </div>

      <!-- Modal de Sucesso -->
      <div v-if="showSuccessModal" class="modal-overlay" @click="closeSuccessModal">
        <div class="modal-content success-modal" @click.stop>
          <div class="success-icon">✅</div>
          <h2>CT-e Emitido com Sucesso!</h2>
          <div class="cte-info">
            <div class="info-row">
              <span class="label">Número:</span>
              <span class="value">{{ cteEmitido.numero }}</span>
            </div>
            <div class="info-row">
              <span class="label">Chave:</span>
              <span class="value mono-text">{{ cteEmitido.chave }}</span>
            </div>
            <div class="info-row">
              <span class="label">Protocolo:</span>
              <span class="value">{{ cteEmitido.protocolo }}</span>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="downloadPDF" class="btn-primary">📄 Download PDF</button>
            <button @click="downloadXML" class="btn-secondary">📋 Download XML</button>
            <button @click="closeSuccessModal" class="btn-secondary">Fechar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const pedidoId = route.params.id
const loading = ref(true)
const error = ref(null)
const emitindo = ref(false)
const showSuccessModal = ref(false)
const pedido = ref({})
const cteEmitido = ref({})

const ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

const formData = ref({
  tomador: {
    tipo: '3',
    documento: '',
    nome: '',
    ie: '',
    endereco: '',
    numero: '',
    complemento: '',
    bairro: '',
    cidade: '',
    uf: '',
    cep: '',
    telefone: '',
    email: ''
  },
  remetente: {
    documento: '',
    nome: '',
    ie: '',
    endereco: '',
    numero: '',
    bairro: '',
    cidade: '',
    uf: '',
    cep: ''
  },
  destinatario: {
    documento: '',
    nome: '',
    ie: '',
    endereco: '',
    numero: '',
    bairro: '',
    cidade: '',
    uf: '',
    cep: ''
  },
  valores: {
    valor_total: 0,
    valor_receber: 0,
    valor_carga: 0,
    peso_kg: 0,
    produto_predominante: 'MERCADORIA'
  },
  veiculo: {
    placa: '',
    uf: '',
    renavam: '',
    tipo: '02'
  },
  natureza_operacao: 'PRESTACAO DE SERVICO DE TRANSPORTE',
  serie: '1',
  modal: '01',
  rntrc: '',
  ciot: '',
  icms_situacao: '00',
  icms_aliquota: '0.00',
  icms_valor: '0.00'
})

const isFormValid = computed(() => {
  return formData.value.tomador.documento &&
         formData.value.tomador.nome &&
         formData.value.remetente.documento &&
         formData.value.remetente.nome &&
         formData.value.destinatario.documento &&
         formData.value.destinatario.nome &&
         formData.value.valores.valor_total > 0 &&
         formData.value.valores.peso_kg > 0 &&
         formData.value.veiculo.placa
})

async function fetchPedido() {
  try {
    loading.value = true
    const response = await api.get(`/pedidos/${pedidoId}`)
    pedido.value = response.data
    
    preencherDadosPedido()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao carregar pedido'
  } finally {
    loading.value = false
  }
}

function preencherDadosPedido() {
  formData.value.valores.valor_total = pedido.value.valor_total || 0
  formData.value.valores.valor_receber = pedido.value.valor_total || 0
  formData.value.valores.valor_carga = pedido.value.valor_mercadoria || 0
  formData.value.valores.peso_kg = pedido.value.peso_kg || 0
  
  if (pedido.value.veiculo_placa) {
    formData.value.veiculo.placa = pedido.value.veiculo_placa
  }
  
  if (pedido.value.origem) {
    formData.value.remetente.endereco = pedido.value.origem.endereco || ''
    formData.value.remetente.cidade = pedido.value.origem.cidade || ''
    formData.value.remetente.uf = pedido.value.origem.uf || ''
    formData.value.remetente.cep = pedido.value.origem.cep || ''
  }
  
  if (pedido.value.destino) {
    formData.value.destinatario.endereco = pedido.value.destino.endereco || ''
    formData.value.destinatario.cidade = pedido.value.destino.cidade || ''
    formData.value.destinatario.uf = pedido.value.destino.uf || ''
    formData.value.destinatario.cep = pedido.value.destino.cep || ''
  }
}

async function emitirCTe() {
  if (!isFormValid.value) {
    alert('Por favor, preencha todos os campos obrigatórios')
    return
  }
  
  try {
    emitindo.value = true
    const response = await api.post('/fiscal/cte/emitir', {
      pedido_id: pedidoId,
      ...formData.value
    })
    
    cteEmitido.value = response.data
    showSuccessModal.value = true
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao emitir CT-e')
  } finally {
    emitindo.value = false
  }
}

function downloadPDF() {
  if (cteEmitido.value.url_danfe) {
    window.open(cteEmitido.value.url_danfe, '_blank')
  }
}

function downloadXML() {
  if (cteEmitido.value.xml) {
    window.open(cteEmitido.value.xml, '_blank')
  }
}

function closeSuccessModal() {
  showSuccessModal.value = false
  voltarPedidos()
}

function voltarPedidos() {
  router.push('/pedidos')
}

function formatMoney(value) {
  return new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2 }).format(value || 0)
}

onMounted(() => {
  fetchPedido()
})
</script>

<style scoped>
.page-container {
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

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.page-subtitle {
  color: #666;
  margin: 0.5rem 0 0 0;
}

.loading-state, .error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.cte-form-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-sections {
  padding: 2rem;
}

.form-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-section:last-child {
  border-bottom: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.cte-badge {
  background: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item label {
  display: block;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.info-item span {
  display: block;
  font-size: 1rem;
  color: #1a1a1a;
  font-weight: 500;
}

.mono-text {
  font-family: 'Courier New', monospace;
  background: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.value-text {
  color: #10b981;
  font-weight: 600;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
  border-radius: 0 0 12px 12px;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.success-modal {
  text-align: center;
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.success-modal h2 {
  color: #10b981;
  margin-bottom: 1.5rem;
}

.cte-info {
  background: #f3f4f6;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row .label {
  font-weight: 600;
  color: #666;
}

.info-row .value {
  color: #1a1a1a;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
</style>
