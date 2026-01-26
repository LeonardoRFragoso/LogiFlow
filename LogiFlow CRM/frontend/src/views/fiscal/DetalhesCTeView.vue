<template>
  <div class="detalhes-cte-container">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando detalhes...</p>
    </div>

    <div v-else-if="cte" class="detalhes-content">
      <div class="header">
        <div class="header-left">
          <h1>CT-e {{ cte.numero }}/{{ cte.serie }}</h1>
          <span :class="['status-badge', `status-${cte.status}`]">
            {{ formatarStatus(cte.status) }}
          </span>
        </div>
        <div class="header-actions">
          <button @click="downloadPDF" class="btn btn-primary">
            <i class="icon-download"></i> Baixar PDF
          </button>
          <button @click="downloadXML" class="btn btn-secondary">
            <i class="icon-download"></i> Baixar XML
          </button>
          <button @click="$router.push('/fiscal/cte')" class="btn btn-secondary">
            <i class="icon-arrow-left"></i> Voltar
          </button>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-card">
          <h2>Informações Gerais</h2>
          <div class="info-row">
            <label>Número:</label>
            <span>{{ cte.numero }}</span>
          </div>
          <div class="info-row">
            <label>Série:</label>
            <span>{{ cte.serie }}</span>
          </div>
          <div class="info-row">
            <label>Chave de Acesso:</label>
            <span class="chave">{{ cte.chave || '-' }}</span>
          </div>
          <div class="info-row">
            <label>Protocolo:</label>
            <span>{{ cte.protocolo || '-' }}</span>
          </div>
          <div class="info-row">
            <label>Data de Emissão:</label>
            <span>{{ formatarDataHora(cte.data_emissao) }}</span>
          </div>
          <div class="info-row">
            <label>Data de Autorização:</label>
            <span>{{ formatarDataHora(cte.data_autorizacao) }}</span>
          </div>
          <div class="info-row">
            <label>Modal:</label>
            <span>{{ formatarModal(cte.modal) }}</span>
          </div>
          <div class="info-row">
            <label>Natureza da Operação:</label>
            <span>{{ cte.natureza_operacao }}</span>
          </div>
        </div>

        <div class="info-card">
          <h2>Valores</h2>
          <div class="info-row">
            <label>Valor Total:</label>
            <span class="valor-destaque">{{ formatarValor(cte.valor_total) }}</span>
          </div>
          <div class="info-row">
            <label>Valor a Receber:</label>
            <span>{{ formatarValor(cte.valor_receber) }}</span>
          </div>
          <div class="info-row">
            <label>Valor da Carga:</label>
            <span>{{ formatarValor(cte.valor_carga) }}</span>
          </div>
          <div class="info-row">
            <label>Peso (kg):</label>
            <span>{{ cte.peso_kg }}</span>
          </div>
          <div class="info-row">
            <label>ICMS Situação:</label>
            <span>{{ cte.icms_situacao }}</span>
          </div>
          <div class="info-row">
            <label>ICMS Alíquota:</label>
            <span>{{ cte.icms_aliquota }}%</span>
          </div>
          <div class="info-row">
            <label>ICMS Valor:</label>
            <span>{{ formatarValor(cte.icms_valor) }}</span>
          </div>
        </div>

        <div class="info-card">
          <h2>Tomador do Serviço</h2>
          <div class="info-row">
            <label>Tipo:</label>
            <span>{{ formatarTomador(cte.tomador_tipo) }}</span>
          </div>
          <div class="info-row">
            <label>CNPJ/CPF:</label>
            <span>{{ cte.tomador_cnpj }}</span>
          </div>
          <div class="info-row">
            <label>Nome:</label>
            <span>{{ cte.tomador_nome }}</span>
          </div>
          <div v-if="cte.tomador_dados" class="endereco">
            <p>{{ cte.tomador_dados.endereco }}, {{ cte.tomador_dados.numero }}</p>
            <p>{{ cte.tomador_dados.bairro }} - {{ cte.tomador_dados.cidade }}/{{ cte.tomador_dados.uf }}</p>
            <p>CEP: {{ cte.tomador_dados.cep }}</p>
          </div>
        </div>

        <div class="info-card">
          <h2>Remetente</h2>
          <div class="info-row">
            <label>CNPJ/CPF:</label>
            <span>{{ cte.remetente_cnpj }}</span>
          </div>
          <div class="info-row">
            <label>Nome:</label>
            <span>{{ cte.remetente_nome }}</span>
          </div>
          <div v-if="cte.remetente_dados" class="endereco">
            <p>{{ cte.remetente_dados.endereco }}, {{ cte.remetente_dados.numero }}</p>
            <p>{{ cte.remetente_dados.bairro }} - {{ cte.remetente_dados.cidade }}/{{ cte.remetente_dados.uf }}</p>
            <p>CEP: {{ cte.remetente_dados.cep }}</p>
          </div>
        </div>

        <div class="info-card">
          <h2>Destinatário</h2>
          <div class="info-row">
            <label>CNPJ/CPF:</label>
            <span>{{ cte.destinatario_cnpj }}</span>
          </div>
          <div class="info-row">
            <label>Nome:</label>
            <span>{{ cte.destinatario_nome }}</span>
          </div>
          <div v-if="cte.destinatario_dados" class="endereco">
            <p>{{ cte.destinatario_dados.endereco }}, {{ cte.destinatario_dados.numero }}</p>
            <p>{{ cte.destinatario_dados.bairro }} - {{ cte.destinatario_dados.cidade }}/{{ cte.destinatario_dados.uf }}</p>
            <p>CEP: {{ cte.destinatario_dados.cep }}</p>
          </div>
        </div>

        <div class="info-card">
          <h2>Veículo</h2>
          <div class="info-row">
            <label>Placa:</label>
            <span>{{ cte.veiculo_placa }}</span>
          </div>
          <div class="info-row">
            <label>UF:</label>
            <span>{{ cte.veiculo_uf }}</span>
          </div>
          <div v-if="cte.veiculo_dados">
            <div class="info-row" v-if="cte.veiculo_dados.renavam">
              <label>RENAVAM:</label>
              <span>{{ cte.veiculo_dados.renavam }}</span>
            </div>
            <div class="info-row" v-if="cte.veiculo_dados.tipo">
              <label>Tipo:</label>
              <span>{{ formatarTipoVeiculo(cte.veiculo_dados.tipo) }}</span>
            </div>
          </div>
          <div class="info-row" v-if="cte.rntrc">
            <label>RNTRC:</label>
            <span>{{ cte.rntrc }}</span>
          </div>
          <div class="info-row" v-if="cte.ciot">
            <label>CIOT:</label>
            <span>{{ cte.ciot }}</span>
          </div>
        </div>
      </div>

      <div v-if="cte.status === 'cancelado' && cte.motivo_cancelamento" class="alert alert-danger">
        <h3>Motivo do Cancelamento</h3>
        <p>{{ cte.motivo_cancelamento }}</p>
        <p class="data">Cancelado em: {{ formatarDataHora(cte.data_cancelamento) }}</p>
      </div>

      <div v-if="cte.status === 'rejeitado' && cte.mensagem_erro" class="alert alert-danger">
        <h3>Motivo da Rejeição</h3>
        <p>{{ cte.mensagem_erro }}</p>
      </div>

      <div v-if="cte.mdfe_id" class="alert alert-info">
        <h3>MDF-e Vinculado</h3>
        <p>Este CT-e está vinculado a um MDF-e</p>
        <button @click="$router.push(`/fiscal/mdfe/${cte.mdfe_id}`)" class="btn btn-sm btn-info">
          Ver MDF-e
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const cte = ref(null)

