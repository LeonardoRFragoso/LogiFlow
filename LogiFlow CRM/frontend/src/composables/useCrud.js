import { ref } from 'vue'
import api from '@/services/api'
import { useToast } from '@/composables/useToast'

export function useCrud(endpoint, options = {}) {
  const items = ref([])
  const item = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({ count: 0, next: null, previous: null, total: 0, pages: 0 })
  
  const { success, handleApiError } = useToast()
  const { showToasts = true, entityName = 'Registro' } = options

  async function fetchAll(params = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(endpoint, { params })
      // Suporta diferentes formatos de resposta
      const data = response.data
      items.value = data.data || data.results || data
      pagination.value = {
        count: data.count || data.total || 0,
        total: data.pagination?.total || data.total || 0,
        pages: data.pagination?.pages || 1,
        next: data.next,
        previous: data.previous
      }
      return items.value
    } catch (e) {
      error.value = e.response?.data || e.message
      if (showToasts) handleApiError(e, `Erro ao carregar ${entityName.toLowerCase()}s`)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(id) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`${endpoint}${id}/`)
      item.value = response.data.data || response.data
      return item.value
    } catch (e) {
      error.value = e.response?.data || e.message
      if (showToasts) handleApiError(e, `Erro ao carregar ${entityName.toLowerCase()}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post(endpoint, data)
      const result = response.data.data || response.data
      if (showToasts) success(`${entityName} criado com sucesso!`)
      return result
    } catch (e) {
      error.value = e.response?.data || e.message
      if (showToasts) handleApiError(e, `Erro ao criar ${entityName.toLowerCase()}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function update(id, data) {
    loading.value = true
    error.value = null
    try {
      // Tenta PUT primeiro, depois PATCH
      let response
      try {
        response = await api.put(`${endpoint}${id}/`, data)
      } catch {
        response = await api.patch(`${endpoint}${id}/`, data)
      }
      const result = response.data.data || response.data
      if (showToasts) success(`${entityName} atualizado com sucesso!`)
      return result
    } catch (e) {
      error.value = e.response?.data || e.message
      if (showToasts) handleApiError(e, `Erro ao atualizar ${entityName.toLowerCase()}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function remove(id) {
    loading.value = true
    error.value = null
    try {
      await api.delete(`${endpoint}${id}/`)
      if (showToasts) success(`${entityName} removido com sucesso!`)
    } catch (e) {
      error.value = e.response?.data || e.message
      if (showToasts) handleApiError(e, `Erro ao remover ${entityName.toLowerCase()}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  return { 
    items, 
    item, 
    loading, 
    error, 
    pagination, 
    fetchAll, 
    fetchOne, 
    create, 
    update, 
    remove 
  }
}
