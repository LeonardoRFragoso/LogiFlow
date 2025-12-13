<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">⚙️ Configurações de SLA</h1>
        <p class="page-subtitle">Defina os parâmetros de SLA para suas entregas</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs-container">
      <button 
        v-for="tab in tabs" 
        :key="tab.id" 
        @click="activeTab = tab.id"
        :class="['tab-btn', activeTab === tab.id && 'active']"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab: Configuração Global -->
    <div v-if="activeTab === 'global'" class="tab-content">
      <div class="config-card">
        <div class="card-header">
          <h2>🎯 Limites de SLA Padrão</h2>
          <p>Defina os limites padrão que serão aplicados a todos os pedidos</p>
        </div>
        <div class="card-body">
          <div class="sla-preview">
            <div class="sla-item verde">
              <span class="sla-dot">🟢</span>
              <div class="sla-info">
                <span class="sla-label">No Prazo</span>
                <span class="sla-desc">Mais de {{ config.limite_verde }} dias para entrega</span>
              </div>
              <div class="sla-input">
                <label>Dias</label>
                <input type="number" v-model.number="config.limite_verde" min="1" />
              </div>
            </div>
            <div class="sla-item amarelo">
              <span class="sla-dot">🟡</span>
              <div class="sla-info">
                <span class="sla-label">Atenção</span>
                <span class="sla-desc">Entre {{ config.limite_amarelo }} e {{ config.limite_verde }} dias</span>
              </div>
              <div class="sla-input">
                <label>Dias</label>
                <input type="number" v-model.number="config.limite_amarelo" min="0" />
              </div>
            </div>
            <div class="sla-item vermelho">
              <span class="sla-dot">🔴</span>
              <div class="sla-info">
                <span class="sla-label">Atrasado</span>
                <span class="sla-desc">Menos de {{ config.limite_amarelo }} dias ou prazo vencido</span>
              </div>
            </div>
          </div>

          <div class="options-section">
            <h3>Opções Adicionais</h3>
            <div class="options-grid">
              <label class="checkbox-option">
                <input type="checkbox" v-model="config.considerar_dias_uteis" />
                <span class="checkbox-label">
                  <span class="checkbox-title">📅 Considerar apenas dias úteis</span>
                  <span class="checkbox-desc">Ignora sábados, domingos e feriados no cálculo</span>
                </span>
              </label>
              <label class="checkbox-option">
                <input type="checkbox" v-model="config.alertar_sla_amarelo" />
                <span class="checkbox-label">
                  <span class="checkbox-title">🔔 Alertar quando SLA ficar amarelo</span>
                  <span class="checkbox-desc">Envia notificação quando pedido entrar em atenção</span>
                </span>
              </label>
              <label class="checkbox-option">
                <input type="checkbox" v-model="config.alertar_sla_vermelho" />
                <span class="checkbox-label">
                  <span class="checkbox-title">🚨 Alertar quando SLA ficar vermelho</span>
                  <span class="checkbox-desc">Envia notificação quando pedido atrasar</span>
                </span>
              </label>
            </div>
          </div>

          <div class="card-actions">
            <button @click="salvarConfig" :disabled="salvando" class="btn-save">
              <span v-if="salvando" class="spinner"></span>
              {{ salvando ? 'Salvando...' : '✓ Salvar Configurações' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: SLA por Cliente -->
    <div v-if="activeTab === 'clientes'" class="tab-content">
      <div class="config-card">
        <div class="card-header">
          <div>
            <h2>👥 SLA por Cliente</h2>
            <p>Configure SLA diferenciado para clientes VIP ou especiais</p>
          </div>
          <button @click="openClienteModal()" class="btn-add-small">+ Adicionar</button>
        </div>
        <div class="card-body">
          <div class="table-container-inner">
            <table class="config-table">
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Prioridade</th>
                  <th>Limite Verde</th>
                  <th>Limite Amarelo</th>
                  <th>Bônus</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="sla in slaClientes" :key="sla.id">
                  <td>{{ sla.cliente_nome }}</td>
                  <td>
                    <span :class="['priority-badge', 'priority-' + sla.prioridade]">
                      {{ prioridadeLabel(sla.prioridade) }}
                    </span>
                  </td>
                  <td>{{ sla.limite_verde }} dias</td>
                  <td>{{ sla.limite_amarelo }} dias</td>
                  <td>{{ sla.bonus_horas }}h</td>
                  <td>
                    <div class="action-buttons">
                      <button @click="openClienteModal(sla)" class="btn-action btn-edit">✏️</button>
                      <button @click="deleteSlaCliente(sla.id)" class="btn-action btn-delete">🗑️</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="slaClientes.length === 0" class="empty-state-small">
              <span>👥</span>
              <p>Nenhum SLA de cliente configurado</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: SLA por Rota -->
    <div v-if="activeTab === 'rotas'" class="tab-content">
      <div class="config-card">
        <div class="card-header">
          <div>
            <h2>🗺️ SLA por Rota</h2>
            <p>Configure prazos diferentes para rotas específicas</p>
          </div>
          <button @click="openRotaModal()" class="btn-add-small">+ Adicionar</button>
        </div>
        <div class="card-body">
          <div class="table-container-inner">
            <table class="config-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Rota</th>
                  <th>Dias Adicionais</th>
                  <th>Prazo Médio</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="sla in slaRotas" :key="sla.id">
                  <td>{{ sla.nome }}</td>
                  <td><span class="route-display">{{ sla.rota_display }}</span></td>
                  <td>+{{ sla.dias_adicionais }} dias</td>
                  <td>{{ sla.prazo_medio_dias }} dias</td>
                  <td>
                    <span :class="['status-badge', sla.ativo ? 'status-ativo' : 'status-inativo']">
                      {{ sla.ativo ? 'Ativo' : 'Inativo' }}
                    </span>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button @click="openRotaModal(sla)" class="btn-action btn-edit">✏️</button>
                      <button @click="deleteSlaRota(sla.id)" class="btn-action btn-delete">🗑️</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="slaRotas.length === 0" class="empty-state-small">
              <span>🗺️</span>
              <p>Nenhum SLA de rota configurado</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Cliente -->
    <div v-if="showClienteModal" class="modal-overlay" @click.self="showClienteModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingCliente ? '✏️ Editar' : '➕ Novo' }} SLA de Cliente</h3>
          <button @click="showClienteModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Cliente</label>
            <select v-model="clienteForm.cliente" class="form-select" :disabled="editingCliente">
              <option value="">Selecione um cliente...</option>
              <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.razao_social }}</option>
            </select>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Prioridade</label>
              <select v-model="clienteForm.prioridade" class="form-select">
                <option value="normal">Normal</option>
                <option value="alta">Alta</option>
                <option value="vip">VIP</option>
              </select>
            </div>
            <div class="form-group">
              <label>Bônus de Horas</label>
              <input type="number" v-model.number="clienteForm.bonus_horas" class="form-input" min="0" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Limite Verde (dias)</label>
              <input type="number" v-model.number="clienteForm.limite_verde" class="form-input" min="1" />
            </div>
            <div class="form-group">
              <label>Limite Amarelo (dias)</label>
              <input type="number" v-model.number="clienteForm.limite_amarelo" class="form-input" min="0" />
            </div>
          </div>
          <div class="form-group">
            <label>Observações</label>
            <textarea v-model="clienteForm.observacoes" class="form-textarea" rows="2"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showClienteModal = false" class="btn-cancel">Cancelar</button>
          <button @click="salvarSlaCliente" class="btn-save">Salvar</button>
        </div>
      </div>
    </div>

    <!-- Modal Rota -->
    <div v-if="showRotaModal" class="modal-overlay" @click.self="showRotaModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingRota ? '✏️ Editar' : '➕ Nova' }} SLA de Rota</h3>
          <button @click="showRotaModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nome da Rota</label>
            <input type="text" v-model="rotaForm.nome" class="form-input" placeholder="Ex: SP → RJ Expressa" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>UF Origem</label>
              <select v-model="rotaForm.origem_uf" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Cidade Origem (opcional)</label>
              <input type="text" v-model="rotaForm.origem_cidade" class="form-input" placeholder="Todas as cidades" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>UF Destino</label>
              <select v-model="rotaForm.destino_uf" class="form-select">
                <option value="">Selecione...</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Cidade Destino (opcional)</label>
              <input type="text" v-model="rotaForm.destino_cidade" class="form-input" placeholder="Todas as cidades" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Dias Adicionais</label>
              <input type="number" v-model.number="rotaForm.dias_adicionais" class="form-input" min="0" />
            </div>
            <div class="form-group">
              <label>Prazo Médio (dias)</label>
              <input type="number" v-model.number="rotaForm.prazo_medio_dias" class="form-input" min="1" />
            </div>
          </div>
          <div class="form-group">
            <label class="checkbox-inline">
              <input type="checkbox" v-model="rotaForm.ativo" />
              Rota ativa
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showRotaModal = false" class="btn-cancel">Cancelar</button>
          <button @click="salvarSlaRota" class="btn-save">Salvar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const activeTab = ref('global')
