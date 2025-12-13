import { ref } from 'vue'
import api from '@/services/api'

export function useCrud(endpoint) {
  const items = ref([])
  const item = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({ count: 0, next: null, previous: null })

  async function fetchAll(params = {}) {
    loading.value = true
    try {
      const response = await api.get(endpoint, { params })
      items.value = response.data.results || response.data
      pagination.value = { count: response.data.count, next: response.data.next, previous: response.data.previous }
    } catch (e) {
      error.value = e.response?.data || e.message
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(id) {
    loading.value = true
    try {
      const response = await api.get(`${endpoint}${id}/`)
      item.value = response.data
    } catch (e) {
      error.value = e.response?.data || e.message
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    loading.value = true
    try {
      const response = await api.post(endpoint, data)
      return response.data
    } catch (e) {
      error.value = e.response?.data || e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function update(id, data) {
    loading.value = true
    try {
      const response = await api.patch(`${endpoint}${id}/`, data)
      return response.data
    } catch (e) {
      error.value = e.response?.data || e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function remove(id) {
    loading.value = true
    try {
      await api.delete(`${endpoint}${id}/`)
    } catch (e) {
      error.value = e.response?.data || e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  return { items, item, loading, error, pagination, fetchAll, fetchOne, create, update, remove }
}
