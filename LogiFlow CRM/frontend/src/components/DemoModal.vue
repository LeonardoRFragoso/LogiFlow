<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button @click="$emit('close')" class="close-btn">✕</button>
      
      <div class="modal-header">
        <h2 class="text-3xl font-bold text-gray-900">📋 Solicite uma Demonstração</h2>
        <p class="text-gray-600 mt-2">Preencha o formulário e nossa equipe entrará em contato em até 24 horas</p>
      </div>

      <form @submit.prevent="handleSubmit" class="demo-form">
        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Nome completo *</label>
            <input 
              v-model="form.name" 
              type="text" 
              required 
              class="form-input" 
              placeholder="Seu nome"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Email corporativo *</label>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              class="form-input" 
              placeholder="seu@email.com"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Telefone *</label>
            <input 
              v-model="form.phone" 
              type="tel" 
              required 
              class="form-input" 
              placeholder="(11) 99999-9999"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Empresa *</label>
            <input 
              v-model="form.company" 
              type="text" 
              required 
              class="form-input" 
              placeholder="Nome da empresa"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Quantidade de veículos</label>
          <input 
            v-model="form.vehicles" 
            type="text" 
            class="form-input" 
            placeholder="Ex: 10 caminhões"
          />
        </div>

        <div class="form-group">
          <label class="form-label">Mensagem adicional</label>
          <textarea 
            v-model="form.message" 
            class="form-input" 
            rows="3"
            placeholder="Conte-nos mais sobre suas necessidades..."
          ></textarea>
        </div>

        <p v-if="error" class="error-message">
          ⚠️ {{ error }}
        </p>

        <p v-if="success" class="success-message">
          ✅ {{ success }}
        </p>

        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="loading" class="loading-spinner"></span>
          {{ loading ? 'Enviando...' : 'Enviar Solicitação' }}
        </button>
      </form>

      <div class="modal-footer">
        <p class="text-sm text-gray-600">
          🔒 Seus dados estão seguros • ✅ Sem compromisso • 📞 Resposta em até 24h
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import api from '@/services/api'

const emit = defineEmits(['close'])

const form = reactive({
  name: '',
  email: '',
  phone: '',
  company: '',
  vehicles: '',
  message: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await api.post('/demo/request', form)
    success.value = response.data.message || 'Solicitação enviada com sucesso!'
    
    setTimeout(() => {
      emit('close')
    }, 3000)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erro ao enviar solicitação. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 1.5rem;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #f3f4f6;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
  transform: rotate(90deg);
}

.modal-header {
  text-align: center;
  margin-bottom: 2rem;
}

.demo-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f9fafb;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}

.error-message {
  color: #dc2626;
  font-size: 0.875rem;
  background: #fef2f2;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: center;
}

.success-message {
  color: #059669;
  font-size: 0.875rem;
  background: #f0fdf4;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: center;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.modal-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
  margin-top: 1rem;
}
</style>