const tabs = [
  { id: 'global', label: 'Configuração Global', icon: '🎯' },
  { id: 'clientes', label: 'SLA por Cliente', icon: '👥' },
  { id: 'rotas', label: 'SLA por Rota', icon: '🗺️' },
]

// Config Global
const config = ref({
  limite_verde: 2,
  limite_amarelo: 1,
  considerar_dias_uteis: false,
  alertar_sla_amarelo: true,
  alertar_sla_vermelho: true,
})
const salvando = ref(false)

// SLA Clientes
const slaClientes = ref([])
const clientes = ref([])
const showClienteModal = ref(false)
const editingCliente = ref(null)
const clienteForm = ref({
  cliente: '',
  prioridade: 'normal',
  limite_verde: 2,
  limite_amarelo: 1,
  bonus_horas: 0,
  observacoes: ''
})

// SLA Rotas
const slaRotas = ref([])
const showRotaModal = ref(false)
const editingRota = ref(null)
const rotaForm = ref({
  nome: '',
  origem_uf: '',
  origem_cidade: '',
  destino_uf: '',
  destino_cidade: '',
  dias_adicionais: 0,
  prazo_medio_dias: 3,
  ativo: true
})

const ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

// Funções
async function fetchConfig() {
  try {
    const response = await api.get('/sla/config/atual/')
    config.value = response.data
  } catch (e) {
    console.log('Usando configuração padrão')
  }
}

