<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <div class="header-info">
            <h2>📦 {{ entrega?.codigo }}</h2>
            <span :class="['status-badge', 'status-' + entrega?.status]">
              {{ statusLabel(entrega?.status) }}
            </span>
          </div>
          <button @click="close" class="btn-close">✕</button>
        </div>

        <div class="modal-body">
          <!-- Progress Bar -->
          <div class="progress-section">
            <div class="progress-steps">
              <div :class="['step', getStepClass(1)]">
                <div class="step-dot">📝</div>
                <span>Criado</span>
              </div>
              <div class="step-line" :class="{ active: stepNumber >= 2 }"></div>
              <div :class="['step', getStepClass(2)]">
                <div class="step-dot">📦</div>
                <span>Coletado</span>
              </div>
              <div class="step-line" :class="{ active: stepNumber >= 3 }"></div>
              <div :class="['step', getStepClass(3)]">
                <div class="step-dot">🚛</div>
                <span>Em Trânsito</span>
              </div>
              <div class="step-line" :class="{ active: stepNumber >= 4 }"></div>
              <div :class="['step', getStepClass(4)]">
                <div class="step-dot">🏠</div>
                <span>Saiu p/ Entrega</span>
              </div>
              <div class="step-line" :class="{ active: stepNumber >= 5 }"></div>
              <div :class="['step', getStepClass(5)]">
                <div class="step-dot">✅</div>
                <span>Entregue</span>
              </div>
            </div>
          </div>

          <!-- Info Cards -->
          <div class="info-grid">
            <!-- Cliente -->
            <div class="info-card">
              <h3>👤 Cliente</h3>
              <div class="info-content">
                <p class="info-main">{{ entrega?.cliente_nome || 'N/A' }}</p>
                <p class="info-sub">{{ entrega?.cliente_telefone }}</p>
              </div>
            </div>

            <!-- Destinatário -->
            <div class="info-card">
              <h3>📍 Destinatário</h3>
              <div class="info-content">
                <p class="info-main">{{ entrega?.nome_destinatario || entrega?.cliente_nome }}</p>
                <p class="info-sub">{{ entrega?.telefone_destinatario || entrega?.cliente_telefone }}</p>
              </div>
            </div>

            <!-- Motorista -->
            <div class="info-card">
              <h3>🧑‍✈️ Motorista</h3>
              <div class="info-content">
                <p class="info-main">{{ entrega?.motorista_nome || 'Não atribuído' }}</p>
                <p class="info-sub">{{ entrega?.motorista_telefone || '-' }}</p>
              </div>
            </div>

            <!-- Previsão -->
            <div class="info-card">
              <h3>📅 Previsão</h3>
              <div class="info-content">
                <p class="info-main">{{ formatDate(entrega?.previsao_entrega) }}</p>
                <p class="info-sub">{{ formatTime(entrega?.previsao_entrega) }}</p>
              </div>
            </div>
          </div>

          <!-- Endereço -->
          <div class="address-section">
            <h3>🏠 Endereço de Entrega</h3>
            <div class="address-content">
              <p class="address-main">{{ entrega?.endereco_rua }}</p>
              <p class="address-sub">{{ entrega?.endereco_bairro }} - {{ entrega?.endereco_cidade }}/{{ entrega?.endereco_uf }}</p>
              <p class="address-cep">CEP: {{ entrega?.endereco_cep }}</p>
            </div>
            <button class="btn-map" @click="openMaps">
              🗺️ Ver no Mapa
            </button>
          </div>

          <!-- Volumes e Valores -->
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Volumes</span>
              <span class="detail-value">{{ entrega?.volumes || 1 }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Peso</span>
              <span class="detail-value">{{ entrega?.peso || 0 }} kg</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Valor Mercadoria</span>
              <span class="detail-value">R$ {{ formatCurrency(entrega?.valor_mercadoria) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Valor Frete</span>
              <span class="detail-value">R$ {{ formatCurrency(entrega?.valor_frete) }}</span>
            </div>
          </div>

          <!-- Observações -->
          <div v-if="entrega?.observacoes" class="obs-section">
            <h3>📝 Observações</h3>
            <p>{{ entrega.observacoes }}</p>
          </div>

          <!-- Timeline -->
          <div class="timeline-section">
            <h3>📋 Histórico</h3>
            <div class="timeline">
              <div v-for="(evento, index) in eventos" :key="index" class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <span class="timeline-date">{{ evento.data }}</span>
                  <span class="timeline-text">{{ evento.descricao }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="sendWhatsApp" class="btn-action btn-whatsapp">
            💬 Enviar WhatsApp
          </button>
          <button @click="printComprovante" class="btn-action btn-print">
            🖨️ Imprimir
          </button>
          <button @click="close" class="btn-primary">
            Fechar
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  entrega: Object,
})

const emit = defineEmits(['update:modelValue'])

const statusLabel = (s) => ({
  aguardando_coleta: 'Aguardando Coleta',
  coletado: 'Coletado',
  em_transito: 'Em Trânsito',
  saiu_para_entrega: 'Saiu p/ Entrega',
  entregue: 'Entregue',
  devolvido: 'Devolvido',
  cancelado: 'Cancelado',
}[s] || s)

const stepNumber = computed(() => {
  const steps = { aguardando_coleta: 1, coletado: 2, em_transito: 3, saiu_para_entrega: 4, entregue: 5 }
  return steps[props.entrega?.status] || 1
})

const getStepClass = (step) => {
  if (step < stepNumber.value) return 'completed'
  if (step === stepNumber.value) return 'active'
  return ''
}

const eventos = computed(() => {
  if (props.entrega?.eventos?.length) return props.entrega.eventos
  return [
    { data: 'Hoje 09:30', descricao: 'Entrega criada no sistema' },
    { data: 'Hoje 10:15', descricao: 'Motorista atribuído: Carlos Santos' },
    { data: 'Hoje 11:00', descricao: 'Coleta realizada' },
  ]
})

const formatDate = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : '-'
const formatTime = (d) => d ? new Date(d).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) : ''
const formatCurrency = (v) => (v || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })

