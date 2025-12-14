<template>
  <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 to-cyan-50">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          O que nossos clientes dizem
        </h2>
        <p class="text-xl text-gray-600">
          Transportadoras que já transformaram suas operações
        </p>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <div v-for="testimonial in testimonials" :key="testimonial.name" 
             class="p-8 bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all">
          <div class="flex items-center gap-1 mb-4">
            <svg v-for="i in 5" :key="i" class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </div>
          <p class="text-gray-700 mb-6 italic">"{{ testimonial.quote }}"</p>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
              {{ testimonial.name.charAt(0) }}
            </div>
            <div>
              <div class="font-bold text-gray-900">{{ testimonial.name }}</div>
              <div class="text-sm text-gray-600">{{ testimonial.role }}</div>
              <div class="text-sm text-gray-500">{{ testimonial.company }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const testimonials = [
  {
    name: 'Carlos Silva',
    role: 'Diretor Operacional',
    company: 'TransLog Transportes',
    quote: 'Reduzimos 60% do tempo gasto em gestão operacional. O LogiFlow é simplesmente incrível!'
  },
  {
    name: 'Maria Santos',
    role: 'CEO',
    company: 'Expresso Rápido',
    quote: 'Finalmente conseguimos ter controle total da operação. Melhor investimento que fizemos!'
  },
  {
    name: 'João Oliveira',
    role: 'Gerente de Logística',
    company: 'Carga Pesada Ltda',
    quote: 'Suporte excepcional e sistema muito fácil de usar. Recomendo para qualquer transportadora!'
  }
]
</script>
