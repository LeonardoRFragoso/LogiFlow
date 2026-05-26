<template>
  <div class="timeline-event" :class="eventTypeClass">
    <div class="timeline-marker">
      <div class="timeline-icon">
        <component :is="iconComponent" class="icon" />
      </div>
      <div v-if="!isLast" class="timeline-line"></div>
    </div>
    
    <div class="timeline-content">
      <div class="event-header">
        <h4 class="event-title">{{ event.titulo }}</h4>
        <span class="event-date">{{ formatDate(event.data) }}</span>
      </div>
      
      <p v-if="event.descricao" class="event-description">
        {{ event.descricao }}
      </p>
      
      <div v-if="event.metadata" class="event-metadata">
        <span v-for="(value, key) in displayMetadata" :key="key" class="metadata-item">
          <strong>{{ formatMetadataKey(key) }}:</strong> {{ value }}
        </span>
      </div>
      
      <div v-if="showActions" class="event-actions">
        <slot name="actions" :event="event"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import dayjs from 'dayjs'
import 'dayjs/locale/pt-br'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)
dayjs.locale('pt-br')

const props = defineProps({
  event: {
    type: Object,
    required: true
  },
  isLast: {
    type: Boolean,
    default: false
  },
  showActions: {
    type: Boolean,
    default: false
  }
})

const eventTypeClass = computed(() => {
  return `event-type-${props.event.tipo}`
})

const iconSvgs = {
  oportunidade_criada: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
  interacao: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
  pedido: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 9.4 7.55 4.24"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" x2="12" y1="22" y2="12"/></svg>',
  cotacao: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><line x1="10" x2="8" y1="9" y2="9"/></svg>',
  nota: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15.5 3H5a2 2 0 0 0-2 2v14c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2V8.5L15.5 3Z"/><path d="M15 3v6h6"/></svg>',
  default: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>'
}

const iconComponent = computed(() => {
  const svg = iconSvgs[props.event.tipo] || iconSvgs.default
  return {
    render() {
      return h('span', { innerHTML: svg })
    }
  }
})

const displayMetadata = computed(() => {
  if (!props.event.metadata) return {}
  
  const filtered = {}
  Object.entries(props.event.metadata).forEach(([key, value]) => {
    if (value && !key.includes('_id')) {
      filtered[key] = value
    }
  })
  return filtered
})

function formatDate(date) {
  return dayjs(date).fromNow()
}

function formatMetadataKey(key) {
  const labels = {
    valor: 'Valor',
    status: 'Status',
    responsavel: 'Responsável',
    resultado: 'Resultado'
  }
  return labels[key] || key
}
</script>

<style scoped>
.timeline-event {
  display: grid;
  grid-template-columns: 40px 1fr;
  gap: 16px;
  position: relative;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.timeline-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 3px solid;
  z-index: 2;
  flex-shrink: 0;
}

.event-type-oportunidade_criada .timeline-icon {
  border-color: #3b82f6;
  color: #3b82f6;
}

.event-type-interacao .timeline-icon {
  border-color: #10b981;
  color: #10b981;
}

.event-type-pedido .timeline-icon {
  border-color: #8b5cf6;
  color: #8b5cf6;
}

.event-type-cotacao .timeline-icon {
  border-color: #f59e0b;
  color: #f59e0b;
}

.event-type-nota .timeline-icon {
  border-color: #6b7280;
  color: #6b7280;
}

.timeline-icon .icon {
  width: 20px;
  height: 20px;
}

.timeline-line {
  width: 2px;
  flex: 1;
  background: #e5e7eb;
  margin-top: 8px;
}

.timeline-content {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 8px;
}

.event-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.event-date {
  font-size: 13px;
  color: #6b7280;
  white-space: nowrap;
}

.event-description {
  font-size: 14px;
  color: #4b5563;
  margin: 8px 0 0 0;
  line-height: 1.5;
}

.event-metadata {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.metadata-item {
  font-size: 13px;
  color: #6b7280;
}

.metadata-item strong {
  color: #374151;
  font-weight: 600;
}

.event-actions {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}
</style>