async function fetchSlaClientes() {
  try {
    const response = await api.get('/sla/clientes/')
    slaClientes.value = response.data.results || response.data
  } catch (e) {
    console.error(e)
  }
}

async function fetchSlaRotas() {
  try {
    const response = await api.get('/sla/rotas/')
    slaRotas.value = response.data.results || response.data
  } catch (e) {
    console.error(e)
  }
}

async function fetchClientes() {
  try {
    const response = await api.get('/clientes/')
    clientes.value = response.data.results || response.data
  } catch (e) {
    console.error(e)
  }
}

async function salvarConfig() {
  salvando.value = true
  try {
    await api.patch('/sla/config/atual/', config.value)
    alert('Configurações salvas com sucesso!')
  } catch (e) {
    console.error(e)
    alert('Erro ao salvar configurações')
  }
  salvando.value = false
}

function openClienteModal(sla = null) {
  editingCliente.value = sla
  if (sla) {
    clienteForm.value = { ...sla }
  } else {
    clienteForm.value = {
      cliente: '',
      prioridade: 'normal',
      limite_verde: config.value.limite_verde,
      limite_amarelo: config.value.limite_amarelo,
      bonus_horas: 0,
      observacoes: ''
    }
  }
  showClienteModal.value = true
}

async function salvarSlaCliente() {
  try {
    if (editingCliente.value) {
      await api.patch(`/sla/clientes/${editingCliente.value.id}/`, clienteForm.value)
    } else {
      await api.post('/sla/clientes/', clienteForm.value)
    }
    showClienteModal.value = false
    fetchSlaClientes()
  } catch (e) {
    console.error(e)
    alert('Erro ao salvar SLA do cliente')
  }
}

