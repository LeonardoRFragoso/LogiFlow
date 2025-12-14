<template>
  <section id="publico-alvo" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Feito para transportadoras de 5 a 100 veículos
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Não importa o tamanho da sua operação, temos o plano ideal para você crescer
        </p>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <div v-for="segment in segments" :key="segment.title" 
             class="bg-gradient-to-br from-blue-50 to-cyan-50 p-8 rounded-2xl hover:shadow-xl transition-all">
          <div class="text-4xl mb-4">{{ segment.icon }}</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ segment.title }}</h3>
          <p class="text-gray-600 mb-4">{{ segment.vehicles }}</p>
          
          <div class="space-y-3 mb-6">
            <div v-for="feature in segment.features" :key="feature" class="flex items-start gap-2">
              <svg class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span class="text-sm text-gray-700">{{ feature }}</span>
            </div>
          </div>

          <div class="pt-4 border-t border-gray-200">
            <div class="text-sm text-gray-600 mb-1">A partir de</div>
            <div class="text-3xl font-bold text-blue-600">{{ segment.price }}</div>
          </div>
        </div>
      </div>

      <div class="mt-12 bg-blue-600 text-white p-8 rounded-2xl text-center">
        <h3 class="text-2xl font-bold mb-4">
          🎯 Nicho Mal Atendido no Brasil
        </h3>
        <div class="grid md:grid-cols-3 gap-8 mb-6">
          <div>
            <div class="text-4xl font-bold mb-2">~50.000</div>
            <div class="text-blue-100">Transportadoras no Brasil (ANTT)</div>
          </div>
          <div>
            <div class="text-4xl font-bold mb-2">85%</div>
            <div class="text-blue-100">São pequeno/médio porte</div>
          </div>
          <div>
            <div class="text-4xl font-bold mb-2">R$ 180M</div>
            <div class="text-blue-100">Mercado potencial/ano</div>
          </div>
        </div>
        <p class="text-lg text-blue-100">
          A maioria não pode pagar TOTVS/SSW, mas Agendor/Ploomes não resolvem a operação logística
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
const segments = [
  {
    icon: '🚚',
    title: 'Pequeno Porte',
    vehicles: '5-15 veículos',
    features: [
      'Gestão básica de pedidos',
      'Controle de motoristas',
      'App do motorista incluso',
      'Suporte por email',
      'Ideal para começar'
    ],
    price: 'R$ 299/mês'
  },
  {
    icon: '🚛',
    title: 'Médio Porte',
    vehicles: '15-50 veículos',
    features: [
      'Todas as funcionalidades',
      'Emissão de CT-e/MDF-e',
      'WhatsApp integrado',
      'Rastreamento GPS',
      'Suporte prioritário'
    ],
    price: 'R$ 599/mês'
  },
  {
    icon: '🏭',
    title: 'Grande Porte',
    vehicles: '50-100+ veículos',
    features: [
      'Recursos ilimitados',
      'API personalizada',
      'Integrações customizadas',
      'Gerente de conta dedicado',
      'Treinamento presencial'
    ],
    price: 'R$ 1.499/mês'
  }
]
</script>
