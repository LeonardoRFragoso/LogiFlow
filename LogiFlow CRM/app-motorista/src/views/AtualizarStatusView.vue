<template>
  <div class="app-page">
    <!-- Header -->
    <header class="page-header-simple">
      <div class="flex items-center gap-3">
        <button @click="router.back()" class="header-back-btn">←</button>
        <div>
          <p class="text-white/70 text-xs">Atualizar Status</p>
          <h1 class="text-lg font-bold">{{ entrega?.numero }}</h1>
        </div>
      </div>
    </header>

    <main class="px-4 py-4">
      <!-- Status Options -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h3 class="text-sm font-semibold text-gray-500 mb-4">SELECIONE O NOVO STATUS</h3>
        
        <div class="space-y-2">
          <button 
            v-for="option in statusOptions"
            :key="option.value"
            @click="statusSelecionado = option.value"
            :class="[
              'w-full p-4 rounded-xl border-2 text-left transition flex items-center gap-3',
              statusSelecionado === option.value 
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-200 hover:border-gray-300'
            ]"
          >
            <span class="text-2xl">{{ option.icon }}</span>
            <div>
              <p class="font-medium text-gray-800">{{ option.label }}</p>
              <p class="text-xs text-gray-500">{{ option.desc }}</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Campos Adicionais para Entrega -->
      <div v-if="statusSelecionado === 'entregue'" class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <h3 class="text-sm font-semibold text-gray-500 mb-4">DADOS DA ENTREGA</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-gray-600 mb-1">Nome do Recebedor *</label>
            <input 
              v-model="recebedorNome"
              type="text"
              required
              placeholder="Digite o nome"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label class="block text-sm text-gray-600 mb-1">Documento (opcional)</label>
            <input 
              v-model="recebedorDoc"
              type="text"
              placeholder="RG ou CPF"
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- Foto do Comprovante -->
          <div>
            <label class="block text-sm text-gray-600 mb-2">Foto do Comprovante</label>
            <button 
              @click="tirarFoto"
              class="w-full border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-blue-500 transition"
            >
              <span class="text-3xl block mb-2">📷</span>
              <span class="text-sm text-gray-500">
                {{ fotoUrl ? 'Foto capturada ✓' : 'Toque para tirar foto' }}
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Observações -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <label class="block text-sm font-semibold text-gray-500 mb-2">OBSERVAÇÕES (opcional)</label>
        <textarea 
          v-model="observacao"
          rows="3"
          placeholder="Adicione uma observação..."
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>
      </div>

      <!-- Botão Confirmar -->
      <button 
        @click="confirmarStatus"
        :disabled="!statusSelecionado || loading || (statusSelecionado === 'entregue' && !recebedorNome)"
        class="w-full bg-green-600 text-white py-4 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        <svg v-if="loading" class="animate-spin h-5 w-5" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
        </svg>
        {{ loading ? 'Atualizando...' : 'Confirmar Atualização' }}
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
const statusSelecionado = ref('')
const observacao = ref('')
const recebedorNome = ref('')
const recebedorDoc = ref('')
const fotoUrl = ref('')
const loading = ref(false)

const statusOptions = [
  { value: 'em_coleta', label: 'A caminho da Coleta', desc: 'Saindo para buscar a carga', icon: '🚗' },
  { value: 'coletado', label: 'Carga Coletada', desc: 'Mercadoria foi coletada', icon: '📦' },
  { value: 'em_transito', label: 'Em Trânsito', desc: 'A caminho do destino', icon: '🚛' },
  { value: 'em_rota_entrega', label: 'Saiu para Entrega', desc: 'Próximo ao destino final', icon: '📍' },
  { value: 'entregue', label: 'Entregue', desc: 'Entrega concluída com sucesso', icon: '✅' },
  { value: 'tentativa_falha', label: 'Tentativa sem Sucesso', desc: 'Não foi possível entregar', icon: '❌' }
]

onMounted(() => {
  if (!entregasStore.entregaAtual) {
    entregasStore.carregarEntrega(route.params.id)
  }
})

function tirarFoto() {
  // Simular captura de foto
  fotoUrl.value = 'foto_capturada.jpg'
  alert('Funcionalidade de câmera - foto simulada')
}

async function confirmarStatus() {
  if (!statusSelecionado.value) return
  
  loading.value = true
  
  const dados = {
    observacao: observacao.value
  }
  
  if (statusSelecionado.value === 'entregue') {
    dados.recebedor_nome = recebedorNome.value
    dados.recebedor_documento = recebedorDoc.value
    dados.foto_comprovante_url = fotoUrl.value
  }
  
  const result = await entregasStore.atualizarStatus(
    route.params.id,
    statusSelecionado.value,
    dados
  )
  
  loading.value = false
  
  if (result.success) {
    alert('Status atualizado com sucesso!')
    router.push('/')
  } else {
    alert(result.message || 'Erro ao atualizar status')
  }
}
</script>
