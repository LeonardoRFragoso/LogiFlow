<template>
  <div class="pipeline-kanban">
    <div class="kanban-header">
      <h2 class="kanban-title">Pipeline de Vendas</h2>
      <div class="kanban-summary">
        <div class="summary-item">
          <span class="summary-label">Total de Oportunidades:</span>
          <span class="summary-value">{{ totalOpportunities }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Valor Total:</span>
          <span class="summary-value">R$ {{ formatCurrency(totalValue) }}</span>
        </div>
      </div>
    </div>
    
    <div class="kanban-board">
      <div 
        v-for="stage in stages" 
        :key="stage.value"
        class="kanban-column"
        :class="{ 'column-dragging-over': isDraggingOver[stage.value] }"
        @dragover.prevent="handleDragOver(stage.value)"
        @dragleave="handleDragLeave(stage.value)"
        @drop="handleDrop($event, stage.value)"
      >
        <div class="column-header" :style="{ borderTopColor: stage.color }">
          <div class="column-title-wrapper">
            <h3 class="column-title">{{ stage.label }}</h3>
            <span class="column-count">{{ getStageOpportunities(stage.value).length }}</span>
          </div>
          <div class="column-value">
            R$ {{ formatCurrency(getStageValue(stage.value)) }}
          </div>
        </div>
        
        <div class="column-content">
          <div 
            v-for="opp in getStageOpportunities(stage.value)" 
            :key="opp.id"
            class="opportunity-card"
            draggable="true"
            @dragstart="handleDragStart($event, opp)"
            @dragend="handleDragEnd"
          >
            <div class="card-header">
              <h4 class="card-title">{{ opp.nome }}</h4>
              <button 
                class="card-menu-btn"
                @click="$emit('open-details', opp)"
              >
                ⋮
              </button>
            </div>
            
            <div class="card-meta">
              <div class="meta-item">
                <span class="meta-label">Cliente:</span>
                <span class="meta-value">{{ opp.cliente_nome }}</span>
              </div>
              
              <div class="meta-item">
                <span class="meta-label">Valor:</span>
                <span class="meta-value value-highlight">R$ {{ formatCurrency(opp.valor_estimado) }}</span>
              </div>
              
              <div v-if="opp.probabilidade" class="meta-item">
                <span class="meta-label">Probabilidade:</span>
                <span class="meta-value">{{ opp.probabilidade }}%</span>
              </div>
            </div>
            
            <div v-if="opp.responsavel_nome" class="card-footer">
              <div class="avatar">{{ getInitials(opp.responsavel_nome) }}</div>
              <span class="responsible-name">{{ opp.responsavel_nome }}</span>
            </div>
          </div>
          
          <div v-if="getStageOpportunities(stage.value).length === 0" class="empty-column">
            <p>Nenhuma oportunidade nesta etapa</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  opportunities: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['move-stage', 'open-details'])

const stages = [
  { value: 'lead', label: 'Lead', color: '#9ca3af' },
  { value: 'qualificado', label: 'Qualificado', color: '#3b82f6' },
  { value: 'proposta', label: 'Proposta', color: '#f59e0b' },
  { value: 'negociacao', label: 'Negociação', color: '#8b5cf6' },
  { value: 'ganho', label: 'Ganho', color: '#10b981' }
]

const draggedOpportunity = ref(null)
const isDraggingOver = ref({})

const totalOpportunities = computed(() => {
  return props.opportunities.filter(o => o.sales_stage !== 'perdido').length
})

const totalValue = computed(() => {
  return props.opportunities
    .filter(o => o.sales_stage !== 'perdido')
    .reduce((sum, o) => sum + (o.valor_estimado || 0), 0)
})

function getStageOpportunities(stage) {
  return props.opportunities.filter(o => o.sales_stage === stage)
}

function getStageValue(stage) {
  return getStageOpportunities(stage)
    .reduce((sum, o) => sum + (o.valor_estimado || 0), 0)
}

function handleDragStart(event, opp) {
  draggedOpportunity.value = opp
  event.dataTransfer.effectAllowed = 'move'
  event.target.style.opacity = '0.5'
}

function handleDragEnd(event) {
  event.target.style.opacity = '1'
  draggedOpportunity.value = null
  isDraggingOver.value = {}
}

function handleDragOver(stage) {
  isDraggingOver.value = { [stage]: true }
}

function handleDragLeave(stage) {
  isDraggingOver.value = { [stage]: false }
}

function handleDrop(event, newStage) {
  event.preventDefault()
  isDraggingOver.value = {}
  
  if (!draggedOpportunity.value || draggedOpportunity.value.sales_stage === newStage) {
    return
  }
  
  emit('move-stage', {
    opportunityId: draggedOpportunity.value.id,
    oldStage: draggedOpportunity.value.sales_stage,
    newStage: newStage
  })
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR').format(value || 0)
}

function getInitials(name) {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .substring(0, 2)
    .toUpperCase()
}
</script>

<style scoped>
.pipeline-kanban {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.kanban-header {
  padding: 24px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.kanban-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 16px 0;
}

.kanban-summary {
  display: flex;
  gap: 24px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-label {
  font-size: 14px;
  color: #6b7280;
}

.summary-value {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.kanban-board {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  padding: 24px;
  background: #f9fafb;
  overflow-x: auto;
  min-height: 0;
}

.kanban-column {
  display: flex;
  flex-direction: column;
  background: #f3f4f6;
  border-radius: 8px;
  min-width: 280px;
  max-height: 100%;
  transition: background-color 0.2s;
}

.column-dragging-over {
  background: #dbeafe;
}

.column-header {
  padding: 16px;
  background: white;
  border-top: 4px solid;
  border-radius: 8px 8px 0 0;
}

.column-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.column-title {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.column-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 8px;
  background: #e5e7eb;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.column-value {
  font-size: 14px;
  font-weight: 600;
  color: #10b981;
}

.column-content {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.opportunity-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  cursor: grab;
  transition: box-shadow 0.2s, transform 0.2s;
}

.opportunity-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.opportunity-card:active {
  cursor: grabbing;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 12px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  line-height: 1.4;
}

.card-menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  font-size: 18px;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.card-menu-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.meta-label {
  color: #6b7280;
}

.meta-value {
  color: #374151;
  font-weight: 500;
}

.value-highlight {
  color: #10b981;
  font-weight: 600;
}

.card-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
}

.responsible-name {
  font-size: 12px;
  color: #6b7280;
}

.empty-column {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
  font-size: 14px;
}

/* Scrollbar customizado */
.column-content::-webkit-scrollbar {
  width: 6px;
}

.column-content::-webkit-scrollbar-track {
  background: transparent;
}

.column-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.column-content::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
