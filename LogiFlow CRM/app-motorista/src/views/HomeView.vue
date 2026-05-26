<template>
  <div class="app-container">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div>
          <p class="header-greeting">{{ greeting }},</p>
          <h1 class="header-name">{{ user?.nome || 'Motorista' }} 👋</h1>
        </div>
        <button @click="router.push('/perfil')" class="avatar-button">
          <span class="text-lg">👤</span>
        </button>
      </div>
      
      <!-- Stats KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card kpi-blue">
          <div class="kpi-icon">🚚</div>
          <p class="kpi-value">{{ entregasAtivas.length }}</p>
          <p class="kpi-label">Ativas</p>
        </div>
        <div class="kpi-card kpi-green">
          <div class="kpi-icon">📦</div>
          <p class="kpi-value">{{ entregasHoje }}</p>
          <p class="kpi-label">Hoje</p>
        </div>
        <div class="kpi-card kpi-orange">
          <div class="kpi-icon">✅</div>
          <p class="kpi-value">{{ entregasConcluidas.length }}</p>
          <p class="kpi-label">Concluídas</p>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-4 -mt-4">
      <!-- Quick Actions -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h2 class="text-sm font-semibold text-gray-500 mb-3">AÇÕES RÁPIDAS</h2>
        <div class="grid grid-cols-4 gap-2">
          <button @click="router.push('/entregas')" class="flex flex-col items-center p-3 rounded-xl bg-blue-50 text-blue-600">
            <span class="text-2xl mb-1">📦</span>
            <span class="text-xs">Entregas</span>
          </button>
          <button @click="iniciarGPS" class="flex flex-col items-center p-3 rounded-xl bg-green-50 text-green-600">
            <span class="text-2xl mb-1">📍</span>
            <span class="text-xs">GPS</span>
          </button>
          <button @click="abrirCamera" class="flex flex-col items-center p-3 rounded-xl bg-purple-50 text-purple-600">
            <span class="text-2xl mb-1">📷</span>
            <span class="text-xs">Foto</span>
          </button>
          <button @click="ligarSuporte" class="flex flex-col items-center p-3 rounded-xl bg-orange-50 text-orange-600">
            <span class="text-2xl mb-1">📞</span>
            <span class="text-xs">Suporte</span>
          </button>
        </div>
      </div>

      <!-- Próxima Entrega -->
      <div v-if="proximaEntrega" class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-gray-500">PRÓXIMA ENTREGA</h2>
          <span :class="getPrioridadeClass(proximaEntrega.prioridade)" class="text-xs px-2 py-1 rounded-full">
            {{ proximaEntrega.prioridade?.toUpperCase() }}
          </span>
        </div>
        
        <div class="border border-gray-100 rounded-xl p-3" @click="router.push(`/entrega/${proximaEntrega.id}`)">
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <span class="text-xl">📦</span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-gray-800 truncate">{{ proximaEntrega.cliente_nome }}</p>
              <p class="text-sm text-gray-500 truncate">{{ proximaEntrega.destino?.logradouro }}</p>
              <p class="text-sm text-gray-400">{{ proximaEntrega.destino?.cidade }}/{{ proximaEntrega.destino?.uf }}</p>
            </div>
            <div class="text-right flex-shrink-0">
              <p class="text-xs text-gray-400">Previsão</p>
              <p class="text-sm font-medium text-blue-600">{{ formatarHora(proximaEntrega.data_entrega_prevista) }}</p>
            </div>
          </div>
          
          <div class="flex gap-2 mt-3">
            <button 
              @click.stop="abrirMapa(proximaEntrega)"
              class="flex-1 bg-blue-50 text-blue-600 py-2 rounded-lg text-sm font-medium"
            >
              🗺️ Navegar
            </button>
            <button 
              @click.stop="router.push(`/entrega/${proximaEntrega.id}/status`)"
              class="flex-1 bg-green-50 text-green-600 py-2 rounded-lg text-sm font-medium"
            >
              ✓ Atualizar
            </button>
          </div>
        </div>
      </div>

      <!-- Lista de Entregas -->
      <div class="bg-white rounded-2xl shadow-sm p-4">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-sm font-semibold text-gray-500">ENTREGAS DO DIA</h2>
          <button @click="router.push('/entregas')" class="text-blue-600 text-sm">Ver todas</button>
        </div>
        
        <div v-if="loading" class="py-8 text-center text-gray-400">
          <div class="animate-spin w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-2"></div>
          Carregando...
        </div>
        
        <div v-else-if="entregasAtivas.length === 0" class="py-8 text-center text-gray-400">
          <span class="text-4xl mb-2 block">🎉</span>
          Nenhuma entrega pendente!
        </div>
        
        <div v-else class="space-y-2">
          <div 
            v-for="entrega in entregasAtivas.slice(0, 3)" 
            :key="entrega.id"
            @click="router.push(`/entrega/${entrega.id}`)"
            class="flex items-center gap-3 p-3 border border-gray-100 rounded-xl cursor-pointer hover:bg-gray-50"
          >
            <div :class="getStatusColor(entrega.status)" class="w-2 h-2 rounded-full"></div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-800 truncate">{{ entrega.cliente_nome }}</p>
              <p class="text-xs text-gray-400">{{ entrega.destino?.cidade }}/{{ entrega.destino?.uf }}</p>
            </div>
            <span class="text-gray-400">›</span>
          </div>
        </div>
      </div>
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-3 flex justify-around">
      <button class="flex flex-col items-center text-blue-600">
        <span class="text-xl">🏠</span>
        <span class="text-xs mt-1">Início</span>
      </button>
      <button @click="router.push('/entregas')" class="flex flex-col items-center text-gray-400">
        <span class="text-xl">📦</span>
        <span class="text-xs mt-1">Entregas</span>
      </button>
      <button @click="router.push('/perfil')" class="flex flex-col items-center text-gray-400">
        <span class="text-xl">👤</span>
        <span class="text-xs mt-1">Perfil</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useEntregasStore } from '../stores/entregas'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const entregasStore = useEntregasStore()

