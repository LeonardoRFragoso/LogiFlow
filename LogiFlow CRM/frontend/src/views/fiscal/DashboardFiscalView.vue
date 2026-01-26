<template>
  <div class="dashboard-fiscal-container">
    <div class="header">
      <h1>Dashboard Fiscal</h1>
      <div class="header-actions">
        <select v-model="mesAno.mes" @change="carregarDashboard" class="select-periodo">
          <option v-for="m in 12" :key="m" :value="m">{{ nomeMes(m) }}</option>
        </select>
        <select v-model="mesAno.ano" @change="carregarDashboard" class="select-periodo">
          <option v-for="a in anos" :key="a" :value="a">{{ a }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando dados...</p>
    </div>

    <div v-else class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card cte">
          <div class="stat-icon">📄</div>
          <div class="stat-info">
            <h3>CT-es Emitidos</h3>
            <div class="stat-number">{{ dados.ctes?.total || 0 }}</div>
            <div class="stat-details">
              <span class="stat-badge success">✓ {{ dados.ctes?.autorizados || 0 }} Autorizados</span>
              <span class="stat-badge danger">✕ {{ dados.ctes?.cancelados || 0 }} Cancelados</span>
              <span class="stat-badge warning">! {{ dados.ctes?.rejeitados || 0 }} Rejeitados</span>
            </div>
          </div>
        </div>

        <div class="stat-card valor">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <h3>Valor Total (CT-es)</h3>
            <div class="stat-number">{{ formatarValor(dados.ctes?.valor_total || 0) }}</div>
            <div class="stat-details">
              <span class="stat-text">Somente CT-es autorizados</span>
            </div>
          </div>
        </div>

        <div class="stat-card mdfe">
          <div class="stat-icon">📦</div>
          <div class="stat-info">
            <h3>MDF-es Emitidos</h3>
            <div class="stat-number">{{ dados.mdfes?.total || 0 }}</div>
            <div class="stat-details">
              <span class="stat-badge success">✓ {{ dados.mdfes?.autorizados || 0 }} Autorizados</span>
              <span class="stat-badge info">■ {{ dados.mdfes?.encerrados || 0 }} Encerrados</span>
              <span class="stat-badge danger">✕ {{ dados.mdfes?.cancelados || 0 }} Cancelados</span>
            </div>
          </div>
        </div>

        <div class="stat-card taxa">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <h3>Taxa de Sucesso</h3>
            <div class="stat-number">{{ calcularTaxaSucesso() }}%</div>
            <div class="stat-details">
              <span class="stat-text">CT-es autorizados / Total</span>
            </div>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card">
          <h3>CT-es por Status</h3>
          <div class="chart-placeholder">
            <div class="pie-chart">
              <div class="pie-segment success" :style="{ '--percentage': calcularPercentagem(dados.ctes?.autorizados, dados.ctes?.total) }">
                <span>{{ dados.ctes?.autorizados || 0 }}</span>
              </div>
              <div class="pie-segment danger">
                <span>{{ dados.ctes?.cancelados || 0 }}</span>
              </div>
              <div class="pie-segment warning">
                <span>{{ dados.ctes?.rejeitados || 0 }}</span>
              </div>
            </div>
            <div class="chart-legend">
              <div class="legend-item">
                <span class="legend-color success"></span>
                <span>Autorizados ({{ dados.ctes?.autorizados || 0 }})</span>
              </div>
              <div class="legend-item">
                <span class="legend-color danger"></span>
                <span>Cancelados ({{ dados.ctes?.cancelados || 0 }})</span>
              </div>
              <div class="legend-item">
                <span class="legend-color warning"></span>
                <span>Rejeitados ({{ dados.ctes?.rejeitados || 0 }})</span>
              </div>
            </div>
          </div>
        </div>

        <div class="chart-card">
          <h3>MDF-es por Status</h3>
          <div class="chart-placeholder">
            <div class="bar-chart">
              <div class="bar-item">
                <div class="bar-label">Autorizados</div>
                <div class="bar-container">
                  <div class="bar success" :style="{ width: calcularPercentagem(dados.mdfes?.autorizados, dados.mdfes?.total) + '%' }"></div>
                  <span class="bar-value">{{ dados.mdfes?.autorizados || 0 }}</span>
                </div>
              </div>
              <div class="bar-item">
                <div class="bar-label">Encerrados</div>
                <div class="bar-container">
                  <div class="bar info" :style="{ width: calcularPercentagem(dados.mdfes?.encerrados, dados.mdfes?.total) + '%' }"></div>
                  <span class="bar-value">{{ dados.mdfes?.encerrados || 0 }}</span>
                </div>
              </div>
              <div class="bar-item">
                <div class="bar-label">Cancelados</div>
                <div class="bar-container">
                  <div class="bar danger" :style="{ width: calcularPercentagem(dados.mdfes?.cancelados, dados.mdfes?.total) + '%' }"></div>
                  <span class="bar-value">{{ dados.mdfes?.cancelados || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="quick-actions">
        <h3>Ações Rápidas</h3>
        <div class="actions-grid">
          <button @click="$router.push('/fiscal/cte')" class="action-btn">
            <i class="icon-list"></i>
            <span>Ver CT-es</span>
          </button>
          <button @click="$router.push('/fiscal/mdfe')" class="action-btn">
            <i class="icon-list"></i>
            <span>Ver MDF-es</span>
          </button>
          <button @click="$router.push('/fiscal/mdfe/emitir')" class="action-btn primary">
            <i class="icon-plus"></i>
            <span>Emitir MDF-e</span>
          </button>
          <button @click="$router.push('/configuracoes/fiscal')" class="action-btn">
            <i class="icon-settings"></i>
            <span>Configurações</span>
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

const loading = ref(true)
const dados = ref({
  periodo: {},
  ctes: {},
  mdfes: {}
})

const now = new Date()
const mesAno = ref({
  mes: now.getMonth() + 1,
  ano: now.getFullYear()
})

const anos = Array.from({ length: 5 }, (_, i) => now.getFullYear() - i)

async function carregarDashboard() {
  loading.value = true
  try {
    const response = await api.get('/fiscal/dashboard', {
      params: {
        mes: mesAno.value.mes,
        ano: mesAno.value.ano
      }
    })
    
    dados.value = response.data.data
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
    alert('Erro ao carregar dashboard fiscal')
  } finally {
    loading.value = false
  }
}

function nomeMes(mes) {
  const meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
  ]
  return meses[mes - 1]
}

function formatarValor(valor) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

function calcularTaxaSucesso() {
  const total = dados.value.ctes?.total || 0
  const autorizados = dados.value.ctes?.autorizados || 0
  
  if (total === 0) return 0
  return ((autorizados / total) * 100).toFixed(1)
}

function calcularPercentagem(valor, total) {
  if (!total || total === 0) return 0
  return ((valor || 0) / total) * 100
}

onMounted(() => {
  carregarDashboard()
})
</script>

<style scoped>
.dashboard-fiscal-container {
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
  border-top: 4px solid #007bff;
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

.stat-badge.success {
  background: #d4edda;
  color: #155724;
}

.stat-badge.danger {
  background: #f8d7da;
  color: #721c24;
}

.stat-badge.warning {
  background: #fff3cd;
  color: #856404;
}

.stat-badge.info {
  background: #d1ecf1;
  color: #0c5460;
}

.stat-text {
  font-size: 12px;
  color: #6c757d;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.pie-chart {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    #28a745 0deg 120deg,
    #dc3545 120deg 240deg,
    #ffc107 240deg 360deg
  );
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 2px;
}

.legend-color.success {
  background: #28a745;
}

.legend-color.danger {
  background: #dc3545;
}

.legend-color.warning {
  background: #ffc107;
}

.legend-color.info {
  background: #17a2b8;
}

.bar-chart {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-label {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.bar-container {
  position: relative;
  height: 30px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.bar {
  height: 100%;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.bar.success {
  background: #28a745;
}

.bar.info {
  background: #17a2b8;
}

.bar.danger {
  background: #dc3545;
}

.bar-value {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.quick-actions h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
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
  border-color: #adb5bd;
  transform: translateY(-2px);
}

.action-btn.primary {
  background: #007bff;
  border-color: #007bff;
  color: white;
}

.action-btn.primary:hover {
  background: #0056b3;
  border-color: #0056b3;
}
</style>
