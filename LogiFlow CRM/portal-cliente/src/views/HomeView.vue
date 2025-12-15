<template>
  <div class="home-container">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">📦</span>
          <span class="logo-text">LogiFlow</span>
        </div>
        <p class="header-subtitle">Rastreamento de Entregas</p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="search-container">
        <h1 class="search-title">Rastreie sua entrega</h1>
        <p class="search-subtitle">Digite o código de rastreamento</p>

        <form @submit.prevent="rastrear" class="search-form">
          <div class="input-group">
            <span class="input-icon">🔍</span>
            <input
              v-model="codigoRastreio"
              type="text"
              placeholder="Ex: ENT-2024-001"
              class="search-input"
              :class="{ 'input-error': erro }"
            />
            <button type="submit" class="search-button" :disabled="!codigoRastreio || loading">
              <span v-if="!loading">Rastrear</span>
              <span v-else class="loader"></span>
            </button>
          </div>
          <p v-if="erro" class="error-message">{{ erro }}</p>
        </form>

        <!-- Exemplos -->
        <div class="examples">
          <p class="examples-label">Exemplos de código:</p>
          <div class="examples-list">
            <button @click="codigoRastreio = 'ENT-2024-001'" class="example-btn">
              ENT-2024-001
            </button>
            <button @click="codigoRastreio = 'ENT-2024-002'" class="example-btn">
              ENT-2024-002
            </button>
          </div>
        </div>
      </div>

      <!-- Funcionalidades -->
      <div class="features">
        <div class="feature-card">
          <span class="feature-icon">🗺️</span>
          <h3 class="feature-title">Localização em Tempo Real</h3>
          <p class="feature-text">Acompanhe sua entrega no mapa</p>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔔</span>
          <h3 class="feature-title">Notificações</h3>
          <p class="feature-text">Receba atualizações por WhatsApp</p>
        </div>
        <div class="feature-card">
          <span class="feature-icon">📋</span>
          <h3 class="feature-title">Histórico Completo</h3>
          <p class="feature-text">Veja todas as atualizações da entrega</p>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <p>&copy; 2024 LogiFlow CRM - Todos os direitos reservados</p>
      <div class="footer-links">
        <a href="#">Termos</a>
        <span>•</span>
        <a href="#">Privacidade</a>
        <span>•</span>
        <a href="#">Suporte</a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const codigoRastreio = ref('')
const loading = ref(false)
const erro = ref('')

function rastrear() {
  erro.value = ''
  
  if (!codigoRastreio.value) {
    erro.value = 'Digite um código de rastreamento'
    return
  }

  loading.value = true
  
  setTimeout(() => {
    loading.value = false
    router.push(`/rastrear/${codigoRastreio.value}`)
  }, 500)
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #1e40af 0%, #059669 100%);
}

.header {
  padding: 2rem 1rem;
  color: white;
  text-align: center;
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.logo-icon {
  font-size: 2.5rem;
}

.logo-text {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
}

.main-content {
  flex: 1;
  padding: 2rem 1rem;
}

.search-container {
  max-width: 600px;
  margin: 0 auto 3rem;
  background: white;
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.search-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  text-align: center;
}

.search-subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 2rem;
}

.search-form {
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
  align-items: stretch;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
  pointer-events: none;
}

.search-input {
  flex: 1;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
  position: relative;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-error {
  border-color: #ef4444;
}

.search-button {
  padding: 0 2rem;
  background: linear-gradient(135deg, #3b82f6 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 120px;
}

.search-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.search-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loader {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.examples {
  text-align: center;
}

.examples-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.examples-list {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.example-btn {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Courier New', monospace;
}

.example-btn:hover {
  background: #e5e7eb;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.feature-text {
  color: #6b7280;
  font-size: 0.875rem;
}

.footer {
  padding: 2rem 1rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  margin-top: 0.5rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: white;
}

@media (max-width: 640px) {
  .search-container {
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  .search-title {
    font-size: 1.5rem;
  }

  .input-group {
    flex-direction: column;
  }

  .search-button {
    width: 100%;
    padding: 1rem;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
}
</style>

