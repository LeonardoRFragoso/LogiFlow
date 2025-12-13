<template>
  <div v-if="isActive" class="tour-overlay" @click="handleOverlayClick">
    <div class="tour-spotlight" :style="spotlightStyle"></div>
    <div class="tour-card" :style="cardStyle">
      <div class="tour-header">
        <h3>{{ currentStep.title }}</h3>
        <button @click="closeTour" class="tour-close">✕</button>
      </div>
      <div class="tour-body">
        <p>{{ currentStep.description }}</p>
      </div>
      <div class="tour-footer">
        <div class="tour-progress">
          <span>{{ currentStepIndex + 1 }} de {{ steps.length }}</span>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
        </div>
        <div class="tour-actions">
          <button v-if="currentStepIndex > 0" @click="previousStep" class="btn-secondary">Anterior</button>
          <button v-if="currentStepIndex < steps.length - 1" @click="nextStep" class="btn-primary">Próximo</button>
          <button v-else @click="closeTour" class="btn-primary">Finalizar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  steps: {
    type: Array,
    required: true
  },
  autoStart: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['complete', 'skip'])

const isActive = ref(false)
const currentStepIndex = ref(0)

const currentStep = computed(() => props.steps[currentStepIndex.value])
const progressPercentage = computed(() => ((currentStepIndex.value + 1) / props.steps.length) * 100)

const spotlightStyle = ref({})
const cardStyle = ref({})

function startTour() {
  isActive.value = true
  currentStepIndex.value = 0
  updatePositions()
}

function closeTour() {
  isActive.value = false
  emit('complete')
  localStorage.setItem('tour_completed', 'true')
}

function skipTour() {
  isActive.value = false
  emit('skip')
  localStorage.setItem('tour_completed', 'true')
}

function nextStep() {
  if (currentStepIndex.value < props.steps.length - 1) {
    currentStepIndex.value++
    navigateToStep()
  }
}

function previousStep() {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--
    navigateToStep()
  }
}

function navigateToStep() {
  const step = currentStep.value
  if (step.route && router.currentRoute.value.path !== step.route) {
    router.push(step.route).then(() => {
      setTimeout(updatePositions, 300)
    })
  } else {
    updatePositions()
  }
}

function updatePositions() {
  const step = currentStep.value
  if (!step.element) {
    spotlightStyle.value = {}
    cardStyle.value = { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }
    return
  }

  setTimeout(() => {
    const element = document.querySelector(step.element)
    if (!element) {
      spotlightStyle.value = {}
      cardStyle.value = { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }
      return
    }

    const rect = element.getBoundingClientRect()
    const padding = 8

    spotlightStyle.value = {
      top: `${rect.top - padding}px`,
      left: `${rect.left - padding}px`,
      width: `${rect.width + padding * 2}px`,
      height: `${rect.height + padding * 2}px`
    }

    const cardTop = rect.bottom + 20
    const cardLeft = rect.left

    cardStyle.value = {
      top: `${cardTop}px`,
      left: `${cardLeft}px`
    }
  }, 100)
}

function handleOverlayClick(e) {
  if (e.target.classList.contains('tour-overlay')) {
    // Não fecha ao clicar no overlay
  }
}

watch(() => currentStepIndex.value, updatePositions)

onMounted(() => {
  if (props.autoStart && !localStorage.getItem('tour_completed')) {
    setTimeout(startTour, 1000)
  }
  window.addEventListener('resize', updatePositions)
})

onUnmounted(() => {
  window.removeEventListener('resize', updatePositions)
})

defineExpose({ startTour, closeTour, skipTour })
</script>

<style scoped>
.tour-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9998;
  backdrop-filter: blur(2px);
}

.tour-spotlight {
  position: fixed;
  background: transparent;
  border: 3px solid #3b82f6;
  border-radius: 8px;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.7);
  z-index: 9999;
  pointer-events: none;
  transition: all 0.3s ease;
}

.tour-card {
  position: fixed;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  z-index: 10000;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tour-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.tour-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.tour-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s;
}

.tour-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.tour-body {
  padding: 1.5rem;
}

.tour-body p {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
}

.tour-footer {
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.tour-progress {
  margin-bottom: 1rem;
}

.tour-progress span {
  display: block;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
  transition: width 0.3s ease;
}

.tour-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn-primary,
.btn-secondary {
  padding: 0.625rem 1.25rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: #f3f4f6;
  color: #4b5563;
}

.btn-secondary:hover {
  background: #e5e7eb;
}
</style>
