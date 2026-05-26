<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Logo -->
      <div class="logo-section">
        <span class="logo-icon">📦</span>
        <h1 class="logo-text">LogiFlow</h1>
        <p class="logo-subtitle">Portal do Cliente</p>
      </div>

      <!-- Form -->
      <div class="login-card">
        <h2 class="form-title">Acesse sua conta</h2>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="seu@email.com"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Senha</label>
            <input
              v-model="senha"
              type="password"
              required
              placeholder="••••••••"
              class="form-input"
            />
          </div>

          <div v-if="error" class="error-message">
            ⚠️ {{ error }}
          </div>

          <button type="submit" :disabled="loading" class="submit-button">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <!-- Demo Info -->
        <div class="demo-info">
          <p class="demo-label">Credenciais de demonstração:</p>
          <p class="demo-credentials">cliente@demo.com / cliente123</p>
        </div>

        <!-- Back Link -->
        <div class="back-link">
          <router-link to="/">← Voltar ao rastreamento</router-link>
        </div>
      </div>
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
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #1e40af 0%, #059669 100%);
}

.login-container {
  width: 100%;
  max-width: 420px;
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
  color: white;
}

.logo-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.logo-text {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.logo-subtitle {
  font-size: 0.875rem;
  opacity: 0.9;
  margin: 0.5rem 0 0 0;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
  margin: 0 0 1.5rem 0;
  color: #1f2937;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
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

.error-message {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.submit-button {
  padding: 0.875rem 1rem;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.demo-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  text-align: center;
}

.demo-label {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0 0 0.5rem 0;
}

.demo-credentials {
  font-size: 0.875rem;
  color: #374151;
  font-family: monospace;
  margin: 0;
}

.back-link {
  text-align: center;
  margin-top: 1.5rem;
}

.back-link a {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.back-link a:hover {
  color: #1e40af;
}
</style>
