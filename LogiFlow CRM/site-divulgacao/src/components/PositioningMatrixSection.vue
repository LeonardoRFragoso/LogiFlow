<template>
  <section id="comparacao" class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-50 to-blue-50">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Como nos comparamos com a concorrência
        </h2>
        <p class="text-xl text-gray-600">
          Posicionamento único: especialização em logística com preço acessível
        </p>
      </div>

      <!-- Matriz Visual -->
      <div class="bg-white p-8 rounded-2xl shadow-xl mb-12">
        <div class="relative h-96">
          <!-- Eixos -->
          <div class="absolute inset-0 flex items-center justify-center">
            <!-- Eixo Vertical (Preço) -->
            <div class="absolute left-0 top-0 bottom-0 w-px bg-gray-300"></div>
            <div class="absolute left-0 top-0 -ml-20 text-sm font-semibold text-gray-600 transform -rotate-90 origin-left">
              PREÇO ALTO
            </div>
            <div class="absolute left-0 bottom-0 -ml-20 text-sm font-semibold text-gray-600 transform -rotate-90 origin-left">
              PREÇO BAIXO
            </div>
            
            <!-- Eixo Horizontal (Especialização) -->
            <div class="absolute left-0 right-0 bottom-0 h-px bg-gray-300"></div>
            <div class="absolute left-0 bottom-0 -mb-8 text-sm font-semibold text-gray-600">
              GENÉRICO
            </div>
            <div class="absolute right-0 bottom-0 -mb-8 text-sm font-semibold text-gray-600">
              ESPECIALIZADO
            </div>
          </div>

          <!-- Competidores -->
          <div v-for="competitor in competitors" :key="competitor.name"
               :class="['absolute transform -translate-x-1/2 -translate-y-1/2 transition-all hover:scale-110', competitor.highlight ? 'z-10' : 'z-0']"
               :style="{ left: competitor.x + '%', top: competitor.y + '%' }">
            <div :class="['px-4 py-2 rounded-lg font-semibold text-sm shadow-lg cursor-pointer',
                          competitor.highlight 
                            ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white ring-4 ring-blue-200' 
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200']">
              {{ competitor.highlight ? '★ ' : '' }}{{ competitor.name }}
            </div>
          </div>
        </div>
      </div>

      <!-- Tabela Comparativa -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-600 to-cyan-500 text-white">
              <tr>
                <th class="px-6 py-4 text-left font-bold">Solução</th>
                <th class="px-6 py-4 text-left font-bold">Especialização</th>
                <th class="px-6 py-4 text-left font-bold">Preço</th>
                <th class="px-6 py-4 text-left font-bold">Setup</th>
                <th class="px-6 py-4 text-left font-bold">Contrato</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(solution, index) in solutions" :key="solution.name"
                  :class="[solution.highlight ? 'bg-blue-50 border-l-4 border-blue-600' : index % 2 === 0 ? 'bg-white' : 'bg-gray-50']">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <span v-if="solution.highlight" class="text-2xl">★</span>
                    <span :class="solution.highlight ? 'font-bold text-blue-600' : 'font-semibold text-gray-900'">
                      {{ solution.name }}
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span :class="['px-3 py-1 rounded-full text-sm font-medium',
                                 solution.specialized ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700']">
                    {{ solution.specialized ? '✓ Logística' : '✗ Genérico' }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span :class="['font-bold', solution.highlight ? 'text-green-600 text-lg' : 'text-gray-900']">
                    {{ solution.price }}
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-700">{{ solution.setup }}</td>
                <td class="px-6 py-4">
                  <span :class="['px-3 py-1 rounded-full text-sm font-medium',
                                 solution.noContract ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
                    {{ solution.noContract ? '✓ Sem contrato' : '✗ Fidelidade' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-8 text-center">
        <p class="text-lg text-gray-600 mb-4">
          <strong class="text-blue-600">LogiFlow:</strong> O único que combina especialização em logística com preço acessível
        </p>
        <button @click="scrollToPrecos" class="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-xl font-bold text-lg hover:shadow-2xl hover:scale-105 transition-all">
          Comparar Planos Detalhadamente →
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
const scrollToPrecos = () => {
  const element = document.getElementById('precos')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const competitors = [
  { name: 'TOTVS', x: 75, y: 15, highlight: false },
  { name: 'SSW', x: 85, y: 20, highlight: false },
  { name: 'SAP', x: 70, y: 10, highlight: false },
  { name: 'Gestran', x: 80, y: 55, highlight: false },
  { name: 'Fleetsmart', x: 75, y: 60, highlight: false },
  { name: 'LogiFlow', x: 80, y: 75, highlight: true },
  { name: 'Ploomes', x: 35, y: 55, highlight: false },
  { name: 'Agendor', x: 30, y: 70, highlight: false },
  { name: 'RD Station', x: 25, y: 80, highlight: false }
]

const solutions = [
  {
    name: 'LogiFlow CRM',
    specialized: true,
    price: 'R$ 199-599/mês',
    setup: '48 horas',
    noContract: true,
    highlight: true
  },
  {
    name: 'TOTVS Logística',
    specialized: true,
    price: 'R$ 3.000-15.000/mês',
    setup: '3-6 meses',
    noContract: false,
    highlight: false
  },
  {
    name: 'SSW (TMS)',
    specialized: true,
    price: 'R$ 1.500-5.000/mês',
    setup: '2-4 meses',
    noContract: false,
    highlight: false
  },
  {
    name: 'Gestran',
    specialized: true,
    price: 'R$ 800-2.500/mês',
    setup: '1-2 meses',
    noContract: false,
    highlight: false
  },
  {
    name: 'Ploomes',
    specialized: false,
    price: 'R$ 249-699/mês',
    setup: '1 semana',
    noContract: true,
    highlight: false
  },
  {
    name: 'Agendor',
    specialized: false,
    price: 'R$ 53-106/usuário',
    setup: 'Imediato',
    noContract: true,
    highlight: false
  }
]
</script>
