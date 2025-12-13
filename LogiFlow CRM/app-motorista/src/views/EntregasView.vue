<template>
  <div class="app-page">
    <!-- Header -->
    <header class="page-header-simple">
      <div class="flex items-center gap-3">
        <button @click="router.back()" class="header-back-btn">←</button>
        <h1 class="text-xl font-bold">Minhas Entregas</h1>
      </div>
    </header>

    <!-- Tabs -->
    <div class="bg-white border-b border-gray-200 px-4 flex gap-4">
      <button 
        @click="tab = 'ativas'"
        :class="tab === 'ativas' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500'"
        class="py-3 border-b-2 font-medium text-sm"
      >
        Ativas ({{ entregasAtivas.length }})
      </button>
      <button 
        @click="tab = 'concluidas'"
        :class="tab === 'concluidas' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500'"
        class="py-3 border-b-2 font-medium text-sm"
      >
        Concluídas ({{ entregasConcluidas.length }})
      </button>
    </div>

    <!-- Content -->
    <main class="px-4 py-4">
      <div v-if="loading" class="py-12 text-center text-gray-400">
        <div class="animate-spin w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-2"></div>
        Carregando entregas...
      </div>

      <div v-else-if="listaAtual.length === 0" class="py-12 text-center text-gray-400">
        <span class="text-5xl block mb-3">📭</span>
        <p>Nenhuma entrega {{ tab === 'ativas' ? 'ativa' : 'concluída' }}</p>
      </div>

      <div v-else class="space-y-3">
        <div 
          v-for="entrega in listaAtual" 
          :key="entrega.id"
          @click="router.push(`/entrega/${entrega.id}`)"
          class="bg-white rounded-xl shadow-sm p-4 cursor-pointer active:bg-gray-50"
        >
          <div class="flex items-start justify-between mb-2">
            <div>
              <span class="text-xs text-gray-400">{{ entrega.numero }}</span>
              <h3 class="font-semibold text-gray-800">{{ entrega.cliente_nome }}</h3>
            </div>
            <span :class="getStatusClass(entrega.status)" class="text-xs px-2 py-1 rounded-full">
              {{ getStatusLabel(entrega.status) }}
            </span>
          </div>

          <div class="flex items-center gap-2 text-sm text-gray-500 mb-3">
            <span>📍</span>
            <span>{{ entrega.destino?.cidade }}/{{ entrega.destino?.uf }}</span>
          </div>

          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center gap-4">
              <span class="text-gray-400">
                📦 {{ entrega.peso_total_kg }}kg
              </span>
              <span v-if="entrega.prioridade === 'urgente'" class="text-red-500 font-medium">
                🔥 Urgente
              </span>
            </div>
            <span class="text-blue-600 font-medium">
              {{ formatarHora(entrega.data_entrega_prevista) }}
            </span>
          </div>
        </div>
      </div>
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-3 flex justify-around">
      <button @click="router.push('/')" class="flex flex-col items-center text-gray-400">
        <span class="text-xl">🏠</span>
        <span class="text-xs mt-1">Início</span>
      </button>
      <button class="flex flex-col items-center text-blue-600">
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
import { useEntregasStore } from '../stores/entregas'

const router = useRouter()
const entregasStore = useEntregasStore()

const tab = ref('ativas')
const loading = computed(() => entregasStore.loading)
const entregasAtivas = computed(() => entregasStore.entregasAtivas)
const entregasConcluidas = computed(() => entregasStore.entregasConcluidas)
const listaAtual = computed(() => tab.value === 'ativas' ? entregasAtivas.value : entregasConcluidas.value)

onMounted(() => {
  entregasStore.carregarEntregas()
})

function formatarHora(data) {
  if (!data) return '--:--'
  return new Date(data).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function getStatusLabel(status) {
  const labels = {
    aguardando_coleta: 'Aguardando',
    em_coleta: 'Em Coleta',
    coletado: 'Coletado',
    em_transito: 'Em Trânsito',
    em_rota_entrega: 'Saiu p/ Entrega',
    entregue: 'Entregue',
    cancelado: 'Cancelado'
  }
  return labels[status] || status
}

function getStatusClass(status) {
  const classes = {
    aguardando_coleta: 'bg-yellow-100 text-yellow-700',
    em_coleta: 'bg-orange-100 text-orange-700',
    coletado: 'bg-blue-100 text-blue-700',
    em_transito: 'bg-blue-100 text-blue-700',
    em_rota_entrega: 'bg-green-100 text-green-700',
    entregue: 'bg-green-100 text-green-700',
    cancelado: 'bg-red-100 text-red-700'
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}
</script>
