<template>
  <div class="config-whatsapp-container">
    <div class="header">
      <h1>Configurações WhatsApp</h1>
      <button @click="verificarConexao" class="btn btn-primary" :disabled="verificando">
        <i class="icon-refresh"></i> {{ verificando ? 'Verificando...' : 'Verificar Conexão' }}
      </button>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando configurações...</p>
    </div>

    <div v-else class="config-content">
      <div class="connection-status" :class="statusClass">
        <div class="status-icon">{{ statusEmoji }}</div>
        <div class="status-info">
          <h3>{{ statusText }}</h3>
          <p>{{ statusDescription }}</p>
          <button v-if="!config.is_connected" @click="mostrarQRCode" class="btn btn-primary">
            <i class="icon-qrcode"></i> Conectar WhatsApp
          </button>
        </div>
      </div>

      <form @submit.prevent="salvarConfiguracoes" class="config-form">
        <div class="section">
          <h2>🤖 Chatbot</h2>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.chatbot_enabled" />
              <span>Habilitar chatbot inteligente</span>
            </label>
            <p class="hint">O bot responderá automaticamente às mensagens dos clientes</p>
          </div>

          <div class="form-group">
            <label>Mensagem de Boas-vindas</label>
            <textarea 
              v-model="formData.chatbot_welcome_message" 
              rows="3"
              class="form-control"
              placeholder="Olá! Bem-vindo à LogiFlow..."
            ></textarea>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.chatbot_auto_reply" />
              <span>Resposta automática</span>
            </label>
            <p class="hint">Bot responderá automaticamente às mensagens</p>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.chatbot_business_hours_only" />
              <span>Apenas em horário comercial</span>
            </label>
            <p class="hint">Bot funcionará apenas durante horário de expediente</p>
          </div>
        </div>

        <div class="section" v-if="formData.chatbot_business_hours_only">
          <h2>🕐 Horário Comercial</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label>Horário Início</label>
              <input 
                type="time" 
                v-model="formData.business_hours_start" 
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label>Horário Fim</label>
              <input 
                type="time" 
                v-model="formData.business_hours_end" 
                class="form-control"
              />
            </div>
          </div>

          <div class="form-group">
            <label>Dias da Semana</label>
            <div class="days-selector">
              <label v-for="day in weekDays" :key="day.value" class="day-checkbox">
                <input 
                  type="checkbox" 
                  :value="day.value" 
                  v-model="formData.business_days"
                />
                <span>{{ day.label }}</span>
              </label>
            </div>
          </div>

          <div class="form-group">
            <label>Mensagem Fora do Horário</label>
            <textarea 
              v-model="formData.out_of_hours_message" 
              rows="3"
              class="form-control"
              placeholder="Estamos fora do horário comercial..."
            ></textarea>
          </div>
        </div>

        <div class="section">
          <h2>📢 Notificações Automáticas</h2>
          <p class="section-description">Configure quais eventos enviarão notificações automáticas</p>
          
          <div class="notifications-grid">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.auto_notify_pedido_confirmado" />
              <span>✅ Pedido Confirmado</span>
            </label>

            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.auto_notify_coleta_realizada" />
              <span>📦 Coleta Realizada</span>
            </label>

            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.auto_notify_em_transito" />
              <span>🚛 Em Trânsito</span>
            </label>

            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.auto_notify_saiu_entrega" />
              <span>🎉 Saiu para Entrega</span>
            </label>

            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.auto_notify_entregue" />
              <span>✅ Entregue</span>
            </label>

            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.auto_notify_ocorrencia" />
              <span>⚠️ Ocorrência</span>
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" :disabled="salvando" class="btn btn-primary btn-lg">
            {{ salvando ? 'Salvando...' : 'Salvar Configurações' }}
          </button>
          <button type="button" @click="$router.back()" class="btn btn-secondary btn-lg">
            Voltar
          </button>
        </div>
      </form>
    </div>

    <div v-if="showQRModal" class="modal">
      <div class="modal-content">
        <h2>Conectar WhatsApp</h2>
        <p>Escaneie o QR Code com seu WhatsApp</p>
        
        <div v-if="qrCodeLoading" class="loading">
          <div class="spinner"></div>
          <p>Gerando QR Code...</p>
        </div>
        
        <div v-else-if="qrCodeData" class="qrcode-container">
          <img :src="qrCodeData" alt="QR Code" class="qrcode-image" />
          <p class="qrcode-instructions">
            1. Abra o WhatsApp no seu celular<br>
            2. Toque em Menu > Dispositivos conectados<br>
            3. Toque em Conectar um dispositivo<br>
            4. Aponte seu celular para esta tela
          </p>
        </div>
        
        <div class="modal-actions">
          <button @click="showQRModal = false" class="btn btn-secondary">
            Fechar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const loading = ref(true)
const salvando = ref(false)
const verificando = ref(false)
const showQRModal = ref(false)
const qrCodeLoading = ref(false)
const qrCodeData = ref(null)

