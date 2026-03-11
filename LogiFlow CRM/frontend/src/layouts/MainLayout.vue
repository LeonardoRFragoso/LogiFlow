<template>
  <div class="layout-container">
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- Logo -->
      <div class="sidebar-header">
        <div class="logo-container">
          <img src="/logo.png" alt="LogiFlow" class="sidebar-logo" />
          <span class="logo-text">LogiFlow</span>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav">
        <div class="nav-section">
          <span class="nav-section-title">Principal</span>
          <router-link to="/" class="nav-item" exact-active-class="active">
            <span class="nav-icon">📊</span>
            <span class="nav-text">Dashboard</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span class="nav-section-title">Comercial</span>
          <router-link to="/clientes" class="nav-item" active-class="active">
            <span class="nav-icon">👥</span>
            <span class="nav-text">Clientes</span>
          </router-link>
          <router-link to="/cotacoes" class="nav-item" active-class="active">
            <span class="nav-icon">💰</span>
            <span class="nav-text">Cotações</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span class="nav-section-title">Operacional</span>
          <router-link to="/pedidos" class="nav-item" active-class="active">
            <span class="nav-icon">📦</span>
            <span class="nav-text">Pedidos</span>
          </router-link>
          <router-link to="/motoristas" class="nav-item" active-class="active">
            <span class="nav-icon">🧑‍✈️</span>
            <span class="nav-text">Motoristas</span>
          </router-link>
          <router-link to="/veiculos" class="nav-item" active-class="active">
            <span class="nav-icon">🚚</span>
            <span class="nav-text">Veículos</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span class="nav-section-title">Gestão</span>
          <router-link to="/ocorrencias" class="nav-item" active-class="active">
            <span class="nav-icon">⚠️</span>
            <span class="nav-text">Ocorrências</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span class="nav-section-title">Configurações</span>
          <router-link to="/configuracoes/sla" class="nav-item" active-class="active">
            <span class="nav-icon">⚙️</span>
            <span class="nav-text">SLA</span>
          </router-link>
        </div>

        <div class="nav-section" v-if="isAdmin">
          <span class="nav-section-title">Admin</span>
          <router-link to="/admin/leads" class="nav-item" active-class="active">
            <span class="nav-icon">🎯</span>
            <span class="nav-text">Leads</span>
            <span v-if="newLeadsCount > 0" class="badge-count">{{ newLeadsCount }}</span>
          </router-link>
        </div>
      </nav>

      <!-- Sidebar Footer -->
      <div class="sidebar-footer">
        <div class="user-mini">
          <div class="user-avatar">{{ userInitial }}</div>
          <div class="user-info">
            <span class="user-name">{{ authStore.user?.first_name || authStore.user?.username || 'Usuário' }}</span>
            <span class="user-role">Administrador</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <div class="main-wrapper">
      <header class="top-header">
        <div class="header-left">
          <h2 class="page-title">{{ $route.name }}</h2>
        </div>
        <div class="header-right">
          <!-- Search -->
          <div class="search-wrapper">
            <span class="search-icon-header">🔍</span>
            <input type="text" v-model="searchQuery" placeholder="Buscar no sistema..." class="search-input-header" />
          </div>
          
          <!-- Notifications -->
          <div class="dropdown-wrapper">
            <button @click="toggleNotifications" class="header-btn" title="Notificações">
              <span>🔔</span>
              <span class="notification-badge" v-if="notifications.length">{{ notifications.length }}</span>
            </button>
            <div v-if="showNotifications" class="dropdown-menu notifications-dropdown">
              <div class="dropdown-header">
                <span class="dropdown-title">🔔 Notificações</span>
                <button class="mark-read-btn">Marcar todas como lidas</button>
              </div>
              <div class="dropdown-content">
                <div v-if="notifications.length === 0" class="empty-notifications">
                  <span>🎉</span>
                  <p>Nenhuma notificação</p>
                </div>
                <div v-else class="notification-item" v-for="(notif, i) in notifications" :key="i">
                  <span class="notif-icon">{{ notif.icon }}</span>
                  <div class="notif-content">
                    <p class="notif-text">{{ notif.text }}</p>
                    <span class="notif-time">{{ notif.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Theme Toggle -->
          <button @click="toggleTheme" class="header-btn" title="Alternar tema">
            <span v-if="themeStore.isDark">☀️</span>
            <span v-else>🌙</span>
          </button>
          
          <!-- User Menu -->
          <div class="dropdown-wrapper">
            <button @click="toggleUserMenu" class="user-avatar-btn" :title="userName">
              {{ userInitial }}
            </button>
            <div v-if="showUserMenu" class="dropdown-menu user-dropdown">
              <div class="user-dropdown-header">
                <div class="user-avatar-large">{{ userInitial }}</div>
                <div class="user-info-dropdown">
                  <span class="user-name-dropdown">{{ userName }}</span>
                  <span class="user-email-dropdown">{{ userEmail }}</span>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <button @click="goToProfile" class="dropdown-item">
                <span>👤</span> Meu Perfil
              </button>
              <button @click="goToSettings" class="dropdown-item">
                <span>⚙️</span> Configurações
              </button>
              <div class="dropdown-divider"></div>
              <button @click="logout" class="dropdown-item text-red">
                <span>🚪</span> Sair
              </button>
            </div>
          </div>
        </div>
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()

// Search
const searchQuery = ref('')

// Dropdowns
const showNotifications = ref(false)
const showUserMenu = ref(false)

// Admin
const newLeadsCount = ref(0)

// Mock notifications (replace with real data later)
const notifications = ref([
  { icon: '📦', text: 'Novo pedido PED-2024-001 criado', time: 'Há 5 min' },
  { icon: '🚚', text: 'Entrega confirmada - ABC-1234', time: 'Há 15 min' },
  { icon: '⚠️', text: '2 entregas com SLA crítico', time: 'Há 1 hora' },
])

// User info
const userName = computed(() => authStore.user?.first_name || authStore.user?.username || 'Usuário')
const userEmail = computed(() => authStore.user?.email || 'usuario@logiflow.com')
const userInitial = computed(() => {
  const name = authStore.user?.first_name || authStore.user?.username || 'U'
  return name.charAt(0).toUpperCase()
})
const isAdmin = computed(() => authStore.user?.tipo === 'admin' || authStore.user?.is_admin === true)

function toggleNotifications() {
  showNotifications.value = !showNotifications.value
  showUserMenu.value = false
}

function toggleUserMenu() {
  showUserMenu.value = !showUserMenu.value
  showNotifications.value = false
}

function toggleTheme() {
  themeStore.toggleTheme()
}

function logout() {
  authStore.logout()
  router.push('/login')
}

function goToProfile() {
  showUserMenu.value = false
  router.push('/perfil')
}

function goToSettings() {
  showUserMenu.value = false
  router.push('/configuracoes')
}

// Close dropdowns when clicking outside
function handleClickOutside(e) {
  if (!e.target.closest('.dropdown-wrapper')) {
    showNotifications.value = false
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Fetch user if not loaded
  if (!authStore.user && authStore.token) {
    authStore.fetchUser()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.layout-container {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
}

.dark .layout-container {
  background: #0f172a;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 40;
}

.dark .sidebar {
  background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
}

.sidebar-header {
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  height: 65px;
  box-sizing: border-box;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar-logo {
  height: 40px;
  width: 40px;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  padding: 4px;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 1.5rem;
}

.nav-section-title {
  display: block;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.4);
  padding: 0 0.75rem;
  margin-bottom: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.2s;
  margin-bottom: 0.25rem;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  width: 3px;
  height: 100%;
  background: white;
  border-radius: 0 2px 2px 0;
}

.nav-icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.nav-text {
  font-size: 0.9rem;
  font-weight: 500;
}

.badge-count {
  margin-left: auto;
  background: #ef4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  min-width: 20px;
  text-align: center;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-mini {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  color: white;
  font-size: 0.85rem;
  font-weight: 500;
}

.user-role {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.7rem;
}

/* Main Wrapper */
.main-wrapper {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
}

/* Header */
.top-header {
  background: white;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 30;
  height: 65px;
  box-sizing: border-box;
}

.dark .top-header {
  background: #1f2937;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.page-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.dark .page-title {
  color: white;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Search */
.search-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  min-width: 220px;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.dark .search-wrapper {
  background: #374151;
  border-color: #4b5563;
}

.search-wrapper:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  background: white;
}

.dark .search-wrapper:focus-within {
  background: #1f2937;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
}

.search-icon-header {
  font-size: 0.9rem;
  opacity: 0.5;
}

.search-input-header {
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.875rem;
  color: #1f2937;
  width: 100%;
}

.dark .search-input-header {
  color: white;
}

.search-input-header::placeholder {
  color: #9ca3af;
}

/* Dropdown */
.dropdown-wrapper {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  min-width: 280px;
  z-index: 100;
  overflow: hidden;
  animation: dropdownFade 0.2s ease;
}

.dark .dropdown-menu {
  background: #1f2937;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

@keyframes dropdownFade {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.dark .dropdown-header {
  border-color: #374151;
}

.dropdown-title {
  font-weight: 600;
  color: #1f2937;
}

.dark .dropdown-title {
  color: white;
}

.mark-read-btn {
  font-size: 0.75rem;
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
}

.mark-read-btn:hover {
  text-decoration: underline;
}

.dropdown-content {
  max-height: 300px;
  overflow-y: auto;
}

.empty-notifications {
  text-align: center;
  padding: 2rem;
  color: #9ca3af;
}

.empty-notifications span {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

.notification-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  cursor: pointer;
  transition: background 0.15s;
}

.notification-item:hover {
  background: #f8fafc;
}

.dark .notification-item:hover {
  background: #111827;
}

.notif-icon {
  font-size: 1.25rem;
}

.notif-content {
  flex: 1;
}

.notif-text {
  font-size: 0.875rem;
  color: #374151;
  margin: 0;
}

.dark .notif-text {
  color: #e5e7eb;
}

.notif-time {
  font-size: 0.75rem;
  color: #9ca3af;
}

/* User Avatar Button */
.user-avatar-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.user-avatar-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

/* User Dropdown */
.user-dropdown {
  min-width: 240px;
}

.user-dropdown-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
}

.user-avatar-large {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 1.1rem;
}

.user-info-dropdown {
  display: flex;
  flex-direction: column;
}

.user-name-dropdown {
  font-weight: 600;
  color: #1f2937;
}

.dark .user-name-dropdown {
  color: white;
}

.user-email-dropdown {
  font-size: 0.75rem;
  color: #9ca3af;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0.25rem 0;
}

.dark .dropdown-divider {
  background: #374151;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  color: #374151;
  transition: background 0.15s;
  text-align: left;
}

.dark .dropdown-item {
  color: #e5e7eb;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.dark .dropdown-item:hover {
  background: #111827;
}

.dropdown-item.text-red {
  color: #ef4444;
}

.dropdown-item.text-red:hover {
  background: #fef2f2;
}

.dark .dropdown-item.text-red:hover {
  background: rgba(239, 68, 68, 0.1);
}

.header-btn {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  font-size: 1.1rem;
}

.dark .header-btn {
  background: #374151;
}

.header-btn:hover {
  background: #e2e8f0;
  transform: scale(1.05);
}

.dark .header-btn:hover {
  background: #4b5563;
}

.notification-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 18px;
  height: 18px;
  background: #ef4444;
  color: white;
  font-size: 0.65rem;
  font-weight: 600;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 0.5rem;
  padding-left: 0.75rem;
  border-left: 1px solid #e5e7eb;
}

.dark .user-menu {
  border-color: #374151;
}

.user-avatar-header {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  font-size: 0.85rem;
}

.logout-btn {
  width: 36px;
  height: 36px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fee2e2;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.dark .logout-btn {
  background: rgba(239, 68, 68, 0.2);
}

.logout-btn:hover {
  background: #fecaca;
  transform: scale(1.05);
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 1.5rem;
}
</style>
