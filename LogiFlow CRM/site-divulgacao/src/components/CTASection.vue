<template>
  <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 to-cyan-500">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-4xl md:text-5xl font-bold text-white mb-6">
        Pronto para transformar sua transportadora?
      </h2>
      <p class="text-xl text-blue-100 mb-8">
        Junte-se a mais de 500 transportadoras que já usam o LogiFlow
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button @click="$emit('request-demo')" 
                class="px-8 py-4 bg-white text-blue-600 rounded-xl font-bold text-lg hover:shadow-2xl hover:scale-105 transition-all">
          🚀 Começar Teste Grátis de 14 Dias
        </button>
        <button @click="openWhatsApp" class="px-8 py-4 bg-blue-700 text-white rounded-xl font-bold text-lg hover:bg-blue-800 transition-all">
          💬 Falar com Especialista
        </button>
      </div>
      <p class="mt-6 text-blue-100 text-sm">
        ✓ Sem cartão de crédito  ✓ Sem compromisso  ✓ Suporte em português
      </p>
    </div>
  </section>
</template>

<script setup>
defineEmits(['request-demo'])

const openWhatsApp = () => {
  // Substitua pelo número real do WhatsApp da empresa
  const phoneNumber = '5521999999999' // Formato: código país + DDD + número
  const message = encodeURIComponent('Olá! Gostaria de falar com um especialista sobre o LogiFlow CRM.')
  window.open(`https://wa.me/${phoneNumber}?text=${message}`, '_blank')
}
</script>
