/**
 * LogiFlow CRM - Pinia Store Enterprise
 * ======================================
 * Gerenciamento de estado do CRM
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import crmEnterpriseApi from '../services/crmEnterpriseApi'

export const useCRMStore = defineStore('crm', () => {
  // Estado
  const opportunities = ref([])
  const currentOpportunity = ref(null)
  const interactions = ref([])
  const metrics = ref(null)
  const alerts = ref(null)
  const cliente360 = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  // Computeds
  const opportunitiesByStage = computed(() => {
    const byStage = {}
    opportunities.value.forEach(opp => {
      if (!byStage[opp.sales_stage]) {
        byStage[opp.sales_stage] = []
      }
      byStage[opp.sales_stage].push(opp)
    })
    return byStage
  })
  
  const totalPipelineValue = computed(() => {
    return opportunities.value.reduce((sum, opp) => {
      if (opp.sales_stage !== 'ganho' && opp.sales_stage !== 'perdido') {
        return sum + (opp.valor_estimado || 0)
      }
      return sum
    }, 0)
  })
  
  const criticalAlerts = computed(() => {
    if (!alerts.value) return []
    return alerts.value.all_alerts?.filter(a => a.priority === 'critical') || []
  })
  
  // Actions
  async function loadOpportunities(filters = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.opportunities.list(filters)
      opportunities.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function loadOpportunity(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.opportunities.get(id)
      currentOpportunity.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function createOpportunity(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.opportunities.create(data)
      opportunities.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function updateOpportunity(id, data, usuarioId = null) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.opportunities.update(id, data, usuarioId)
      
      const index = opportunities.value.findIndex(o => o.id === id)
      if (index !== -1) {
        opportunities.value[index] = response.data
      }
      
      if (currentOpportunity.value?.id === id) {
        currentOpportunity.value = response.data
      }
      
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function moveOpportunityStage(opportunityId, newStage, usuarioId = null) {
    return updateOpportunity(opportunityId, { sales_stage: newStage }, usuarioId)
  }
  
  async function loadInteractions(filters = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.interactions.list(filters)
      interactions.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function createInteraction(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.interactions.create(data)
      interactions.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function loadMetrics() {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.metrics.dashboard()
      metrics.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function loadAlerts() {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.alerts.all()
      alerts.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function loadCliente360(clienteId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await crmEnterpriseApi.cliente360.get(clienteId)
      cliente360.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }
  
  function clearError() {
    error.value = null
  }
  
  return {
    // Estado
    opportunities,
    currentOpportunity,
    interactions,
    metrics,
    alerts,
    cliente360,
    loading,
    error,
    
    // Computeds
    opportunitiesByStage,
    totalPipelineValue,
    criticalAlerts,
    
    // Actions
    loadOpportunities,
    loadOpportunity,
    createOpportunity,
    updateOpportunity,
    moveOpportunityStage,
    loadInteractions,
    createInteraction,
    loadMetrics,
    loadAlerts,
    loadCliente360,
    clearError
  }
})
