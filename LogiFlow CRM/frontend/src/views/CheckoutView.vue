<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-3xl mb-6 shadow-xl">
          <span class="text-4xl">💳</span>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-4">Finalize sua Assinatura</h1>
        <p class="text-xl text-gray-600">Escolha seu plano e forma de pagamento</p>
      </div>

      <div class="grid lg:grid-cols-3 gap-8">
        <!-- Planos -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Seleção de Plano -->
          <div class="bg-white rounded-2xl shadow-xl p-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Escolha seu Plano</h2>
            
            <div class="space-y-4">
              <div v-for="plan in plans" :key="plan.id"
                   @click="selectedPlan = plan.id"
                   :class="[
                     'border-2 rounded-xl p-6 cursor-pointer transition-all',
                     selectedPlan === plan.id 
                       ? 'border-blue-600 bg-blue-50 shadow-lg' 
                       : 'border-gray-200 hover:border-blue-300'
                   ]">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center gap-3 mb-2">
                      <input type="radio" 
                             :checked="selectedPlan === plan.id"
                             class="w-5 h-5 text-blue-600">
                      <h3 class="text-xl font-bold text-gray-900">{{ plan.name }}</h3>
                      <span v-if="plan.popular" class="px-3 py-1 bg-gradient-to-r from-blue-600 to-cyan-500 text-white text-xs font-bold rounded-full">
                        MAIS POPULAR
                      </span>
                    </div>
                    <p class="text-gray-600 mb-3 ml-8">{{ plan.description }}</p>
                    <ul class="space-y-2 ml-8">
                      <li v-for="feature in plan.features" :key="feature" class="flex items-center gap-2 text-sm text-gray-700">
                        <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                        </svg>
                        {{ feature }}
                      </li>
                    </ul>
                  </div>
                  <div class="text-right">
                    <div class="text-3xl font-bold text-gray-900">R$ {{ plan.price }}</div>
                    <div class="text-sm text-gray-500">/mês</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Forma de Pagamento -->
          <div class="bg-white rounded-2xl shadow-xl p-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Forma de Pagamento</h2>
            
            <div class="grid md:grid-cols-2 gap-4 mb-6">
              <button @click="paymentMethod = 'credit_card'"
                      :class="[
                        'p-6 border-2 rounded-xl transition-all text-left',
                        paymentMethod === 'credit_card'
                          ? 'border-blue-600 bg-blue-50 shadow-lg'
                          : 'border-gray-200 hover:border-blue-300'
                      ]">
                <div class="flex items-center gap-3 mb-2">
                  <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                  </svg>
                  <span class="font-bold text-gray-900">Cartão de Crédito</span>
                </div>
                <p class="text-sm text-gray-600">Pagamento recorrente mensal</p>
              </button>

              <button @click="paymentMethod = 'pix'"
                      :class="[
                        'p-6 border-2 rounded-xl transition-all text-left',
                        paymentMethod === 'pix'
                          ? 'border-blue-600 bg-blue-50 shadow-lg'
                          : 'border-gray-200 hover:border-blue-300'
                      ]">
                <div class="flex items-center gap-3 mb-2">
                  <svg class="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                  </svg>
                  <span class="font-bold text-gray-900">PIX</span>
                </div>
                <p class="text-sm text-gray-600">Pagamento único mensal</p>
              </button>
            </div>

            <!-- Formulário de Cartão -->
            <div v-if="paymentMethod === 'credit_card'" class="space-y-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Número do Cartão</label>
                <input v-model="cardData.number" type="text" placeholder="0000 0000 0000 0000"
                       class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Validade</label>
                  <input v-model="cardData.expiry" type="text" placeholder="MM/AA"
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">CVV</label>
                  <input v-model="cardData.cvv" type="text" placeholder="123"
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Nome no Cartão</label>
                <input v-model="cardData.name" type="text" placeholder="NOME COMPLETO"
                       class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              </div>
            </div>

            <!-- QR Code PIX -->
            <div v-if="paymentMethod === 'pix' && pixData" class="text-center space-y-4">
              <div class="bg-white p-6 rounded-xl border-2 border-gray-200 inline-block">
                <img :src="pixData.qrCode" alt="QR Code PIX" class="w-64 h-64">
              </div>
              <p class="text-sm text-gray-600">Escaneie o QR Code com o app do seu banco</p>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-xs text-gray-500 mb-2">Ou copie o código PIX:</p>
                <div class="flex items-center gap-2">
                  <input :value="pixData.code" readonly
                         class="flex-1 px-3 py-2 bg-white border border-gray-300 rounded text-sm">
                  <button @click="copyPixCode" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                    Copiar
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Dados da Empresa -->
          <div class="bg-white rounded-2xl shadow-xl p-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Dados da Empresa</h2>
            
            <div class="space-y-4">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Nome da Empresa *</label>
                  <input v-model="companyData.name" type="text" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">CNPJ *</label>
                  <input v-model="companyData.cnpj" type="text" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
              </div>
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Nome do Responsável *</label>
                  <input v-model="companyData.contactName" type="text" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Email *</label>
                  <input v-model="companyData.email" type="email" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                </div>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Telefone *</label>
                <input v-model="companyData.phone" type="tel" required
                       class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              </div>
            </div>
          </div>
        </div>

        <!-- Resumo do Pedido -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl shadow-xl p-8 sticky top-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Resumo do Pedido</h2>
            
            <div class="space-y-4 mb-6">
              <div class="flex justify-between items-center pb-4 border-b border-gray-200">
                <span class="text-gray-600">Plano Selecionado</span>
                <span class="font-bold text-gray-900">{{ selectedPlanData?.name }}</span>
              </div>
              <div class="flex justify-between items-center pb-4 border-b border-gray-200">
                <span class="text-gray-600">Valor Mensal</span>
                <span class="font-bold text-gray-900">R$ {{ selectedPlanData?.price }}</span>
              </div>
              <div class="flex justify-between items-center pb-4 border-b border-gray-200">
                <span class="text-gray-600">Usuários Inclusos</span>
                <span class="font-bold text-gray-900">{{ selectedPlanData?.maxUsers }}</span>
              </div>
              <div class="flex justify-between items-center text-xl font-bold">
                <span>Total</span>
                <span class="text-blue-600">R$ {{ selectedPlanData?.price }}</span>
              </div>
            </div>

            <button @click="handleCheckout" :disabled="processing"
                    class="w-full py-4 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              {{ processing ? 'Processando...' : 'Confirmar Pagamento' }}
            </button>

            <div class="mt-6 space-y-3">
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <span>Pagamento 100% seguro</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <span>Cancele quando quiser</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                </svg>
                <span>Suporte 24/7</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const plans = ref([
  {
    id: 'starter',
    name: 'Plano Starter',
    description: 'Ideal para pequenas empresas',
    price: '299',
    maxUsers: 5,
    popular: false,
    features: [
      'Até 5 usuários',
      'Gestão de clientes',
      'Cotações e pedidos',
      'Rastreamento básico',
      'Suporte por email'
    ]
  },
  {
    id: 'professional',
    name: 'Plano Professional',
    description: 'Para empresas em crescimento',
    price: '599',
    maxUsers: 15,
    popular: true,
    features: [
      'Até 15 usuários',
      'Todos os recursos do Starter',
      'Rastreamento avançado',
      'Integração WhatsApp',
      'Relatórios avançados',
      'Suporte prioritário'
    ]
  },
  {
    id: 'enterprise',
    name: 'Plano Enterprise',
    description: 'Para grandes operações',
    price: '1499',
    maxUsers: 50,
    popular: false,
    features: [
      'Até 50 usuários',
      'Todos os recursos do Professional',
      'API completa',
      'Customizações',
      'Treinamento dedicado',
      'Suporte 24/7'
    ]
  }
])

