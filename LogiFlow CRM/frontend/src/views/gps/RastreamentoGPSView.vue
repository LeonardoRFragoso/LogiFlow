<template>
  <div class="rastreamento-gps">
    <div class="page-header">
      <h1>🛰️ Rastreamento GPS</h1>
      <p>Monitore sua frota em tempo real</p>
    </div>

    <div v-if="errorMessage" class="error-banner">
      <div class="error-icon">⚠️</div>
      <div>
        <p>{{ errorMessage }}</p>
        <p class="error-hint">Verifique credenciais do provider do tenant ou tente novamente.</p>
      </div>
    </div>

    <!-- Estatísticas da Frota -->
    <div class="stats-grid">
      <div class="stat-card movimento">
        <div class="stat-icon">🚛</div>
        <div class="stat-content">
          <h3>Em Movimento</h3>
          <div class="stat-value">{{ estatisticas.em_movimento || 0 }}</div>
        </div>
      </div>

      <div class="stat-card parado">
        <div class="stat-icon">⏸️</div>
        <div class="stat-content">
          <h3>Parados</h3>
          <div class="stat-value">{{ estatisticas.parados || 0 }}</div>
        </div>
      </div>

      <div class="stat-card total">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>Total de Veículos</h3>
          <div class="stat-value">{{ estatisticas.total_veiculos || 0 }}</div>
        </div>
      </div>

      <div class="stat-card alertas">
        <div class="stat-icon">⚠️</div>
        <div class="stat-content">
          <h3>Alertas Ativos</h3>
          <div class="stat-value">{{ estatisticas.alertas_ativos || 0 }}</div>
        </div>
      </div>

      <div class="stat-card km">
        <div class="stat-icon">🛣️</div>
        <div class="stat-content">
          <h3>KM Rodados Hoje</h3>
          <div class="stat-value">{{ estatisticas.km_rodados_hoje || 0 }}</div>
        </div>
      </div>

      <div class="stat-card velocidade">
        <div class="stat-icon">⚡</div>
        <div class="stat-content">
          <h3>Velocidade Média</h3>
          <div class="stat-value">{{ estatisticas.velocidade_media || 0 }} km/h</div>
        </div>
      </div>
    </div>

    <!-- Mapa e Lista -->
    <div class="content-grid">
      <!-- Mapa -->
      <div class="mapa-card">
        <div class="card-header">
          <h2>🗺️ Mapa em Tempo Real</h2>
          <div class="mapa-controls">
            <button @click="atualizarMapa" class="btn-icon" title="Atualizar">
              🔄
            </button>
            <button @click="centralizarMapa" class="btn-icon" title="Centralizar">
              🎯
            </button>
          </div>
        </div>
        
        <div class="mapa-container">
          <div class="mapa-placeholder">
            <p>🗺️ Mapa Interativo</p>
            <p class="mapa-info">{{ veiculos.length }} veículos rastreados</p>
            <div v-if="veiculos.length > 0" class="veiculos-no-mapa">
              <div 
                v-for="veiculo in veiculos.slice(0, 5)" 
                :key="veiculo.placa"
                class="veiculo-marker"
                @click="selecionarVeiculo(veiculo)"
              >
                <span class="marker-icon">📍</span>
                <span class="marker-placa">{{ veiculo.placa }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="mapa-legenda">
          <div class="legenda-item">
            <span class="legenda-cor movimento"></span>
            <span>Em Movimento</span>
          </div>
          <div class="legenda-item">
            <span class="legenda-cor parado"></span>
            <span>Parado</span>
          </div>
          <div class="legenda-item">
            <span class="legenda-cor offline"></span>
            <span>Offline</span>
          </div>
        </div>
      </div>

      <!-- Lista de Veículos -->
      <div class="veiculos-card">
        <div class="card-header">
          <h2>🚛 Veículos</h2>
          <input 
            v-model="filtro" 
            type="text" 
            placeholder="Buscar placa..." 
            class="search-input"
          >
        </div>

        <div class="veiculos-lista">
          <div 
            v-for="veiculo in veiculosFiltrados" 
            :key="veiculo.placa"
            class="veiculo-item"
            :class="{ 'selecionado': veiculoSelecionado?.placa === veiculo.placa }"
            @click="selecionarVeiculo(veiculo)"
          >
            <div class="veiculo-header">
              <span class="veiculo-placa">{{ veiculo.placa }}</span>
              <span class="veiculo-status" :class="veiculo.status">
                {{ statusLabel(veiculo.status) }}
              </span>
            </div>
            <div class="veiculo-info">
              <p class="veiculo-modelo">{{ veiculo.modelo || 'Modelo não informado' }}</p>
              <p class="veiculo-fonte">
                <span class="fonte-badge" :class="veiculo.fonte_rastreamento">
                  {{ fonteLabel(veiculo.fonte_rastreamento) }}
                </span>
              </p>
            </div>
            <div v-if="veiculo.posicao_atual" class="veiculo-posicao">
              <div class="posicao-item">
                <span class="label">Velocidade:</span>
                <span class="value">{{ veiculo.posicao_atual.velocidade_km_h || veiculo.posicao_atual.velocidade || veiculo.posicao_atual.speed || 0 }} km/h</span>
              </div>
              <div class="posicao-item">
                <span class="label">Última atualização:</span>
                <span class="value">{{ formatarHora(veiculo.posicao_atual.data_hora || veiculo.posicao_atual.timestamp || veiculo.posicao_atual.time) }}</span>
              </div>
            </div>
          </div>

          <div v-if="veiculosFiltrados.length === 0" class="empty-veiculos">
            <p>Nenhum veículo encontrado</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Detalhes do Veículo Selecionado -->
    <div v-if="veiculoSelecionado" class="detalhes-card">
      <div class="detalhes-header">
        <h2>📋 Detalhes: {{ veiculoSelecionado.placa }}</h2>
        <button @click="fecharDetalhes" class="btn-close">×</button>
      </div>

      <div class="detalhes-content">
        <div class="detalhes-grid">
          <div class="detalhe-item">
            <span class="label">Modelo:</span>
            <span class="value">{{ veiculoSelecionado.modelo || '-' }}</span>
          </div>
          <div class="detalhe-item">
            <span class="label">Ano:</span>
            <span class="value">{{ veiculoSelecionado.ano || '-' }}</span>
          </div>
          <div class="detalhe-item">
            <span class="label">Status:</span>
            <span class="value">{{ statusLabel(veiculoSelecionado.status) }}</span>
          </div>
          <div class="detalhe-item">
            <span class="label">Fonte:</span>
            <span class="value">{{ fonteLabel(veiculoSelecionado.fonte_rastreamento) }}</span>
          </div>
        </div>

        <div v-if="veiculoSelecionado.posicao_atual" class="posicao-detalhada">
          <h3>📍 Posição Atual</h3>
          <div class="posicao-grid">
            <div class="posicao-item">
              <span class="label">Latitude:</span>
              <span class="value">{{ veiculoSelecionado.posicao_atual.latitude || veiculoSelecionado.posicao_atual.lat }}</span>
            </div>
            <div class="posicao-item">
              <span class="label">Longitude:</span>
              <span class="value">{{ veiculoSelecionado.posicao_atual.longitude || veiculoSelecionado.posicao_atual.lng }}</span>
            </div>
            <div class="posicao-item">
              <span class="label">Velocidade:</span>
              <span class="value">{{ veiculoSelecionado.posicao_atual.velocidade_km_h || veiculoSelecionado.posicao_atual.velocidade || veiculoSelecionado.posicao_atual.speed || 0 }} km/h</span>
            </div>
            <div class="posicao-item">
              <span class="label">Ignição:</span>
              <span class="value">{{ veiculoSelecionado.posicao_atual.ignicao || veiculoSelecionado.posicao_atual.engine_on ? 'Ligada' : 'Desligada' }}</span>
            </div>
          </div>
        </div>

        <div class="detalhes-actions">
          <button @click="verHistorico(veiculoSelecionado)" class="btn-primary">
            📊 Ver Histórico
          </button>
          <button @click="atualizarPosicao(veiculoSelecionado)" class="btn-secondary">
            🔄 Atualizar Posição
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Histórico -->
    <div v-if="showHistorico" class="modal-overlay" @click="showHistorico = false">
      <div class="modal-content historico-modal" @click.stop>
        <div class="modal-header">
          <h3>📊 Histórico de Rota - {{ veiculoHistorico?.placa }}</h3>
          <button @click="showHistorico = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="historico-filtros">
            <div class="form-group">
              <label>Data Início:</label>
              <input v-model="filtroHistorico.dataInicio" type="datetime-local" class="form-control">
            </div>
            <div class="form-group">
              <label>Data Fim:</label>
              <input v-model="filtroHistorico.dataFim" type="datetime-local" class="form-control">
            </div>
            <button @click="carregarHistorico" class="btn-primary">Buscar</button>
          </div>

          <div v-if="historico" class="historico-resultado">
            <div class="historico-stats">
              <div class="stat">
                <span class="label">Total de Pontos:</span>
                <span class="value">{{ historico.total_posicoes || historico.posicoes?.length || 0 }}</span>
              </div>
              <div class="stat">
                <span class="label">Distância Percorrida:</span>
                <span class="value">{{ historico.distancia_percorrida_km || 0 }} km</span>
              </div>
            </div>

            <div class="historico-timeline">
              <div 
                v-for="(posicao, index) in (historico.posicoes || []).slice(0, 10)" 
                :key="index"
                class="timeline-item"
              >
                <div class="timeline-marker">{{ index + 1 }}</div>
                <div class="timeline-content">
                  <p class="timeline-time">{{ formatarDataHora(posicao.data_hora || posicao.timestamp || posicao.time) }}</p>
                  <p class="timeline-info">
                    Velocidade: {{ posicao.velocidade_km_h || posicao.velocidade || posicao.speed || 0 }} km/h
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '../../services/api'

const veiculos = ref([])
const estatisticas = ref({})
const errorMessage = ref('')
const veiculoSelecionado = ref(null)
const filtro = ref('')
const showHistorico = ref(false)
const veiculoHistorico = ref(null)
const historico = ref(null)
const filtroHistorico = ref({
  dataInicio: '',
  dataFim: ''
})

let intervalId = null

const veiculosFiltrados = computed(() => {
  if (!filtro.value) return veiculos.value
  return veiculos.value.filter(v => 
    v.placa.toLowerCase().includes(filtro.value.toLowerCase())
  )
})

const statusLabel = (status) => {
  const labels = {
    'em_movimento': 'Em Movimento',
    'parado': 'Parado',
    'offline': 'Offline',
    'ativo': 'Ativo',
    'rastreando': 'Rastreando'
  }
  return labels[status] || status || 'Desconhecido'
}

const fonteLabel = (fonte) => {
  const labels = {
    'sascar': 'Sascar',
    'autotrac': 'Autotrac',
    'onixsat': 'Onixsat'
  }
  return labels[fonte] || fonte || '-'
}

const formatarHora = (data) => {
  if (!data) return '-'
  try {
    return new Date(data).toLocaleTimeString('pt-BR')
  } catch {
    return '-'
  }
}

const formatarDataHora = (data) => {
  if (!data) return '-'
  try {
    return new Date(data).toLocaleString('pt-BR')
  } catch {
    return '-'
  }
}

const carregarVeiculos = async () => {
  try {
    const response = await api.get('/gps/veiculos')
    if (response.data.success) {
      veiculos.value = response.data.veiculos || []
      errorMessage.value = ''
    } else {
      veiculos.value = []
      errorMessage.value = response.data.message || 'Nenhum veículo retornado'
    }
  } catch (error) {
    console.error('Erro ao carregar veículos:', error)
    errorMessage.value = error.response?.data?.detail || 'Erro ao carregar veículos'
  }
}

const carregarEstatisticas = async () => {
  try {
    const response = await api.get('/gps/dashboard/estatisticas')
    if (response.data.success) {
      estatisticas.value = response.data.estatisticas || {}
      errorMessage.value = ''
    } else {
      estatisticas.value = {}
      errorMessage.value = response.data.message || 'Estatísticas indisponíveis'
    }
  } catch (error) {
    console.error('Erro ao carregar estatísticas:', error)
    errorMessage.value = error.response?.data?.detail || 'Erro ao carregar estatísticas'
  }
}

const carregarDadosMapa = async () => {
  try {
    const response = await api.get('/gps/dashboard/mapa')
    if (response.data.success) {
      veiculos.value = response.data.veiculos || []
      errorMessage.value = ''
    } else {
      veiculos.value = []
      errorMessage.value = response.data.message || 'Mapa sem dados'
    }
  } catch (error) {
    console.error('Erro ao carregar dados do mapa:', error)
    errorMessage.value = error.response?.data?.detail || 'Erro ao carregar mapa'
  }
}

const selecionarVeiculo = (veiculo) => {
  veiculoSelecionado.value = veiculo
}

const fecharDetalhes = () => {
  veiculoSelecionado.value = null
}

const atualizarMapa = async () => {
  await Promise.all([
    carregarVeiculos(),
    carregarEstatisticas(),
    carregarDadosMapa()
  ])
}

const centralizarMapa = () => {
  alert('Centralizar mapa (funcionalidade de mapa interativo)')
}

const atualizarPosicao = async (veiculo) => {
  try {
    const response = await api.get(`/gps/posicao/${veiculo.placa}`)
    if (response.data.success) {
      alert('Posição atualizada!')
      await atualizarMapa()
    } else {
      alert(response.data.message || 'Não foi possível atualizar a posição.')
    }
  } catch (error) {
    console.error('Erro ao atualizar posição:', error)
    alert('Erro ao atualizar posição do veículo.')
  }
}

const verHistorico = (veiculo) => {
  veiculoHistorico.value = veiculo
  showHistorico.value = true
  
  // Definir período padrão (últimas 24h)
  const agora = new Date()
  const ontem = new Date(agora.getTime() - 24 * 60 * 60 * 1000)
  
  filtroHistorico.value.dataFim = agora.toISOString().slice(0, 16)
  filtroHistorico.value.dataInicio = ontem.toISOString().slice(0, 16)
  
  carregarHistorico()
}

const carregarHistorico = async () => {
  if (!veiculoHistorico.value) return
  
  try {
    const params = new URLSearchParams()
    if (filtroHistorico.value.dataInicio) {
      params.append('data_inicio', new Date(filtroHistorico.value.dataInicio).toISOString())
    }
    if (filtroHistorico.value.dataFim) {
      params.append('data_fim', new Date(filtroHistorico.value.dataFim).toISOString())
    }
    
    const response = await api.get(`/gps/historico/${veiculoHistorico.value.placa}?${params}`)
    if (response.data.success) {
      historico.value = response.data.historico || response.data
    } else {
      historico.value = null
      errorMessage.value = response.data.message || 'Histórico indisponível'
    }
  } catch (error) {
    console.error('Erro ao carregar histórico:', error)
    errorMessage.value = error.response?.data?.detail || 'Erro ao carregar histórico'
  }
}

onMounted(() => {
  atualizarMapa()
  
  // Atualizar a cada 30 segundos
  intervalId = setInterval(() => {
    atualizarMapa()
  }, 30000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.rastreamento-gps {
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  gap: 1rem;
  align-items: center;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content h3 {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: bold;
  color: #1a1a1a;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.mapa-card, .veiculos-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  font-size: 1.25rem;
  margin: 0;
}

.mapa-controls {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: #f3f4f6;
  border: none;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.2rem;
}

.btn-icon:hover {
  background: #e5e7eb;
}

.mapa-container {
  height: 500px;
  background: #f9fafb;
}

.mapa-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  position: relative;
}

.mapa-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.veiculos-no-mapa {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  padding: 2rem;
  align-items: flex-start;
  justify-content: center;
}

.veiculo-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.veiculo-marker:hover {
  transform: scale(1.1);
}

.marker-icon {
  font-size: 2rem;
}

.marker-placa {
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.mapa-legenda {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 2rem;
}

.legenda-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.legenda-cor {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.legenda-cor.movimento { background: #10b981; }
.legenda-cor.parado { background: #f59e0b; }
.legenda-cor.offline { background: #ef4444; }

.search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  width: 200px;
}

.veiculos-lista {
  max-height: 500px;
  overflow-y: auto;
}

.veiculo-item {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: background 0.2s;
}

.veiculo-item:hover {
  background: #f9fafb;
}

.veiculo-item.selecionado {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
}

.veiculo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.veiculo-placa {
  font-weight: bold;
  font-size: 1.1rem;
}

.veiculo-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.veiculo-status.em_movimento { background: #d1fae5; color: #065f46; }
.veiculo-status.parado { background: #fef3c7; color: #92400e; }
.veiculo-status.ativo { background: #d1fae5; color: #065f46; }
.veiculo-status.rastreando { background: #dbeafe; color: #1e40af; }

.veiculo-info {
  margin-bottom: 0.5rem;
}

.veiculo-modelo {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.fonte-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 500;
}

.fonte-badge.sascar { background: #dbeafe; color: #1e40af; }
.fonte-badge.autotrac { background: #fce7f3; color: #9f1239; }
.fonte-badge.onixsat { background: #d1fae5; color: #065f46; }

.veiculo-posicao {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
}

.posicao-item {
  display: flex;
  gap: 0.25rem;
}

.posicao-item .label {
  color: #9ca3af;
}

.posicao-item .value {
  color: #374151;
  font-weight: 500;
}

.empty-veiculos {
  padding: 2rem;
  text-align: center;
  color: #9ca3af;
}

.detalhes-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.detalhes-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9fafb;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #9ca3af;
}

.detalhes-content {
  padding: 1.5rem;
}

.detalhes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detalhe-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detalhe-item .label {
  font-size: 0.85rem;
  color: #9ca3af;
}

.detalhe-item .value {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1a1a1a;
}

.posicao-detalhada {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.posicao-detalhada h3 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.posicao-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.detalhes-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 1.5rem;
}

.historico-filtros {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: flex-end;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}

.historico-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.historico-stats .stat {
  display: flex;
  flex-direction: column;
}

.historico-stats .label {
  font-size: 0.85rem;
  color: #9ca3af;
  margin-bottom: 0.25rem;
}

.historico-stats .value {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1a1a1a;
}

.historico-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.timeline-marker {
  background: #3b82f6;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.timeline-content {
  flex: 1;
  padding: 0.5rem 0;
}

.timeline-time {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.timeline-info {
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
