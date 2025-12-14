<template>
  <section id="funcionalidades" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Tudo que sua transportadora precisa
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Funcionalidades completas para gerenciar toda a operação logística em um só lugar
        </p>
      </div>

      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="feature in features" :key="feature.title" 
             class="group p-8 bg-white rounded-2xl border border-gray-200 hover:border-blue-500 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 cursor-pointer">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-600 via-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center text-4xl mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
            {{ feature.icon }}
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">{{ feature.title }}</h3>
          <p class="text-gray-600 leading-relaxed">{{ feature.description }}</p>
          <div class="mt-4 flex items-center text-blue-600 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
            Saiba mais →
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    icon: '📄',
    title: 'Emissão de CT-e/MDF-e Integrada',
    description: 'Emita documentos fiscais sem sistema separado. Economia de R$ 100-300/mês. Integração com Focus NFe e Webmania.'
  },
  {
    icon: '👥',
    title: 'Portal do Cliente com Tracking',
    description: 'Cliente rastreia entrega sem ligar. Link compartilhável por WhatsApp. Reduz 50%+ das ligações "cadê minha carga?"'
  },
  {
    icon: '📱',
    title: 'App do Motorista (PWA)',
    description: 'Aceita/recusa cargas, atualiza status em tempo real, foto de comprovante. Funciona offline!'
  },
  {
    icon: '⏱️',
    title: 'Dashboard de SLA em Tempo Real',
    description: 'Visualização de entregas atrasadas, alertas automáticos, KPIs de performance por motorista/cliente.'
  },
  {
    icon: '💬',
    title: 'WhatsApp Integrado (Evolution API)',
    description: 'Notificações automáticas, chatbot para consulta de status, histórico completo no CRM.'
  },
  {
    icon: '📦',
    title: 'Gestão Completa de Pedidos',
    description: 'Controle total desde cotação até entrega. Workflow automatizado e rastreamento em tempo real.'
  },
  {
    icon: '🚛',
    title: 'Gestão de Motoristas e Frota',
    description: 'Cadastro, avaliação, disponibilidade, manutenções e custos operacionais centralizados.'
  },
  {
    icon: '📊',
    title: 'Relatórios e Analytics',
    description: 'Dashboards operacionais e financeiros. Métricas de performance e tomada de decisão estratégica.'
  },
  {
    icon: '💰',
    title: 'Cotações Automáticas',
    description: 'Cálculo inteligente baseado em distância, peso, volume. Converta cotações em pedidos com 1 clique.'
  }
]
</script>