function openMaps() {
  const address = `${props.entrega?.endereco_rua}, ${props.entrega?.endereco_cidade}, ${props.entrega?.endereco_uf}`
  window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`, '_blank')
}

function sendWhatsApp() {
  const phone = props.entrega?.telefone_destinatario?.replace(/\D/g, '') || props.entrega?.cliente_telefone?.replace(/\D/g, '')
  const msg = encodeURIComponent(`Olá! Sua entrega ${props.entrega?.codigo} está ${statusLabel(props.entrega?.status).toLowerCase()}. Previsão: ${formatDate(props.entrega?.previsao_entrega)}`)
  window.open(`https://wa.me/55${phone}?text=${msg}`, '_blank')
}

function printComprovante() {
  window.print()
}

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; backdrop-filter: blur(4px); }
.modal-container { background: white; border-radius: 1rem; width: 100%; max-width: 700px; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.dark .modal-container { background: #1f2937; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem; border-bottom: 1px solid #e5e7eb; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }
.dark .modal-header { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); border-color: #374151; }
.header-info { display: flex; align-items: center; gap: 1rem; }
.header-info h2 { font-size: 1.25rem; font-weight: 700; margin: 0; color: #1f2937; }
.dark .header-info h2 { color: white; }
.btn-close { width: 32px; height: 32px; border-radius: 0.5rem; border: none; background: #f3f4f6; color: #6b7280; cursor: pointer; font-size: 1rem; transition: all 0.2s; }
.dark .btn-close { background: #374151; color: #9ca3af; }
.btn-close:hover { background: #e5e7eb; }
.modal-body { flex: 1; overflow-y: auto; padding: 1.5rem; }

/* Status Badges */
.status-badge { padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-aguardando_coleta { background: #fef3c7; color: #d97706; }
.status-coletado { background: #e0e7ff; color: #4338ca; }
.status-em_transito { background: #dbeafe; color: #1d4ed8; }
.status-saiu_para_entrega { background: #cffafe; color: #0891b2; }
.status-entregue { background: #d1fae5; color: #059669; }
.dark .status-aguardando_coleta { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .status-coletado { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; }
.dark .status-em_transito { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.dark .status-saiu_para_entrega { background: rgba(6, 182, 212, 0.2); color: #22d3ee; }
.dark .status-entregue { background: rgba(16, 185, 129, 0.2); color: #34d399; }

/* Progress Steps */
.progress-section { margin-bottom: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 0.75rem; }
.dark .progress-section { background: #111827; }
.progress-steps { display: flex; align-items: center; justify-content: space-between; }
.step { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; opacity: 0.4; transition: all 0.3s; }
.step.active, .step.completed { opacity: 1; }
.step-dot { width: 40px; height: 40px; border-radius: 50%; background: #e5e7eb; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.dark .step-dot { background: #374151; }
.step.active .step-dot { background: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2); }
.step.completed .step-dot { background: #10b981; }
.step span { font-size: 0.7rem; color: #6b7280; text-align: center; }
.dark .step span { color: #9ca3af; }
.step-line { flex: 1; height: 3px; background: #e5e7eb; margin: 0 0.5rem; margin-bottom: 1.5rem; }
.dark .step-line { background: #374151; }
.step-line.active { background: #10b981; }

/* Info Grid */
.info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.info-card { background: #f8fafc; padding: 1rem; border-radius: 0.75rem; }
.dark .info-card { background: #111827; }
.info-card h3 { font-size: 0.75rem; color: #6b7280; margin: 0 0 0.5rem; font-weight: 600; }
.dark .info-card h3 { color: #9ca3af; }
.info-main { font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0; }
.dark .info-main { color: white; }
.info-sub { font-size: 0.875rem; color: #6b7280; margin: 0.25rem 0 0; }
.dark .info-sub { color: #9ca3af; }

/* Address */
.address-section { background: #f8fafc; padding: 1rem; border-radius: 0.75rem; margin-bottom: 1.5rem; }
.dark .address-section { background: #111827; }
.address-section h3 { font-size: 0.75rem; color: #6b7280; margin: 0 0 0.75rem; font-weight: 600; }
.dark .address-section h3 { color: #9ca3af; }
.address-main { font-size: 1rem; font-weight: 600; color: #1f2937; margin: 0; }
.dark .address-main { color: white; }
.address-sub { font-size: 0.875rem; color: #6b7280; margin: 0.25rem 0; }
.dark .address-sub { color: #9ca3af; }
.address-cep { font-size: 0.75rem; color: #9ca3af; margin: 0; }
.btn-map { margin-top: 0.75rem; padding: 0.5rem 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; background: white; color: #374151; font-size: 0.875rem; cursor: pointer; transition: all 0.2s; }
.dark .btn-map { background: #374151; border-color: #4b5563; color: white; }
.btn-map:hover { background: #f3f4f6; }
.dark .btn-map:hover { background: #4b5563; }

/* Details Grid */
.details-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.detail-item { text-align: center; padding: 1rem; background: #f8fafc; border-radius: 0.75rem; }
.dark .detail-item { background: #111827; }
.detail-label { display: block; font-size: 0.7rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.dark .detail-label { color: #9ca3af; }
.detail-value { font-size: 1.125rem; font-weight: 700; color: #1f2937; }
.dark .detail-value { color: white; }

/* Observações */
.obs-section { background: #fffbeb; padding: 1rem; border-radius: 0.75rem; margin-bottom: 1.5rem; border-left: 4px solid #f59e0b; }
.dark .obs-section { background: rgba(245, 158, 11, 0.1); }
.obs-section h3 { font-size: 0.75rem; color: #92400e; margin: 0 0 0.5rem; font-weight: 600; }
.dark .obs-section h3 { color: #fbbf24; }
.obs-section p { font-size: 0.875rem; color: #78350f; margin: 0; }
.dark .obs-section p { color: #fde68a; }

/* Timeline */
.timeline-section h3 { font-size: 0.875rem; color: #1f2937; margin: 0 0 1rem; font-weight: 600; }
.dark .timeline-section h3 { color: white; }
.timeline { display: flex; flex-direction: column; gap: 0.75rem; }
.timeline-item { display: flex; align-items: flex-start; gap: 0.75rem; }
.timeline-dot { width: 10px; height: 10px; border-radius: 50%; background: #3b82f6; margin-top: 0.25rem; flex-shrink: 0; }
.timeline-content { display: flex; flex-direction: column; }
.timeline-date { font-size: 0.75rem; color: #6b7280; }
.dark .timeline-date { color: #9ca3af; }
.timeline-text { font-size: 0.875rem; color: #374151; }
.dark .timeline-text { color: #e5e7eb; }

/* Footer */
.modal-footer { display: flex; justify-content: flex-end; gap: 0.75rem; padding: 1.25rem 1.5rem; border-top: 1px solid #e5e7eb; background: #f9fafb; }
.dark .modal-footer { background: #111827; border-color: #374151; }
.btn-action { padding: 0.75rem 1rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; background: white; color: #374151; font-weight: 500; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 0.5rem; }
.dark .btn-action { background: #374151; border-color: #4b5563; color: white; }
.btn-action:hover { background: #f3f4f6; }
.dark .btn-action:hover { background: #4b5563; }
.btn-whatsapp { border-color: #10b981; color: #059669; }
.btn-whatsapp:hover { background: #d1fae5; }
.btn-primary { padding: 0.75rem 1.5rem; border-radius: 0.5rem; border: none; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }

@media (max-width: 640px) {
  .info-grid, .details-grid { grid-template-columns: repeat(2, 1fr); }
  .progress-steps { flex-wrap: wrap; gap: 0.5rem; }
  .step-line { display: none; }
}
</style>
