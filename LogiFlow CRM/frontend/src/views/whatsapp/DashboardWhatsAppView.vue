<template>
  <div class="dashboard-whatsapp-container">
    <div class="header">
      <h1>📊 Dashboard WhatsApp</h1>
      <div class="header-actions">
        <select v-model="periodo" @change="carregarDashboard" class="select-periodo">
          <option value="hoje">Hoje</option>
          <option value="semana">Esta Semana</option>
          <option value="mes">Este Mês</option>
          <option value="custom">Personalizado</option>
        </select>
        <button @click="carregarDashboard" class="btn btn-primary">
          <i class="icon-refresh"></i> Atualizar
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando dados...</p>
    </div>

    <div v-else class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card mensagens">
          <div class="stat-icon">💬</div>
          <div class="stat-info">
            <h3>Mensagens Totais</h3>
            <div class="stat-number">{{ dados.mensagens?.total || 0 }}</div>
            <div class="stat-details">
              <span class="stat-badge enviadas">📤 {{ dados.mensagens?.enviadas || 0 }} Enviadas</span>
              <span class="stat-badge recebidas">📥 {{ dados.mensagens?.recebidas || 0 }} Recebidas</span>
            </div>
          </div>
        </div>

        <div class="stat-card bot">
          <div class="stat-icon">🤖</div>
          <div class="stat-info">
            <h3>Mensagens do Bot</h3>
            <div class="stat-number">{{ dados.mensagens?.bot || 0 }}</div>
            <div class="stat-details">
              <span class="stat-text">Taxa: {{ dados.mensagens?.taxa_bot || 0 }}% automático</span>
            </div>
          </div>
        </div>

        <div class="stat-card conversas">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <h3>Conversas</h3>
            <div class="stat-number">{{ dados.conversas?.total_periodo || 0 }}</div>
            <div class="stat-details">
              <span class="stat-badge ativas">✅ {{ dados.conversas?.ativas || 0 }} Ativas</span>
              <span class="stat-badge pendentes">⏳ {{ dados.conversas?.nao_lidas || 0 }} Não lidas</span>
            </div>
          </div>
        </div>

        <div class="stat-card tempo-resposta">
          <div class="stat-icon">⚡</div>
          <div class="stat-info">
            <h3>Tempo Médio</h3>
            <div class="stat-number">{{ calcularTempoMedio() }}</div>
            <div class="stat-details">
              <span class="stat-text">Tempo de resposta</span>
            </div>
          </div>
        </div>
      </div>

      <div class="charts-row">
        <div class="chart-card">
          <h3>📈 Mensagens por Dia</h3>
          <div class="chart-placeholder">
            <div class="bar-chart">
              <div v-for="(dia, index) in ultimosDias" :key="index" class="bar-item">
                <div class="bar-container">
                  <div 
                    class="bar enviadas" 
                    :style="{ height: calcularAlturaBar(dia.enviadas, maxMensagens) + '%' }"
                    :title="`${dia.enviadas} enviadas`"
                  ></div>
                  <div 
                    class="bar recebidas" 
                    :style="{ height: calcularAlturaBar(dia.recebidas, maxMensagens) + '%' }"
                    :title="`${dia.recebidas} recebidas`"
                  ></div>
                </div>
                <div class="bar-label">{{ dia.dia }}</div>
              </div>
            </div>
            <div class="chart-legend">
              <div class="legend-item">
                <span class="legend-color enviadas"></span>
                <span>Enviadas</span>
              </div>
              <div class="legend-item">
                <span class="legend-color recebidas"></span>
                <span>Recebidas</span>
              </div>
            </div>
          </div>
        </div>

        <div class="chart-card">
          <h3>🎯 Intenções do Chatbot</h3>
          <div class="chart-placeholder">
            <div class="intents-list">
              <div v-for="intent in topIntents" :key="intent.nome" class="intent-item">
                <div class="intent-info">
                  <span class="intent-icon">{{ intent.emoji }}</span>
                  <span class="intent-nome">{{ intent.nome }}</span>
                </div>
                <div class="intent-bar-container">
                  <div 
                    class="intent-bar" 
                    :style="{ width: intent.porcentagem + '%' }"
                  ></div>
                  <span class="intent-count">{{ intent.total }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="recent-section">
        <h3>📱 Conversas Recentes</h3>
        <div class="recent-conversations">
          <div v-for="conv in conversasRecentes" :key="conv.id" class="recent-conv-item">
            <div class="conv-avatar">
              {{ conv.contact_name?.charAt(0) || '?' }}
            </div>
            <div class="conv-info">
              <div class="conv-header">
                <strong>{{ conv.contact_name || conv.phone_number }}</strong>
                <span class="conv-time">{{ formatarHora(conv.last_message_at) }}</span>
              </div>
              <div class="conv-preview">
                {{ conv.last_message_content }}
              </div>
              <div v-if="conv.unread_count > 0" class="conv-badge">
                {{ conv.unread_count }} não lida{{ conv.unread_count > 1 ? 's' : '' }}
              </div>
            </div>
            <button @click="abrirConversa(conv)" class="btn btn-sm btn-primary">
              Abrir
            </button>
          </div>
        </div>
      </div>

      <div class="quick-actions">
        <h3>⚡ Ações Rápidas</h3>
        <div class="actions-grid">
          <button @click="$router.push('/whatsapp/conversas')" class="action-btn">
            <i class="icon-message"></i>
            <span>Ver Conversas</span>
          </button>
          <button @click="$router.push('/whatsapp/config')" class="action-btn">
            <i class="icon-settings"></i>
            <span>Configurações</span>
          </button>
          <button @click="enviarMensagemEmMassa" class="action-btn">
            <i class="icon-broadcast"></i>
            <span>Envio em Massa</span>
          </button>
          <button @click="gerarRelatorio" class="action-btn">
            <i class="icon-download"></i>
            <span>Gerar Relatório</span>
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
const periodo = ref('mes')
const dados = ref({
  periodo: {},
  mensagens: {},
  conversas: {}
})
const conversasRecentes = ref([])

const ultimosDias = ref([
  { dia: 'Seg', enviadas: 120, recebidas: 85 },
  { dia: 'Ter', enviadas: 145, recebidas: 92 },
  { dia: 'Qua', enviadas: 132, recebidas: 78 },
  { dia: 'Qui', enviadas: 158, recebidas: 95 },
  { dia: 'Sex', enviadas: 142, recebidas: 88 },
  { dia: 'Sáb', enviadas: 89, recebidas: 45 },
  { dia: 'Dom', enviadas: 67, recebidas: 32 }
])

const topIntents = ref([
  { nome: 'Rastreamento', emoji: '📦', total: 156, porcentagem: 85 },
  { nome: 'Status Pedido', emoji: '📋', total: 124, porcentagem: 68 },
  { nome: 'Prazo', emoji: '📅', total: 98, porcentagem: 53 },
  { nome: 'Dúvidas', emoji: '❓', total: 76, porcentagem: 41 },
  { nome: 'Preço', emoji: '💰', total: 54, porcentagem: 29 }
])

const maxMensagens = computed(() => {
  const max = Math.max(...ultimosDias.value.map(d => Math.max(d.enviadas, d.recebidas)))
  return max || 1
})

async function carregarDashboard() {
  loading.value = true
  try {
    const params = {}
    
    if (periodo.value === 'hoje') {
      params.date_from = new Date().toISOString().split('T')[0]
      params.date_to = new Date().toISOString().split('T')[0]
    } else if (periodo.value === 'semana') {
      const hoje = new Date()
      const semanaAtras = new Date(hoje)
      semanaAtras.setDate(hoje.getDate() - 7)
      params.date_from = semanaAtras.toISOString().split('T')[0]
      params.date_to = hoje.toISOString().split('T')[0]
    } else if (periodo.value === 'mes') {
      const hoje = new Date()
      const mesAtras = new Date(hoje)
      mesAtras.setMonth(hoje.getMonth() - 1)
      params.date_from = mesAtras.toISOString().split('T')[0]
      params.date_to = hoje.toISOString().split('T')[0]
    }
    
    const [dashboardResponse, conversasResponse] = await Promise.all([
      api.get('/whatsapp/dashboard', { params }),
      api.get('/whatsapp/conversas', { params: { limit: 5 } })
    ])
    
    dados.value = dashboardResponse.data.data
    conversasRecentes.value = conversasResponse.data.data
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  } finally {
    loading.value = false
  }
}

function calcularAlturaBar(valor, max) {
  return (valor / max) * 100
}

function calcularTempoMedio() {
  return '< 5 min'
}

function formatarHora(data) {
  if (!data) return ''
  const d = new Date(data)
  const hoje = new Date()
  
  if (d.toDateString() === hoje.toDateString()) {
    return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  }
  
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
}

function abrirConversa(conv) {
  router.push('/whatsapp/conversas')
}

function enviarMensagemEmMassa() {
  alert('Funcionalidade de envio em massa será implementada')
}

function gerarRelatorio() {
  alert('Relatório será gerado em breve')
}

onMounted(() => {
  carregarDashboard()
})
</script>

<style scoped>
.dashboard-whatsapp-container {
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

.select-periodo {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #25D366;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  gap: 20px;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.stat-icon {
  font-size: 48px;
  line-height: 1;
}

.stat-info {
  flex: 1;
}

.stat-info h3 {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 10px;
  font-weight: 600;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.stat-details {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.stat-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.stat-badge.enviadas,
.stat-badge.ativas {
  background: #d4edda;
  color: #155724;
}

.stat-badge.recebidas {
  background: #d1ecf1;
  color: #0c5460;
}

.stat-badge.pendentes {
  background: #fff3cd;
  color: #856404;
}

.stat-text {
  font-size: 12px;
  color: #6c757d;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-card h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.chart-placeholder {
  min-height: 300px;
}

.bar-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 250px;
  gap: 10px;
  margin-bottom: 20px;
}

.bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bar-container {
  flex: 1;
  width: 100%;
  display: flex;
  gap: 4px;
  align-items: flex-end;
  justify-content: center;
}

.bar {
  width: 20px;
  min-height: 5px;
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.bar.enviadas {
  background: #28a745;
}

.bar.recebidas {
  background: #17a2b8;
}

.bar-label {
  margin-top: 8px;
  font-size: 12px;
  color: #6c757d;
  font-weight: 600;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
}

.legend-color.enviadas {
  background: #28a745;
}

.legend-color.recebidas {
  background: #17a2b8;
}

.intents-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.intent-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.intent-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 150px;
}

.intent-icon {
  font-size: 20px;
}

.intent-nome {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.intent-bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.intent-bar {
  height: 30px;
  background: linear-gradient(90deg, #25D366 0%, #128C7E 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.intent-count {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  min-width: 30px;
}

.recent-section,
.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.recent-section h3,
.quick-actions h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.recent-conversations {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recent-conv-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background 0.2s;
}

.recent-conv-item:hover {
  background: #e9ecef;
}

.conv-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #25D366;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
  flex-shrink: 0;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.conv-time {
  font-size: 12px;
  color: #999;
}

.conv-preview {
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-badge {
  font-size: 11px;
  color: #25D366;
  font-weight: 600;
  margin-top: 4px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.action-btn {
  padding: 20px;
  background: #f8f9fa;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 500;
  color: #495057;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #e9ecef;
  border-color: #25D366;
  transform: translateY(-2px);
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
  padding: 6px 12px;
  font-size: 13px;
}

.btn-primary {
  background: #25D366;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}
</style>
