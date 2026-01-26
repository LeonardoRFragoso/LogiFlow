<template>
  <div class="detalhes-mdfe-container">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando detalhes...</p>
    </div>

    <div v-else-if="mdfe" class="detalhes-content">
      <div class="header">
        <div class="header-left">
          <h1>MDF-e {{ mdfe.numero }}/{{ mdfe.serie }}</h1>
          <span :class="['status-badge', `status-${mdfe.status}`]">
            {{ formatarStatus(mdfe.status) }}
          </span>
        </div>
        <div class="header-actions">
          <button @click="downloadPDF" class="btn btn-primary">
            <i class="icon-download"></i> Baixar PDF
          </button>
          <button @click="downloadXML" class="btn btn-secondary">
            <i class="icon-download"></i> Baixar XML
          </button>
          <button @click="$router.push('/fiscal/mdfe')" class="btn btn-secondary">
            <i class="icon-arrow-left"></i> Voltar
          </button>
        </div>
      </div>

      <div class="info-grid">
        <div class="info-card">
          <h2>Informações Gerais</h2>
          <div class="info-row">
            <label>Número:</label>
            <span>{{ mdfe.numero }}</span>
          </div>
          <div class="info-row">
            <label>Série:</label>
            <span>{{ mdfe.serie }}</span>
          </div>
          <div class="info-row">
            <label>Chave de Acesso:</label>
            <span class="chave">{{ mdfe.chave || '-' }}</span>
          </div>
          <div class="info-row">
            <label>Protocolo:</label>
            <span>{{ mdfe.protocolo || '-' }}</span>
          </div>
          <div class="info-row">
            <label>Data de Emissão:</label>
            <span>{{ formatarDataHora(mdfe.data_emissao) }}</span>
          </div>
          <div class="info-row">
            <label>Data de Autorização:</label>
            <span>{{ formatarDataHora(mdfe.data_autorizacao) }}</span>
          </div>
          <div class="info-row" v-if="mdfe.data_encerramento">
            <label>Data de Encerramento:</label>
            <span>{{ formatarDataHora(mdfe.data_encerramento) }}</span>
          </div>
          <div class="info-row">
            <label>Modal:</label>
            <span>{{ formatarModal(mdfe.modal) }}</span>
          </div>
        </div>

        <div class="info-card">
          <h2>Totalizadores</h2>
          <div class="info-row">
            <label>Quantidade de CT-es:</label>
            <span class="valor-destaque">{{ mdfe.quantidade_ctes }}</span>
          </div>
          <div class="info-row">
            <label>Valor Total da Carga:</label>
            <span class="valor-destaque">{{ formatarValor(mdfe.valor_total_carga) }}</span>
          </div>
          <div class="info-row">
            <label>Peso Total (kg):</label>
            <span>{{ mdfe.peso_total_kg }}</span>
          </div>
        </div>

        <div class="info-card">
          <h2>Percurso</h2>
          <div class="percurso-list">
            <span v-for="uf in mdfe.percurso" :key="uf" class="uf-badge">{{ uf }}</span>
          </div>
          <div v-if="mdfe.uf_carregamento" class="info-row">
            <label>UF Carregamento:</label>
            <span>{{ mdfe.uf_carregamento }}</span>
          </div>
          <div v-if="mdfe.cidade_carregamento" class="info-row">
            <label>Cidade Carregamento:</label>
            <span>{{ mdfe.cidade_carregamento }}</span>
          </div>
          <div v-if="mdfe.uf_descarregamento" class="info-row">
            <label>UF Descarregamento:</label>
            <span>{{ mdfe.uf_descarregamento }}</span>
          </div>
          <div v-if="mdfe.cidade_descarregamento" class="info-row">
            <label>Cidade Descarregamento:</label>
            <span>{{ mdfe.cidade_descarregamento }}</span>
          </div>
        </div>

        <div class="info-card">
          <h2>Veículo</h2>
          <div class="info-row">
            <label>Placa:</label>
            <span>{{ mdfe.veiculo_placa }}</span>
          </div>
          <div class="info-row">
            <label>UF:</label>
            <span>{{ mdfe.veiculo_uf }}</span>
          </div>
          <div v-if="mdfe.veiculo_dados">
            <div class="info-row" v-if="mdfe.veiculo_dados.renavam">
              <label>RENAVAM:</label>
              <span>{{ mdfe.veiculo_dados.renavam }}</span>
            </div>
            <div class="info-row" v-if="mdfe.veiculo_dados.tipo">
              <label>Tipo:</label>
              <span>{{ formatarTipoVeiculo(mdfe.veiculo_dados.tipo) }}</span>
            </div>
          </div>
        </div>

        <div class="info-card full-width">
          <h2>Condutores</h2>
          <div v-for="(condutor, index) in mdfe.condutores" :key="index" class="condutor-item">
            <div class="info-row">
              <label>Nome:</label>
              <span>{{ condutor.nome }}</span>
            </div>
            <div class="info-row">
              <label>CPF:</label>
              <span>{{ condutor.cpf }}</span>
            </div>
          </div>
        </div>

        <div class="info-card full-width">
          <h2>CT-es Vinculados ({{ mdfe.quantidade_ctes }})</h2>
          <div class="ctes-list">
            <div v-for="(doc, index) in mdfe.documentos" :key="index" class="cte-item">
              <span class="cte-numero">CT-e {{ index + 1 }}</span>
              <span class="cte-chave">{{ doc.chave }}</span>
              <button @click="verCTe(doc.chave)" class="btn btn-sm btn-info">Ver Detalhes</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="mdfe.status === 'cancelado' && mdfe.motivo_cancelamento" class="alert alert-danger">
        <h3>Motivo do Cancelamento</h3>
        <p>{{ mdfe.motivo_cancelamento }}</p>
        <p class="data">Cancelado em: {{ formatarDataHora(mdfe.data_cancelamento) }}</p>
      </div>

      <div v-if="mdfe.status === 'rejeitado' && mdfe.mensagem_erro" class="alert alert-danger">
        <h3>Motivo da Rejeição</h3>
        <p>{{ mdfe.mensagem_erro }}</p>
      </div>

      <div v-if="mdfe.status === 'encerrado'" class="alert alert-success">
        <h3>MDF-e Encerrado</h3>
        <p>Este MDF-e foi encerrado com sucesso</p>
        <p class="data">Encerrado em: {{ formatarDataHora(mdfe.data_encerramento) }}</p>
        <p class="data" v-if="mdfe.protocolo_encerramento">Protocolo: {{ mdfe.protocolo_encerramento }}</p>
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
const mdfe = ref(null)

