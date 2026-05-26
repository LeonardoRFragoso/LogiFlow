<template>
  <router-view />
  <ToastContainer />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ToastContainer from '@/components/base/ToastContainer.vue'

const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchUser()
    } catch {
      authStore.logout()
    }
  }
})
</script>