const user = computed(() => authStore.user)
const loading = computed(() => entregasStore.loading)
const entregasAtivas = computed(() => entregasStore.entregasAtivas)
const entregasConcluidas = computed(() => entregasStore.entregasConcluidas)
const proximaEntrega = computed(() => entregasAtivas.value[0])
const entregasHoje = computed(() => entregasAtivas.value.length)
const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Bom dia'
  if (hour < 18) return 'Boa tarde'
  return 'Boa noite'
})

onMounted(() => {
  entregasStore.carregarEntregas()
})

function formatarHora(data) {
  if (!data) return '--:--'
  return new Date(data).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function getStatusColor(status) {
  const colors = {
    aguardando_coleta: 'bg-yellow-400',
    em_coleta: 'bg-orange-400',
    coletado: 'bg-blue-400',
    em_transito: 'bg-blue-600',
    em_rota_entrega: 'bg-green-400',
    entregue: 'bg-green-600'
  }
  return colors[status] || 'bg-gray-400'
}

function getPrioridadeClass(prioridade) {
  const classes = {
    urgente: 'bg-red-100 text-red-600',
    alta: 'bg-orange-100 text-orange-600',
    normal: 'bg-blue-100 text-blue-600',
    baixa: 'bg-gray-100 text-gray-600'
  }
  return classes[prioridade] || classes.normal
}

async function iniciarGPS() {
  if (!navigator.geolocation) {
    alert('Geolocalização não suportada neste dispositivo.')
    return
  }
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      const { latitude, longitude, accuracy } = pos.coords
      const entregaAtiva = proximaEntrega.value
      if (!entregaAtiva) {
        alert(`📍 Localização obtida:\nLat: ${latitude.toFixed(5)}\nLng: ${longitude.toFixed(5)}\n\nNenhuma entrega ativa para enviar posição.`)
        return
      }
      try {
        const authStore = useAuthStore()
        const motorista_id = authStore.user?.id || authStore.user?.motorista_id
        await api.post('/api/v1/rastreamento/posicao', {
          entrega_id: entregaAtiva.id,
          motorista_id,
          latitude,
          longitude,
          precisao: accuracy
        })
        alert(`📍 Posição enviada!\nLat: ${latitude.toFixed(5)}\nLng: ${longitude.toFixed(5)}`)
      } catch (err) {
        console.error('Erro ao enviar posição:', err)
        alert(`📍 Posição obtida (falha ao enviar ao servidor):\nLat: ${latitude.toFixed(5)}\nLng: ${longitude.toFixed(5)}`)
      }
    },
    (err) => alert('Erro ao obter localização: ' + err.message),
    { enableHighAccuracy: true, timeout: 10000 }
  )
}

function abrirCamera() {
  alert('Funcionalidade de câmera será implementada')
}

function ligarSuporte() {
  window.location.href = 'tel:+5511999999999'
}

function abrirMapa(entrega) {
  const endereco = encodeURIComponent(
    `${entrega.destino?.logradouro}, ${entrega.destino?.cidade}, ${entrega.destino?.uf}`
  )
  window.open(`https://www.google.com/maps/search/?api=1&query=${endereco}`, '_blank')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  min-height: 100dvh;
  background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
  padding-bottom: 5rem;
}

.app-header {
  background: linear-gradient(135deg, rgba(30, 64, 175, 0.95) 0%, rgba(5, 150, 105, 0.95) 100%);
  color: white;
  padding: 3rem 1rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header-greeting {
  font-size: 0.875rem;
  opacity: 0.8;
}

.header-name {
  font-size: 1.5rem;
  font-weight: 700;
}

.avatar-button {
  width: 2.75rem;
  height: 2.75rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.avatar-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.kpi-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  padding: 1rem;
  text-align: center;
  transition: all 0.2s;
}

.kpi-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

.kpi-icon {
  font-size: 1.25rem;
  margin-bottom: 0.25rem;
}

.kpi-value {
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1;
}

.kpi-label {
  font-size: 0.7rem;
  opacity: 0.8;
  margin-top: 0.25rem;
}

/* Cards */
.card-modern {
  background: white;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
}

/* Quick Actions */
.quick-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
  border-radius: 0.75rem;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
  background: transparent;
}

.quick-action:active {
  transform: scale(0.95);
}

/* Bottom Nav */
nav {
  background: white;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
}

nav button {
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

nav button:active {
  transform: scale(0.9);
}
</style>
