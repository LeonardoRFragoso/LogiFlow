<template>
  <div class="login-page">
    <div class="mx-auto w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="logo-container">
          <span class="text-4xl">🚛</span>
        </div>
        <h1 class="text-2xl font-bold text-white mt-4">LogiFlow</h1>
        <p class="text-white/70 text-sm">App do Motorista</p>
      </div>

      <!-- Form -->
      <div class="login-card">
        <h2 class="text-xl font-semibold text-gray-800 mb-6 text-center">Bem-vindo de volta!</h2>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input
                v-model="email"
                type="email"
                required
                placeholder="seu@email.com"
                class="input-with-icon"
              />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Senha</label>
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input
                v-model="senha"
                type="password"
                required
                placeholder="••••••••"
                class="input-with-icon"
              />
            </div>
          </div>

          <div v-if="error" class="error-message">
            ⚠️ {{ error }}
          </div>

          <button type="submit" :disabled="loading" class="login-button">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <!-- Demo credentials -->
        <div class="demo-credentials">
          <p class="text-xs text-gray-500 text-center mb-1">Credenciais de demonstração:</p>
          <p class="text-xs text-gray-600 text-center font-mono">admin@logiflow.com / admin123</p>
        </div>
      </div>

      <p class="text-center text-white/60 text-xs mt-6">
        © 2025 LogiFlow CRM - Todos os direitos reservados
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const senha = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  
  try {
    const result = await authStore.login(email.value, senha.value)
    
    if (result.success) {
      router.push('/')
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = 'Erro ao conectar com o servidor'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(30, 64, 175, 0.95) 0%, rgba(5, 150, 105, 0.95) 100%);
}

.logo-container {
  width: 5rem;
  height: 5rem;
  background: white;
  border-radius: 1.25rem;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.1rem;
}

.input-with-icon {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f9fafb;
}

.input-with-icon:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.error-message {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
}

.login-button {
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

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
}

.login-button:disabled {
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

.demo-credentials {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
}
</style>
