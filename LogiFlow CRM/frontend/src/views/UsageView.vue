<template>
  <div class="usage-view">
    <PlanUsageDashboard 
      :tenant-id="1" 
      @upgrade="showUpgradeModal = true"
    />
    
    <!-- Modal de Upgrade -->
    <UpgradeModal 
      v-if="showUpgradeModal"
      @close="showUpgradeModal = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PlanUsageDashboard from '@/components/PlanUsageDashboard.vue'
import UpgradeModal from '@/components/UpgradeModal.vue'

const showUpgradeModal = ref(false)
</script>

<style scoped>
.usage-view {
  @apply p-6;
}
</style>
