<template>
  <div class="app-page">
    <!-- Header -->
    <header class="page-header">
      <div class="flex items-center gap-3 mb-6">
        <button @click="router.back()" class="header-back-btn">←</button>
        <h1 class="text-xl font-bold">Meu Perfil</h1>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
          <span class="text-3xl">👤</span>
        </div>
        <div>
          <h2 class="text-lg font-bold">{{ user?.nome || 'Motorista' }}</h2>
          <p class="text-white/70 text-sm">{{ user?.email }}</p>
        </div>
      </div>
    </header>

    <main class="px-4 -mt-4">
      <!-- Stats -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <p class="text-2xl font-bold text-blue-600">{{ stats.entregasHoje }}</p>
            <p class="text-xs text-gray-500">Hoje</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-green-600">{{ stats.entregasMes }}</p>
            <p class="text-xs text-gray-500">Este mês</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-purple-600">{{ stats.kmRodados }}</p>
            <p class="text-xs text-gray-500">km rodados</p>
          </div>
        </div>
      </div>

      <!-- Menu -->
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden mb-4">
        <button class="w-full px-4 py-4 flex items-center gap-3 border-b border-gray-100 text-left">
          <span class="text-xl">📱</span>
          <div class="flex-1">
            <p class="font-medium text-gray-800">Dados Pessoais</p>
            <p class="text-xs text-gray-500">Telefone, endereço, etc.</p>
          </div>
          <span class="text-gray-400">›</span>
        </button>
        
        <button class="w-full px-4 py-4 flex items-center gap-3 border-b border-gray-100 text-left">
          <span class="text-xl">🚗</span>
          <div class="flex-1">
            <p class="font-medium text-gray-800">Meu Veículo</p>
            <p class="text-xs text-gray-500">Informações do veículo</p>
          </div>
          <span class="text-gray-400">›</span>
        </button>
        
        <button class="w-full px-4 py-4 flex items-center gap-3 border-b border-gray-100 text-left">
          <span class="text-xl">📄</span>
          <div class="flex-1">
            <p class="font-medium text-gray-800">Documentos</p>
            <p class="text-xs text-gray-500">CNH, certificados</p>
          </div>
          <span class="text-gray-400">›</span>
        </button>
        
        <button class="w-full px-4 py-4 flex items-center gap-3 text-left">
          <span class="text-xl">🔔</span>
          <div class="flex-1">
            <p class="font-medium text-gray-800">Notificações</p>
            <p class="text-xs text-gray-500">Configurar alertas</p>
          </div>
          <span class="text-gray-400">›</span>
        </button>
      </div>

      <!-- GPS Status -->
      <div class="bg-white rounded-2xl shadow-sm p-4 mb-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-xl">📍</span>
            <div>
              <p class="font-medium text-gray-800">Rastreamento GPS</p>
              <p class="text-xs text-gray-500">{{ gpsAtivo ? 'Ativo' : 'Inativo' }}</p>
            </div>
          </div>
          <button 
            @click="toggleGPS"
            :class="[
              'w-12 h-6 rounded-full transition-colors',
              gpsAtivo ? 'bg-green-500' : 'bg-gray-300'
            ]"
          >
            <div 
              :class="[
                'w-5 h-5 bg-white rounded-full shadow transition-transform',
                gpsAtivo ? 'translate-x-6' : 'translate-x-0.5'
              ]"
            ></div>
          </button>
        </div>
      </div>

      <!-- Suporte -->
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden mb-4">
        <a href="tel:+5511999999999" class="w-full px-4 py-4 flex items-center gap-3 border-b border-gray-100">
          <span class="text-xl">📞</span>
          <div class="flex-1">
            <p class="font-medium text-gray-800">Ligar para Suporte</p>
            <p class="text-xs text-gray-500">(11) 99999-9999</p>
          </div>
        </a>
        
        <a href="https://wa.me/5511999999999" target="_blank" class="w-full px-4 py-4 flex items-center gap-3">
          <span class="text-xl">💬</span>
          <div class="flex-1">
            <p class="font-medium text-gray-800">WhatsApp Suporte</p>
            <p class="text-xs text-gray-500">Atendimento rápido</p>
          </div>
        </a>
      </div>

      <!-- Logout -->
      <button 
        @click="handleLogout"
        class="w-full bg-red-50 text-red-600 py-4 rounded-xl font-medium flex items-center justify-center gap-2"
      >
        🚪 Sair do App
      </button>

      <!-- Versão -->
      <p class="text-center text-gray-400 text-xs mt-4">
        LogiFlow App v1.0.0
      </p>
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-3 flex justify-around">
      <button @click="router.push('/')" class="flex flex-col items-center text-gray-400">
        <span class="text-xl">🏠</span>
        <span class="text-xs mt-1">Início</span>
      </button>
      <button @click="router.push('/entregas')" class="flex flex-col items-center text-gray-400">
        <span class="text-xl">📦</span>
        <span class="text-xs mt-1">Entregas</span>
      </button>
      <button class="flex flex-col items-center text-blue-600">
        <span class="text-xl">👤</span>
        <span class="text-xs mt-1">Perfil</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const gpsAtivo = ref(true)

const stats = ref({
  entregasHoje: 3,
  entregasMes: 47,
  kmRodados: 1250
})

function toggleGPS() {
  gpsAtivo.value = !gpsAtivo.value
}

function handleLogout() {
  if (confirm('Deseja realmente sair?')) {
    authStore.logout()
    router.push('/login')
  }
}
</script>
