import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'
import { useAuthStore } from './auth'

export const useEntregasStore = defineStore('entregas', () => {
  const entregas = ref([])
  const entregaAtual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  const entregasAtivas = computed(() => 
    entregas.value.filter(e => !['entregue', 'cancelado', 'devolvido'].includes(e.status))
  )
  
  const entregasConcluidas = computed(() => 
    entregas.value.filter(e => e.status === 'entregue')
  )
  
  async function carregarEntregas() {
    loading.value = true
    error.value = null
    
    const authStore = useAuthStore()
    const motorista_id = authStore.user?.id || authStore.user?.motorista_id

    try {
      let data = []
      if (motorista_id) {
        const response = await api.get(`/api/v1/rastreamento/motorista/${motorista_id}/entregas`)
        data = response.data.data || []
      } else {
        const response = await api.get('/api/v1/demo/entregas')
        data = response.data.data || []
      }
      // Mapear dados para o formato esperado pelo app
      entregas.value = data.map(e => ({
        id: e.id,
        numero: e.numero || e.pedido_numero,
        codigo_rastreio: e.codigo_rastreio || e.codigo,
        status: e.status,
        cliente_nome: e.cliente_nome,
        origem: e.origem || {
          cidade: 'Origem',
          uf: '',
          logradouro: ''
        },
        destino: e.destino || {
          cidade: e.endereco_cidade || '',
          uf: e.endereco_uf || '',
          logradouro: e.endereco_rua || '',
          contato_nome: e.cliente_nome,
          contato_telefone: e.cliente_telefone
        },
        peso_total_kg: e.peso_total_kg || e.peso,
        valor_total: e.valor_total || e.valor_mercadoria,
        data_entrega_prevista: e.data_entrega_prevista || e.previsao_entrega,
        prioridade: e.prioridade || (e.atrasada ? 'urgente' : 'normal')
      }))
    } catch (err) {
      console.error('Erro ao carregar entregas:', err)
      error.value = 'Erro ao carregar entregas'
      entregas.value = getDadosDemostracao()
    } finally {
      loading.value = false
    }
  }
  
  async function carregarEntrega(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/api/v1/rastreamento/entregas/${id}`)
      entregaAtual.value = response.data.data
    } catch (err) {
      console.error('Erro ao carregar entrega:', err)
      // Buscar nos dados locais como fallback
      entregaAtual.value = entregas.value.find(e => e.id === id) || getDadosDemostracao()[0]
    } finally {
      loading.value = false
    }
  }
  
  async function atualizarStatus(id, status, dados = {}) {
    const authStore = useAuthStore()
    const motorista_id = authStore.user?.id || authStore.user?.motorista_id
    try {
      await api.patch(`/api/v1/rastreamento/entrega/status`, {
        entrega_id: id,
        status,
        motorista_id,
        ...dados
      })
      
      // Atualizar localmente
      const index = entregas.value.findIndex(e => e.id === id)
      if (index !== -1) {
        entregas.value[index].status = status
      }
      if (entregaAtual.value?.id === id) {
        entregaAtual.value.status = status
      }
      
      return { success: true }
    } catch (err) {
      console.error('Erro ao atualizar status:', err)
      return { success: false, message: 'Erro ao atualizar status' }
    }
  }
  
  async function registrarOcorrencia(id, dados) {
    const authStore = useAuthStore()
    const motorista_id = authStore.user?.id || authStore.user?.motorista_id
    try {
      await api.post(`/api/v1/rastreamento/entrega/ocorrencia`, {
        entrega_id: id,
        motorista_id,
        ...dados
      })
      return { success: true }
    } catch (err) {
      console.error('Erro ao registrar ocorrência:', err)
      return { success: false, message: 'Erro ao registrar ocorrência' }
    }
  }
  
  function getDadosDemostracao() {
    return [
      {
        id: 'demo-1',
        numero: 'PED-2024-005001',
        codigo_rastreio: 'LF1234567890',
        status: 'em_transito',
        cliente_nome: 'Supermercados ABC',
        origem: {
          cidade: 'São Paulo',
          uf: 'SP',
          logradouro: 'Av. Paulista, 1000'
        },
        destino: {
          cidade: 'Campinas',
          uf: 'SP',
          logradouro: 'Rua das Flores, 500',
          contato_nome: 'João Silva',
          contato_telefone: '(19) 99999-9999'
        },
        peso_total_kg: 450,
        valor_total: 1250.00,
        data_entrega_prevista: new Date(Date.now() + 3600000 * 4).toISOString(),
        prioridade: 'alta'
      },
      {
        id: 'demo-2',
        numero: 'PED-2024-005002',
        codigo_rastreio: 'LF0987654321',
        status: 'aguardando_coleta',
        cliente_nome: 'Loja XYZ',
        origem: {
          cidade: 'Jundiaí',
          uf: 'SP',
          logradouro: 'Rod. Anhanguera, km 50'
        },
        destino: {
          cidade: 'Sorocaba',
          uf: 'SP',
          logradouro: 'Av. Industrial, 1200',
          contato_nome: 'Maria Santos',
          contato_telefone: '(15) 98888-8888'
        },
        peso_total_kg: 280,
        valor_total: 850.00,
        data_entrega_prevista: new Date(Date.now() + 3600000 * 8).toISOString(),
        prioridade: 'normal'
      }
    ]
  }
  
  return {
    entregas,
    entregaAtual,
    loading,
    error,
    entregasAtivas,
    entregasConcluidas,
    carregarEntregas,
    carregarEntrega,
    atualizarStatus,
    registrarOcorrencia
  }
})
