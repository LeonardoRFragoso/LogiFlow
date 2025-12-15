/**
 * LogiFlow CRM - Composable de Funcionalidades por Plano
 * Verifica se o tenant tem acesso a funcionalidades baseado no plano
 */

import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const features = ref([])
const currentPlan = ref(null)
const loading = ref(true)

export function usePlanFeatures() {
  /**
   * Carrega features disponíveis do backend
   */
  const loadFeatures = async () => {
    try {
      loading.value = true
      const response = await api.get('/my-features')
      
      if (response.data.success) {
        features.value = response.data.features
      }
      
      // Carregar plano atual
      const planResponse = await api.get('/my-plan')
      if (planResponse.data.success) {
        currentPlan.value = planResponse.data.plan
      }
    } catch (error) {
      console.error('Erro ao carregar features:', error)
      // Em caso de erro, assume plano starter
      features.value = [
        'cotacoes',
        'pedidos',
        'entregas',
        'motoristas',
        'veiculos',
        'clientes',
        'ocorrencias',
        'fiscal_cte',
        'fiscal_mdfe',
        'whatsapp',
        'dashboard'
      ]
    } finally {
      loading.value = false
    }
  }

  /**
   * Verifica se tem acesso a uma feature
   */
  const hasFeature = (feature) => {
    return features.value.includes(feature)
  }

  /**
   * Verifica se tem plano mínimo
   */
  const hasPlan = (minPlan) => {
    const planHierarchy = ['starter', 'pro', 'enterprise']
    const currentPlanId = currentPlan.value?.id || 'starter'
    
    const currentIndex = planHierarchy.indexOf(currentPlanId)
    const requiredIndex = planHierarchy.indexOf(minPlan)
    
    return currentIndex >= requiredIndex
  }

  /**
   * Obtém informações sobre uma feature bloqueada
   */
  const getFeatureInfo = async (feature) => {
    try {
      const response = await api.get(`/check-feature/${feature}`)
      return response.data
    } catch (error) {
      console.error('Erro ao verificar feature:', error)
      return null
    }
  }

  /**
   * Redireciona para upgrade se feature bloqueada
   */
  const requireFeature = async (feature, router) => {
    if (!hasFeature(feature)) {
      const info = await getFeatureInfo(feature)
      
      if (info && info.required_plan) {
        // Mostrar modal de upgrade ou redirecionar
        const shouldUpgrade = confirm(
          `Esta funcionalidade requer o plano ${info.required_plan.name}.\n` +
          `Deseja fazer upgrade agora?`
        )
        
        if (shouldUpgrade && router) {
          router.push('/checkout')
        }
        
        return false
      }
      
      return false
    }
    
    return true
  }

  /**
   * Mapeamento de features para nomes amigáveis
   */
  const featureNames = {
    'cotacao_automatica': 'Cotação Automática',
    'integracao_frete': 'Integração de Frete',
    'integracao_erp': 'Integração ERP',
    'nps_satisfacao': 'NPS e Satisfação',
    'health_score': 'Health Score',
    'customer_success': 'Customer Success',
    'rastreamento_gps': 'Rastreamento GPS',
    'relatorios_avancados': 'Relatórios Avançados',
    'api_access': 'Acesso à API',
    'bi_analytics': 'BI e Analytics',
    'white_label': 'White Label',
    'suporte_prioritario': 'Suporte Prioritário'
  }

  /**
   * Obtém nome amigável da feature
   */
  const getFeatureName = (feature) => {
    return featureNames[feature] || feature
  }

  /**
   * Verifica se está carregando
   */
  const isLoading = computed(() => loading.value)

  /**
   * Plano atual formatado
   */
  const planInfo = computed(() => {
    if (!currentPlan.value) return null
    
    return {
      id: currentPlan.value.id,
      name: currentPlan.value.name,
      price: currentPlan.value.price,
      features: currentPlan.value.features,
      limits: currentPlan.value.limits
    }
  })

  /**
   * Verifica se pode fazer upgrade
   */
  const canUpgrade = computed(() => {
    const currentPlanId = currentPlan.value?.id || 'starter'
    return currentPlanId !== 'enterprise'
  })

  /**
   * Próximo plano disponível
   */
  const nextPlan = computed(() => {
    const currentPlanId = currentPlan.value?.id || 'starter'
    
    if (currentPlanId === 'starter') return 'pro'
    if (currentPlanId === 'pro') return 'enterprise'
    return null
  })

  // Carregar features ao montar
  onMounted(() => {
    loadFeatures()
  })

  return {
    // Estado
    features,
    currentPlan,
    loading,
    
    // Computed
    isLoading,
    planInfo,
    canUpgrade,
    nextPlan,
    
    // Métodos
    hasFeature,
    hasPlan,
    getFeatureInfo,
    requireFeature,
    getFeatureName,
    loadFeatures
  }
}
