<template>
  <div class="plan-usage-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h2 class="text-2xl font-bold text-gray-900">Uso do Plano</h2>
        <div class="plan-badge" :class="getPlanBadgeClass()">
          {{ planName }}
        </div>
      </div>
      <button @click="$emit('upgrade')" class="upgrade-btn">
        🚀 Fazer Upgrade
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando estatísticas...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>❌ {{ error }}</p>
      <button @click="loadUsage" class="retry-btn">Tentar Novamente</button>
    </div>

    <!-- Usage Stats -->
    <div v-else class="usage-grid">
      <!-- Usuários -->
      <div class="usage-card">
        <div class="card-header">
          <div class="icon-wrapper bg-blue-100">
            <span class="text-2xl">👥</span>
          </div>
          <div>
            <h3 class="card-title">Usuários</h3>
            <p class="card-subtitle">Motoristas cadastrados</p>
          </div>
        </div>
        
        <div class="usage-stats">
          <div class="stat-numbers">
            <span class="current">{{ usage.limits.users.current }}</span>
            <span class="separator">/</span>
            <span class="max">{{ formatLimit(usage.limits.users.max) }}</span>
          </div>
          
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :class="getProgressClass(usage.limits.users)"
              :style="{ width: getProgressWidth(usage.limits.users) }"
            ></div>
          </div>
          
          <p class="available-text">
            {{ getAvailableText(usage.limits.users.available, 'usuários') }}
          </p>
        </div>
      </div>

      <!-- Veículos -->
      <div class="usage-card">
        <div class="card-header">
          <div class="icon-wrapper bg-green-100">
            <span class="text-2xl">🚗</span>
          </div>
          <div>
            <h3 class="card-title">Veículos</h3>
            <p class="card-subtitle">Frota cadastrada</p>
          </div>
        </div>
        
        <div class="usage-stats">
          <div class="stat-numbers">
            <span class="current">{{ usage.limits.vehicles.current }}</span>
            <span class="separator">/</span>
            <span class="max">{{ formatLimit(usage.limits.vehicles.max) }}</span>
          </div>
          
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :class="getProgressClass(usage.limits.vehicles)"
              :style="{ width: getProgressWidth(usage.limits.vehicles) }"
            ></div>
          </div>
          
          <p class="available-text">
            {{ getAvailableText(usage.limits.vehicles.available, 'veículos') }}
          </p>
        </div>
      </div>

      <!-- Pedidos do Mês -->
      <div class="usage-card">
        <div class="card-header">
          <div class="icon-wrapper bg-purple-100">
            <span class="text-2xl">📦</span>
          </div>
          <div>
            <h3 class="card-title">Pedidos do Mês</h3>
            <p class="card-subtitle">{{ getCurrentMonth() }}</p>
          </div>
        </div>
        
        <div class="usage-stats">
          <div class="stat-numbers">
            <span class="current">{{ usage.limits.orders_per_month.current }}</span>
            <span class="separator">/</span>
            <span class="max">{{ formatLimit(usage.limits.orders_per_month.max) }}</span>
          </div>
          
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :class="getProgressClass(usage.limits.orders_per_month)"
              :style="{ width: getProgressWidth(usage.limits.orders_per_month) }"
            ></div>
          </div>
          
          <p class="available-text">
            {{ getAvailableText(usage.limits.orders_per_month.available, 'pedidos') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Trial Info -->
    <div v-if="usage.is_trial" class="trial-banner">
      <span class="trial-icon">⏰</span>
      <div>
        <p class="trial-title">Período de Teste</p>
        <p class="trial-text">
          Seu período de teste termina em {{ getTrialDaysLeft() }} dias
        </p>
      </div>
    </div>

    <!-- Upgrade CTA -->
    <div v-if="shouldShowUpgradeCTA()" class="upgrade-cta">
      <div class="cta-content">
        <h3 class="cta-title">⚠️ Você está próximo do limite!</h3>
        <p class="cta-text">
          Faça upgrade do seu plano para continuar crescendo sem interrupções.
        </p>
      </div>
      <button @click="$emit('upgrade')" class="cta-button">
        Ver Planos Disponíveis
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const props = defineProps({
  tenantId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['upgrade'])

const loading = ref(true)
const error = ref(null)
const usage = ref({
  plan: '',
  limits: {
    users: { max: 0, current: 0, available: 0 },
    vehicles: { max: 0, current: 0, available: 0 },
    orders_per_month: { max: 0, current: 0, available: 0 }
  },
  trial_ends_at: null,
  is_trial: false
})

const planName = computed(() => {
  const names = {
    'starter': 'Starter',
    'professional': 'Professional',
    'enterprise': 'Enterprise'
  }
  return names[usage.value.plan] || usage.value.plan
})

async function loadUsage() {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`/api/tenants/${props.tenantId}/usage`)
    usage.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erro ao carregar estatísticas'
  } finally {
    loading.value = false
  }
}

function formatLimit(value) {
  return value === 'ilimitado' ? '∞' : value
}

function getProgressWidth(limit) {
  if (limit.max === 'ilimitado') return '100%'
  const percentage = (limit.current / limit.max) * 100
  return `${Math.min(percentage, 100)}%`
}

function getProgressClass(limit) {
  if (limit.max === 'ilimitado') return 'bg-blue-500'
  
  const percentage = (limit.current / limit.max) * 100
  if (percentage >= 90) return 'bg-red-500'
  if (percentage >= 75) return 'bg-yellow-500'
  return 'bg-green-500'
}

function getAvailableText(available, resource) {
  if (available === 'ilimitado') return 'Ilimitado'
  if (available === 0) return `⚠️ Limite atingido`
  if (available <= 2) return `⚠️ Apenas ${available} ${resource} disponíveis`
  return `${available} ${resource} disponíveis`
}

function getPlanBadgeClass() {
  const classes = {
    'starter': 'badge-starter',
    'professional': 'badge-professional',
    'enterprise': 'badge-enterprise'
  }
  return classes[usage.value.plan] || 'badge-starter'
}

function getCurrentMonth() {
  const months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
  return months[new Date().getMonth()]
}

function getTrialDaysLeft() {
  if (!usage.value.trial_ends_at) return 0
  const end = new Date(usage.value.trial_ends_at)
  const now = new Date()
  const diff = Math.ceil((end - now) / (1000 * 60 * 60 * 24))
  return Math.max(0, diff)
}

function shouldShowUpgradeCTA() {
  const limits = usage.value.limits
  
  // Mostrar se qualquer recurso estiver acima de 80%
  for (const limit of Object.values(limits)) {
    if (limit.max !== 'ilimitado') {
      const percentage = (limit.current / limit.max) * 100
      if (percentage >= 80) return true
    }
  }
  
  return false
}

onMounted(() => {
  loadUsage()
  
  // Atualizar a cada 30 segundos
  setInterval(loadUsage, 30000)
})
</script>

<style scoped>
.plan-usage-dashboard {
  @apply bg-white rounded-xl shadow-lg p-6 space-y-6;
}

.dashboard-header {
  @apply flex items-center justify-between pb-4 border-b border-gray-200;
}

.header-content {
  @apply flex items-center gap-4;
}

.plan-badge {
  @apply px-4 py-1 rounded-full text-sm font-semibold;
}

.badge-starter {
  @apply bg-blue-100 text-blue-700;
}

.badge-professional {
  @apply bg-purple-100 text-purple-700;
}

.badge-enterprise {
  @apply bg-gradient-to-r from-yellow-100 to-orange-100 text-orange-700;
}

.upgrade-btn {
  @apply px-6 py-2 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-lg font-semibold hover:scale-105 transition-transform;
}

.loading-state, .error-state {
  @apply flex flex-col items-center justify-center py-12 text-gray-600;
}

.spinner {
  @apply w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-4;
}

.retry-btn {
  @apply mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700;
}

.usage-grid {
  @apply grid grid-cols-1 md:grid-cols-3 gap-6;
}

.usage-card {
  @apply bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-200 hover:shadow-md transition-shadow;
}

.card-header {
  @apply flex items-start gap-3 mb-4;
}

.icon-wrapper {
  @apply w-12 h-12 rounded-xl flex items-center justify-center;
}

.card-title {
  @apply text-lg font-bold text-gray-900;
}

.card-subtitle {
  @apply text-sm text-gray-600;
}

.usage-stats {
  @apply space-y-3;
}

.stat-numbers {
  @apply flex items-baseline gap-2;
}

.stat-numbers .current {
  @apply text-3xl font-bold text-gray-900;
}

.stat-numbers .separator {
  @apply text-2xl text-gray-400;
}

.stat-numbers .max {
  @apply text-2xl font-semibold text-gray-600;
}

.progress-bar {
  @apply w-full h-3 bg-gray-200 rounded-full overflow-hidden;
}

.progress-fill {
  @apply h-full transition-all duration-500 ease-out;
}

.available-text {
  @apply text-sm font-medium text-gray-700;
}

.trial-banner {
  @apply flex items-center gap-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg;
}

.trial-icon {
  @apply text-2xl;
}

.trial-title {
  @apply font-bold text-yellow-900;
}

.trial-text {
  @apply text-sm text-yellow-800;
}

.upgrade-cta {
  @apply flex items-center justify-between p-6 bg-gradient-to-r from-blue-50 to-cyan-50 border-2 border-blue-200 rounded-xl;
}

.cta-content {
  @apply flex-1;
}

.cta-title {
  @apply text-lg font-bold text-gray-900 mb-1;
}

.cta-text {
  @apply text-gray-700;
}

.cta-button {
  @apply px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-lg font-bold hover:scale-105 transition-transform shadow-lg;
}
</style>