const selectedPlan = ref('professional')
const paymentMethod = ref('credit_card')
const processing = ref(false)
const pixData = ref(null)

const cardData = ref({
  number: '',
  expiry: '',
  cvv: '',
  name: ''
})

const companyData = ref({
  name: '',
  cnpj: '',
  contactName: '',
  email: '',
  phone: ''
})

const selectedPlanData = computed(() => {
  return plans.value.find(p => p.id === selectedPlan.value)
})

const handleCheckout = async () => {
  processing.value = true
  
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    
    if (paymentMethod.value === 'pix') {
      // Gerar PIX
      const response = await fetch(`${apiUrl}/api/billing/checkout/pix`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: selectedPlan.value,
          company_name: companyData.value.name,
          contact_name: companyData.value.contactName,
          contact_email: companyData.value.email,
          contact_phone: companyData.value.phone
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        pixData.value = {
          qrCode: data.qr_code_base64,
          code: data.qr_code
        }
      }
    } else {
      // Processar cartão de crédito
      const response = await fetch(`${apiUrl}/api/billing/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: selectedPlan.value,
          company_name: companyData.value.name,
          contact_name: companyData.value.contactName,
          contact_email: companyData.value.email,
          contact_phone: companyData.value.phone,
          card_number: cardData.value.number,
          card_expiry: cardData.value.expiry,
          card_cvv: cardData.value.cvv,
          card_holder_name: cardData.value.name
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        router.push('/checkout/success')
      }
    }
  } catch (error) {
    console.error('Erro no checkout:', error)
    alert('Erro ao processar pagamento. Tente novamente.')
  } finally {
    processing.value = false
  }
}

const copyPixCode = () => {
  navigator.clipboard.writeText(pixData.value.code)
  alert('Código PIX copiado!')
}
</script>
