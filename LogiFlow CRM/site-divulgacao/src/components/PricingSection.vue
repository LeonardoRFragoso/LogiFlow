<template>
  <section id="precos" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Planos que cabem no seu bolso
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Escolha o plano ideal para o tamanho da sua operação
        </p>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <div v-for="plan in plans" :key="plan.name" 
             :class="['group p-8 rounded-2xl border-2 transition-all duration-300 hover:-translate-y-2 relative overflow-hidden', 
                      plan.popular ? 'border-blue-600 shadow-2xl bg-gradient-to-br from-blue-50 to-white' : 'border-gray-200 bg-white hover:border-blue-400 hover:shadow-xl']">
          <!-- Popular Badge -->
          <div v-if="plan.popular" class="absolute top-0 right-0 bg-gradient-to-r from-blue-600 to-cyan-500 text-white text-xs font-bold px-6 py-2 rounded-bl-2xl shadow-lg">
            ⭐ MAIS POPULAR
          </div>
          
          <!-- Glow Effect for Popular -->
          <div v-if="plan.popular" class="absolute inset-0 bg-gradient-to-br from-blue-100/50 to-cyan-100/50 -z-10"></div>
          
          <div :class="plan.popular ? 'mt-8' : ''">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ plan.name }}</h3>
            <p class="text-gray-600 mb-6 min-h-[3rem]">{{ plan.description }}</p>
            
            <div class="mb-6">
              <div class="flex items-baseline gap-2">
                <span class="text-5xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">R$ {{ plan.price }}</span>
                <span class="text-gray-600 font-semibold">/mês</span>
              </div>
            </div>
            
            <a :href="`${frontendUrl}/checkout?plan=${plan.name.toLowerCase()}`" 
               target="_blank"
               :class="['w-full py-4 rounded-xl font-bold transition-all duration-300 shadow-md hover:shadow-xl block text-center', 
                        plan.popular 
                          ? 'bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 text-white hover:scale-105' 
                          : 'bg-gray-900 text-white hover:bg-blue-600']">
              {{ plan.popular ? '🚀 Assinar Agora' : 'Assinar Agora' }}
            </a>
            
            <button @click="$emit('request-demo')" 
                    class="w-full py-3 mt-3 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-all">
              📞 Solicitar Demonstração
            </button>
            
            <ul class="mt-8 space-y-4">
              <li v-for="feature in plan.features" :key="feature" class="flex items-start gap-3">
                <svg class="w-6 h-6 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <span class="text-gray-700">{{ feature }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="mt-12 text-center text-gray-600">
        <p class="text-lg">💡 Todos os planos incluem: Suporte 24/7, Atualizações grátis, App do motorista</p>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['request-demo'])

// URL do frontend (checkout)
const frontendUrl = import.meta.env.VITE_FRONTEND_URL || 'http://localhost:3001'

const plans = [
  {
    name: 'Starter',
    description: 'Para transportadoras iniciantes (até 5 usuários)',
    price: '299',
    popular: false,
    features: [
      'Até 5 usuários',
      'Gestão de clientes',
      'Cotações e pedidos',
      'Rastreamento básico',
      'App do motorista',
      'Suporte por email'
    ]
  },
  {
    name: 'Professional',
    description: 'Para operações em crescimento (até 15 usuários)',
    price: '599',
    popular: true,
    features: [
      'Até 15 usuários',
      'Todos os recursos do Starter',
      'Rastreamento avançado',
      'Integração WhatsApp',
      'Emissão de CT-e/MDF-e',
      'Relatórios avançados',
      'Suporte prioritário'
    ]
  },
  {
    name: 'Enterprise',
    description: 'Para grandes operações (até 50 usuários)',
    price: '1499',
    popular: false,
    features: [
      'Até 50 usuários',
      'Todos os recursos do Professional',
      'API completa',
      'Customizações',
      'Integrações personalizadas',
      'Treinamento dedicado',
      'Gerente de conta',
      'Suporte 24/7'
    ]
  }
]
</script>
