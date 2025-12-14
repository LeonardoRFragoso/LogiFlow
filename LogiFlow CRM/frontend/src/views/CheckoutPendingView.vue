<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 via-white to-amber-50 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full">
      <div class="bg-white rounded-3xl shadow-2xl p-12 text-center">
        <!-- Pending Icon -->
        <div class="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-yellow-500 to-amber-600 rounded-full mb-8">
          <svg class="w-12 h-12 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>

        <!-- Title -->
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          ⏳ Pagamento Pendente
        </h1>
        
        <p class="text-xl text-gray-600 mb-8">
          Seu pagamento está sendo processado
        </p>

        <!-- Info Box -->
        <div class="bg-gradient-to-br from-yellow-50 to-amber-50 rounded-2xl p-8 mb-8 text-left">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">O que está acontecendo?</h2>
          
          <div class="space-y-4">
            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Processamento</h3>
                <p class="text-gray-600">Seu pagamento está sendo verificado pela operadora</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Tempo Estimado</h3>
                <p class="text-gray-600">A confirmação pode levar de alguns minutos até 2 dias úteis</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Notificação</h3>
                <p class="text-gray-600">Você receberá um email assim que o pagamento for confirmado</p>
              </div>
            </div>
          </div>
        </div>

        <!-- PIX Instructions (if PIX payment) -->
        <div v-if="paymentMethod === 'pix'" class="bg-blue-50 rounded-2xl p-6 mb-8">
          <h3 class="font-bold text-gray-900 mb-3">💡 Pagamento via PIX</h3>
          <p class="text-gray-700 mb-4">
            Se você ainda não pagou, o QR Code e código PIX foram enviados para seu email.
          </p>
          <p class="text-sm text-gray-600">
            O PIX tem validade de 24 horas. Após o pagamento, a confirmação é instantânea.
          </p>
        </div>

        <!-- Boleto Instructions (if boleto payment) -->
        <div v-if="paymentMethod === 'boleto'" class="bg-blue-50 rounded-2xl p-6 mb-8">
          <h3 class="font-bold text-gray-900 mb-3">💡 Pagamento via Boleto</h3>
          <p class="text-gray-700 mb-4">
            O boleto foi enviado para seu email. Você pode pagar em qualquer banco ou lotérica.
          </p>
          <p class="text-sm text-gray-600">
            Após o pagamento, a compensação leva de 1 a 2 dias úteis.
          </p>
        </div>

        <!-- Status Check -->
        <div class="bg-gray-50 rounded-2xl p-6 mb-8">
          <h3 class="font-bold text-gray-900 mb-4">Acompanhe seu Pagamento</h3>
          <p class="text-gray-600 mb-4">
            Número do pedido: <span class="font-mono font-bold text-blue-600">#{{ orderId }}</span>
          </p>
          <button @click="checkStatus" :disabled="checking"
                  class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all disabled:opacity-50">
            {{ checking ? 'Verificando...' : 'Verificar Status' }}
          </button>
        </div>

        <!-- Actions -->
        <div class="space-y-4">
          <button @click="goToDashboard" 
                  class="w-full py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 transition-all">
            Ir para o Dashboard
          </button>
          
          <button @click="goToHome" 
                  class="w-full py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-bold hover:bg-gray-50 transition-all">
            Voltar para o Site
          </button>
        </div>

        <!-- Support -->
        <div class="mt-8 pt-8 border-t border-gray-200">
          <p class="text-sm text-gray-600 mb-4">
            Dúvidas sobre seu pagamento?
          </p>
          <div class="flex items-center justify-center gap-6">
            <a href="mailto:financeiro@logiflow.com.br" class="text-blue-600 hover:text-blue-700 font-semibold">
              📧 Financeiro
            </a>
            <a href="https://wa.me/5511999999999" class="text-green-600 hover:text-green-700 font-semibold">
              💬 WhatsApp
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const paymentMethod = ref('credit_card')
const orderId = ref('000000')
const checking = ref(false)

onMounted(() => {
  // Obter dados da query string
  paymentMethod.value = route.query.method || 'credit_card'
  orderId.value = route.query.orderId || Math.random().toString(36).substr(2, 9).toUpperCase()
  
  // Auto-verificar status a cada 30 segundos
  setInterval(() => {
    checkStatusSilently()
  }, 30000)
})

const checkStatus = async () => {
  checking.value = true
  
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/billing/payment-status/${orderId.value}`)
    const data = await response.json()
    
    if (data.status === 'approved') {
      router.push('/checkout/success')
    } else if (data.status === 'rejected') {
      router.push('/checkout/failure')
    }
  } catch (error) {
    console.error('Erro ao verificar status:', error)
  } finally {
    checking.value = false
  }
}

const checkStatusSilently = async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/billing/payment-status/${orderId.value}`)
    const data = await response.json()
    
    if (data.status === 'approved') {
      router.push('/checkout/success')
    } else if (data.status === 'rejected') {
      router.push('/checkout/failure')
    }
  } catch (error) {
    // Silencioso - não mostrar erro
  }
}

const goToDashboard = () => {
  router.push('/')
}

const goToHome = () => {
  window.location.href = 'https://logiflow.com.br'
}
</script>
