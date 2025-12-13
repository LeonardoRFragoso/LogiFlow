<template>
  <div class="dashboard">
    <!-- Welcome Section -->
    <div class="welcome-section">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ greeting }}, {{ userName }}! 👋</h1>
        <p class="text-gray-500 dark:text-gray-400 mt-1">Aqui está o resumo das operações de hoje.</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-500 dark:text-gray-400">{{ currentDate }}</span>
      </div>
    </div>

    <!-- KPIs -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
      <div class="kpi-card kpi-blue">
        <div class="kpi-icon">🚚</div>
        <div class="kpi-content">
          <p class="kpi-value">{{ stats.em_transito }}</p>
          <p class="kpi-label">Em Trânsito</p>
        </div>
        <div class="kpi-trend up">↗ Ativo</div>
      </div>
      
      <div class="kpi-card kpi-green">
        <div class="kpi-icon">📦</div>
        <div class="kpi-content">
          <p class="kpi-value">{{ stats.entregas_hoje }}</p>
          <p class="kpi-label">Entregas Hoje</p>
        </div>
        <div class="kpi-trend">📅 Previsão</div>
      </div>
      
      <div class="kpi-card kpi-red">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-content">
          <p class="kpi-value">{{ stats.atrasados }}</p>
          <p class="kpi-label">Atrasados</p>
        </div>
        <div class="kpi-trend down" v-if="stats.atrasados > 0">🔴 Urgente</div>
        <div class="kpi-trend up" v-else>✅ OK</div>
      </div>
      
      <div class="kpi-card kpi-orange">
        <div class="kpi-icon">💰</div>
        <div class="kpi-content">
          <p class="kpi-value">{{ stats.cotacoes_abertas || 0 }}</p>
          <p class="kpi-label">Cotações Abertas</p>
        </div>
        <div class="kpi-trend">💼 Comercial</div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- SLA Status -->
      <div class="lg:col-span-2">
        <div class="card-modern">
          <div class="card-header">
            <h3 class="card-title">📊 Status SLA</h3>
            <span class="text-sm text-gray-500 dark:text-gray-400">Tempo real</span>
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div class="sla-card sla-green">
              <div class="sla-icon">✅</div>
              <p class="sla-value">{{ stats.sla?.verde || 0 }}</p>
              <p class="sla-label">No Prazo</p>
              <div class="sla-bar"></div>
            </div>
            <div class="sla-card sla-yellow">
              <div class="sla-icon">⚡</div>
              <p class="sla-value">{{ stats.sla?.amarelo || 0 }}</p>
              <p class="sla-label">Atenção</p>
              <div class="sla-bar"></div>
            </div>
            <div class="sla-card sla-red">
              <div class="sla-icon">🚨</div>
              <p class="sla-value">{{ stats.sla?.vermelho || 0 }}</p>
              <p class="sla-label">Atrasado</p>
              <div class="sla-bar"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card-modern">
        <div class="card-header">
          <h3 class="card-title">⚡ Ações Rápidas</h3>
        </div>
        <div class="space-y-3">
          <router-link to="/cotacoes" class="quick-action">
            <span class="quick-action-icon">💰</span>
            <span>Nova Cotação</span>
            <span class="quick-action-arrow">→</span>
          </router-link>
          <router-link to="/pedidos" class="quick-action">
            <span class="quick-action-icon">📦</span>
            <span>Novo Pedido</span>
            <span class="quick-action-arrow">→</span>
          </router-link>
          <router-link to="/motoristas" class="quick-action">
            <span class="quick-action-icon">🧑‍✈️</span>
            <span>Ver Motoristas</span>
            <span class="quick-action-arrow">→</span>
          </router-link>
          <router-link to="/ocorrencias" class="quick-action">
            <span class="quick-action-icon">⚠️</span>
            <span>Ocorrências</span>
            <span class="quick-action-arrow">→</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Bottom Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
      <!-- Recent Activity -->
      <div class="card-modern">
        <div class="card-header">
          <h3 class="card-title">🕐 Atividades Recentes</h3>
          <a href="#" class="text-sm text-blue-600 dark:text-blue-400 hover:underline">Ver todas</a>
        </div>
        <div class="space-y-4">
          <div class="activity-item">
            <div class="activity-icon bg-green-100 dark:bg-green-900/50 text-green-600">✅</div>
            <div class="activity-content">
              <p class="activity-text">Entrega confirmada - <span class="font-medium">PED-001234</span></p>
              <p class="activity-time">Há 15 minutos</p>
            </div>
          </div>
          <div class="activity-item">
            <div class="activity-icon bg-blue-100 dark:bg-blue-900/50 text-blue-600">🚚</div>
            <div class="activity-content">
              <p class="activity-text">Veículo em trânsito - <span class="font-medium">ABC-1234</span></p>
              <p class="activity-time">Há 32 minutos</p>
            </div>
          </div>
          <div class="activity-item">
            <div class="activity-icon bg-orange-100 dark:bg-orange-900/50 text-orange-600">💰</div>
            <div class="activity-content">
              <p class="activity-text">Cotação aprovada - <span class="font-medium">COT-005678</span></p>
              <p class="activity-time">Há 1 hora</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Alerts -->
      <div class="card-modern">
        <div class="card-header">
          <h3 class="card-title">🔔 Alertas</h3>
          <span class="badge-alert" v-if="stats.atrasados > 0">{{ stats.atrasados }} novos</span>
        </div>
        <div class="space-y-3" v-if="stats.atrasados > 0 || stats.sla?.amarelo > 0">
          <div class="alert-item alert-warning" v-if="stats.sla?.amarelo > 0">
            <span class="alert-icon">⚡</span>
            <div>
              <p class="font-medium">{{ stats.sla?.amarelo }} entregas precisam de atenção</p>
              <p class="text-sm opacity-80">Verifique o status para evitar atrasos</p>
            </div>
          </div>
          <div class="alert-item alert-danger" v-if="stats.atrasados > 0">
            <span class="alert-icon">🚨</span>
            <div>
              <p class="font-medium">{{ stats.atrasados }} entregas atrasadas</p>
              <p class="text-sm opacity-80">Ação imediata necessária</p>
            </div>
          </div>
        </div>
        <div class="empty-state" v-else>
          <span class="text-4xl">🎉</span>
          <p class="text-gray-500 dark:text-gray-400 mt-2">Nenhum alerta no momento!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const stats = ref({ em_transito: 0, entregas_hoje: 0, atrasados: 0, cotacoes_abertas: 0, sla: {} })