async function deleteSlaCliente(id) {
  if (confirm('Tem certeza que deseja excluir este SLA?')) {
    await api.delete(`/sla/clientes/${id}/`)
    fetchSlaClientes()
  }
}

function openRotaModal(sla = null) {
  editingRota.value = sla
  if (sla) {
    rotaForm.value = { ...sla }
  } else {
    rotaForm.value = {
      nome: '',
      origem_uf: '',
      origem_cidade: '',
      destino_uf: '',
      destino_cidade: '',
      dias_adicionais: 0,
      prazo_medio_dias: 3,
      ativo: true
    }
  }
  showRotaModal.value = true
}

async function salvarSlaRota() {
  try {
    if (editingRota.value) {
      await api.patch(`/sla/rotas/${editingRota.value.id}/`, rotaForm.value)
    } else {
      await api.post('/sla/rotas/', rotaForm.value)
    }
    showRotaModal.value = false
    fetchSlaRotas()
  } catch (e) {
    console.error(e)
    alert('Erro ao salvar SLA da rota')
  }
}

async function deleteSlaRota(id) {
  if (confirm('Tem certeza que deseja excluir este SLA?')) {
    await api.delete(`/sla/rotas/${id}/`)
    fetchSlaRotas()
  }
}

const prioridadeLabel = (p) => ({ normal: 'Normal', alta: 'Alta', vip: 'VIP' }[p] || p)

onMounted(() => {
  fetchConfig()
  fetchSlaClientes()
  fetchSlaRotas()
  fetchClientes()
})
</script>

