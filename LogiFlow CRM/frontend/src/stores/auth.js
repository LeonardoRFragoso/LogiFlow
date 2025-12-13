import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(username, password) {
    const response = await api.post('/auth/token/', { username, password })
    token.value = response.data.access
    localStorage.setItem('token', token.value)
    localStorage.setItem('refreshToken', response.data.refresh)
    await fetchUser()
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await api.get('/users/me/')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (e) {
      console.error('Erro ao buscar usuário:', e)
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }

  // Recupera usuário ao inicializar se tiver token
  if (token.value && !user.value) {
    fetchUser()
  }

  return { user, token, isAuthenticated, login, logout, fetchUser }
})
