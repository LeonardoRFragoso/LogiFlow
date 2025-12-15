import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import TrackingView from './views/TrackingView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
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

