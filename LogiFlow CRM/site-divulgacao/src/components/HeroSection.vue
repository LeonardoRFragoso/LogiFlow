<template>
  <section class="pt-24 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 via-white to-cyan-50 overflow-hidden">
    <div class="max-w-7xl mx-auto">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <!-- Left Content -->
        <div class="animate-fade-in-up">
          <div class="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold mb-6">
            🇧🇷 O único CRM brasileiro especializado em Transportadoras
          </div>
          
          <h1 class="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
            Sua transportadora no controle.
            <span class="text-gradient">Do comercial à entrega.</span>
          </h1>
          
          <p class="text-xl text-gray-600 mb-8 leading-relaxed">
            <strong>CRM + TMS + Fiscal em um só sistema.</strong> Gestão comercial, operacional e emissão de CT-e/MDF-e integrada — sem precisar de múltiplos sistemas.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 mb-8">
            <button @click="$emit('request-demo')" class="group px-8 py-4 bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 relative overflow-hidden">
              <span class="relative z-10 flex items-center justify-center gap-2">
                <span class="text-2xl">🎯</span>
                Solicitar Demonstração Grátis
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>
            <button @click="openVideo" class="px-8 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-xl font-bold text-lg hover:border-blue-600 hover:text-blue-600 hover:bg-blue-50 transition-all duration-300 shadow-md hover:shadow-lg flex items-center justify-center gap-2">
              <span class="text-2xl">📹</span>
              Ver Vídeo Demo
            </button>
          </div>
          
          <div class="flex items-center gap-8 text-sm text-gray-600">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span>Sem contrato de fidelidade</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span>Setup em 48 horas</span>
            </div>
          </div>
        </div>
        
        <!-- Right Content - Dashboard Preview -->
        <div class="relative animate-float">
          <div class="relative z-10 bg-white rounded-2xl shadow-2xl p-6 border border-gray-200 overflow-hidden">
            <!-- Browser Chrome -->
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
              <div class="w-3 h-3 rounded-full bg-red-500 hover:bg-red-600 transition-colors cursor-pointer"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-500 hover:bg-yellow-600 transition-colors cursor-pointer"></div>
              <div class="w-3 h-3 rounded-full bg-green-500 hover:bg-green-600 transition-colors cursor-pointer"></div>
              <div class="ml-4 text-xs text-gray-400 font-mono">logiflow.com.br/dashboard</div>
            </div>
            
            <!-- Dashboard Content -->
            <div class="space-y-4">
              <!-- Header Bar -->
              <div class="h-10 bg-gradient-to-r from-blue-500 via-blue-600 to-cyan-500 rounded-lg flex items-center px-4 shadow-md">
                <div class="w-20 h-3 bg-white/30 rounded"></div>
              </div>
              
              <!-- Stats Cards -->
              <div class="grid grid-cols-3 gap-4">
                <div class="group h-28 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl flex items-center justify-center hover:shadow-lg transition-all cursor-pointer border border-blue-200">
                  <div class="text-center">
                    <div class="text-3xl font-bold text-blue-600 group-hover:scale-110 transition-transform">127</div>
                    <div class="text-xs text-gray-600 font-semibold mt-1">Pedidos</div>
                  </div>
                </div>
                <div class="group h-28 bg-gradient-to-br from-green-50 to-green-100 rounded-xl flex items-center justify-center hover:shadow-lg transition-all cursor-pointer border border-green-200">
                  <div class="text-center">
                    <div class="text-3xl font-bold text-green-600 group-hover:scale-110 transition-transform">45</div>
                    <div class="text-xs text-gray-600 font-semibold mt-1">Em Rota</div>
                  </div>
                </div>
                <div class="group h-28 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl flex items-center justify-center hover:shadow-lg transition-all cursor-pointer border border-purple-200">
                  <div class="text-center">
                    <div class="text-3xl font-bold text-purple-600 group-hover:scale-110 transition-transform">98%</div>
                    <div class="text-xs text-gray-600 font-semibold mt-1">SLA</div>
                  </div>
                </div>
              </div>
              
              <!-- List Items -->
              <div class="space-y-2">
                <div class="h-4 bg-gradient-to-r from-gray-200 to-gray-100 rounded-full w-full animate-pulse"></div>
                <div class="h-4 bg-gradient-to-r from-gray-200 to-gray-100 rounded-full w-5/6 animate-pulse" style="animation-delay: 0.1s"></div>
                <div class="h-4 bg-gradient-to-r from-gray-200 to-gray-100 rounded-full w-4/6 animate-pulse" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
          
          <!-- Decorative Dots -->
          <div class="absolute top-1/4 -left-4 w-2 h-2 bg-blue-500 rounded-full animate-ping"></div>
          <div class="absolute bottom-1/4 -right-4 w-2 h-2 bg-cyan-500 rounded-full animate-ping" style="animation-delay: 0.3s"></div>
        </div>
      </div>
      
      <!-- Stats Bar -->
      <div class="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
        <div>
          <div class="text-4xl font-bold text-blue-600 mb-2">500+</div>
          <div class="text-gray-600">Transportadoras</div>
        </div>
        <div>
          <div class="text-4xl font-bold text-blue-600 mb-2">50k+</div>
          <div class="text-gray-600">Entregas/Mês</div>
        </div>
        <div>
          <div class="text-4xl font-bold text-blue-600 mb-2">98%</div>
          <div class="text-gray-600">Satisfação</div>
        </div>
        <div>
          <div class="text-4xl font-bold text-blue-600 mb-2">24/7</div>
          <div class="text-gray-600">Suporte</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['request-demo'])

const openVideo = () => {
  // Pode ser um link do YouTube, Vimeo ou modal com vídeo
  window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '_blank')
  // Ou você pode implementar um modal de vídeo
}
</script>
