<template>
  <div class="tracking-container">
    <!-- Header -->
    <header class="tracking-header">
      <button @click="router.push('/')" class="back-button">
        ← Voltar
      </button>
      <h1 class="header-title">Rastreamento</h1>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando informações...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-state">
      <span class="error-icon">⚠️</span>
      <h2>Entrega não encontrada</h2>
      <p>{{ error }}</p>
      <button @click="router.push('/')" class="btn-primary">
        Fazer nova busca
      </button>
    </div>

    <!-- Content -->
    <div v-else-if="entrega" class="tracking-content">
      <!-- Status Card -->
      <div class="status-card">
        <div class="status-icon-wrapper" :class="`status-${entrega.status}`">
          <span class="status-icon">{{ getStatusIcon(entrega.status) }}</span>
        </div>
        <h2 class="status-title">{{ getStatusLabel(entrega.status) }}</h2>
        <p class="status-subtitle">{{ entrega.codigo }}</p>
        <p v-if="entrega.previsao_entrega" class="status-date">
          Previsão: {{ formatarData(entrega.previsao_entrega) }}
        </p>
      </div>

      <!-- Informações -->
      <div class="info-card">
        <h3 class="card-title">📋 Informações da Entrega</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Remetente:</span>
            <span class="info-value">{{ entrega.remetente || 'LogiFlow' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Destinatário:</span>
            <span class="info-value">{{ entrega.destinatario }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Destino:</span>
            <span class="info-value">
              {{ entrega.destino?.cidade }}/{{ entrega.destino?.uf }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Peso:</span>
            <span class="info-value">{{ entrega.peso_kg }}kg</span>
          </div>
        </div>
      </div>

      <!-- Mapa -->
      <div v-if="entrega.localizacao" class="map-card">
        <h3 class="card-title">🗺️ Localização Atual</h3>
        <div class="map-container">
          <div class="map-placeholder">
            <span class="map-icon">📍</span>
            <p class="map-text">
              {{ entrega.localizacao.cidade }}, {{ entrega.localizacao.uf }}
            </p>
            <p class="map-coords">
              {{ entrega.localizacao.lat }}, {{ entrega.localizacao.lng }}
            </p>
            <button @click="abrirMapa" class="btn-map">
              Abrir no Google Maps
            </button>
          </div>
        </div>
      </div>

      <!-- Timeline -->
      <div class="timeline-card">
        <h3 class="card-title">📊 Histórico de Rastreamento</h3>
        <div class="timeline">
          <div 
            v-for="(evento, index) in entrega.timeline"
            :key="index"
            class="timeline-item"
            :class="{ 'timeline-item-last': index === entrega.timeline.length - 1 }"
          >
            <div class="timeline-marker" :class="`marker-${evento.tipo}`"></div>
            <div class="timeline-content">
              <p class="timeline-date">{{ formatarDataHora(evento.data) }}</p>
              <h4 class="timeline-title">{{ evento.titulo }}</h4>
              <p class="timeline-description">{{ evento.descricao }}</p>
              <p v-if="evento.local" class="timeline-local">
                📍 {{ evento.local }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Notificações -->
      <div class="notification-card">
        <h3 class="card-title">🔔 Receber Atualizações</h3>
        <p class="notification-text">
          Cadastre seu WhatsApp para receber notificações sobre esta entrega
        </p>
        <form @submit.prevent="cadastrarWhatsApp" class="notification-form">
          <input
            v-model="whatsapp"
            type="tel"
            placeholder="(11) 99999-9999"
            class="notification-input"
          />
          <button type="submit" class="btn-primary" :disabled="loadingWhatsApp">
            {{ loadingWhatsApp ? 'Cadastrando...' : 'Cadastrar' }}
          </button>
        </form>
        <p v-if="whatsappSuccess" class="success-message">
          ✓ WhatsApp cadastrado com sucesso!
        </p>
      </div>

      <!-- Ações -->
      <div class="actions-card">
        <button @click="compartilhar" class="btn-action">
          <span>📤</span>
          Compartilhar
        </button>
        <button @click="imprimir" class="btn-action">
          <span>🖨️</span>
          Imprimir
        </button>
        <button @click="atualizar" class="btn-action">
          <span>🔄</span>
          Atualizar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const codigo = computed(() => route.params.codigo)
const loading = ref(true)
const error = ref('')
const entrega = ref(null)
const whatsapp = ref('')
const loadingWhatsApp = ref(false)
const whatsappSuccess = ref(false)

onMounted(() => {
  carregarEntrega()
})

async function carregarEntrega() {
  loading.value = true
  error.value = ''

  try {
    // Simulação - em produção, fazer fetch para API
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Mock de dados
    entrega.value = {
      codigo: codigo.value,
      status: 'em_transito',
      destinatario: 'João Silva',
      remetente: 'Loja Exemplo',
      destino: {
        cidade: 'São Paulo',
        uf: 'SP',
        endereco: 'Rua Exemplo, 123'
      },
      peso_kg: 5.5,
      previsao_entrega: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
      localizacao: {
        lat: -23.5505,
        lng: -46.6333,
        cidade: 'Campinas',
        uf: 'SP'
      },
      timeline: [
        {
          tipo: 'info',
          data: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
          titulo: 'Entrega em trânsito',
          descricao: 'Veículo está a caminho do destino',
          local: 'Campinas, SP'
        },
        {
          tipo: 'success',
          data: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          titulo: 'Saiu para entrega',
          descricao: 'Pedido saiu do centro de distribuição',
          local: 'São Paulo, SP'
        },
        {
          tipo: 'success',
          data: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
          titulo: 'Em trânsito',
          descricao: 'Mercadoria em transporte',
          local: 'Guarulhos, SP'
        },
        {
          tipo: 'success',
          data: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
          titulo: 'Coletado',
          descricao: 'Pacote foi coletado',
          local: 'Rio de Janeiro, RJ'
        },
        {
          tipo: 'default',
          data: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          titulo: 'Pedido criado',
          descricao: 'Pedido registrado no sistema',
          local: 'Rio de Janeiro, RJ'
        }
      ]
    }
  } catch (err) {
    error.value = 'Não foi possível carregar as informações da entrega. Tente novamente.'
  } finally {
    loading.value = false
  }
}

function getStatusIcon(status) {
  const icons = {
    aguardando_coleta: '⏳',
    coletado: '📦',
    em_transito: '🚚',
    saiu_para_entrega: '🚛',
    entregue: '✅',
    cancelado: '❌'
  }
  return icons[status] || '📦'
}

function getStatusLabel(status) {
  const labels = {
    aguardando_coleta: 'Aguardando Coleta',
    coletado: 'Coletado',
    em_transito: 'Em Trânsito',
    saiu_para_entrega: 'Saiu para Entrega',
    entregue: 'Entregue',
    cancelado: 'Cancelado'
  }
  return labels[status] || status
}

function formatarData(data) {
  return new Date(data).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatarDataHora(data) {
  return new Date(data).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function abrirMapa() {
  const { lat, lng } = entrega.value.localizacao
  window.open(`https://www.google.com/maps?q=${lat},${lng}`, '_blank')
}

async function cadastrarWhatsApp() {
  if (!whatsapp.value) return

  loadingWhatsApp.value = true
  whatsappSuccess.value = false

  try {
    // Simular chamada API
    await new Promise(resolve => setTimeout(resolve, 1500))
    whatsappSuccess.value = true
    setTimeout(() => {
      whatsappSuccess.value = false
    }, 3000)
  } finally {
    loadingWhatsApp.value = false
  }
}

function compartilhar() {
  if (navigator.share) {
    navigator.share({
      title: `Rastreamento ${entrega.value.codigo}`,
      text: `Acompanhe minha entrega: ${entrega.value.codigo}`,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    alert('Link copiado para área de transferência!')
  }
}

function imprimir() {
  window.print()
}

function atualizar() {
  carregarEntrega()
}
</script>

<style scoped>
.tracking-container {
  min-height: 100vh;
  background: #f8fafc;
  padding-bottom: 2rem;
}

.tracking-header {
  background: linear-gradient(135deg, #1e40af 0%, #059669 100%);
  padding: 1.5rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
}

.error-state h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.error-state p {
  color: #6b7280;
  margin-bottom: 2rem;
}

.tracking-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.status-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
}

.status-icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
}

.status-icon-wrapper.status-em_transito {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
}

.status-icon-wrapper.status-entregue {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
}

.status-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.status-subtitle {
  color: #6b7280;
  font-family: 'Courier New', monospace;
  margin-bottom: 0.5rem;
}

.status-date {
  color: #9ca3af;
  font-size: 0.875rem;
}

.info-card,
.map-card,
.timeline-card,
.notification-card,
.actions-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.info-value {
  font-weight: 500;
  color: #1a1a1a;
}

.map-container {
  border-radius: 0.75rem;
  overflow: hidden;
  border: 2px solid #e5e7eb;
}

.map-placeholder {
  height: 250px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.map-icon {
  font-size: 3rem;
}

.map-text {
  font-weight: 600;
  color: #374151;
}

.map-coords {
  font-size: 0.75rem;
  color: #9ca3af;
  font-family: 'Courier New', monospace;
}

.btn-map {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-map:hover {
  background: #2563eb;
}

.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline-item {
  position: relative;
  padding-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -1.5rem;
  top: 1rem;
  bottom: -1rem;
  width: 2px;
  background: #e5e7eb;
}

.timeline-item-last::before {
  display: none;
}

.timeline-marker {
  position: absolute;
  left: -1.875rem;
  top: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #3b82f6;
  border: 3px solid white;
  box-shadow: 0 0 0 2px #e5e7eb;
}

.timeline-marker.marker-success {
  background: #10b981;
}

.timeline-marker.marker-info {
  background: #3b82f6;
}

.timeline-marker.marker-default {
  background: #9ca3af;
}

.timeline-content {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 0.75rem;
}

.timeline-date {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.timeline-title {
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.25rem;
}

.timeline-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.timeline-local {
  font-size: 0.75rem;
  color: #9ca3af;
}

.notification-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.notification-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.notification-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.notification-text {
  color: #6b7280;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.success-message {
  color: #10b981;
  font-size: 0.875rem;
  font-weight: 500;
}

.actions-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.btn-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #f3f4f6;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.btn-action:hover {
  background: #e5e7eb;
  transform: translateY(-2px);
}

.btn-action span {
  font-size: 1.5rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .tracking-content {
    padding: 1rem 0.5rem;
  }

  .status-card {
    padding: 2rem 1rem;
  }

  .notification-form {
    flex-direction: column;
  }
}

@media print {
  .tracking-header,
  .notification-card,
  .actions-card {
    display: none;
  }
}
</style>

