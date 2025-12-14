<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" @click.self="$emit('close')">
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"></div>
        
        <!-- Modal -->
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-8 transform transition-all">
            <!-- Close Button -->
            <button @click="$emit('close')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>

            <!-- Header -->
            <div class="text-center mb-8">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-2xl mb-4">
                <span class="text-3xl">🚀</span>
              </div>
              <h2 class="text-3xl font-bold text-gray-900 mb-2">Solicitar Demonstração</h2>
              <p class="text-gray-600">Preencha o formulário e nossa equipe entrará em contato em até 24 horas</p>
            </div>

            <!-- Form -->
            <form @submit.prevent="handleSubmit" class="space-y-6">
              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Nome Completo *</label>
                  <input v-model="form.name" type="text" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                         placeholder="João Silva">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Email *</label>
                  <input v-model="form.email" type="email" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                         placeholder="joao@empresa.com.br">
                </div>
              </div>

              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Telefone/WhatsApp *</label>
                  <input v-model="form.phone" type="tel" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                         placeholder="(11) 99999-9999">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Empresa *</label>
                  <input v-model="form.company" type="text" required
                         class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                         placeholder="Transportadora XYZ">
                </div>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Quantos veículos você tem?</label>
                <select v-model="form.vehicles"
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all">
                  <option value="">Selecione...</option>
                  <option value="5-15">5-15 veículos</option>
                  <option value="15-50">15-50 veículos</option>
                  <option value="50-100">50-100 veículos</option>
                  <option value="100+">Mais de 100 veículos</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Mensagem (opcional)</label>
                <textarea v-model="form.message" rows="3"
                          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                          placeholder="Conte-nos mais sobre suas necessidades..."></textarea>
              </div>

              <!-- Success Message -->
              <div v-if="submitted" class="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start gap-3">
                <svg class="w-6 h-6 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <div>
                  <h4 class="font-bold text-green-800 mb-1">Solicitação enviada com sucesso!</h4>
                  <p class="text-sm text-green-700">Nossa equipe entrará em contato em breve. Verifique seu email.</p>
                </div>
              </div>

              <!-- Buttons -->
              <div class="flex gap-4">
                <button type="button" @click="$emit('close')"
                        class="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all">
                  Cancelar
                </button>
                <button type="submit" :disabled="submitting"
                        class="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-lg font-semibold hover:shadow-lg hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
                  {{ submitting ? 'Enviando...' : 'Solicitar Demonstração' }}
                </button>
              </div>

              <p class="text-xs text-center text-gray-500">
                Ao enviar, você concorda com nossa <a href="#" class="text-blue-600 hover:underline">Política de Privacidade</a>
              </p>
            </form>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, reactive } from 'vue'

defineProps({
  show: Boolean
})

const emit = defineEmits(['close'])

const form = reactive({
  name: '',
  email: '',
  phone: '',
  company: '',
  vehicles: '',
  message: ''
})

const submitting = ref(false)
const submitted = ref(false)

const handleSubmit = async () => {
  submitting.value = true
  
  try {
    // Enviar para o backend FastAPI
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/demo/request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form)
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.detail || 'Erro ao enviar solicitação')
    }
    
    console.log('✅ Solicitação enviada com sucesso:', data)
    
    submitting.value = false
    submitted.value = true
    
    // Fechar modal após 3 segundos
    setTimeout(() => {
      submitted.value = false
      emit('close')
      // Reset form
      Object.keys(form).forEach(key => form[key] = '')
    }, 3000)
    
  } catch (error) {
    console.error('❌ Erro ao enviar solicitação:', error)
    submitting.value = false
    
    // Mostrar erro para o usuário
    alert('Erro ao enviar solicitação. Por favor, tente novamente ou entre em contato por WhatsApp.')
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.9);
}
</style>
