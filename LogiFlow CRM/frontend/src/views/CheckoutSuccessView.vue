<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full">
      <div class="bg-white rounded-3xl shadow-2xl p-12 text-center">
        <!-- Success Icon -->
        <div class="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full mb-8 animate-bounce">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
          </svg>
        </div>

        <!-- Title -->
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          🎉 Pagamento Aprovado!
        </h1>
        
        <p class="text-xl text-gray-600 mb-8">
          Sua assinatura foi confirmada com sucesso
        </p>

        <!-- Info Box -->
        <div class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 mb-8 text-left">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">O que acontece agora?</h2>
          
          <div class="space-y-4">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Provisionamento Automático</h3>
                <p class="text-gray-600">Estamos criando sua conta e configurando seu ambiente personalizado</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Email de Boas-Vindas</h3>
                <p class="text-gray-600">Em alguns minutos você receberá um email com suas credenciais de acesso</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <div class="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Acesso ao Sistema</h3>
                <p class="text-gray-600">Você poderá acessar sua conta em até 5 minutos</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Subscription Details -->
        <div v-if="subscriptionData" class="bg-gray-50 rounded-2xl p-6 mb-8 text-left">
          <h3 class="font-bold text-gray-900 mb-4">Detalhes da Assinatura</h3>
          <div class="space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-600">Plano:</span>
              <span class="font-bold text-gray-900">{{ subscriptionData.plan }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Valor:</span>
              <span class="font-bold text-gray-900">R$ {{ subscriptionData.amount }}/mês</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Próxima cobrança:</span>
              <span class="font-bold text-gray-900">{{ subscriptionData.nextBilling }}</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="space-y-4">
          <button @click="goToDashboard" 
                  class="w-full py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 transition-all">
            Acessar Minha Conta
          </button>
          
          <button @click="goToHome" 
                  class="w-full py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-bold hover:bg-gray-50 transition-all">
            Voltar para o Site
          </button>
        </div>

        <!-- Support -->
        <div class="mt-8 pt-8 border-t border-gray-200">
          <p class="text-sm text-gray-600 mb-4">
            Precisa de ajuda? Nossa equipe está disponível 24/7
          </p>
          <div class="flex items-center justify-center gap-6">
            <a href="mailto:suporte@logiflow.com.br" class="text-blue-600 hover:text-blue-700 font-semibold">
              📧 Email
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

const subscriptionData = ref(null)

onMounted(() => {
  // Buscar dados da assinatura da query string ou localStorage
  const data = route.query
  if (data.plan) {
    subscriptionData.value = {
      plan: data.plan,
      amount: data.amount || '299',
      nextBilling: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toLocaleDateString('pt-BR')
    }
  }
})

const goToDashboard = () => {
  router.push('/')
}

const goToHome = () => {
  window.location.href = 'https://logiflow.com.br'
}
</script>
