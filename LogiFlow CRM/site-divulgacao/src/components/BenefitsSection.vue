<template>
  <section id="beneficios" class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-50 to-blue-50">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Por que escolher o LogiFlow?
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Diferenciais que fazem toda a diferença na sua operação
        </p>
      </div>

      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-6">
          <div v-for="benefit in benefits" :key="benefit.title" 
               class="flex gap-4 p-6 bg-white rounded-xl hover:shadow-lg transition-all">
            <div class="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center text-white text-2xl">
              {{ benefit.icon }}
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-2">{{ benefit.title }}</h3>
              <p class="text-gray-600">{{ benefit.description }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-8 rounded-2xl shadow-xl">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">70% Mais Barato que TOTVS/SSW</h3>
          <div class="space-y-4">
            <div class="p-4 bg-red-50 rounded-lg border-2 border-red-200">
              <div class="text-sm text-gray-600 mb-1">Soluções Enterprise</div>
              <div class="flex justify-between items-center">
                <span class="text-gray-700 font-semibold">TOTVS / SSW / SAP</span>
                <span class="text-2xl font-bold text-red-600">R$ 3.000-15.000/mês</span>
              </div>
              <div class="text-xs text-gray-500 mt-2">+ Setup demorado + Contrato de fidelidade</div>
            </div>
            <div class="text-center text-gray-400 font-bold text-2xl">VS</div>
            <div class="p-4 bg-green-50 rounded-lg border-2 border-green-500">
              <div class="text-sm text-gray-600 mb-1">LogiFlow CRM</div>
              <div class="flex justify-between items-center">
                <span class="text-gray-700 font-semibold">Tudo Incluído</span>
                <span class="text-2xl font-bold text-green-600">R$ 299/mês</span>
              </div>
              <div class="text-xs text-green-700 mt-2 font-semibold">✓ Setup 48h ✓ Sem contrato ✓ Suporte incluso</div>
            </div>
            <div class="pt-4 border-t border-gray-200">
              <div class="text-center">
                <div class="text-3xl font-bold text-blue-600 mb-2">Economize até 70%</div>
                <div class="text-gray-600">Até R$ 180.000 por ano</div>
                <div class="text-sm text-gray-500 mt-2">Comparado com soluções enterprise</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const benefits = [
  {
    icon: '⚡',
    title: 'Setup em 48 horas',
    description: 'Comece a usar em 2 dias. Sem projetos de meses, sem complicação.'
  },
  {
    icon: '💰',
    title: '70% mais barato',
    description: 'Preço acessível comparado a soluções enterprise como TOTVS e SAP.'
  },
  {
    icon: '🔓',
    title: 'Sem contrato de fidelidade',
    description: 'Pagamento mensal. Cancele quando quiser, sem multas ou burocracias.'
  },
  {
    icon: '🇧🇷',
    title: 'Suporte em português',
    description: 'Atendimento humano, não bot. Time brasileiro que entende seu negócio.'
  },
  {
    icon: '📱',
    title: 'App do motorista incluso',
    description: 'Aplicativo móvel profissional para seus motoristas, sem custo adicional.'
  },
  {
    icon: '🔄',
    title: 'Atualizações constantes',
    description: 'Novas funcionalidades todo mês, sem custo extra.'
  }
]
</script>
