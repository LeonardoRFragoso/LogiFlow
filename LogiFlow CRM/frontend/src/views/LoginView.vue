<template>
  <div class="login-page">
    <!-- Left Side - Branding -->
    <div class="login-branding">
      <div class="branding-content">
        <img src="/logo.png" alt="LogiFlow CRM" class="logo-large" />
        <h1 class="tagline">Sua transportadora no controle.</h1>
        <p class="subtitle">Do comercial à entrega.</p>
        
        <div class="features">
          <div class="feature-item">
            <span class="feature-icon">📦</span>
            <span>Gestão de Pedidos</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🚚</span>
            <span>Controle de Frota</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">📄</span>
            <span>CT-e / MDF-e Integrado</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">📊</span>
            <span>Dashboard em Tempo Real</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side - Login Form -->
    <div class="login-form-container">
      <div class="login-card">
        <div class="text-center mb-8">
          <img src="/logo.png" alt="LogiFlow CRM" class="h-16 mx-auto mb-4 md:hidden" />
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white">Bem-vindo de volta!</h2>
          <p class="text-gray-500 dark:text-gray-400 mt-1">Acesse sua conta para continuar</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Usuário</label>
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input v-model="form.username" type="text" required class="input-with-icon" placeholder="Digite seu usuário" />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Senha</label>
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input v-model="form.password" type="password" required class="input-with-icon" placeholder="Digite sua senha" />
            </div>
          </div>
          
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
              <span class="text-gray-600 dark:text-gray-400">Lembrar-me</span>
            </label>
            <a href="#" class="text-blue-600 hover:text-blue-700 dark:text-blue-400">Esqueceu a senha?</a>
          </div>

          <p v-if="error" class="text-red-600 dark:text-red-400 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
            ⚠️ {{ error }}
          </p>

          <button type="submit" :disabled="loading" class="login-button">
            <span v-if="loading" class="loading-spinner"></span>
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <p class="text-center text-gray-500 dark:text-gray-400 text-sm">
            Novo por aqui? <a href="#" class="text-blue-600 hover:underline dark:text-blue-400 font-medium">Solicite uma demonstração</a>
          </p>
        </div>

        <p class="text-center text-gray-400 text-xs mt-6">© 2025 LogiFlow CRM - Todos os direitos reservados</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(form.username, form.password)
    router.push('/')
  } catch (e) {
    error.value = 'Usuário ou senha inválidos'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
}

/* Left Branding Side */
.login-branding {
  flex: 1;
  background: linear-gradient(135deg, rgba(30, 64, 175, 0.9) 0%, rgba(5, 150, 105, 0.9) 100%), 
              url('/backgroud.png');
  background-size: cover;
  background-position: center;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

@media (min-width: 1024px) {
  .login-branding {
    display: flex;
  }
}

.branding-content {
  color: white;
  max-width: 500px;
}

.logo-large {
  height: 120px;
  margin-bottom: 2rem;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
}

.tagline {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.5rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.features {
  display: grid;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.15);
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  backdrop-filter: blur(10px);
  transition: transform 0.2s, background 0.2s;
}

.feature-item:hover {
  transform: translateX(10px);
  background: rgba(255, 255, 255, 0.25);
}

.feature-icon {
  font-size: 1.5rem;
}

/* Right Form Side */
.login-form-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 2rem;
}

.dark .login-form-container {
  background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 420px;
}

.dark .login-card {
  background: #1f2937;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

/* Input Styling */
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

.dark .input-with-icon {
  background: #374151;
  border-color: #4b5563;
  color: white;
}

.input-with-icon:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.dark .input-with-icon:focus {
  background: #1f2937;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

/* Button Styling */
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
</style>
