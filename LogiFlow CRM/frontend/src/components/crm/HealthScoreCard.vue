<template>
  <div class="health-score-card">
    <div class="score-display" :class="scoreClass">
      <div class="score-value">{{ score }}</div>
      <div class="score-label">Health Score</div>
    </div>
    
    <div v-if="showVariacao && variacao !== undefined" class="score-variation" :class="variacaoClass">
      <span class="variation-icon">{{ variacao >= 0 ? '↑' : '↓' }}</span>
      <span class="variation-value">{{ Math.abs(variacao).toFixed(1) }}</span>
    </div>
    
    <div v-if="showCategory" class="score-category">
      <span class="category-badge" :class="categoryClass">{{ categoryLabel }}</span>
    </div>
    
    <div v-if="showFactors && fatores" class="score-factors">
      <div class="factors-title">Fatores de Impacto</div>
      <div class="factors-list">
        <div v-for="(value, key) in fatores" :key="key" class="factor-item">
          <div class="factor-name">{{ formatFactorName(key) }}</div>
          <div class="factor-bar">
            <div class="factor-progress" :style="{ width: value + '%' }" :class="getFactorClass(value)"></div>
          </div>
          <div class="factor-value">{{ value.toFixed(0) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: {
    type: Number,
    required: true
  },
  variacao: {
    type: Number,
    default: null
  },
  categoria: {
    type: String,
    default: null
  },
  fatores: {
    type: Object,
    default: null
  },
  showVariacao: {
    type: Boolean,
    default: true
  },
  showCategory: {
    type: Boolean,
    default: true
  },
  showFactors: {
    type: Boolean,
    default: false
  }
})

const scoreClass = computed(() => {
  if (props.score >= 80) return 'score-excellent'
  if (props.score >= 60) return 'score-good'
  if (props.score >= 40) return 'score-warning'
  return 'score-critical'
})

const variacaoClass = computed(() => {
  return props.variacao >= 0 ? 'variation-positive' : 'variation-negative'
})

const categoryClass = computed(() => {
  const category = props.categoria || getCategoryFromScore(props.score)
  return `category-${category}`
})

const categoryLabel = computed(() => {
  const category = props.categoria || getCategoryFromScore(props.score)
  const labels = {
    excelente: 'Excelente',
    saudavel: 'Saudável',
    atencao: 'Atenção',
    critico: 'Crítico'
  }
  return labels[category] || category
})

function getCategoryFromScore(score) {
  if (score >= 80) return 'excelente'
  if (score >= 60) return 'saudavel'
  if (score >= 40) return 'atencao'
  return 'critico'
}

function formatFactorName(key) {
  const names = {
    recencia: 'Recência',
    frequencia: 'Frequência',
    monetario: 'Monetário',
    engajamento: 'Engajamento',
    relacionamento: 'Relacionamento'
  }
  return names[key] || key
}

function getFactorClass(value) {
  if (value >= 70) return 'factor-good'
  if (value >= 40) return 'factor-warning'
  return 'factor-critical'
}
</script>

<style scoped>
.health-score-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.score-display {
  text-align: center;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.score-value {
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 8px;
}

.score-label {
  font-size: 14px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.8;
}

.score-excellent {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.score-good {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.score-warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.score-critical {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.score-variation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.variation-positive {
  background: #d1fae5;
  color: #065f46;
}

.variation-negative {
  background: #fee2e2;
  color: #991b1b;
}

.score-category {
  text-align: center;
  margin-bottom: 16px;
}

.category-badge {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.category-excelente {
  background: #d1fae5;
  color: #065f46;
}

.category-saudavel {
  background: #dbeafe;
  color: #1e40af;
}

.category-atencao {
  background: #fed7aa;
  color: #92400e;
}

.category-critico {
  background: #fee2e2;
  color: #991b1b;
}

.score-factors {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.factors-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.factors-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.factor-item {
  display: grid;
  grid-template-columns: 120px 1fr 40px;
  align-items: center;
  gap: 12px;
}

.factor-name {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.factor-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.factor-progress {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.factor-good {
  background: #10b981;
}

.factor-warning {
  background: #f59e0b;
}

.factor-critical {
  background: #ef4444;
}

.factor-value {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-align: right;
}
</style>
