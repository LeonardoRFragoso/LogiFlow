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
import { computed, defineAsyncComponent } from 'vue'
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

const iconComponent = computed(() => {
  const icons = {
    oportunidade_criada: 'IconTarget',
    interacao: 'IconMessageCircle',
    pedido: 'IconPackage',
    cotacao: 'IconFileText',
    nota: 'IconStickyNote'
  }
  
  const iconName = icons[props.event.tipo] || 'IconCircle'
  
  return defineAsyncComponent(() => 
    import(`../icons/${iconName}.vue`).catch(() => 
      import(`../icons/IconCircle.vue`)
    )
  )
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
