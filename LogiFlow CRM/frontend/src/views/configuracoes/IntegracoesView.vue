<template>
  <div class="integracoes-view">
    <div class="page-header">
      <h1>🔌 Integrações</h1>
      <p>Configure suas credenciais de ERP, GPS e outras integrações</p>
    </div>

    <!-- Tabs de Categorias -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.icon }} {{ tab.name }}
      </button>
    </div>

    <!-- Conteúdo da Tab Ativa -->
    <div class="tab-content">
      <!-- ERP -->
      <div v-if="activeTab === 'erp'" class="integrations-section">
        <div class="section-header">
          <h2>🔗 Integrações ERP</h2>
          <p>Conecte seu ERP para sincronização automática de clientes e pedidos</p>
        </div>

        <div class="integrations-grid">
          <div 
            v-for="provider in erpProviders" 
            :key="provider.id"
            class="integration-card"
            :class="{ configured: isConfigured('erp', provider.id) }"
          >
            <div class="card-header">
              <div class="provider-info">
                <span class="provider-icon">{{ provider.icon }}</span>
                <h3>{{ provider.name }}</h3>
              </div>
              <span v-if="isConfigured('erp', provider.id)" class="badge-configured">✓ Configurado</span>
            </div>

            <p class="provider-description">{{ provider.description }}</p>

            <div class="provider-fields">
              <p><strong>Campos necessários:</strong></p>
              <ul>
                <li v-for="field in provider.fields" :key="field">{{ formatFieldName(field) }}</li>
              </ul>
            </div>

            <div class="card-actions">
              <button 
                v-if="!isConfigured('erp', provider.id)"
                @click="openConfigModal('erp', provider)"
                class="btn-primary"
              >
                Configurar
              </button>
              <button 
                v-else
                @click="openConfigModal('erp', provider)"
                class="btn-secondary"
              >
                Editar
              </button>
              <button 
                v-if="isConfigured('erp', provider.id)"
                @click="testConnection('erp', provider.id)"
                class="btn-test"
              >
                🔍 Testar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- GPS -->
      <div v-if="activeTab === 'gps'" class="integrations-section">
        <div class="section-header">
          <h2>🛰️ Rastreamento GPS</h2>
          <p>Conecte seu sistema de rastreamento para monitorar sua frota em tempo real</p>
          <div class="plan-badge">Disponível no Plano Enterprise</div>
        </div>

        <div class="integrations-grid">
          <div 
            v-for="provider in gpsProviders" 
            :key="provider.id"
            class="integration-card"
            :class="{ configured: isConfigured('gps', provider.id) }"
          >
            <div class="card-header">
              <div class="provider-info">
                <span class="provider-icon">{{ provider.icon }}</span>
                <h3>{{ provider.name }}</h3>
              </div>
              <span v-if="isConfigured('gps', provider.id)" class="badge-configured">✓ Configurado</span>
            </div>

            <p class="provider-description">{{ provider.description }}</p>

            <div class="provider-fields">
              <p><strong>Campos necessários:</strong></p>
              <ul>
                <li v-for="field in provider.fields" :key="field">{{ formatFieldName(field) }}</li>
              </ul>
            </div>

            <div class="card-actions">
              <button 
                v-if="!isConfigured('gps', provider.id)"
                @click="openConfigModal('gps', provider)"
                class="btn-primary"
              >
                Configurar
              </button>
              <button 
                v-else
                @click="openConfigModal('gps', provider)"
                class="btn-secondary"
              >
                Editar
              </button>
              <button 
                v-if="isConfigured('gps', provider.id)"
                @click="testConnection('gps', provider.id)"
                class="btn-test"
              >
                🔍 Testar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Frete -->
      <div v-if="activeTab === 'freight'" class="integrations-section">
        <div class="section-header">
          <h2>📦 Cotação de Frete</h2>
          <p>Configure suas integrações de frete para cotação automática</p>
        </div>

        <div class="integrations-grid">
          <div 
            v-for="provider in freightProviders" 
            :key="provider.id"
            class="integration-card"
            :class="{ configured: isConfigured('freight', provider.id) }"
          >
            <div class="card-header">
              <div class="provider-info">
                <span class="provider-icon">{{ provider.icon }}</span>
                <h3>{{ provider.name }}</h3>
              </div>
              <span v-if="isConfigured('freight', provider.id)" class="badge-configured">✓ Configurado</span>
            </div>

            <p class="provider-description">{{ provider.description }}</p>

            <div class="provider-fields">
              <p><strong>Campos necessários:</strong></p>
              <ul>
                <li v-for="field in provider.fields" :key="field">{{ formatFieldName(field) }}</li>
              </ul>
            </div>

            <div class="card-actions">
              <button 
                v-if="!isConfigured('freight', provider.id)"
                @click="openConfigModal('freight', provider)"
                class="btn-primary"
              >
                Configurar
              </button>
              <button 
                v-else
                @click="openConfigModal('freight', provider)"
                class="btn-secondary"
              >
                Editar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Configuração -->
    <div v-if="showConfigModal" class="modal-overlay" @click="closeConfigModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalProvider?.icon }} Configurar {{ modalProvider?.name }}</h3>
          <button @click="closeConfigModal" class="btn-close">×</button>
        </div>

        <div class="modal-body">
          <p class="modal-description">{{ modalProvider?.description }}</p>

          <form @submit.prevent="saveCredentials">
            <div v-for="field in modalProvider?.fields" :key="field" class="form-group">
              <label>{{ formatFieldName(field) }} *</label>
              <input 
                v-model="credentialsForm[field]"
                :type="field.includes('password') || field.includes('secret') ? 'password' : 'text'"
                class="form-control"
                :placeholder="`Digite ${formatFieldName(field).toLowerCase()}`"
                required
              >
            </div>

            <div class="form-group checkbox-group">
              <label>
                <input type="checkbox" v-model="credentialsForm.is_active">
                Ativar integração imediatamente
              </label>
            </div>

            <div class="modal-actions">
              <button type="button" @click="closeConfigModal" class="btn-secondary">
                Cancelar
              </button>
              <button type="submit" class="btn-primary" :disabled="saving">
                {{ saving ? 'Salvando...' : 'Salvar Credenciais' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal de Teste -->
    <div v-if="showTestModal" class="modal-overlay" @click="showTestModal = false">
      <div class="modal-content test-modal" @click.stop>
        <div class="modal-header">
          <h3>🔍 Teste de Conexão</h3>
          <button @click="showTestModal = false" class="btn-close">×</button>
        </div>

        <div class="modal-body">
          <div v-if="testResult" class="test-result" :class="testResult.is_valid ? 'success' : 'error'">
            <div class="result-icon">
              {{ testResult.is_valid ? '✅' : '❌' }}
            </div>
            <h4>{{ testResult.message }}</h4>
            <div v-if="testResult.details" class="result-details">
              <p><strong>Provider:</strong> {{ testResult.details.provider }}</p>
              <p><strong>Teste:</strong> {{ testResult.details.test_performed }}</p>
              <p v-if="testResult.details.response_time_ms">
                <strong>Tempo de resposta:</strong> {{ testResult.details.response_time_ms }}ms
              </p>
            </div>
          </div>
          <div v-else class="testing">
            <div class="spinner"></div>
            <p>Testando conexão...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const activeTab = ref('erp')
const showConfigModal = ref(false)
const showTestModal = ref(false)
const modalType = ref('')
const modalProvider = ref(null)
const credentialsForm = ref({})
const saving = ref(false)
const testResult = ref(null)
const configuredCredentials = ref([])

const tabs = [
  { id: 'erp', name: 'ERP', icon: '🔗' },
  { id: 'gps', name: 'GPS', icon: '🛰️' },
  { id: 'freight', name: 'Frete', icon: '📦' }
]

const erpProviders = [
  {
    id: 'omie',
    name: 'Omie ERP',
    icon: '🔵',
    description: 'Sistema ERP completo para gestão empresarial',
    fields: ['app_key', 'app_secret']
  },
  {
    id: 'bling',
    name: 'Bling ERP',
    icon: '🟢',
    description: 'ERP online para e-commerce e varejo',
    fields: ['access_token']
  },
  {
    id: 'tiny',
    name: 'Tiny ERP',
    icon: '🟠',
    description: 'Sistema de gestão empresarial simplificado',
    fields: ['token']
  }
]

const gpsProviders = [
  {
    id: 'sascar',
    name: 'Sascar',
    icon: '🛰️',
    description: 'Rastreamento e gestão de frotas',
    fields: ['api_key', 'api_secret']
  },
  {
    id: 'autotrac',
    name: 'Autotrac',
    icon: '📡',
    description: 'Tecnologia em rastreamento veicular',
    fields: ['username', 'password']
  },
  {
    id: 'onixsat',
    name: 'Onixsat',
    icon: '🌐',
    description: 'Rastreamento via satélite',
    fields: ['api_token']
  }
]

const freightProviders = [
  {
    id: 'melhor_envio',
    name: 'Melhor Envio',
    icon: '📦',
    description: 'Cotação com múltiplas transportadoras',
    fields: ['token']
  },
  {
    id: 'frenet',
    name: 'Frenet',
    icon: '🚚',
    description: 'Cálculo de frete inteligente',
    fields: ['token']
  }
]

const isConfigured = (type, providerId) => {
  return configuredCredentials.value.some(
    c => c.integration_type === type && c.provider === providerId
  )
}

const formatFieldName = (field) => {
  const names = {
    'app_key': 'App Key',
    'app_secret': 'App Secret',
    'access_token': 'Access Token',
    'token': 'Token',
    'api_key': 'API Key',
    'api_secret': 'API Secret',
    'username': 'Usuário',
    'password': 'Senha',
    'api_token': 'API Token'
  }
  return names[field] || field
}

const openConfigModal = (type, provider) => {
  modalType.value = type
  modalProvider.value = provider
  credentialsForm.value = {
    is_active: true
  }
  showConfigModal.value = true
}

const closeConfigModal = () => {
  showConfigModal.value = false
  modalType.value = ''
  modalProvider.value = null
  credentialsForm.value = {}
}

const saveCredentials = async () => {
  saving.value = true
  try {
    const credentials = { ...credentialsForm.value }
    delete credentials.is_active

    const response = await api.post('/tenant-credentials/credentials', {
      integration_type: modalType.value,
      provider: modalProvider.value.id,
      credentials: credentials
    })

    if (response.data.success) {
      alert('Credenciais salvas com sucesso!')
      await loadCredentials()
      closeConfigModal()
    }
  } catch (error) {
    console.error('Erro ao salvar credenciais:', error)
    alert('Erro ao salvar credenciais: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

const testConnection = async (type, providerId) => {
  showTestModal.value = true
  testResult.value = null

  try {
    const credential = configuredCredentials.value.find(
      c => c.integration_type === type && c.provider === providerId
    )

    if (!credential) {
      testResult.value = {
        is_valid: false,
        message: 'Credencial não encontrada'
      }
      return
    }

    const response = await api.post(`/tenant-credentials/credentials/${credential.id}/validate`)
    testResult.value = response.data
  } catch (error) {
    console.error('Erro ao testar conexão:', error)
    testResult.value = {
      is_valid: false,
      message: 'Erro ao testar conexão: ' + (error.response?.data?.detail || error.message)
    }
  }
}

const loadCredentials = async () => {
  try {
    const response = await api.get('/tenant-credentials/credentials')
    if (response.data.success) {
      configuredCredentials.value = response.data.credentials
    }
  } catch (error) {
    console.error('Erro ao carregar credenciais:', error)
  }
}

onMounted(() => {
  loadCredentials()
})
</script>

<style scoped>
.integracoes-view {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e5e7eb;
}

.tab {
  background: none;
  border: none;
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: #6b7280;
  border-bottom: 3px solid transparent;
  transition: all 0.2s;
}

.tab:hover {
  color: #3b82f6;
}

.tab.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
}

.integrations-section {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.section-header p {
  color: #666;
}

.plan-badge {
  display: inline-block;
  background: #fef3c7;
  color: #92400e;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

.integrations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.integration-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s;
}

.integration-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.integration-card.configured {
  border-color: #10b981;
  background: #f0fdf4;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.provider-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.provider-icon {
  font-size: 2rem;
}

.provider-info h3 {
  font-size: 1.25rem;
  margin: 0;
}

.badge-configured {
  background: #10b981;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.provider-description {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.provider-fields {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.provider-fields p {
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.provider-fields ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.provider-fields li {
  padding: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.provider-fields li:before {
  content: "• ";
  color: #3b82f6;
  font-weight: bold;
  margin-right: 0.5rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-primary, .btn-secondary, .btn-test {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  background: #d1d5db;
}

.btn-test {
  background: #10b981;
  color: white;
  flex: 0.5;
}

.btn-test:hover {
  background: #059669;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #9ca3af;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 1.5rem;
}

.modal-description {
  color: #666;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.modal-actions button {
  flex: 1;
}

.test-modal .modal-body {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.test-result {
  text-align: center;
  padding: 2rem;
}

.test-result.success {
  color: #10b981;
}

.test-result.error {
  color: #ef4444;
}

.result-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.result-details {
  margin-top: 1.5rem;
  text-align: left;
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
}

.result-details p {
  margin: 0.5rem 0;
  color: #374151;
}

.testing {
  text-align: center;
}

.spinner {
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
