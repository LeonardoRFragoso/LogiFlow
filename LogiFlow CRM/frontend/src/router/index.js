import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/DashboardView.vue') },
      { path: 'clientes', name: 'Clientes', component: () => import('@/views/clientes/ClientesListView.vue') },
      { path: 'cotacoes', name: 'Cotacoes', component: () => import('@/views/comercial/CotacoesListView.vue') },
      { path: 'pedidos', name: 'Pedidos', component: () => import('@/views/operacional/PedidosListView.vue') },
      { path: 'motoristas', name: 'Motoristas', component: () => import('@/views/frota/MotoristasListView.vue') },
      { path: 'veiculos', name: 'Veiculos', component: () => import('@/views/frota/VeiculosListView.vue') },
      { path: 'ocorrencias', name: 'Ocorrencias', component: () => import('@/views/ocorrencias/OcorrenciasListView.vue') },
      { path: 'configuracoes/sla', name: 'Configurações SLA', component: () => import('@/views/configuracoes/SLAConfigView.vue') },
      { path: 'perfil', name: 'Meu Perfil', component: () => import('@/views/configuracoes/PerfilView.vue') },
      { path: 'configuracoes', name: 'Configurações', component: () => import('@/views/configuracoes/ConfiguracoesView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
