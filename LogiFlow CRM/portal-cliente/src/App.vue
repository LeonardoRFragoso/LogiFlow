<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const codigoRastreio = ref('')
const loading = ref(false)
const error = ref('')
const resultado = ref(null)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function buscarTracking() {
  if (!codigoRastreio.value.trim()) {
    error.value = 'Digite o código de rastreio'
    return
  }
  
  loading.value = true
  error.value = ''
  resultado.value = null
  
  try {
    const response = await axios.get(`${API_URL}/demo/rastreamento/${codigoRastreio.value}`)
    const data = response.data.data
    resultado.value = {
      codigo_rastreio: data.codigo,
      status: data.status,
      status_descricao: data.status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      ultima_atualizacao: new Date().toISOString(),
      previsao_entrega: data.previsao_entrega,
      eventos: data.eventos?.filter(e => e) || []
    }
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = 'Código de rastreio não encontrado. Tente: ENT-2024-0001'
    } else {
      // Dados de demonstração se API não disponível
      resultado.value = getDadosDemo()
    }
  } finally {
    loading.value = false
  }
}

function getDadosDemo() {
  return {
    codigo_rastreio: codigoRastreio.value,
    status: 'em_transito',
    status_descricao: 'Em trânsito',
    ultima_atualizacao: new Date().toISOString(),
    previsao_entrega: new Date(Date.now() + 3600000 * 4).toISOString(),
    eventos: [
      {
        data: new Date().toISOString(),
        descricao: 'Carga em trânsito para o destino',
        local: 'Rodovia Anhanguera, km 45'
      },
      {
        data: new Date(Date.now() - 3600000 * 2).toISOString(),
        descricao: 'Carga coletada',
        local: 'São Paulo - SP'
      },
      {
        data: new Date(Date.now() - 3600000 * 4).toISOString(),
        descricao: 'Pedido confirmado',
        local: 'Central LogiFlow'
      }
    ]
  }
}

