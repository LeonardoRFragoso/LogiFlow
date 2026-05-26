<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">⚙️ Configurações</h1>
        <p class="page-subtitle">Personalize sua experiência no LogiFlow</p>
      </div>
    </div>

    <div class="settings-grid">
      <!-- Aparência -->
      <div class="settings-card">
        <div class="card-header">
          <div class="card-icon">🎨</div>
          <div>
            <h3>Aparência</h3>
            <p>Personalize o visual do sistema</p>
          </div>
        </div>
        <div class="card-body">
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Tema</span>
              <span class="setting-desc">Escolha entre claro, escuro ou automático</span>
            </div>
            <div class="theme-selector">
              <button 
                @click="setTheme('light')" 
                :class="['theme-btn', currentTheme === 'light' && 'active']"
              >
                ☀️ Claro
              </button>
              <button 
                @click="setTheme('dark')" 
                :class="['theme-btn', currentTheme === 'dark' && 'active']"
              >
                🌙 Escuro
              </button>
              <button 
                @click="setTheme('auto')" 
                :class="['theme-btn', currentTheme === 'auto' && 'active']"
              >
                🔄 Auto
              </button>
            </div>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Tamanho da fonte</span>
              <span class="setting-desc">Ajuste o tamanho do texto</span>
            </div>
            <select v-model="settings.fontSize" class="setting-select">
              <option value="small">Pequeno</option>
              <option value="medium">Médio</option>
              <option value="large">Grande</option>
            </select>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Sidebar compacta</span>
              <span class="setting-desc">Reduza o tamanho do menu lateral</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.compactSidebar" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Notificações -->
      <div class="settings-card">
        <div class="card-header">
          <div class="card-icon">🔔</div>
          <div>
            <h3>Notificações</h3>
            <p>Configure seus alertas e avisos</p>
          </div>
        </div>
        <div class="card-body">
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Notificações push</span>
              <span class="setting-desc">Receba alertas no navegador</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.pushNotifications" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Alertas de SLA</span>
              <span class="setting-desc">Notificar quando pedidos mudarem de status</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.slaAlerts" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">E-mail diário</span>
              <span class="setting-desc">Resumo das atividades do dia</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.dailyEmail" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Som de notificação</span>
              <span class="setting-desc">Tocar som ao receber notificações</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.notificationSound" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Regional -->
      <div class="settings-card">
        <div class="card-header">
          <div class="card-icon">🌍</div>
          <div>
            <h3>Regional</h3>
            <p>Idioma e formatação</p>
          </div>
        </div>
        <div class="card-body">
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Idioma</span>
              <span class="setting-desc">Idioma da interface</span>
            </div>
            <select v-model="settings.language" class="setting-select">
              <option value="pt-BR">Português (Brasil)</option>
              <option value="en-US">English (US)</option>
              <option value="es">Español</option>
            </select>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Formato de data</span>
              <span class="setting-desc">Como as datas são exibidas</span>
            </div>
            <select v-model="settings.dateFormat" class="setting-select">
              <option value="DD/MM/YYYY">DD/MM/YYYY</option>
              <option value="MM/DD/YYYY">MM/DD/YYYY</option>
              <option value="YYYY-MM-DD">YYYY-MM-DD</option>
            </select>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Fuso horário</span>
              <span class="setting-desc">Seu fuso horário local</span>
            </div>
            <select v-model="settings.timezone" class="setting-select">
              <option value="America/Sao_Paulo">Brasília (GMT-3)</option>
              <option value="America/Manaus">Manaus (GMT-4)</option>
              <option value="America/Rio_Branco">Rio Branco (GMT-5)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Privacidade -->
      <div class="settings-card">
        <div class="card-header">
          <div class="card-icon">🔒</div>
          <div>
            <h3>Privacidade</h3>
            <p>Controle seus dados</p>
          </div>
        </div>
        <div class="card-body">
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Mostrar status online</span>
              <span class="setting-desc">Outros usuários podem ver se você está online</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.showOnlineStatus" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <span class="setting-title">Histórico de atividades</span>
              <span class="setting-desc">Salvar registro das suas ações</span>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.activityHistory" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Atalhos -->
      <div class="settings-card">
        <div class="card-header">
          <div class="card-icon">⌨️</div>
          <div>
            <h3>Atalhos de Teclado</h3>
            <p>Navegue mais rápido</p>
          </div>
        </div>
        <div class="card-body">
          <div class="shortcuts-list">
            <div class="shortcut-item">
              <span class="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>K</kbd></span>
              <span class="shortcut-desc">Busca rápida</span>
            </div>
            <div class="shortcut-item">
              <span class="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>N</kbd></span>
              <span class="shortcut-desc">Novo pedido</span>
            </div>
            <div class="shortcut-item">
              <span class="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>D</kbd></span>
              <span class="shortcut-desc">Dashboard</span>
            </div>
            <div class="shortcut-item">
              <span class="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd></span>
              <span class="shortcut-desc">Alternar tema</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Dados -->
      <div class="settings-card">
        <div class="card-header">
          <div class="card-icon">💾</div>
          <div>
            <h3>Dados</h3>
            <p>Exportação e backup</p>
          </div>
        </div>
        <div class="card-body">
          <div class="data-actions">
            <button class="btn-data">
              📥 Exportar meus dados
            </button>
            <button class="btn-data">
              📊 Baixar relatório de atividades
            </button>
            <button class="btn-data danger">
              🗑️ Limpar cache local
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer com botão salvar -->
    <div class="settings-footer">
      <button @click="resetSettings" class="btn-reset">
        Restaurar padrões
      </button>
      <button @click="saveSettings" :disabled="salvando" class="btn-save">
        <span v-if="salvando" class="spinner"></span>
        {{ salvando ? 'Salvando...' : '✓ Salvar configurações' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import api from '@/services/api'

const themeStore = useThemeStore()
const currentTheme = ref('dark')
const salvando = ref(false)

const settings = ref({
  fontSize: 'medium',
  compactSidebar: false,
  pushNotifications: true,
  slaAlerts: true,
  dailyEmail: false,
  notificationSound: true,
  language: 'pt-BR',
  dateFormat: 'DD/MM/YYYY',
  timezone: 'America/Sao_Paulo',
  showOnlineStatus: true,
  activityHistory: true,
})

function setTheme(theme) {
  currentTheme.value = theme
  if (theme === 'dark') {
    themeStore.setDark(true)
  } else if (theme === 'light') {
    themeStore.setDark(false)
  } else {
    // Auto - usa preferência do sistema
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    themeStore.setDark(prefersDark)
  }
}

function loadSettings() {
  const saved = localStorage.getItem('userSettings')
  if (saved) {
    settings.value = { ...settings.value, ...JSON.parse(saved) }
  }
  currentTheme.value = themeStore.isDark ? 'dark' : 'light'
}

async function saveSettings() {
  salvando.value = true
  try {
    localStorage.setItem('userSettings', JSON.stringify(settings.value))
    try {
      await api.patch('/auth/me/preferences', settings.value)
    } catch {
      // Endpoint opcional — configurações ficam salvas localmente
    }
    alert('Configurações salvas com sucesso!')
  } catch (e) {
    alert('Erro ao salvar configurações')
  }
  salvando.value = false
}

function resetSettings() {
  if (confirm('Tem certeza que deseja restaurar as configurações padrão?')) {
    settings.value = {
      fontSize: 'medium',
      compactSidebar: false,
      pushNotifications: true,
      slaAlerts: true,
      dailyEmail: false,
      notificationSound: true,
      language: 'pt-BR',
      dateFormat: 'DD/MM/YYYY',
      timezone: 'America/Sao_Paulo',
      showOnlineStatus: true,
      activityHistory: true,
    }
    localStorage.removeItem('userSettings')
    alert('Configurações restauradas!')
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.page-container { max-width: 1200px; margin: 0 auto; }
.page-header { margin-bottom: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #1f2937; margin: 0; }
.dark .page-title { color: white; }
.page-subtitle { color: #6b7280; font-size: 0.875rem; margin-top: 0.25rem; }
.dark .page-subtitle { color: #9ca3af; }

.settings-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
@media (max-width: 900px) { .settings-grid { grid-template-columns: 1fr; } }

.settings-card { background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); overflow: hidden; }
.dark .settings-card { background: #1f2937; }

.card-header { display: flex; align-items: center; gap: 1rem; padding: 1.25rem; border-bottom: 1px solid #e5e7eb; }
.dark .card-header { border-color: #374151; }
.card-icon { font-size: 1.5rem; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; background: #f3f4f6; border-radius: 0.75rem; }
.dark .card-icon { background: #374151; }
.card-header h3 { margin: 0; font-size: 1rem; color: #1f2937; }
.dark .card-header h3 { color: white; }
.card-header p { margin: 0.25rem 0 0; font-size: 0.8rem; color: #6b7280; }
.card-body { padding: 1rem 1.25rem; }

.setting-item { display: flex; justify-content: space-between; align-items: center; padding: 0.875rem 0; border-bottom: 1px solid #f3f4f6; }
.dark .setting-item { border-color: #374151; }
.setting-item:last-child { border-bottom: none; }
.setting-info { display: flex; flex-direction: column; }
.setting-title { font-weight: 500; color: #1f2937; font-size: 0.9rem; }
.dark .setting-title { color: white; }
.setting-desc { font-size: 0.75rem; color: #6b7280; margin-top: 0.125rem; }

.setting-select { padding: 0.5rem 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; background: white; color: #1f2937; font-size: 0.875rem; cursor: pointer; }
.dark .setting-select { background: #374151; border-color: #4b5563; color: white; }

.theme-selector { display: flex; gap: 0.25rem; }
.theme-btn { padding: 0.5rem 0.75rem; border: 1px solid #e5e7eb; background: white; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; color: #6b7280; transition: all 0.2s; }
.dark .theme-btn { background: #374151; border-color: #4b5563; color: #9ca3af; }
.theme-btn.active { background: #3b82f6; border-color: #3b82f6; color: white; }

/* Toggle Switch */
.toggle { position: relative; display: inline-block; width: 48px; height: 26px; }
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background: #e5e7eb; transition: 0.3s; border-radius: 26px; }
.dark .toggle-slider { background: #4b5563; }
.toggle-slider:before { position: absolute; content: ""; height: 20px; width: 20px; left: 3px; bottom: 3px; background: white; transition: 0.3s; border-radius: 50%; }
.toggle input:checked + .toggle-slider { background: #3b82f6; }
.toggle input:checked + .toggle-slider:before { transform: translateX(22px); }

.shortcuts-list { display: flex; flex-direction: column; gap: 0.75rem; }
.shortcut-item { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; }
.shortcut-keys { display: flex; gap: 0.25rem; }
.shortcut-keys kbd { padding: 0.25rem 0.5rem; background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 0.25rem; font-size: 0.75rem; font-family: monospace; color: #374151; }
.dark .shortcut-keys kbd { background: #374151; border-color: #4b5563; color: #e5e7eb; }
.shortcut-desc { font-size: 0.85rem; color: #6b7280; }

.data-actions { display: flex; flex-direction: column; gap: 0.75rem; }
.btn-data { padding: 0.75rem 1rem; background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 0.5rem; cursor: pointer; font-size: 0.875rem; color: #374151; text-align: left; transition: all 0.2s; }
.dark .btn-data { background: #374151; border-color: #4b5563; color: #e5e7eb; }
.btn-data:hover { background: #e5e7eb; }
.dark .btn-data:hover { background: #4b5563; }
.btn-data.danger { color: #ef4444; }
.btn-data.danger:hover { background: #fef2f2; }
.dark .btn-data.danger:hover { background: rgba(239, 68, 68, 0.1); }

.settings-footer { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; padding: 1.5rem; background: white; border-radius: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); }
.dark .settings-footer { background: #1f2937; }
.btn-reset { padding: 0.75rem 1.5rem; background: transparent; border: 1px solid #e5e7eb; border-radius: 0.5rem; cursor: pointer; font-size: 0.9rem; color: #6b7280; }
.dark .btn-reset { border-color: #4b5563; color: #9ca3af; }
.btn-save { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-save:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); }
.btn-save:disabled { opacity: 0.7; cursor: not-allowed; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
