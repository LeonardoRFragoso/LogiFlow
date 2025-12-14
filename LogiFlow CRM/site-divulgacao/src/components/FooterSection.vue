<template>
  <footer class="bg-gray-900 text-gray-300 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <div class="grid md:grid-cols-4 gap-8 mb-8">
        <!-- Logo e Descrição -->
        <div class="md:col-span-1">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">L</span>
            </div>
            <span class="text-2xl font-bold text-white">LogiFlow</span>
          </div>
          <p class="text-sm text-gray-400">
            O CRM completo para transportadoras brasileiras. Gestão, operação e fiscal em um só lugar.
          </p>
        </div>

        <!-- Produto -->
        <div>
          <h3 class="text-white font-bold mb-4">Produto</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="#funcionalidades" class="hover:text-white transition-colors">Funcionalidades</a></li>
            <li><a href="#precos" class="hover:text-white transition-colors">Preços</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Integrações</a></li>
            <li><a href="#" class="hover:text-white transition-colors">API</a></li>
          </ul>
        </div>

        <!-- Empresa -->
        <div>
          <h3 class="text-white font-bold mb-4">Empresa</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-white transition-colors">Sobre Nós</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Carreiras</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Contato</a></li>
          </ul>
        </div>

        <!-- Suporte -->
        <div>
          <h3 class="text-white font-bold mb-4">Suporte</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="#faq" class="hover:text-white transition-colors">FAQ</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Documentação</a></li>
            <li><a href="#" class="hover:text-white transition-colors">Status do Sistema</a></li>
            <li class="pt-2">
              <a href="mailto:contato@logiflow.com.br" class="text-blue-400 hover:text-blue-300">
                contato@logiflow.com.br
              </a>
            </li>
            <li>
              <a href="tel:+5521999999999" class="text-blue-400 hover:text-blue-300">
                (21) 99999-9999
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-sm text-gray-400">
          © 2024 LogiFlow CRM. Todos os direitos reservados.
        </p>
        <div class="flex gap-6 text-sm">
          <a href="#" class="hover:text-white transition-colors">Termos de Uso</a>
          <a href="#" class="hover:text-white transition-colors">Política de Privacidade</a>
          <a href="#" class="hover:text-white transition-colors">LGPD</a>
        </div>
      </div>
    </div>
  </footer>
</template>
