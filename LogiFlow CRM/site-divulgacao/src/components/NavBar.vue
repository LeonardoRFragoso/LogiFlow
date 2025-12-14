<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center space-x-2">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-xl">L</span>
          </div>
          <span class="text-2xl font-bold text-gray-900">LogiFlow</span>
          <span class="text-sm text-gray-500 font-medium">CRM</span>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center space-x-6">
          <a href="#funcionalidades" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            Funcionalidades
          </a>
          <a href="#beneficios" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            Benefícios
          </a>
          <a href="#publico-alvo" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            Para Quem
          </a>
          <a href="#comparacao" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            Comparação
          </a>
          <a href="#casos-uso" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            Casos de Uso
          </a>
          <a href="#precos" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            Preços
          </a>
          <a href="#faq" class="text-gray-700 hover:text-blue-600 transition-colors font-medium">
            FAQ
          </a>
          <button @click="$emit('request-demo')" class="px-6 py-2 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-lg font-semibold hover:shadow-lg hover:scale-105 transition-all">
            Solicitar Demo
          </button>
        </div>

        <!-- Mobile Menu Button -->
        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 rounded-lg hover:bg-gray-100">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden py-4 space-y-3">
        <a href="#funcionalidades" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          Funcionalidades
        </a>
        <a href="#beneficios" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          Benefícios
        </a>
        <a href="#publico-alvo" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          Para Quem
        </a>
        <a href="#comparacao" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          Comparação
        </a>
        <a href="#casos-uso" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          Casos de Uso
        </a>
        <a href="#precos" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          Preços
        </a>
        <a href="#faq" @click="mobileMenuOpen = false" class="block px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg">
          FAQ
        </a>
        <button @click="$emit('request-demo'); mobileMenuOpen = false" class="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-lg font-semibold">
          Solicitar Demo
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['request-demo'])

const mobileMenuOpen = ref(false)
</script>
