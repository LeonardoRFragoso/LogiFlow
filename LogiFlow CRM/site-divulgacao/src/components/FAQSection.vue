<template>
  <section id="faq" class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Perguntas Frequentes
        </h2>
        <p class="text-xl text-gray-600">
          Tire suas dúvidas sobre o LogiFlow CRM
        </p>
      </div>

      <div class="space-y-4">
        <div v-for="(faq, index) in faqs" :key="index" 
             class="border border-gray-200 rounded-xl overflow-hidden">
          <button @click="toggleFAQ(index)" 
                  class="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors">
            <span class="font-semibold text-gray-900">{{ faq.question }}</span>
            <svg :class="['w-5 h-5 text-gray-500 transition-transform', openFAQ === index && 'rotate-180']" 
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div v-show="openFAQ === index" class="px-6 py-4 bg-gray-50 text-gray-700">
            {{ faq.answer }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const openFAQ = ref(null)

const toggleFAQ = (index) => {
  openFAQ.value = openFAQ.value === index ? null : index
}

const faqs = [
  {
    question: 'Quanto tempo leva para implementar o LogiFlow?',
    answer: 'Em média 48 horas. Fazemos a migração dos seus dados, configuração inicial e treinamento da equipe em apenas 2 dias úteis.'
  },
  {
    question: 'Preciso de conhecimento técnico para usar?',
    answer: 'Não! O LogiFlow foi desenvolvido para ser extremamente intuitivo. Qualquer pessoa consegue usar após um treinamento rápido de 1 hora.'
  },
  {
    question: 'Posso cancelar a qualquer momento?',
    answer: 'Sim! Não temos contrato de fidelidade. Você pode cancelar quando quiser, sem multas ou burocracias.'
  },
  {
    question: 'Os dados ficam seguros?',
    answer: 'Absolutamente! Usamos criptografia de ponta a ponta, backups diários e servidores em nuvem com certificação ISO 27001.'
  },
  {
    question: 'Tem limite de usuários ou pedidos?',
    answer: 'Depende do plano. O plano Professional tem pedidos ilimitados. O Enterprise não tem limite nenhum.'
  },
  {
    question: 'Como funciona o suporte?',
    answer: 'Oferecemos suporte por WhatsApp, email e telefone. Tempo médio de resposta: 2 horas. Plano Enterprise tem suporte 24/7 prioritário.'
  }
]
</script>
