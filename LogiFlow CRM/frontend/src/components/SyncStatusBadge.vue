<template>
  <div class="sync-status-badge" :class="statusClass">
    <span class="status-icon">{{ statusIcon }}</span>
    <span class="status-text">{{ statusText }}</span>
    <button 
      v-if="showSyncButton" 
      @click="handleSync" 
      class="sync-button"
      :disabled="syncing"
    >
      <span v-if="syncing">⏳</span>
      <span v-else>🔄</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import syncService from '../services/syncService'

const props = defineProps({
  showSyncButton: {
    type: Boolean,
    default: true
  },
  autoRefresh: {
    type: Boolean,
    default: true
  },
  refreshInterval: {
    type: Number,
    default: 60000 // 1 minuto
  }
})

const emit = defineEmits(['sync-started', 'sync-completed', 'sync-error'])

const status = ref(null)
const syncing = ref(false)
const connected = ref(false)
let refreshTimer = null

const statusIcon = computed(() => {
  if (syncing.value) return '⏳'
  if (!connected.value) return '❌'
  return '✅'
})

const statusText = computed(() => {
  if (syncing.value) return 'Sincronizando...'
  if (!connected.value) return 'Desconectado'
  
  if (status.value?.last_sync) {
    const lastSyncTime = syncService.formatLastSync(
      Object.values(status.value.last_sync).find(t => t) || null
    )
    return `Sync: ${lastSyncTime}`
  }
  
  return 'Aguardando sync'
})

const statusClass = computed(() => {
  if (syncing.value) return 'syncing'
  if (!connected.value) return 'error'
  return 'success'
})

const loadStatus = async () => {
  try {
    const [statusData, connectionData] = await Promise.all([
      syncService.getStatus(),
      syncService.checkSuiteCRMConnection()
    ])
    
    status.value = statusData.data
    connected.value = connectionData.success
  } catch (error) {
    console.error('Erro ao carregar status:', error)
    connected.value = false
  }
}

const handleSync = async () => {
  if (syncing.value) return
  
  syncing.value = true
  emit('sync-started')
  
  try {
    const result = await syncService.syncBidirectional()
    emit('sync-completed', result)
    await loadStatus()
  } catch (error) {
    emit('sync-error', error)
    console.error('Erro na sincronização:', error)
  } finally {
    syncing.value = false
  }
}

onMounted(async () => {
  await loadStatus()
  
  if (props.autoRefresh) {
    refreshTimer = setInterval(loadStatus, props.refreshInterval)
  }
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})

defineExpose({
  loadStatus,
  handleSync
})
</script>

<style scoped>
.sync-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
}

.sync-status-badge.success {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #10b981;
}

.sync-status-badge.syncing {
  background-color: #fef3c7;
  color: #92400e;
  border: 1px solid #f59e0b;
  animation: pulse 2s infinite;
}

.sync-status-badge.error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #ef4444;
}

.status-icon {
  font-size: 1.125rem;
}

.status-text {
  white-space: nowrap;
}

.sync-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.sync-button:hover:not(:disabled) {
  background-color: rgba(0, 0, 0, 0.1);
  transform: scale(1.1);
}

.sync-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>