function formatarData(data) {
  if (!data) return ''
  return new Date(data).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getStatusClass(status) {
  const classes = {
    aguardando_coleta: 'status-aguardando',
    em_coleta: 'status-coleta',
    coletado: 'status-coletado',
    em_transito: 'status-transito',
    em_rota_entrega: 'status-entrega',
    entregue: 'status-concluido'
  }
  return classes[status] || 'status-transito'
}

function novaConsulta() {
  resultado.value = null
  codigoRastreio.value = ''
}
</script>

<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="header-gradient text-white py-6 px-4">
      <div class="max-w-3xl mx-auto">
        <div class="flex items-center justify-center gap-3 mb-2">
          <div class="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
            <span class="text-2xl">🚛</span>
          </div>
          <div>
            <h1 class="text-2xl font-bold">LogiFlow</h1>
            <p class="text-white/70 text-sm">Rastreamento de Entregas</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-3xl mx-auto px-4 -mt-8">
      <!-- Search Card -->
      <div class="card mb-6" v-if="!resultado">
        <div class="text-center mb-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-2">Rastreie sua entrega</h2>
          <p class="text-gray-500 text-sm">Digite o código de rastreio para acompanhar seu pedido</p>
        </div>

        <form @submit.prevent="buscarTracking" class="space-y-4">
          <div class="relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-xl">🔍</span>
            <input
              v-model="codigoRastreio"
              type="text"
              placeholder="Ex: LF1234567890"
              class="input-field pl-12"
              :disabled="loading"
            />
          </div>

          <div v-if="error" class="alert-error">
            ⚠️ {{ error }}
          </div>

          <button type="submit" :disabled="loading" class="btn-primary">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Buscando...' : 'Rastrear' }}
          </button>
        </form>

        <div class="mt-6 pt-6 border-t border-gray-100 text-center">
          <p class="text-gray-400 text-xs">
            O código de rastreio foi enviado por email ou WhatsApp quando seu pedido foi confirmado
          </p>
        </div>
      </div>

      <!-- Result Card -->
      <div v-if="resultado" class="space-y-4">
        <!-- Status Header -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="text-gray-400 text-xs">Código de Rastreio</p>
              <p class="font-mono font-semibold text-gray-800">{{ resultado.codigo_rastreio }}</p>
            </div>
            <span :class="['status-badge', getStatusClass(resultado.status)]">
              {{ resultado.status_descricao }}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
            <div>
              <p class="text-gray-400 text-xs">Última Atualização</p>
              <p class="text-sm font-medium text-gray-700">{{ formatarData(resultado.ultima_atualizacao) }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs">Previsão de Entrega</p>
              <p class="text-sm font-medium text-green-600">{{ formatarData(resultado.previsao_entrega) }}</p>
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="card">
          <h3 class="text-sm font-semibold text-gray-500 mb-4">PROGRESSO DA ENTREGA</h3>
          <div class="progress-steps">
            <div class="progress-step completed">
              <div class="step-icon">✓</div>
              <span class="step-label">Confirmado</span>
            </div>
            <div class="progress-line completed"></div>
            <div class="progress-step completed">
              <div class="step-icon">✓</div>
              <span class="step-label">Coletado</span>
            </div>
            <div class="progress-line" :class="{ completed: ['em_transito', 'em_rota_entrega', 'entregue'].includes(resultado.status) }"></div>
            <div class="progress-step" :class="{ completed: ['em_transito', 'em_rota_entrega', 'entregue'].includes(resultado.status), active: resultado.status === 'em_transito' }">
              <div class="step-icon">{{ ['em_transito', 'em_rota_entrega', 'entregue'].includes(resultado.status) ? '✓' : '3' }}</div>
              <span class="step-label">Em Trânsito</span>
            </div>
            <div class="progress-line" :class="{ completed: resultado.status === 'entregue' }"></div>
            <div class="progress-step" :class="{ completed: resultado.status === 'entregue' }">
              <div class="step-icon">{{ resultado.status === 'entregue' ? '✓' : '4' }}</div>
              <span class="step-label">Entregue</span>
            </div>
          </div>
        </div>

        <!-- Timeline -->
        <div class="card">
          <h3 class="text-sm font-semibold text-gray-500 mb-4">HISTÓRICO DE MOVIMENTAÇÃO</h3>
          <div class="timeline">
            <div v-for="(evento, index) in resultado.eventos" :key="index" class="timeline-item">
              <div class="timeline-dot" :class="{ active: index === 0 }"></div>
              <div class="timeline-content">
                <p class="font-medium text-gray-800">{{ evento.descricao }}</p>
                <p class="text-sm text-gray-500">{{ evento.local }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ formatarData(evento.data) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- New Search Button -->
        <button @click="novaConsulta" class="btn-secondary w-full">
          🔍 Nova Consulta
        </button>
      </div>
    </main>

    <!-- Footer -->
    <footer class="text-center py-6 mt-8">
      <p class="text-gray-400 text-xs">© 2025 LogiFlow CRM - Todos os direitos reservados</p>
      <p class="text-gray-300 text-xs mt-1">Sua transportadora no controle</p>
    </footer>
  </div>
</template>

<style scoped>
.header-gradient {
  background: linear-gradient(135deg, rgba(30, 64, 175, 0.95) 0%, rgba(5, 150, 105, 0.95) 100%);
  padding-bottom: 4rem;
}

.card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.input-field {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f9fafb;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 1rem;
  background: #f3f4f6;
  color: #374151;
  font-weight: 500;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.alert-error {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.status-badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-weight: 500;
}

.status-aguardando { background: #fef3c7; color: #92400e; }
.status-coleta { background: #fed7aa; color: #9a3412; }
.status-coletado { background: #dbeafe; color: #1e40af; }
.status-transito { background: #dbeafe; color: #1e40af; }
.status-entrega { background: #d1fae5; color: #065f46; }
.status-concluido { background: #d1fae5; color: #065f46; }

/* Progress Steps */
.progress-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #e5e7eb;
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.progress-step.completed .step-icon {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: white;
}

.progress-step.active .step-icon {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
}

.step-label {
  font-size: 0.7rem;
  color: #6b7280;
  text-align: center;
}

.progress-line {
  flex: 1;
  height: 3px;
  background: #e5e7eb;
  margin: 0 0.25rem;
  margin-bottom: 1.5rem;
}

.progress-line.completed {
  background: linear-gradient(90deg, #059669, #10b981);
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 1.5rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.4rem;
  top: 0.5rem;
  bottom: 0.5rem;
  width: 2px;
  background: #e5e7eb;
}

.timeline-item {
  position: relative;
  padding-bottom: 1.5rem;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -1.5rem;
  top: 0.25rem;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  background: #d1d5db;
  border: 2px solid white;
}

.timeline-dot.active {
  background: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.timeline-content {
  padding-left: 0.5rem;
}
</style>