<style scoped>
.page-container { max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #1f2937; margin: 0; }
.dark .page-title { color: white; }
.page-subtitle { color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem; }
.dark .page-subtitle { color: #9ca3af; }

/* Tabs */
.tabs-container { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; background: #f3f4f6; padding: 0.5rem; border-radius: 0.75rem; }
.dark .tabs-container { background: #1f2937; }
.tab-btn { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; border: none; background: transparent; border-radius: 0.5rem; font-size: 0.9rem; cursor: pointer; color: #6b7280; transition: all 0.2s; font-weight: 500; }
.dark .tab-btn { color: #9ca3af; }
.tab-btn.active { background: white; color: #1f2937; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.dark .tab-btn.active { background: #374151; color: white; }
.tab-icon { font-size: 1.1rem; }

/* Config Card */
.config-card { background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); overflow: hidden; }
.dark .config-card { background: #1f2937; }
.card-header { padding: 1.5rem; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; }
.dark .card-header { border-color: #374151; }
.card-header h2 { font-size: 1.1rem; font-weight: 600; margin: 0; color: #1f2937; }
.dark .card-header h2 { color: white; }
.card-header p { font-size: 0.875rem; color: #6b7280; margin: 0.25rem 0 0; }
.card-body { padding: 1.5rem; }
.card-actions { display: flex; justify-content: flex-end; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb; }
.dark .card-actions { border-color: #374151; }

/* SLA Preview */
.sla-preview { display: flex; flex-direction: column; gap: 1rem; }
.sla-item { display: flex; align-items: center; gap: 1rem; padding: 1rem; border-radius: 0.75rem; }
.sla-item.verde { background: rgba(16, 185, 129, 0.1); }
.sla-item.amarelo { background: rgba(245, 158, 11, 0.1); }
.sla-item.vermelho { background: rgba(239, 68, 68, 0.1); }
.sla-dot { font-size: 1.5rem; }
.sla-info { flex: 1; }
.sla-label { display: block; font-weight: 600; color: #1f2937; }
.dark .sla-label { color: white; }
.sla-desc { font-size: 0.8rem; color: #6b7280; }
.sla-input { display: flex; flex-direction: column; gap: 0.25rem; }
.sla-input label { font-size: 0.75rem; color: #6b7280; }
.sla-input input { width: 80px; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.375rem; text-align: center; font-size: 1rem; font-weight: 600; }
.dark .sla-input input { background: #374151; border-color: #4b5563; color: white; }

/* Options */
.options-section { margin-top: 2rem; }
.options-section h3 { font-size: 0.9rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem; }
.dark .options-section h3 { color: white; }
.options-grid { display: flex; flex-direction: column; gap: 0.75rem; }
.checkbox-option { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 1rem; background: #f8fafc; border-radius: 0.5rem; cursor: pointer; }
.dark .checkbox-option { background: #111827; }
.checkbox-option input { margin-top: 0.25rem; }
.checkbox-label { display: flex; flex-direction: column; }
.checkbox-title { font-size: 0.875rem; font-weight: 500; color: #1f2937; }
.dark .checkbox-title { color: white; }
.checkbox-desc { font-size: 0.75rem; color: #6b7280; }

/* Table */
.table-container-inner { overflow-x: auto; }
.config-table { width: 100%; border-collapse: collapse; }
.config-table th { text-align: left; padding: 0.75rem 1rem; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #6b7280; background: #f8fafc; }
.dark .config-table th { background: #111827; color: #9ca3af; }
.config-table td { padding: 0.75rem 1rem; border-bottom: 1px solid #f3f4f6; color: #374151; }
.dark .config-table td { border-color: #1f2937; color: #e5e7eb; }

/* Badges */
.priority-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.priority-normal { background: #f3f4f6; color: #6b7280; }
.priority-alta { background: #fef3c7; color: #d97706; }
.priority-vip { background: #dbeafe; color: #1d4ed8; }
.dark .priority-normal { background: #374151; color: #9ca3af; }
.dark .priority-alta { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
.dark .priority-vip { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.status-badge { padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-ativo { background: #d1fae5; color: #059669; }
.status-inativo { background: #f3f4f6; color: #6b7280; }
.dark .status-ativo { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.dark .status-inativo { background: #374151; color: #9ca3af; }
.route-display { font-size: 0.85rem; color: #6b7280; }

/* Buttons */
.btn-add-small { padding: 0.5rem 1rem; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; border-radius: 0.5rem; font-size: 0.85rem; font-weight: 600; cursor: pointer; }
.btn-save { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-save:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); }
.btn-save:disabled { opacity: 0.7; cursor: not-allowed; }
.btn-cancel { padding: 0.75rem 1.5rem; background: #f3f4f6; color: #374151; border: none; border-radius: 0.5rem; font-weight: 500; cursor: pointer; }
.dark .btn-cancel { background: #374151; color: #e5e7eb; }
.action-buttons { display: flex; gap: 0.5rem; }
.btn-action { width: 32px; height: 32px; border-radius: 0.375rem; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 0.9rem; }
.btn-edit { background: #eff6ff; color: #3b82f6; }
.btn-edit:hover { background: #dbeafe; }
.dark .btn-edit { background: rgba(59, 130, 246, 0.2); }
.btn-delete { background: #fef2f2; color: #ef4444; }
.btn-delete:hover { background: #fee2e2; }
.dark .btn-delete { background: rgba(239, 68, 68, 0.2); }

/* Empty State */
.empty-state-small { text-align: center; padding: 2rem; color: #9ca3af; }
.empty-state-small span { font-size: 2rem; display: block; margin-bottom: 0.5rem; }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; border-radius: 1rem; width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; }
.dark .modal-content { background: #1f2937; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem; border-bottom: 1px solid #e5e7eb; }
.dark .modal-header { border-color: #374151; }
.modal-header h3 { margin: 0; font-size: 1.1rem; color: #1f2937; }
.dark .modal-header h3 { color: white; }
.modal-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #6b7280; }
.modal-body { padding: 1.25rem; }
.modal-footer { display: flex; justify-content: flex-end; gap: 0.75rem; padding: 1.25rem; border-top: 1px solid #e5e7eb; }
.dark .modal-footer { border-color: #374151; }

/* Form */
.form-group { margin-bottom: 1rem; }
.form-group label { display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.5rem; }
.dark .form-group label { color: #d1d5db; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-input, .form-select, .form-textarea { width: 100%; padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 0.9rem; background: white; color: #1f2937; }
.dark .form-input, .dark .form-select, .dark .form-textarea { background: #374151; border-color: #4b5563; color: white; }
.form-input:focus, .form-select:focus, .form-textarea:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
.checkbox-inline { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
