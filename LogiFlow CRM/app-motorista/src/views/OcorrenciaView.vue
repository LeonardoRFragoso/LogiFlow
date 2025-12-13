<template>
  <div class="app-page">
    <!-- Header -->
    <header class="page-header-simple" style="background: linear-gradient(135deg, rgba(194, 65, 12, 0.95) 0%, rgba(234, 88, 12, 0.95) 100%);">
      <div class="flex items-center gap-3">
        <button @click="router.back()" class="header-back-btn">←</button>
        <div>
          <p class="text-white/70 text-xs">Registrar Ocorrência</p>
          <h1 class="text-lg font-bold">{{ entrega?.numero }}</h1>
        </div>
      </div>
    </header>

    <main class="px-4 py-4">
      <!-- Tipo de Ocorrência -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h3 class="text-sm font-semibold text-gray-500 mb-4">TIPO DE OCORRÊNCIA</h3>
        
        <div class="grid grid-cols-2 gap-2">
          <button 
            v-for="option in tiposOcorrencia"
            :key="option.value"
            @click="tipoSelecionado = option.value"
            :class="[
              'p-3 rounded-xl border-2 text-center transition',
              tipoSelecionado === option.value 
                ? 'border-orange-500 bg-orange-50' 
                : 'border-gray-200'
            ]"
          >
            <span class="text-2xl block mb-1">{{ option.icon }}</span>
            <span class="text-xs text-gray-700">{{ option.label }}</span>
          </button>
        </div>
      </div>

      <!-- Descrição -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <label class="block text-sm font-semibold text-gray-500 mb-2">DESCRIÇÃO *</label>
        <textarea 
          v-model="descricao"
          rows="4"
          required
          placeholder="Descreva o ocorrido em detalhes..."
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 resize-none"
        ></textarea>
      </div>

      <!-- Fotos -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h3 class="text-sm font-semibold text-gray-500 mb-3">FOTOS (opcional)</h3>
        
        <div class="flex gap-2 overflow-x-auto pb-2">
          <button 
            @click="adicionarFoto"
            class="w-20 h-20 border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center flex-shrink-0"
          >
            <span class="text-2xl">📷</span>
            <span class="text-xs text-gray-500">Adicionar</span>
          </button>
          
          <div 
            v-for="(foto, index) in fotos" 
            :key="index"
            class="w-20 h-20 bg-gray-200 rounded-xl flex items-center justify-center flex-shrink-0 relative"
          >
            <span class="text-3xl">🖼️</span>
            <button 
              @click="removerFoto(index)"
              class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-xs"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <!-- Localização -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-semibold text-gray-500">LOCALIZAÇÃO</h3>
            <p class="text-xs text-gray-400">{{ posicaoAtual ? 'Capturada ✓' : 'Não capturada' }}</p>
          </div>
          <button 
            @click="capturarLocalizacao"
            class="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm"
          >
            📍 {{ posicaoAtual ? 'Atualizar' : 'Capturar' }}
          </button>
        </div>
      </div>

      <!-- Botão Enviar -->
      <button 
        @click="enviarOcorrencia"
        :disabled="!tipoSelecionado || !descricao || loading"
        class="w-full bg-orange-600 text-white py-4 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        <svg v-if="loading" class="animate-spin h-5 w-5" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Enviando...' : 'Enviar Ocorrência' }}
      </button>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEntregasStore } from '../stores/entregas'

const router = useRouter()
const route = useRoute()
const entregasStore = useEntregasStore()

const entrega = computed(() => entregasStore.entregaAtual)
const tipoSelecionado = ref('')
const descricao = ref('')
const fotos = ref([])
const posicaoAtual = ref(null)
const loading = ref(false)

const tiposOcorrencia = [
  { value: 'avaria', label: 'Avaria', icon: '📦' },
  { value: 'atraso', label: 'Atraso', icon: '⏰' },
  { value: 'extravio', label: 'Extravio', icon: '❓' },
  { value: 'recusa', label: 'Recusa', icon: '🚫' },
  { value: 'endereco_incorreto', label: 'Endereço Incorreto', icon: '📍' },
  { value: 'acidente', label: 'Acidente', icon: '🚗' },
  { value: 'problema_veiculo', label: 'Problema Veículo', icon: '🔧' },
  { value: 'outro', label: 'Outro', icon: '📝' }
]

onMounted(() => {
  if (!entregasStore.entregaAtual) {
    entregasStore.carregarEntrega(route.params.id)
  }
  capturarLocalizacao()
})

function adicionarFoto() {
  fotos.value.push(`foto_${fotos.value.length + 1}.jpg`)
  alert('Câmera simulada - foto adicionada')
}

function removerFoto(index) {
  fotos.value.splice(index, 1)
}

function capturarLocalizacao() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        posicaoAtual.value = {
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude
        }
      },
      (err) => {
        console.error('Erro GPS:', err)
        alert('Não foi possível capturar a localização')
      }
    )
  }
}

async function enviarOcorrencia() {
  if (!tipoSelecionado.value || !descricao.value) return
  
  loading.value = true
  
  const result = await entregasStore.registrarOcorrencia(route.params.id, {
    tipo: tipoSelecionado.value,
    descricao: descricao.value,
    fotos: fotos.value,
    posicao: posicaoAtual.value
  })
  
  loading.value = false
  
  if (result.success) {
    alert('Ocorrência registrada com sucesso!')
    router.push('/')
  } else {
    alert(result.message || 'Erro ao registrar ocorrência')
  }
}
</script>