const config = ref({
  is_connected: false,
  connection_status: 'disconnected'
})

const formData = ref({
  chatbot_enabled: true,
  chatbot_welcome_message: 'Olá! Bem-vindo à LogiFlow! Como posso ajudar?',
  chatbot_auto_reply: true,
  chatbot_business_hours_only: false,
  business_hours_start: '08:00',
  business_hours_end: '18:00',
  business_days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
  out_of_hours_message: 'Olá! Estamos fora do horário comercial. Retornaremos em breve!',
  auto_notify_pedido_confirmado: true,
  auto_notify_coleta_realizada: true,
  auto_notify_em_transito: true,
  auto_notify_saiu_entrega: true,
  auto_notify_entregue: true,
  auto_notify_ocorrencia: true
})

const weekDays = [
  { value: 'monday', label: 'Seg' },
  { value: 'tuesday', label: 'Ter' },
  { value: 'wednesday', label: 'Qua' },
  { value: 'thursday', label: 'Qui' },
  { value: 'friday', label: 'Sex' },
  { value: 'saturday', label: 'Sáb' },
  { value: 'sunday', label: 'Dom' }
]

const statusClass = computed(() => {
  if (config.value.is_connected) return 'status-connected'
  return 'status-disconnected'
})

const statusEmoji = computed(() => {
  if (config.value.is_connected) return '✅'
  return '❌'
})

const statusText = computed(() => {
  if (config.value.is_connected) return 'WhatsApp Conectado'
  return 'WhatsApp Desconectado'
})

const statusDescription = computed(() => {
  if (config.value.is_connected) return 'Seu WhatsApp está conectado e pronto para enviar mensagens'
  return 'Conecte seu WhatsApp para começar a enviar mensagens'
})

async function carregarConfiguracoes() {
  loading.value = true
  try {
    const response = await api.get('/whatsapp/config')
    
    if (response.data.data) {
      Object.assign(config.value, response.data.data)
      Object.assign(formData.value, response.data.data)
    }
  } catch (error) {
    console.error('Erro ao carregar configurações:', error)
  } finally {
    loading.value = false
  }
}

async function verificarConexao() {
  verificando.value = true
  try {
    const response = await api.get('/whatsapp/status-conexao')
    config.value.is_connected = response.data.connected
    config.value.connection_status = response.data.status?.state || 'disconnected'
    
    if (response.data.connected) {
      alert('WhatsApp conectado com sucesso!')
    } else {
      alert('WhatsApp não está conectado')
    }
  } catch (error) {
    console.error('Erro ao verificar conexão:', error)
    alert('Erro ao verificar conexão')
  } finally {
    verificando.value = false
  }
}

async function mostrarQRCode() {
  showQRModal.value = true
  qrCodeLoading.value = true
  
  try {
    const response = await api.get('/whatsapp/qrcode')
    
    if (response.data.qrcode) {
      qrCodeData.value = response.data.qrcode.base64 || response.data.qrcode
    }
  } catch (error) {
    console.error('Erro ao obter QR Code:', error)
    alert('Erro ao gerar QR Code')
  } finally {
    qrCodeLoading.value = false
  }
}

async function salvarConfiguracoes() {
  salvando.value = true
  try {
    await api.put('/whatsapp/config', formData.value)
    alert('Configurações salvas com sucesso!')
  } catch (error) {
    console.error('Erro ao salvar configurações:', error)
    alert('Erro ao salvar configurações')
  } finally {
    salvando.value = false
  }
}

onMounted(() => {
  carregarConfiguracoes()
})
</script>

<style scoped>
.config-whatsapp-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  color: #333;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #25D366;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.config-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 30px;
  border-radius: 8px 8px 0 0;
  border-bottom: 2px solid #e9ecef;
}

.status-connected {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
}

.status-disconnected {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
}

.status-icon {
  font-size: 48px;
}

.status-info {
  flex: 1;
}

.status-info h3 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #333;
}

.status-info p {
  color: #666;
  margin-bottom: 15px;
}

.config-form {
  padding: 30px;
}

.section {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #e9ecef;
}

.section:last-child {
  border-bottom: none;
}

.section h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
}

.section-description {
  color: #6c757d;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #495057;
}

.form-control {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

.hint {
  font-size: 12px;
  color: #6c757d;
  margin: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.days-selector {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.day-checkbox {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.day-checkbox:hover {
  background: #e9ecef;
}

.notifications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-lg {
  padding: 12px 32px;
  font-size: 16px;
}

.btn-primary {
  background: #25D366;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 40px;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  text-align: center;
}

.modal-content h2 {
  margin-bottom: 10px;
  color: #333;
}

.qrcode-container {
  margin: 30px 0;
}

.qrcode-image {
  max-width: 300px;
  width: 100%;
  border: 4px solid #25D366;
  border-radius: 8px;
  margin-bottom: 20px;
}

.qrcode-instructions {
  text-align: left;
  line-height: 1.8;
  color: #666;
  font-size: 14px;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}
</style>