async function carregarDetalhes() {
  loading.value = true
  try {
    const response = await api.get(`/fiscal/cte/${route.params.ref}`)
    cte.value = response.data
  } catch (error) {
    console.error('Erro ao carregar CT-e:', error)
    alert('Erro ao carregar detalhes do CT-e')
    router.push('/fiscal/cte')
  } finally {
    loading.value = false
  }
}

async function downloadPDF() {
  try {
    const response = await api.get(`/fiscal/cte/${route.params.ref}/pdf`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `DACTE_${cte.value.numero}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar PDF:', error)
    alert('Erro ao baixar PDF')
  }
}

async function downloadXML() {
  try {
    const response = await api.get(`/fiscal/cte/${route.params.ref}/xml`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `CTE_${cte.value.numero}.xml`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar XML:', error)
    alert('Erro ao baixar XML')
  }
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

function formatarModal(modal) {
  const modalMap = {
    '01': 'Rodoviário',
    '02': 'Aéreo',
    '03': 'Aquaviário',
    '04': 'Ferroviário',
    '05': 'Dutoviário',
    '06': 'Multimodal'
  }
  return modalMap[modal] || modal
}

function formatarTomador(tipo) {
  const tipoMap = {
    '0': 'Remetente',
    '1': 'Expedidor',
    '2': 'Recebedor',
    '3': 'Destinatário',
    '4': 'Outros'
  }
  return tipoMap[tipo] || tipo
}

function formatarTipoVeiculo(tipo) {
  const tipoMap = {
    '01': 'Truck',
    '02': 'Toco',
    '03': 'Cavalo Mecânico',
    '04': 'VAN',
    '05': 'Utilitário',
    '06': 'Outros'
  }
  return tipoMap[tipo] || tipo
}

function formatarDataHora(data) {
  if (!data) return '-'
  return new Date(data).toLocaleString('pt-BR')
}

function formatarValor(valor) {
  if (!valor) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor)
}

onMounted(() => {
  carregarDetalhes()
})
</script>

<style scoped>
.detalhes-cte-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
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

.detalhes-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header h1 {
  font-size: 28px;
  color: #333;
  margin: 0;
}

.status-badge {
  padding: 6px 16px;
  border-radius: 16px;
  font-size: 14px;
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

.header-actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  white-space: nowrap;
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

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
}

.btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  padding: 30px;
}

.info-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.info-card h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #007bff;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row label {
  font-weight: 600;
  color: #6c757d;
  font-size: 14px;
}

.info-row span {
  color: #333;
  font-size: 14px;
  text-align: right;
}

.chave {
  font-family: monospace;
  font-size: 11px;
  word-break: break-all;
}

.valor-destaque {
  font-size: 18px !important;
  font-weight: 700 !important;
  color: #007bff !important;
}

.endereco {
  margin-top: 10px;
  padding: 15px;
  background: white;
  border-radius: 4px;
}

.endereco p {
  margin: 5px 0;
  font-size: 14px;
  color: #495057;
}

.alert {
  margin: 0 30px 30px;
  padding: 20px;
  border-radius: 8px;
}

.alert h3 {
  font-size: 16px;
  margin-bottom: 10px;
}

.alert p {
  margin: 5px 0;
  font-size: 14px;
}

.alert.alert-danger {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert.alert-info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.data {
  font-size: 12px;
  color: #6c757d;
  margin-top: 10px;
}
</style>
