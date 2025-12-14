<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">💚 Customer Success</h1>
        <p class="page-subtitle">Health Score e Prevenção de Churn</p>
      </div>
      <div class="header-actions">
        <button @click="atualizarDados" class="btn-refresh" :disabled="loading">
          <span v-if="!loading">🔄</span>
          <span v-else class="spinner-small"></span>
          Atualizar
        </button>
      </div>
    </div>

    <!-- Estatísticas Gerais -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-label">Health Score Médio</div>
          <div class="stat-value">{{ dashboard.estatisticas?.health_score_medio || 0 }}</div>
          <div class="stat-trend positive">+2.5 vs mês anterior</div>
        </div>
      </div>

      <div class="stat-card green">
        <div class="stat-icon">🟢</div>
        <div class="stat-content">
          <div class="stat-label">Clientes Saudáveis</div>
          <div class="stat-value">{{ dashboard.estatisticas?.distribuicao?.verde || 0 }}</div>
          <div class="stat-subtitle">Score 80-100</div>
        </div>
      </div>

      <div class="stat-card yellow">
        <div class="stat-icon">🟡</div>
        <div class="stat-content">
          <div class="stat-label">Atenção</div>
          <div class="stat-value">{{ dashboard.estatisticas?.distribuicao?.amarelo || 0 }}</div>
          <div class="stat-subtitle">Score 50-79</div>
        </div>
      </div>

      <div class="stat-card red">
        <div class="stat-icon">🔴</div>
        <div class="stat-content">
          <div class="stat-label">Risco de Churn</div>
          <div class="stat-value">{{ dashboard.estatisticas?.distribuicao?.vermelho || 0 }}</div>
          <div class="stat-subtitle">Score 0-49</div>
        </div>
      </div>
    </div>

    <!-- Alertas de Risco -->
    <div class="section-card" v-if="alertas.length > 0">
      <div class="section-header">
        <h2>⚠️ Alertas de Risco de Churn</h2>
        <span class="badge-count">{{ alertas.length }} alertas ativos</span>
      </div>

      <div class="alertas-container">
        <div v-for="alerta in alertas" :key="alerta.cliente_id" 
             :class="['alerta-card', `urgencia-${alerta.urgencia}`]">
          <div class="alerta-header">
            <div class="alerta-info">
              <h3>{{ alerta.cliente_nome }}</h3>
              <span :class="['status-badge', `status-${alerta.status}`]">
                {{ statusLabel[alerta.status] }}
              </span>
            </div>
            <div class="alerta-score">
              <div class="score-circle" :class="`score-${alerta.status}`">
                {{ alerta.health_score }}
              </div>
            </div>
          </div>

          <div class="alerta-metricas">
            <div class="metrica-item">
              <span class="metrica-label">Risco de Churn:</span>
              <span class="metrica-value">{{ alerta.risco_churn.probabilidade_pct }}%</span>
            </div>
            <div class="metrica-item">
              <span class="metrica-label">Urgência:</span>
              <span :class="['urgencia-badge', `urgencia-${alerta.urgencia}`]">
                {{ alerta.urgencia === 'alta' ? '🔥 Alta' : '⚠️ Média' }}
              </span>
            </div>
          </div>

          <div class="alerta-recomendacoes">
            <strong>Recomendações:</strong>
            <ul>
              <li v-for="(rec, idx) in alerta.recomendacoes" :key="idx">{{ rec }}</li>
            </ul>
          </div>

          <div class="alerta-actions">
            <button @click="verDetalhes(alerta.cliente_id)" class="btn-action">
              📊 Ver Detalhes
            </button>
            <button @click="registrarAcao(alerta.cliente_id)" class="btn-action primary">
              ✅ Registrar Ação
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Clientes em Risco -->
    <div class="section-card">
      <div class="section-header">
        <h2>🎯 Top 5 Clientes em Risco</h2>
      </div>
      <div class="table-container">
        <table class="modern-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Health Score</th>
              <th>Status</th>
              <th>Risco Churn</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cliente in dashboard.top_risco" :key="cliente.cliente_id">
              <td><strong>{{ cliente.cliente_nome }}</strong></td>
              <td>
                <div class="score-bar">
                  <div class="score-fill" :style="{width: cliente.health_score + '%'}" 
                       :class="`score-${cliente.status}`"></div>
                  <span class="score-text">{{ cliente.health_score }}</span>
                </div>
              </td>
              <td>
                <span :class="['status-badge', `status-${cliente.status}`]">
                  {{ statusLabel[cliente.status] }}
                </span>
              </td>
              <td>{{ cliente.risco_churn.probabilidade_pct }}%</td>
              <td>
                <button @click="verDetalhes(cliente.cliente_id)" class="btn-sm">
                  Ver Detalhes
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Top Clientes Saudáveis -->
    <div class="section-card">
      <div class="section-header">
        <h2>⭐ Top 5 Clientes Saudáveis</h2>
      </div>
      <div class="table-container">
        <table class="modern-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Health Score</th>
              <th>Status</th>
              <th>Tendência</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cliente in dashboard.top_saudaveis" :key="cliente.cliente_id">
              <td><strong>{{ cliente.cliente_nome }}</strong></td>
              <td>
                <div class="score-bar">
                  <div class="score-fill" :style="{width: cliente.health_score + '%'}" 
                       :class="`score-${cliente.status}`"></div>
                  <span class="score-text">{{ cliente.health_score }}</span>
                </div>
              </td>
              <td>
                <span :class="['status-badge', `status-${cliente.status}`]">
                  {{ statusLabel[cliente.status] }}
                </span>
              </td>
              <td><span class="trend-badge positive">📈 Crescendo</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de Detalhes -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content large" @click.stop>
        <div class="modal-header">
          <h2>📊 Health Score Detalhado</h2>
          <button @click="closeModal" class="btn-close">✕</button>
        </div>

        <div v-if="detalhesCliente" class="modal-body">
          <div class="cliente-header">
            <h3>{{ detalhesCliente.cliente_nome || 'Cliente' }}</h3>
            <div class="score-circle large" :class="`score-${detalhesCliente.status}`">
              {{ detalhesCliente.health_score }}
            </div>
          </div>

          <div class="metricas-detalhadas">
            <div class="metrica-card">
              <div class="metrica-header">
                <span class="metrica-icon">💻</span>
                <span class="metrica-nome">Uso do Sistema</span>
                <span class="metrica-peso">30%</span>
              </div>
              <div class="metrica-score">{{ detalhesCliente.metricas?.uso?.score || 0 }}/100</div>
              <div class="metrica-progress">
                <div class="progress-bar" :style="{width: (detalhesCliente.metricas?.uso?.score || 0) + '%'}"></div>
              </div>
              <div class="metrica-detalhes">
                <small>Logins (30d): {{ detalhesCliente.metricas?.uso?.logins_30d || 0 }}</small>
                <small>Última atividade: {{ formatDias(detalhesCliente.metricas?.uso?.dias_sem_uso) }}</small>
              </div>
            </div>

            <div class="metrica-card">
              <div class="metrica-header">
                <span class="metrica-icon">🎯</span>
                <span class="metrica-nome">Adoção de Features</span>
                <span class="metrica-peso">20%</span>
              </div>
              <div class="metrica-score">{{ detalhesCliente.metricas?.adocao?.score || 0 }}/100</div>
              <div class="metrica-progress">
                <div class="progress-bar" :style="{width: (detalhesCliente.metricas?.adocao?.score || 0) + '%'}"></div>
              </div>
              <div class="metrica-detalhes">
                <small>Features ativas: {{ detalhesCliente.metricas?.adocao?.features_utilizadas?.length || 0 }}</small>
                <small>Taxa de adoção: {{ detalhesCliente.metricas?.adocao?.taxa_adocao || 0 }}%</small>
              </div>
            </div>

            <div class="metrica-card">
              <div class="metrica-header">
                <span class="metrica-icon">🔥</span>
                <span class="metrica-nome">Engajamento</span>
                <span class="metrica-peso">15%</span>
              </div>
              <div class="metrica-score">{{ detalhesCliente.metricas?.engajamento?.score || 0 }}/100</div>
              <div class="metrica-progress">
                <div class="progress-bar" :style="{width: (detalhesCliente.metricas?.engajamento?.score || 0) + '%'}"></div>
              </div>
              <div class="metrica-detalhes">
                <small>Ações (30d): {{ detalhesCliente.metricas?.engajamento?.acoes_30d || 0 }}</small>
                <small>Nível: {{ detalhesCliente.metricas?.engajamento?.nivel_engajamento || 'N/A' }}</small>
              </div>
            </div>

            <div class="metrica-card">
              <div class="metrica-header">
                <span class="metrica-icon">🎧</span>
                <span class="metrica-nome">Suporte</span>
                <span class="metrica-peso">15%</span>
              </div>
              <div class="metrica-score">{{ detalhesCliente.metricas?.suporte?.score || 0 }}/100</div>
              <div class="metrica-progress">
                <div class="progress-bar" :style="{width: (detalhesCliente.metricas?.suporte?.score || 0) + '%'}"></div>
              </div>
              <div class="metrica-detalhes">
                <small>Tickets abertos: {{ detalhesCliente.metricas?.suporte?.tickets_abertos || 0 }}</small>
                <small>NPS: {{ detalhesCliente.metricas?.suporte?.nps_suporte || 0 }}/10</small>
              </div>
            </div>

            <div class="metrica-card">
              <div class="metrica-header">
                <span class="metrica-icon">💰</span>
                <span class="metrica-nome">Financeiro</span>
                <span class="metrica-peso">20%</span>
              </div>
              <div class="metrica-score">{{ detalhesCliente.metricas?.financeiro?.score || 0 }}/100</div>
              <div class="metrica-progress">
                <div class="progress-bar" :style="{width: (detalhesCliente.metricas?.financeiro?.score || 0) + '%'}"></div>
              </div>
              <div class="metrica-detalhes">
                <small>Pagamentos em dia: {{ detalhesCliente.metricas?.financeiro?.pagamentos_em_dia_pct || 0 }}%</small>
                <small>Status: {{ detalhesCliente.metricas?.financeiro?.status_financeiro || 'N/A' }}</small>
              </div>
            </div>
          </div>

          <div class="recomendacoes-section">
            <h4>💡 Recomendações</h4>
            <ul>
              <li v-for="(rec, idx) in detalhesCliente.recomendacoes" :key="idx">{{ rec }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const loading = ref(false)
const showModal = ref(false)
const dashboard = ref({
  estatisticas: {},
  top_risco: [],
  top_saudaveis: []
})
const alertas = ref([])
const detalhesCliente = ref(null)

const statusLabel = {
  verde: '🟢 Saudável',
  amarelo: '🟡 Atenção',
  vermelho: '🔴 Risco'
}

async function carregarDashboard() {
  try {
    loading.value = true
    const response = await api.get('/customer-success/dashboard')
    dashboard.value = response.data
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  } finally {
    loading.value = false
  }
}

async function carregarAlertas() {
  try {
    const response = await api.get('/customer-success/alertas')
    alertas.value = response.data.alertas || []
  } catch (error) {
    console.error('Erro ao carregar alertas:', error)
  }
}

async function verDetalhes(clienteId) {
  try {
    const response = await api.get(`/health-score/${clienteId}`)
    detalhesCliente.value = response.data.data
    showModal.value = true
  } catch (error) {
    console.error('Erro ao carregar detalhes:', error)
    alert('Erro ao carregar detalhes do cliente')
  }
}

function registrarAcao(clienteId) {
  const descricao = prompt('Descreva a ação a ser tomada:')
  if (descricao) {
    api.post(`/customer-success/acao/${clienteId}`, {
      tipo: 'intervencao',
      descricao: descricao,
      responsavel: 'Usuário Atual'
    }).then(() => {
      alert('Ação registrada com sucesso!')
      atualizarDados()
    }).catch(error => {
      console.error('Erro ao registrar ação:', error)
      alert('Erro ao registrar ação')
    })
  }
}

function closeModal() {
  showModal.value = false
  detalhesCliente.value = null
}

function atualizarDados() {
  carregarDashboard()
  carregarAlertas()
}

function formatDias(dias) {
  if (dias === 0) return 'Hoje'
  if (dias === 1) return 'Ontem'
  return `${dias} dias atrás`
}

onMounted(() => {
  atualizarDados()
})
</script>

<style scoped>
.page-container {
  padding: 2rem;
  max-width: 1600px;
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
  margin: 0;
}

.page-subtitle {
  color: #666;
  margin: 0.5rem 0 0 0;
}

.btn-refresh {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-refresh:hover:not(:disabled) {
  background: #2563eb;
}

.btn-refresh:disabled {
  background: #9ca3af;
  cursor: not-allowed;
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
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  gap: 1rem;
}

.stat-card.green { border-left: 4px solid #10b981; }
.stat-card.yellow { border-left: 4px solid #f59e0b; }
.stat-card.red { border-left: 4px solid #ef4444; }

.stat-icon {
  font-size: 2.5rem;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-subtitle {
  font-size: 0.75rem;
  color: #999;
  margin-top: 0.25rem;
}

.stat-trend {
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.stat-trend.positive {
  color: #10b981;
}

.section-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
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
  margin: 0;
}

.badge-count {
  background: #ef4444;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.alertas-container {
  display: grid;
  gap: 1rem;
}

.alerta-card {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.alerta-card.urgencia-alta {
  border-color: #ef4444;
  background: #fef2f2;
}

.alerta-card.urgencia-media {
  border-color: #f59e0b;
  background: #fffbeb;
}

.alerta-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.alerta-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-badge.status-verde {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.status-amarelo {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.status-vermelho {
  background: #fee2e2;
  color: #991b1b;
}

.score-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.score-circle.large {
  width: 80px;
  height: 80px;
  font-size: 1.5rem;
}

.score-circle.score-verde { background: #10b981; }
.score-circle.score-amarelo { background: #f59e0b; }
.score-circle.score-vermelho { background: #ef4444; }

.alerta-metricas {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 6px;
}

.metrica-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metrica-label {
  font-size: 0.875rem;
  color: #666;
}

.metrica-value {
  font-size: 1.125rem;
  font-weight: 600;
}

.urgencia-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.urgencia-badge.urgencia-alta {
  background: #fee2e2;
  color: #991b1b;
}

.urgencia-badge.urgencia-media {
  background: #fef3c7;
  color: #92400e;
}

.alerta-recomendacoes {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
}

.alerta-recomendacoes ul {
  margin: 0.5rem 0 0 0;
  padding-left: 1.5rem;
}

.alerta-recomendacoes li {
  margin: 0.25rem 0;
}

.alerta-actions {
  display: flex;
  gap: 1rem;
}

.btn-action {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-action:hover {
  background: #f3f4f6;
}

.btn-action.primary {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.btn-action.primary:hover {
  background: #2563eb;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table th {
  text-align: left;
  padding: 0.75rem;
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.modern-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.score-bar {
  position: relative;
  width: 100%;
  height: 24px;
  background: #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  transition: width 0.3s;
}

.score-fill.score-verde { background: #10b981; }
.score-fill.score-amarelo { background: #f59e0b; }
.score-fill.score-vermelho { background: #ef4444; }

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-weight: 600;
  font-size: 0.875rem;
  color: #1a1a1a;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-sm:hover {
  background: #2563eb;
}

.trend-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.trend-badge.positive {
  background: #d1fae5;
  color: #065f46;
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
  max-width: 900px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.btn-close:hover {
  color: #1a1a1a;
}

.modal-body {
  padding: 1.5rem;
}

.cliente-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

.cliente-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

.metricas-detalhadas {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.metrica-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
}

.metrica-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.metrica-icon {
  font-size: 1.5rem;
}

.metrica-nome {
  flex: 1;
  font-weight: 600;
}

.metrica-peso {
  font-size: 0.875rem;
  color: #666;
}

.metrica-score {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.metrica-progress {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s;
}

.metrica-detalhes {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: #666;
}

.recomendacoes-section {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 8px;
}

.recomendacoes-section h4 {
  margin: 0 0 1rem 0;
}

.recomendacoes-section ul {
  margin: 0;
  padding-left: 1.5rem;
}

.recomendacoes-section li {
  margin: 0.5rem 0;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
