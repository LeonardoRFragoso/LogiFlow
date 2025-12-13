import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/entregas',
    name: 'Entregas',
    component: () => import('../views/EntregasView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/entrega/:id',
    name: 'EntregaDetalhe',
    component: () => import('../views/EntregaDetalheView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/entrega/:id/status',
    name: 'AtualizarStatus',
    component: () => import('../views/AtualizarStatusView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/entrega/:id/ocorrencia',
    name: 'RegistrarOcorrencia',
    component: () => import('../views/OcorrenciaView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: () => import('../views/PerfilView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
