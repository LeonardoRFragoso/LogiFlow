/**
 * LogiFlow CRM - Serviço de Sincronização Frontend
 * Comunicação com API de sincronização SuiteCRM
 */

import api from './api'

class SyncService {
  /**
   * Obtém status atual da sincronização
   */
  async getStatus() {
    try {
      const response = await api.get('/sync/status')
      return response.data
    } catch (error) {
      console.error('Erro ao obter status de sincronização:', error)
      throw error
    }
  }

  /**
   * Sincroniza dados do SuiteCRM para o local
   * @param {Array<string>} modules - Módulos específicos ou null para todos
   */
  async syncFromSuiteCRM(modules = null) {
    try {
      const payload = modules ? { modules } : {}
      const response = await api.post('/sync/from-suitecrm', payload)
      return response.data
    } catch (error) {
      console.error('Erro ao sincronizar do SuiteCRM:', error)
      throw error
    }
  }

  /**
   * Sincroniza dados do local para o SuiteCRM
   * @param {Array<string>} modules - Módulos específicos ou null para todos
   */
  async syncToSuiteCRM(modules = null) {
    try {
      const payload = modules ? { modules } : {}
      const response = await api.post('/sync/to-suitecrm', payload)
      return response.data
    } catch (error) {
      console.error('Erro ao sincronizar para o SuiteCRM:', error)
      throw error
    }
  }

  /**
   * Sincronização bidirecional completa
   * @param {Array<string>} modules - Módulos específicos ou null para todos
   */
  async syncBidirectional(modules = null) {
    try {
      const payload = modules ? { modules } : {}
      const response = await api.post('/sync/bidirectional', payload)
      return response.data
    } catch (error) {
      console.error('Erro na sincronização bidirecional:', error)
      throw error
    }
  }

  /**
   * Força sincronização completa (use com cuidado)
   */
  async forceFullSync() {
    try {
      const response = await api.post('/sync/force-full-sync')
      return response.data
    } catch (error) {
      console.error('Erro ao forçar sincronização completa:', error)
      throw error
    }
  }

  /**
   * Lista módulos disponíveis para sincronização
   */
  async getAvailableModules() {
    try {
      const response = await api.get('/sync/modules')
      return response.data
    } catch (error) {
      console.error('Erro ao listar módulos:', error)
      throw error
    }
  }

  /**
   * Sincroniza módulo específico do SuiteCRM
   * @param {string} moduleName - Nome do módulo
   */
  async syncModuleFromSuiteCRM(moduleName) {
    try {
      const response = await api.post(`/sync/module/${moduleName}/from-suitecrm`)
      return response.data
    } catch (error) {
      console.error(`Erro ao sincronizar ${moduleName} do SuiteCRM:`, error)
      throw error
    }
  }

  /**
   * Sincroniza módulo específico para o SuiteCRM
   * @param {string} moduleName - Nome do módulo
   */
  async syncModuleToSuiteCRM(moduleName) {
    try {
      const response = await api.post(`/sync/module/${moduleName}/to-suitecrm`)
      return response.data
    } catch (error) {
      console.error(`Erro ao sincronizar ${moduleName} para o SuiteCRM:`, error)
      throw error
    }
  }

  /**
   * Verifica status da conexão com SuiteCRM
   */
  async checkSuiteCRMConnection() {
    try {
      const response = await api.get('/suitecrm/status')
      return response.data
    } catch (error) {
      console.error('Erro ao verificar conexão SuiteCRM:', error)
      throw error
    }
  }

  /**
   * Formata data de última sincronização
   * @param {string} timestamp - ISO timestamp
   */
  formatLastSync(timestamp) {
    if (!timestamp) return 'Nunca'
    
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Agora mesmo'
    if (diffMins < 60) return `${diffMins} min atrás`
    
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h atrás`
    
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays}d atrás`
  }

  /**
   * Retorna ícone de status baseado no módulo
   * @param {string} moduleName - Nome do módulo
   */
  getModuleIcon(moduleName) {
    const icons = {
      pedidos: '📦',
      motoristas: '🚚',
      veiculos: '🚛',
      clientes: '👥',
      cotacoes: '💰'
    }
    return icons[moduleName] || '📋'
  }

  /**
   * Retorna nome amigável do módulo
   * @param {string} moduleName - Nome do módulo
   */
  getModuleFriendlyName(moduleName) {
    const names = {
      pedidos: 'Pedidos',
      motoristas: 'Motoristas',
      veiculos: 'Veículos',
      clientes: 'Clientes',
      cotacoes: 'Cotações'
    }
    return names[moduleName] || moduleName
  }
}

export default new SyncService()
