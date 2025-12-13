import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const token = ref(localStorage.getItem('token') || null)
  
  const isAuthenticated = computed(() => !!token.value)
  
  async function login(email, senha) {
    try {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', senha)
      
      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      
      token.value = response.data.access_token
      user.value = response.data.user
      
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      localStorage.setItem('refresh_token', response.data.refresh_token)
      
      return { success: true }
    } catch (error) {
      console.error('Erro no login:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Erro ao fazer login' 
      }
    }
  }
  
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('refresh_token')
  }
  
  return {
    user,
    token,
    isAuthenticated,
    login,
    logout
  }
})
