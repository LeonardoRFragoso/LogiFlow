<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 via-white to-orange-50 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full">
      <div class="bg-white rounded-3xl shadow-2xl p-12 text-center">
        <!-- Error Icon -->
        <div class="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-red-500 to-orange-600 rounded-full mb-8">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </div>

        <!-- Title -->
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          ❌ Pagamento Não Aprovado
        </h1>
        
        <p class="text-xl text-gray-600 mb-8">
          Não foi possível processar seu pagamento
        </p>

        <!-- Error Details -->
        <div class="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-8 mb-8 text-left">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Possíveis Motivos</h2>
          
          <div class="space-y-4">
            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-red-500 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Saldo Insuficiente</h3>
                <p class="text-gray-600">Verifique se há saldo disponível no cartão</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-red-500 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Dados Incorretos</h3>
                <p class="text-gray-600">Confira o número do cartão, validade e CVV</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-red-500 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Limite Excedido</h3>
                <p class="text-gray-600">O limite do cartão pode ter sido atingido</p>
              </div>
            </div>

            <div class="flex items-start gap-4">
              <svg class="w-6 h-6 text-red-500 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
              <div>
                <h3 class="font-bold text-gray-900 mb-1">Bloqueio de Segurança</h3>
                <p class="text-gray-600">Entre em contato com seu banco para liberar</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Alternative Payment -->
        <div class="bg-blue-50 rounded-2xl p-6 mb-8">
          <h3 class="font-bold text-gray-900 mb-3">💡 Sugestão</h3>
          <p class="text-gray-700 mb-4">
            Que tal tentar com PIX? É instantâneo e não tem risco de recusa!
          </p>
          <button @click="tryAgainWithPix" 
                  class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all">
            Pagar com PIX
          </button>
        </div>

        <!-- Actions -->
        <div class="space-y-4">
          <button @click="tryAgain" 
                  class="w-full py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 transition-all">
            Tentar Novamente
          </button>
          
          <button @click="contactSupport" 
                  class="w-full py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-bold hover:bg-gray-50 transition-all">
            Falar com Suporte
          </button>
          
          <button @click="goToHome" 
                  class="w-full py-4 text-gray-600 hover:text-gray-900 font-semibold transition-all">
            Voltar para o Site
          </button>
        </div>

        <!-- Support -->
        <div class="mt-8 pt-8 border-t border-gray-200">
          <p class="text-sm text-gray-600 mb-4">
            Precisa de ajuda? Estamos aqui para você!
          </p>
          <div class="flex items-center justify-center gap-6">
            <a href="mailto:suporte@logiflow.com.br" class="text-blue-600 hover:text-blue-700 font-semibold">
              📧 Email
            </a>
            <a href="https://wa.me/5511999999999" class="text-green-600 hover:text-green-700 font-semibold">
              💬 WhatsApp
            </a>
            <a href="tel:08007771234" class="text-purple-600 hover:text-purple-700 font-semibold">
              📞 0800 777 1234
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const tryAgain = () => {
  router.push('/checkout')
}

const tryAgainWithPix = () => {
  router.push({ path: '/checkout', query: { method: 'pix' } })
}

const contactSupport = () => {
  window.open('https://wa.me/5511999999999?text=Olá, tive um problema com o pagamento', '_blank')
}

const goToHome = () => {
  window.location.href = 'https://logiflow.com.br'
}
</script>