async function carregarDetalhes() {
  loading.value = true
  try {
    const response = await api.get(`/fiscal/mdfe/${route.params.ref}`)
    mdfe.value = response.data
  } catch (error) {
    console.error('Erro ao carregar MDF-e:', error)
    alert('Erro ao carregar detalhes do MDF-e')
    router.push('/fiscal/mdfe')
  } finally {
    loading.value = false
  }
}

async function downloadPDF() {
  try {
    const response = await api.get(`/fiscal/mdfe/${route.params.ref}/pdf`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `DAMDFE_${mdfe.value.numero}.pdf`)
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
    const response = await api.get(`/fiscal/mdfe/${route.params.ref}/xml`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `MDFE_${mdfe.value.numero}.xml`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Erro ao baixar XML:', error)
    alert('Erro ao baixar XML')
  }
}

function verCTe(chave) {
  router.push(`/fiscal/cte/${chave}`)
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

function formatarModal(modal) {
  const modalMap = {
    '1': 'Rodoviário',
    '2': 'Aéreo',
    '3': 'Aquaviário',
    '4': 'Ferroviário'
  }
  return modalMap[modal] || modal
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
.detalhes-mdfe-container {
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

.info-card.full-width {
  grid-column: 1 / -1;
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

.percurso-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.uf-badge {
  background: #007bff;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
}

.condutor-item {
  background: white;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 10px;
}

.condutor-item:last-child {
  margin-bottom: 0;
}

.ctes-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cte-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
}

.cte-numero {
  font-weight: 600;
  color: #495057;
  min-width: 80px;
}

.cte-chave {
  flex: 1;
  font-family: monospace;
  font-size: 12px;
  color: #6c757d;
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

.alert.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.data {
  font-size: 12px;
  color: #6c757d;
  margin-top: 10px;
}
</style>