const userName = computed(() => authStore.user?.first_name || authStore.user?.username || 'Usuário')
const currentDate = computed(() => new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' }))
const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Bom dia'
  if (hour < 18) return 'Boa tarde'
  return 'Boa noite'
})

onMounted(async () => {
  // Garante que os dados do usuário sejam carregados
  if (!authStore.user) {
    await authStore.fetchUser()
  }
  
  try {
    const response = await api.get('/api/dashboard/stats')
    const data = response.data.data
    stats.value = {
      em_transito: data.entregas.em_transito,
      entregas_hoje: data.entregas.entregues_hoje,
      atrasados: data.entregas.atrasadas,
      cotacoes_abertas: data.cotacoes.pendentes,
      sla: {
        verde: data.pedidos.entregues,
        amarelo: data.pedidos.em_transito,
        vermelho: data.entregas.atrasadas
      }
    }
  } catch (e) {
    console.error('Erro ao carregar dashboard:', e)
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

/* KPI Cards */
.kpi-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.dark .kpi-card {
  background: #1f2937;
  border-color: rgba(255, 255, 255, 0.1);
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.kpi-blue::before { background: linear-gradient(90deg, #3b82f6, #1d4ed8); }
.kpi-green::before { background: linear-gradient(90deg, #10b981, #059669); }
.kpi-red::before { background: linear-gradient(90deg, #ef4444, #dc2626); }
.kpi-orange::before { background: linear-gradient(90deg, #f59e0b, #d97706); }

.kpi-icon {
  font-size: 2rem;
}

.kpi-content {
  flex: 1;
}

.kpi-value {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1;
  color: #1f2937;
}

.dark .kpi-value {
  color: white;
}

.kpi-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.dark .kpi-label {
  color: #9ca3af;
}

.kpi-trend {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: #f3f4f6;
  color: #6b7280;
  width: fit-content;
}

.dark .kpi-trend {
  background: #374151;
  color: #9ca3af;
}

.kpi-trend.up { background: #d1fae5; color: #059669; }
.kpi-trend.down { background: #fee2e2; color: #dc2626; }
.dark .kpi-trend.up { background: rgba(16, 185, 129, 0.2); }
.dark .kpi-trend.down { background: rgba(239, 68, 68, 0.2); }

/* Modern Card */
.card-modern {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.dark .card-modern {
  background: #1f2937;
  border-color: rgba(255, 255, 255, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.dark .card-title {
  color: white;
}

/* SLA Cards */
.sla-card {
  text-align: center;
  padding: 1.5rem 1rem;
  border-radius: 0.75rem;
  position: relative;
  overflow: hidden;
}

.sla-green { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); }
.sla-yellow { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); }
.sla-red { background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); }

.dark .sla-green { background: linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(16, 185, 129, 0.1) 100%); }
.dark .sla-yellow { background: linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(245, 158, 11, 0.1) 100%); }
.dark .sla-red { background: linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(239, 68, 68, 0.1) 100%); }

.sla-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.sla-value {
  font-size: 2rem;
  font-weight: 800;
  color: #1f2937;
}

.dark .sla-value {
  color: white;
}

.sla-label {
  font-size: 0.875rem;
  color: #4b5563;
  margin-top: 0.25rem;
}

.dark .sla-label {
  color: #9ca3af;
}

.sla-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.sla-green .sla-bar { background: #10b981; }
.sla-yellow .sla-bar { background: #f59e0b; }
.sla-red .sla-bar { background: #ef4444; }

/* Quick Actions */
.quick-action {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: #f9fafb;
  border-radius: 0.75rem;
  color: #374151;
  transition: all 0.2s;
  text-decoration: none;
}

.dark .quick-action {
  background: #374151;
  color: #e5e7eb;
}

.quick-action:hover {
  background: #3b82f6;
  color: white;
  transform: translateX(4px);
}

.quick-action-icon {
  font-size: 1.25rem;
}

.quick-action-arrow {
  margin-left: auto;
  opacity: 0;
  transition: opacity 0.2s;
}

.quick-action:hover .quick-action-arrow {
  opacity: 1;
}

/* Activity */
.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.activity-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-text {
  color: #374151;
  font-size: 0.9rem;
}

.dark .activity-text {
  color: #e5e7eb;
}

.activity-time {
  font-size: 0.75rem;
  color: #9ca3af;
}

/* Alerts */
.badge-alert {
  background: #ef4444;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.75rem;
}

.alert-warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
}

.alert-danger {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
}

.dark .alert-warning {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(245, 158, 11, 0.1) 100%);
  color: #fcd34d;
}

.dark .alert-danger {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(239, 68, 68, 0.1) 100%);
  color: #fca5a5;
}

.alert-icon {
  font-size: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
}
</style>
