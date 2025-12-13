<template>
  <div class="app-page" style="padding-bottom: 6rem;">
    <!-- Header -->
    <header class="page-header-simple">
      <div class="flex items-center gap-3 mb-4">
        <button @click="router.back()" class="header-back-btn">←</button>
        <div>
          <p class="text-white/70 text-xs">Entrega</p>
          <h1 class="text-lg font-bold">{{ entrega?.numero || 'Carregando...' }}</h1>
        </div>
      </div>
      
      <div v-if="entrega" class="flex items-center gap-2">
        <span :class="getStatusClass(entrega.status)" class="text-xs px-3 py-1 rounded-full">
          {{ getStatusLabel(entrega.status) }}
        </span>
        <span v-if="entrega.prioridade === 'urgente'" class="text-xs px-3 py-1 rounded-full bg-red-500 text-white">
          🔥 URGENTE
        </span>
      </div>
    </header>

    <main v-if="entrega" class="px-4 -mt-2">
      <!-- Info Card -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h2 class="font-semibold text-gray-800 mb-3">{{ entrega.cliente_nome }}</h2>
        
        <!-- Origem -->
        <div class="flex gap-3 mb-4">
          <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-green-600 text-sm">A</span>
          </div>
          <div>
            <p class="text-xs text-gray-400">Origem</p>
            <p class="text-sm text-gray-800">{{ entrega.origem?.logradouro }}</p>
            <p class="text-xs text-gray-500">{{ entrega.origem?.cidade }}/{{ entrega.origem?.uf }}</p>
          </div>
        </div>

        <!-- Linha conectora -->
        <div class="ml-4 border-l-2 border-dashed border-gray-200 h-4"></div>

        <!-- Destino -->
        <div class="flex gap-3">
          <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-red-600 text-sm">B</span>
          </div>
          <div>
            <p class="text-xs text-gray-400">Destino</p>
            <p class="text-sm text-gray-800">{{ entrega.destino?.logradouro }}</p>
            <p class="text-xs text-gray-500">{{ entrega.destino?.cidade }}/{{ entrega.destino?.uf }}</p>
          </div>
        </div>

        <!-- Botão Navegar -->
        <button 
          @click="abrirMapa"
          class="w-full mt-4 bg-blue-50 text-blue-600 py-3 rounded-xl font-medium flex items-center justify-center gap-2"
        >
          🗺️ Abrir no Maps
        </button>
      </div>

      <!-- Contato -->
      <div v-if="entrega.destino?.contato_nome" class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h3 class="text-sm font-semibold text-gray-500 mb-3">CONTATO</h3>
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-gray-800">{{ entrega.destino.contato_nome }}</p>
            <p class="text-sm text-gray-500">{{ entrega.destino.contato_telefone }}</p>
          </div>
          <a 
            :href="`tel:${entrega.destino.contato_telefone}`"
            class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center"
          >
            <span class="text-xl">📞</span>
          </a>
        </div>
      </div>

      <!-- Detalhes -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h3 class="text-sm font-semibold text-gray-500 mb-3">DETALHES</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-xs text-gray-400">Peso</p>
            <p class="font-medium text-gray-800">{{ entrega.peso_total_kg }} kg</p>
          </div>
          <div>
            <p class="text-xs text-gray-400">Valor</p>
            <p class="font-medium text-gray-800">R$ {{ entrega.valor_total?.toFixed(2) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-400">Previsão</p>
            <p class="font-medium text-gray-800">{{ formatarData(entrega.data_entrega_prevista) }}</p>
          </div>
          <div>
            <p class="text-xs text-gray-400">Código Rastreio</p>
            <p class="font-medium text-gray-800 text-sm">{{ entrega.codigo_rastreio }}</p>
          </div>
        </div>
      </div>

      <!-- Observações -->
      <div v-if="entrega.observacoes_entrega" class="bg-yellow-50 rounded-2xl p-4 mb-4">
        <h3 class="text-sm font-semibold text-yellow-700 mb-2">⚠️ OBSERVAÇÕES</h3>
        <p class="text-sm text-yellow-800">{{ entrega.observacoes_entrega }}</p>
      </div>
    </main>

    <!-- Loading -->
    <div v-else class="px-4 py-12 text-center text-gray-400">
      <div class="animate-spin w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-2"></div>
      Carregando...
    </div>

    <!-- Bottom Actions -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4">
      <div class="flex gap-3">
        <button 
          @click="router.push(`/entrega/${entrega?.id}/ocorrencia`)"
          class="flex-1 bg-orange-50 text-orange-600 py-3 rounded-xl font-medium"
        >
          ⚠️ Ocorrência
        </button>
        <button 
          @click="router.push(`/entrega/${entrega?.id}/status`)"
          class="flex-1 bg-green-600 text-white py-3 rounded-xl font-medium"
        >
          ✓ Atualizar Status
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEntregasStore } from '../stores/entregas'

const router = useRouter()
const route = useRoute()
const entregasStore = useEntregasStore()

const entrega = computed(() => entregasStore.entregaAtual)

onMounted(() => {
  entregasStore.carregarEntrega(route.params.id)
})

function formatarData(data) {
  if (!data) return '--'
  return new Date(data).toLocaleString('pt-BR', { 
    day: '2-digit', 
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getStatusLabel(status) {
  const labels = {
    aguardando_coleta: 'Aguardando Coleta',
    em_coleta: 'Em Coleta',
    coletado: 'Coletado',
    em_transito: 'Em Trânsito',
    em_rota_entrega: 'Saiu para Entrega',
    entregue: 'Entregue'
  }
  return labels[status] || status
}

function getStatusClass(status) {
  const classes = {
    aguardando_coleta: 'bg-yellow-400 text-yellow-900',
    em_coleta: 'bg-orange-400 text-white',
    coletado: 'bg-blue-400 text-white',
    em_transito: 'bg-blue-500 text-white',
    em_rota_entrega: 'bg-green-400 text-white',
    entregue: 'bg-green-600 text-white'
  }
  return classes[status] || 'bg-gray-400 text-white'
}

function abrirMapa() {
  if (!entrega.value) return
  const endereco = encodeURIComponent(
    `${entrega.value.destino?.logradouro}, ${entrega.value.destino?.cidade}, ${entrega.value.destino?.uf}`
  )
  window.open(`https://www.google.com/maps/search/?api=1&query=${endereco}`, '_blank')
}
</script>
