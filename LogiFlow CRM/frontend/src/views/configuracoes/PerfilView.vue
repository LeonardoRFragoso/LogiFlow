<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">👤 Meu Perfil</h1>
        <p class="page-subtitle">Gerencie suas informações pessoais</p>
      </div>
    </div>

    <div class="profile-grid">
      <!-- Card Avatar -->
      <div class="profile-card avatar-card">
        <div class="avatar-section">
          <div class="avatar-large">{{ userInitial }}</div>
          <div class="avatar-info">
            <h2>{{ user.first_name }} {{ user.last_name }}</h2>
            <span class="role-badge">{{ roleLabel }}</span>
          </div>
        </div>
        <div class="avatar-actions">
          <button class="btn-upload">
            📷 Alterar foto
          </button>
        </div>
        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-value">{{ stats.pedidos }}</span>
            <span class="stat-label">Pedidos</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.entregas }}</span>
            <span class="stat-label">Entregas</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ stats.dias }}</span>
            <span class="stat-label">Dias ativos</span>
          </div>
        </div>
      </div>

      <!-- Card Informações Pessoais -->
      <div class="profile-card">
        <div class="card-header">
          <h3>📋 Informações Pessoais</h3>
          <button @click="editMode = !editMode" class="btn-edit-toggle">
            {{ editMode ? '✕ Cancelar' : '✏️ Editar' }}
          </button>
        </div>
        <div class="card-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Nome</label>
              <input 
                v-model="form.first_name" 
                :disabled="!editMode" 
                class="form-input"
                placeholder="Seu nome"
              />
            </div>
            <div class="form-group">
              <label>Sobrenome</label>
              <input 
                v-model="form.last_name" 
                :disabled="!editMode" 
                class="form-input"
                placeholder="Seu sobrenome"
              />
            </div>
            <div class="form-group full-width">
              <label>E-mail</label>
              <input 
                v-model="form.email" 
                :disabled="!editMode" 
                type="email"
                class="form-input"
                placeholder="seu@email.com"
              />
            </div>
            <div class="form-group">
              <label>Telefone</label>
              <input 
                v-model="form.phone" 
                :disabled="!editMode" 
                class="form-input"
                placeholder="(11) 99999-9999"
              />
            </div>
            <div class="form-group">
              <label>Usuário</label>
              <input 
                v-model="form.username" 
                disabled 
                class="form-input disabled"
              />
            </div>
          </div>
          <div v-if="editMode" class="form-actions">
            <button @click="salvarPerfil" :disabled="salvando" class="btn-save">
              <span v-if="salvando" class="spinner"></span>
              {{ salvando ? 'Salvando...' : '✓ Salvar alterações' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Card Segurança -->
      <div class="profile-card">
        <div class="card-header">
          <h3>🔒 Segurança</h3>
        </div>
        <div class="card-body">
          <div class="security-item">
            <div class="security-info">
              <span class="security-title">Senha</span>
              <span class="security-desc">Última alteração: {{ ultimaAlteracaoSenha }}</span>
            </div>
            <button @click="showPasswordModal = true" class="btn-secondary">
              Alterar senha
            </button>
          </div>
          <div class="security-item">
            <div class="security-info">
              <span class="security-title">Autenticação de dois fatores</span>
              <span class="security-desc">Adicione uma camada extra de segurança</span>
            </div>
            <button class="btn-secondary" disabled>
              Em breve
            </button>
          </div>
          <div class="security-item">
            <div class="security-info">
              <span class="security-title">Sessões ativas</span>
              <span class="security-desc">Gerencie seus dispositivos conectados</span>
            </div>
            <button class="btn-secondary" disabled>
              Ver sessões
            </button>
          </div>
        </div>
      </div>

      <!-- Card Atividade Recente -->
      <div class="profile-card">
        <div class="card-header">
          <h3>📊 Atividade Recente</h3>
        </div>
        <div class="card-body">
          <div class="activity-list">
            <div v-for="(activity, i) in activities" :key="i" class="activity-item">
              <span class="activity-icon">{{ activity.icon }}</span>
              <div class="activity-content">
                <span class="activity-text">{{ activity.text }}</span>
                <span class="activity-time">{{ activity.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Alterar Senha -->
    <div v-if="showPasswordModal" class="modal-overlay" @click.self="showPasswordModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>🔒 Alterar Senha</h3>
          <button @click="showPasswordModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Senha atual</label>
            <input type="password" v-model="passwordForm.current" class="form-input" />
          </div>
          <div class="form-group">
            <label>Nova senha</label>
            <input type="password" v-model="passwordForm.new" class="form-input" />
            <div class="password-strength">
              <div :class="['strength-bar', passwordStrength]"></div>
              <span>{{ passwordStrengthLabel }}</span>
            </div>
          </div>
          <div class="form-group">
            <label>Confirmar nova senha</label>
            <input type="password" v-model="passwordForm.confirm" class="form-input" />
            <span v-if="passwordForm.new && passwordForm.confirm && passwordForm.new !== passwordForm.confirm" class="error-text">
              As senhas não coincidem
            </span>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showPasswordModal = false" class="btn-cancel">Cancelar</button>
          <button @click="alterarSenha" :disabled="!senhaValida" class="btn-save">Alterar senha</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

const user = computed(() => authStore.user || {})
const userInitial = computed(() => {
  const name = user.value.first_name || user.value.username || 'U'
  return name.charAt(0).toUpperCase()
})

const roleLabel = computed(() => {
  const roles = {
    admin: 'Administrador',
    manager: 'Gerente',
    operator: 'Operador',
    driver: 'Motorista',
    viewer: 'Visualizador'
  }
  return roles[user.value.role] || 'Usuário'
})

const editMode = ref(false)
const salvando = ref(false)
const showPasswordModal = ref(false)

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  username: ''
})

const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

const stats = ref({
  pedidos: 0,
  entregas: 0,
  dias: 0
})

const activities = ref([
  { icon: '📦', text: 'Criou pedido PED-2024-0125', time: 'Há 2 horas' },
  { icon: '✅', text: 'Confirmou entrega ABC-1234', time: 'Há 5 horas' },
  { icon: '👤', text: 'Atualizou perfil', time: 'Ontem' },
  { icon: '🔐', text: 'Login realizado', time: 'Ontem às 08:30' },
])

const ultimaAlteracaoSenha = computed(() => {
  return 'Há mais de 30 dias'
})

const passwordStrength = computed(() => {
  const pwd = passwordForm.value.new
  if (!pwd) return ''
  if (pwd.length < 6) return 'weak'
  if (pwd.length < 10) return 'medium'
  return 'strong'
})

const passwordStrengthLabel = computed(() => {
  const labels = { weak: 'Fraca', medium: 'Média', strong: 'Forte' }
  return labels[passwordStrength.value] || ''
})

const senhaValida = computed(() => {
  return passwordForm.value.current &&
    passwordForm.value.new &&
    passwordForm.value.new.length >= 6 &&
    passwordForm.value.new === passwordForm.value.confirm
})

function loadUserData() {
  form.value = {
    first_name: user.value.first_name || '',
    last_name: user.value.last_name || '',
    email: user.value.email || '',
    phone: user.value.phone || '',
    username: user.value.username || ''
  }
  
  // Calcular dias ativos
  if (user.value.date_joined) {
    const joined = new Date(user.value.date_joined)
    const today = new Date()
    stats.value.dias = Math.floor((today - joined) / (1000 * 60 * 60 * 24))
  }
}

async function salvarPerfil() {
  salvando.value = true
  try {
    await api.patch('/users/me/', {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      email: form.value.email,
      phone: form.value.phone
    })
    await authStore.fetchUser()
    editMode.value = false
    alert('Perfil atualizado com sucesso!')
  } catch (e) {
    console.error(e)
    alert('Erro ao atualizar perfil')
  }
  salvando.value = false
}

async function alterarSenha() {
  try {
    await api.post('/users/change-password/', {
      old_password: passwordForm.value.current,
      new_password: passwordForm.value.new
    })
    showPasswordModal.value = false
    passwordForm.value = { current: '', new: '', confirm: '' }
    alert('Senha alterada com sucesso!')
  } catch (e) {
    console.error(e)
    alert('Erro ao alterar senha. Verifique a senha atual.')
  }
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.page-container { max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #1f2937; margin: 0; }
.dark .page-title { color: white; }
.page-subtitle { color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem; }
.dark .page-subtitle { color: #9ca3af; }

.profile-grid { display: grid; grid-template-columns: 300px 1fr; gap: 1.5rem; }
@media (max-width: 900px) { .profile-grid { grid-template-columns: 1fr; } }

.profile-card { background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); overflow: hidden; }
.dark .profile-card { background: #1f2937; }

.avatar-card { grid-row: span 2; }
.avatar-section { display: flex; flex-direction: column; align-items: center; padding: 2rem; text-align: center; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); color: white; }
.avatar-large { width: 100px; height: 100px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; border: 4px solid rgba(255,255,255,0.3); }
.avatar-info h2 { margin: 0; font-size: 1.25rem; }
.role-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; margin-top: 0.5rem; }
.avatar-actions { padding: 1rem; border-bottom: 1px solid #e5e7eb; text-align: center; }
.dark .avatar-actions { border-color: #374151; }
.btn-upload { background: #f3f4f6; border: none; padding: 0.5rem 1rem; border-radius: 0.5rem; cursor: pointer; font-size: 0.875rem; color: #374151; }
.dark .btn-upload { background: #374151; color: #e5e7eb; }
.stats-row { display: flex; justify-content: space-around; padding: 1.5rem; }
.stat-item { text-align: center; }
.stat-value { display: block; font-size: 1.5rem; font-weight: 700; color: #1f2937; }
.dark .stat-value { color: white; }
.stat-label { font-size: 0.75rem; color: #6b7280; }

.card-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid #e5e7eb; }
.dark .card-header { border-color: #374151; }
.card-header h3 { margin: 0; font-size: 1rem; color: #1f2937; }
.dark .card-header h3 { color: white; }
.btn-edit-toggle { background: none; border: none; color: #3b82f6; cursor: pointer; font-size: 0.875rem; }
.card-body { padding: 1.5rem; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group.full-width { grid-column: span 2; }
.form-group label { font-size: 0.875rem; font-weight: 500; color: #374151; }
.dark .form-group label { color: #d1d5db; }
.form-input { padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 0.9rem; background: white; color: #1f2937; transition: all 0.2s; }
.dark .form-input { background: #374151; border-color: #4b5563; color: white; }
.form-input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
.form-input:disabled { background: #f9fafb; color: #9ca3af; cursor: not-allowed; }
.dark .form-input:disabled { background: #1f2937; }
.form-input.disabled { opacity: 0.6; }
.form-actions { margin-top: 1.5rem; display: flex; justify-content: flex-end; }

.security-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; border-bottom: 1px solid #f3f4f6; }
.dark .security-item { border-color: #374151; }
.security-item:last-child { border-bottom: none; }
.security-info { display: flex; flex-direction: column; }
.security-title { font-weight: 500; color: #1f2937; }
.dark .security-title { color: white; }
.security-desc { font-size: 0.8rem; color: #6b7280; }
.btn-secondary { padding: 0.5rem 1rem; background: #f3f4f6; border: none; border-radius: 0.5rem; cursor: pointer; font-size: 0.85rem; color: #374151; transition: all 0.2s; }
.dark .btn-secondary { background: #374151; color: #e5e7eb; }
.btn-secondary:hover:not(:disabled) { background: #e5e7eb; }
.dark .btn-secondary:hover:not(:disabled) { background: #4b5563; }
.btn-secondary:disabled { opacity: 0.5; cursor: not-allowed; }

.activity-list { display: flex; flex-direction: column; gap: 0.75rem; }
.activity-item { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem; background: #f9fafb; border-radius: 0.5rem; }
.dark .activity-item { background: #111827; }
.activity-icon { font-size: 1.25rem; }
.activity-content { display: flex; flex-direction: column; }
.activity-text { font-size: 0.875rem; color: #374151; }
.dark .activity-text { color: #e5e7eb; }
.activity-time { font-size: 0.75rem; color: #9ca3af; }

.btn-save { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-save:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); }
.btn-save:disabled { opacity: 0.7; cursor: not-allowed; }
.btn-cancel { padding: 0.75rem 1.5rem; background: #f3f4f6; color: #374151; border: none; border-radius: 0.5rem; font-weight: 500; cursor: pointer; }
.dark .btn-cancel { background: #374151; color: #e5e7eb; }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; border-radius: 1rem; width: 100%; max-width: 450px; }
.dark .modal-content { background: #1f2937; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem; border-bottom: 1px solid #e5e7eb; }
.dark .modal-header { border-color: #374151; }
.modal-header h3 { margin: 0; font-size: 1.1rem; color: #1f2937; }
.dark .modal-header h3 { color: white; }
.modal-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #6b7280; }
.modal-body { padding: 1.25rem; }
.modal-footer { display: flex; justify-content: flex-end; gap: 0.75rem; padding: 1.25rem; border-top: 1px solid #e5e7eb; }
.dark .modal-footer { border-color: #374151; }

.password-strength { margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }
.strength-bar { height: 4px; width: 60px; border-radius: 2px; background: #e5e7eb; }
.strength-bar.weak { background: #ef4444; }
.strength-bar.medium { background: #f59e0b; }
.strength-bar.strong { background: #10b981; }
.password-strength span { font-size: 0.75rem; color: #6b7280; }
.error-text { font-size: 0.75rem; color: #ef4444; margin-top: 0.25rem; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
