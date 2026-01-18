/**
 * LogiFlow CRM - API Service Enterprise
 * ======================================
 * Serviço de comunicação com o backend CRM Enterprise
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const CRM_BASE = `${API_BASE_URL}/api/v1/crm`

const api = axios.create({
  baseURL: CRM_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para tratamento de erros
api.interceptors.response.use(
  response => response,
  error => {
    console.error('Erro na API:', error)
    return Promise.reject(error)
  }
)

export const crmEnterpriseApi = {
  // ========================================
  // Oportunidades
  // ========================================
  
  opportunities: {
    list: (filters = {}) => {
      return api.get('/opportunities', { params: filters })
    },
    
    get: (id) => {
      return api.get(`/opportunities/${id}`)
    },
    
    create: (data) => {
      return api.post('/opportunities', data)
    },
    
    update: (id, data, usuarioId = null) => {
      return api.put(`/opportunities/${id}`, data, {
        params: { usuario_id: usuarioId }
      })
    },
    
    getHistory: (id) => {
      return api.get(`/opportunities/${id}/history`)
    }
  },
  
  // ========================================
  // Interações
  // ========================================
  
  interactions: {
    list: (filters = {}) => {
      return api.get('/interactions', { params: filters })
    },
    
    create: (data) => {
      return api.post('/interactions', data)
    }
  },
  
  // ========================================
  // Métricas
  // ========================================
  
  metrics: {
    conversionRates: (startDate = null, endDate = null) => {
      return api.get('/metrics/conversion-rates', {
        params: { start_date: startDate, end_date: endDate }
      })
    },
    
    pipelineValue: () => {
      return api.get('/metrics/pipeline-value')
    },
    
    customerActivity: () => {
      return api.get('/metrics/customer-activity')
    },
    
    dashboard: () => {
      return api.get('/metrics/dashboard')
    }
  },
  
  // ========================================
  // Alertas
  // ========================================
  
  alerts: {
    all: () => {
      return api.get('/alerts/all')
    },
    
    inactiveCustomers: (days = 30, minimumRevenue = 0) => {
      return api.get('/alerts/inactive-customers', {
        params: { days, minimum_revenue: minimumRevenue }
      })
    },
    
    stalledOpportunities: (days = 15) => {
      return api.get('/alerts/stalled-opportunities', {
        params: { days }
      })
    }
  },
  
  // ========================================
  // Health Score
  // ========================================
  
  healthScore: {
    calculate: (clienteId, salvar = true) => {
      return api.get(`/health-score/${clienteId}`, {
        params: { salvar }
      })
    },
    
    recalculateAll: () => {
      return api.post('/health-score/recalcular-todos')
    },
    
    atRisk: (threshold = 40) => {
      return api.get('/health-score/clientes-em-risco', {
        params: { threshold }
      })
    }
  },
  
  // ========================================
  // Forecast
  // ========================================
  
  forecast: {
    monthly: (ano, mes, responsavelId = null) => {
      return api.get('/forecast/mensal', {
        params: { ano, mes, responsavel_id: responsavelId }
      })
    },
    
    quarterly: (ano, trimestre, responsavelId = null) => {
      return api.get('/forecast/trimestral', {
        params: { ano, trimestre, responsavel_id: responsavelId }
      })
    }
  },
  
  // ========================================
  // SLA
  // ========================================
  
  sla: {
    checkOpportunity: (opportunityId) => {
      return api.get(`/sla/opportunity/${opportunityId}`)
    },
    
    aging: () => {
      return api.get('/sla/aging')
    },
    
    overdue: () => {
      return api.get('/sla/vencidas')
    }
  },
  
  // ========================================
  // Cliente 360
  // ========================================
  
  cliente360: {
    get: (clienteId) => {
      return api.get(`/cliente-360/${clienteId}`)
    }
  }
}

export default crmEnterpriseApi
