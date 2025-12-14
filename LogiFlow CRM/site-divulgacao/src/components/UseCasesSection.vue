<template>
  <section id="casos-uso" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Casos de uso reais por tamanho de operação
        </h2>
        <p class="text-xl text-gray-600">
          Veja como transportadoras como a sua usam o LogiFlow no dia a dia
        </p>
      </div>

      <div class="space-y-12">
        <div v-for="useCase in useCases" :key="useCase.title" 
             class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl overflow-hidden">
          <div class="grid lg:grid-cols-2 gap-8 p-8">
            <div>
              <div class="inline-block px-4 py-2 bg-blue-600 text-white rounded-full text-sm font-bold mb-4">
                {{ useCase.segment }}
              </div>
              <h3 class="text-3xl font-bold text-gray-900 mb-4">{{ useCase.title }}</h3>
              <p class="text-lg text-gray-600 mb-6">{{ useCase.description }}</p>
              
              <div class="space-y-4 mb-6">
                <div class="bg-white p-4 rounded-lg">
                  <div class="font-bold text-gray-900 mb-2">😰 Problema Antes:</div>
                  <p class="text-gray-700">{{ useCase.problem }}</p>
                </div>
                <div class="bg-white p-4 rounded-lg">
                  <div class="font-bold text-green-600 mb-2">✅ Solução com LogiFlow:</div>
                  <p class="text-gray-700">{{ useCase.solution }}</p>
                </div>
              </div>

              <div class="grid grid-cols-3 gap-4">
                <div v-for="metric in useCase.metrics" :key="metric.label" 
                     class="bg-white p-4 rounded-lg text-center">
                  <div class="text-2xl font-bold text-blue-600 mb-1">{{ metric.value }}</div>
                  <div class="text-xs text-gray-600">{{ metric.label }}</div>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <div class="bg-white p-6 rounded-xl">
                <h4 class="font-bold text-gray-900 mb-4">Funcionalidades Mais Usadas:</h4>
                <ul class="space-y-3">
                  <li v-for="feature in useCase.topFeatures" :key="feature" 
                      class="flex items-start gap-3">
                    <svg class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                    <span class="text-gray-700">{{ feature }}</span>
                  </li>
                </ul>
              </div>

              <div class="bg-blue-600 text-white p-6 rounded-xl">
                <div class="text-sm font-semibold mb-2">Depoimento</div>
                <p class="italic mb-4">"{{ useCase.testimonial }}"</p>
                <div class="text-sm">
                  <div class="font-bold">{{ useCase.client.name }}</div>
                  <div class="text-blue-200">{{ useCase.client.role }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const useCases = [
  {
    segment: 'Pequeno Porte (5-15 veículos)',
    title: 'TransLog Express',
    description: 'Transportadora familiar com 8 caminhões, focada em entregas regionais',
    problem: 'Usavam planilhas Excel e WhatsApp para tudo. Perdiam pedidos, esqueciam de cobrar, não sabiam onde estavam os motoristas.',
    solution: 'Com LogiFlow, centralizaram tudo: pedidos, motoristas, cobranças. App do motorista eliminou ligações. Cresceram 40% em 6 meses.',
    metrics: [
      { value: '40%', label: 'Crescimento' },
      { value: '-60%', label: 'Ligações' },
      { value: '2h/dia', label: 'Economia' }
    ],
    topFeatures: [
      'Gestão de pedidos simples e rápida',
      'App do motorista para atualizações',
      'WhatsApp automático para clientes',
      'Controle de cobranças'
    ],
    testimonial: 'Antes era tudo bagunçado. Agora tenho controle total. Melhor investimento que fiz!',
    client: {
      name: 'João Silva',
      role: 'Proprietário, TransLog Express'
    }
  },
  {
    segment: 'Médio Porte (15-50 veículos)',
    title: 'Expresso Rápido Ltda',
    description: 'Transportadora com 32 veículos, operação estadual e emissão de CT-e',
    problem: 'Usavam 3 sistemas diferentes: CRM genérico, planilha para operação, sistema fiscal separado. Dados desencontrados, retrabalho constante.',
    solution: 'LogiFlow unificou tudo. Emissão de CT-e integrada economizou R$ 200/mês. Dashboard de SLA reduziu atrasos em 70%.',
    metrics: [
      { value: '-70%', label: 'Atrasos' },
      { value: 'R$ 200', label: 'Economia/mês' },
      { value: '98%', label: 'SLA' }
    ],
    topFeatures: [
      'Emissão de CT-e/MDF-e integrada',
      'Dashboard de SLA em tempo real',
      'Portal do cliente com tracking',
      'Gestão completa de frota',
      'Relatórios financeiros'
    ],
    testimonial: 'Eliminamos 3 sistemas. Agora tudo está integrado. A emissão de CT-e integrada foi um divisor de águas.',
    client: {
      name: 'Maria Santos',
      role: 'Diretora Operacional, Expresso Rápido'
    }
  },
  {
    segment: 'Grande Porte (50-100+ veículos)',
    title: 'Carga Pesada Transportes',
    description: 'Transportadora com 85 veículos, operação nacional e múltiplas filiais',
    problem: 'TOTVS custava R$ 12.000/mês. Setup demorou 8 meses. Suporte ruim. Precisavam de algo mais ágil e econômico.',
    solution: 'Migraram para LogiFlow em 1 semana. Economizam R$ 140.000/ano. API personalizada integrou com ERP. Gerente de conta dedicado.',
    metrics: [
      { value: 'R$ 140k', label: 'Economia/ano' },
      { value: '1 semana', label: 'Migração' },
      { value: '100%', label: 'Satisfação' }
    ],
    topFeatures: [
      'API personalizada para integrações',
      'Multi-filial e multi-usuário',
      'Relatórios customizados',
      'Gerente de conta dedicado',
      'Treinamento presencial',
      'Suporte 24/7 prioritário'
    ],
    testimonial: 'Saímos do TOTVS e não nos arrependemos. LogiFlow é mais ágil, mais barato e o suporte é infinitamente melhor.',
    client: {
      name: 'Carlos Oliveira',
      role: 'CEO, Carga Pesada Transportes'
    }
  }
]
</script>
