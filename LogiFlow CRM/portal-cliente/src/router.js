import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import TrackingView from './views/TrackingView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/rastrear/:codigo?',
    name: 'Tracking',
    component: TrackingView,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

