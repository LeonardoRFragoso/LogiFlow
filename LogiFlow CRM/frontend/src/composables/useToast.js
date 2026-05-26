/**
 * Composable para notificações toast
 */

import { ref, reactive } from 'vue'

const toasts = reactive([])
let toastId = 0

export function useToast() {
  
  /**
   * Adiciona uma notificação toast
   * @param {Object} options - Opções do toast
   * @param {string} options.message - Mensagem a exibir
   * @param {string} options.type - Tipo: 'success', 'error', 'warning', 'info'
   * @param {number} options.duration - Duração em ms (padrão: 5000)
   * @param {string} options.title - Título opcional
   */
  const addToast = ({ message, type = 'info', duration = 5000, title = '' }) => {
    const id = ++toastId
    
    const toast = {
      id,
      message,
      type,
      title: title || getDefaultTitle(type),
      visible: true
    }
    
    toasts.push(toast)
    
    // Auto-remove após duração
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
    
    return id
  }

  /**
   * Remove um toast pelo ID
   */
  const removeToast = (id) => {
    const index = toasts.findIndex(t => t.id === id)
    if (index !== -1) {
      toasts.splice(index, 1)
    }
  }

  /**
   * Remove todos os toasts
   */
  const clearToasts = () => {
    toasts.splice(0, toasts.length)
  }

  /**
   * Título padrão por tipo
   */
  const getDefaultTitle = (type) => {
    switch (type) {
      case 'success': return 'Sucesso!'
      case 'error': return 'Erro!'
      case 'warning': return 'Atenção!'
      case 'info': return 'Informação'
      default: return ''
    }
  }

  // Atalhos para tipos comuns
  const success = (message, options = {}) => 
    addToast({ message, type: 'success', ...options })
  
  const error = (message, options = {}) => 
    addToast({ message, type: 'error', duration: 8000, ...options })
  
  const warning = (message, options = {}) => 
    addToast({ message, type: 'warning', ...options })
  
  const info = (message, options = {}) => 
    addToast({ message, type: 'info', ...options })

  /**
   * Trata erro de API e exibe toast apropriado
   */
  const handleApiError = (err, defaultMessage = 'Ocorreu um erro inesperado') => {
    let message = defaultMessage
    
    if (err.response) {
      // Erro da API
      const data = err.response.data
      if (data?.detail) {
        message = data.detail
      } else if (data?.message) {
        message = data.message
      } else if (typeof data === 'string') {
        message = data
      }
      
      // Mensagens específicas por código HTTP
      switch (err.response.status) {
        case 400:
          message = message || 'Dados inválidos. Verifique os campos.'
          break
        case 401:
          message = 'Sessão expirada. Faça login novamente.'
          break
        case 403:
          message = 'Você não tem permissão para esta ação.'
          break
        case 404:
          message = 'Recurso não encontrado.'
          break
        case 409:
          message = message || 'Conflito: este registro já existe.'
          break
        case 422:
          message = message || 'Dados inválidos. Verifique os campos.'
          break
        case 500:
          message = 'Erro interno do servidor. Tente novamente.'
          break
      }
    } else if (err.request) {
      // Sem resposta do servidor
      message = 'Sem conexão com o servidor. Verifique sua internet.'
    } else if (err.message) {
      message = err.message
    }
    
    error(message)
    console.error('API Error:', err)
    
    return message
  }

  return {
    toasts,
    addToast,
    removeToast,
    clearToasts,
    success,
    error,
    warning,
    info,
    handleApiError
  }
}
