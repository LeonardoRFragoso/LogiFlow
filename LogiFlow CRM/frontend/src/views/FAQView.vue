<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">❓ FAQ - Perguntas Frequentes</h1>
        <p class="page-subtitle">Encontre respostas rápidas para suas dúvidas</p>
      </div>
      <button @click="startTour" class="btn-tour">
        🎯 Iniciar Tour Guiado
      </button>
    </div>

    <div class="search-box">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Buscar perguntas..."
        class="search-input"
      />
      <span class="search-icon">🔍</span>
    </div>

    <div class="faq-categories">
      <button 
        v-for="cat in categories" 
        :key="cat.id"
        @click="selectedCategory = cat.id"
        :class="['category-btn', selectedCategory === cat.id && 'active']"
      >
        {{ cat.icon }} {{ cat.name }}
      </button>
    </div>

    <div class="faq-list">
      <div v-for="(item, index) in filteredFAQ" :key="index" class="faq-item">
        <button @click="toggleItem(index)" class="faq-question">
          <span>{{ item.question }}</span>
          <span class="faq-icon">{{ expandedItems.includes(index) ? '−' : '+' }}</span>
        </button>
        <transition name="expand">
          <div v-if="expandedItems.includes(index)" class="faq-answer">
            <p v-html="item.answer"></p>
            <div v-if="item.links" class="faq-links">
              <a v-for="link in item.links" :key="link.url" :href="link.url" class="faq-link">
                {{ link.text }} →
              </a>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <div v-if="filteredFAQ.length === 0" class="empty-state">
      <span class="empty-icon">🔍</span>
      <h3>Nenhuma pergunta encontrada</h3>
      <p>Tente buscar com outras palavras-chave</p>
    </div>

    <div class="help-card">
      <h3>Ainda precisa de ajuda?</h3>
      <p>Entre em contato com nosso suporte técnico</p>
      <div class="help-actions">
        <a href="mailto:suporte@logiflow.com" class="btn-help">📧 Email</a>
        <a href="https://wa.me/5521999999999" class="btn-help">💬 WhatsApp</a>
        <button @click="downloadGuide" class="btn-help">📄 Baixar Guia</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedCategory = ref('all')
const expandedItems = ref([])

const categories = [
  { id: 'all', name: 'Todas', icon: '📋' },
  { id: 'pedidos', name: 'Pedidos', icon: '📦' },
  { id: 'motoristas', name: 'Motoristas', icon: '🚛' },
  { id: 'ocorrencias', name: 'Ocorrências', icon: '⚠️' },
  { id: 'sistema', name: 'Sistema', icon: '⚙️' }
]

const faqData = [
  {
    category: 'pedidos',
    question: 'Como criar um novo pedido de frete?',
    answer: `
      <strong>Passo a passo:</strong><br>
      1. Acesse o menu "Pedidos" na barra lateral<br>
      2. Clique no botão "+ Novo Pedido"<br>
      3. Preencha os dados do cliente e endereços de origem/destino<br>
      4. Adicione os itens da carga (peso, volume, valor)<br>
      5. Defina o tipo de frete (CIF ou FOB)<br>
      6. Revise os valores e clique em "Criar Pedido"<br><br>
      <em>Dica: Você pode criar um pedido a partir de uma cotação aprovada!</em>
    `
  },
  {
    category: 'pedidos',
    question: 'Como atribuir um motorista a um pedido?',
    answer: `
      Existem duas formas:<br><br>
      <strong>1. Durante a criação do pedido:</strong><br>
      - Selecione o motorista e veículo nos campos correspondentes<br><br>
      <strong>2. Após a criação:</strong><br>
      - Abra o pedido<br>
      - Clique em "Atribuir Motorista"<br>
      - Selecione o motorista disponível<br>
      - Confirme a atribuição<br><br>
      O motorista receberá uma notificação automaticamente.
    `
  },
  {
    category: 'pedidos',
    question: 'O que significam os status dos pedidos?',
    answer: `
      <strong>Aguardando Confirmação:</strong> Pedido criado, aguardando aprovação<br>
      <strong>Confirmado:</strong> Pedido aprovado, pronto para coleta<br>
      <strong>Aguardando Coleta:</strong> Motorista atribuído, aguardando coleta<br>
      <strong>Em Coleta:</strong> Motorista a caminho do local de coleta<br>
      <strong>Coletado:</strong> Carga coletada com sucesso<br>
      <strong>Em Trânsito:</strong> Carga em transporte<br>
      <strong>Em Rota de Entrega:</strong> Motorista a caminho do destino<br>
      <strong>Entregue:</strong> Entrega concluída com sucesso<br>
      <strong>Cancelado:</strong> Pedido cancelado
    `
  },
  {
    category: 'pedidos',
    question: 'Como acompanhar um pedido em tempo real?',
    answer: `
      1. Acesse a lista de pedidos<br>
      2. Clique no pedido desejado<br>
      3. Na tela de detalhes, você verá:<br>
      - Status atual da entrega<br>
      - Localização do motorista (se disponível)<br>
      - Histórico de movimentações<br>
      - Previsão de entrega<br><br>
      Você também pode compartilhar o link de rastreamento com o cliente.
    `
  },
  {
    category: 'motoristas',
    question: 'Como cadastrar um novo motorista?',
    answer: `
      1. Vá em "Motoristas" no menu<br>
      2. Clique em "+ Novo Motorista"<br>
      3. Preencha os dados pessoais (nome, CPF, telefone)<br>
      4. Adicione os dados da CNH (número, categoria, validade)<br>
      5. Faça upload da foto e documentos<br>
      6. Defina o status inicial (disponível/indisponível)<br>
      7. Salve o cadastro<br><br>
      <em>Importante: Verifique sempre a validade da CNH!</em>
    `
  },
  {
    category: 'motoristas',
    question: 'Como verificar a disponibilidade dos motoristas?',
    answer: `
      Na tela de "Motoristas", você pode:<br><br>
      - Ver o status de cada motorista (disponível, em rota, indisponível)<br>
      - Filtrar apenas motoristas disponíveis<br>
      - Ver quantas entregas cada um tem no dia<br>
      - Verificar a localização atual (se em rota)<br><br>
      Use os filtros para encontrar rapidamente o motorista ideal para cada pedido.
    `
  },
  {
    category: 'motoristas',
    question: 'Como funciona a avaliação dos motoristas?',
    answer: `
      O sistema avalia automaticamente os motoristas com base em:<br><br>
      - Taxa de entregas no prazo<br>
      - Número de ocorrências registradas<br>
      - Feedback dos clientes<br>
      - Tempo médio de entrega<br><br>
      A avaliação é exibida em estrelas (1 a 5) e pode ser vista no perfil do motorista.
    `
  },
  {
    category: 'ocorrencias',
    question: 'Quando devo registrar uma ocorrência?',
    answer: `
      Registre uma ocorrência sempre que houver:<br><br>
      ⏰ <strong>Atraso:</strong> Entrega fora do prazo previsto<br>
      📦 <strong>Avaria:</strong> Dano à mercadoria<br>
      ❌ <strong>Extravio:</strong> Carga perdida ou não localizada<br>
      🚫 <strong>Recusa:</strong> Cliente recusou receber<br>
      🚗 <strong>Acidente:</strong> Acidente com o veículo<br>
      🔒 <strong>Roubo:</strong> Roubo de carga<br><br>
      Quanto mais rápido registrar, melhor para resolver o problema!
    `
  },
  {
    category: 'ocorrencias',
    question: 'Como resolver uma ocorrência?',
    answer: `
      1. Acesse "Ocorrências" no menu<br>
      2. Clique na ocorrência que deseja resolver<br>
      3. Analise os detalhes e comentários<br>
      4. Tome as ações necessárias<br>
      5. Clique em "Resolver Ocorrência"<br>
      6. Descreva a solução aplicada<br>
      7. Confirme a resolução<br><br>
      A ocorrência será marcada como resolvida e o histórico será mantido.
    `
  },
  {
    category: 'ocorrencias',
    question: 'O que são as prioridades de ocorrências?',
    answer: `
      As ocorrências são classificadas em 4 níveis:<br><br>
      🔴 <strong>Crítica:</strong> Requer ação imediata (roubo, acidente grave)<br>
      🟠 <strong>Alta:</strong> Problema sério que afeta a entrega (extravio, avaria grande)<br>
      🟡 <strong>Média:</strong> Problema moderado (atraso, recusa)<br>
      🟢 <strong>Baixa:</strong> Problema menor (documentação, endereço)<br><br>
      O sistema ordena automaticamente por prioridade.
    `
  },
  {
    category: 'sistema',
    question: 'Como alterar minha senha?',
    answer: `
      1. Clique no seu avatar no canto superior direito<br>
      2. Selecione "Configurações"<br>
      3. Vá na aba "Segurança"<br>
      4. Clique em "Alterar Senha"<br>
      5. Digite a senha atual<br>
      6. Digite a nova senha (mínimo 8 caracteres)<br>
      7. Confirme a nova senha<br>
      8. Salve as alterações
    `
  },
  {
    category: 'sistema',
    question: 'Como ativar o tema escuro?',
    answer: `
      1. Clique no ícone de sol/lua no canto superior direito<br>
      2. O tema será alternado automaticamente<br><br>
      Ou:<br>
      1. Vá em "Configurações"<br>
      2. Aba "Aparência"<br>
      3. Selecione "Tema Escuro"<br><br>
      Sua preferência será salva automaticamente.
    `
  },
  {
    category: 'sistema',
    question: 'Como exportar relatórios?',
    answer: `
      1. Acesse a seção desejada (Pedidos, Entregas, etc.)<br>
      2. Aplique os filtros necessários<br>
      3. Clique no botão "Exportar"<br>
      4. Escolha o formato (Excel, PDF, CSV)<br>
      5. O download iniciará automaticamente<br><br>
      Os relatórios incluem todos os dados visíveis na tela com os filtros aplicados.
    `
  },
  {
    category: 'sistema',
    question: 'Como funciona o sistema de notificações?',
    answer: `
      Você recebe notificações sobre:<br><br>
      - Novos pedidos criados<br>
      - Mudanças de status nas entregas<br>
      - Ocorrências registradas<br>
      - Mensagens de motoristas<br>
      - Alertas de SLA<br><br>
      Configure suas preferências em "Configurações > Notificações"
    `
  },
  {
    category: 'sistema',
    question: 'O sistema funciona offline?',
    answer: `
      <strong>Sistema Web:</strong> Requer conexão com internet<br><br>
      <strong>App do Motorista:</strong> Funciona parcialmente offline:<br>
      - Visualizar entregas já carregadas<br>
      - Registrar ocorrências (sincroniza depois)<br>
      - Tirar fotos de comprovantes<br><br>
      Quando a conexão retornar, os dados serão sincronizados automaticamente.
    `
  }
]

const filteredFAQ = computed(() => {
  let filtered = faqData

  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(item => item.category === selectedCategory.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(item => 
      item.question.toLowerCase().includes(query) ||
      item.answer.toLowerCase().includes(query)
    )
  }

  return filtered
})

function toggleItem(index) {
  const idx = expandedItems.value.indexOf(index)
  if (idx > -1) {
    expandedItems.value.splice(idx, 1)
  } else {
    expandedItems.value.push(index)
  }
}

function startTour() {
  // Implementar integração com TourGuide
  alert('Tour guiado será iniciado!')
}

function downloadGuide() {
  window.open('/guia-completo-logiflow.pdf', '_blank')
}
</script>

<style scoped>
.page-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; }
.page-title { font-size: 2rem; font-weight: 700; color: #1f2937; margin: 0; }
.dark .page-title { color: white; }
.page-subtitle { color: #6b7280; font-size: 1rem; margin-top: 0.5rem; }
.dark .page-subtitle { color: #9ca3af; }

.btn-tour {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}

.btn-tour:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
}

.search-box {
  position: relative;
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 1rem 3rem 1rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.dark .search-input {
  background: #1f2937;
  border-color: #374151;
  color: white;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
}

.faq-categories {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.category-btn {
  padding: 0.625rem 1.25rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: #4b5563;
}

.category-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.category-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.dark .category-btn {
  background: #1f2937;
  border-color: #374151;
  color: #9ca3af;
}

.dark .category-btn.active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.faq-item {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.2s;
}

.faq-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dark .faq-item {
  background: #1f2937;
}

.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: none;
  border: none;
  text-align: left;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  cursor: pointer;
  transition: all 0.2s;
}

.faq-question:hover {
  background: #f9fafb;
}

.dark .faq-question {
  color: white;
}

.dark .faq-question:hover {
  background: #111827;
}

.faq-icon {
  font-size: 1.5rem;
  color: #3b82f6;
  font-weight: 300;
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  color: #4b5563;
  line-height: 1.8;
}

.dark .faq-answer {
  color: #d1d5db;
}

.faq-links {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.faq-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.faq-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.expand-enter-active, .expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from, .expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.expand-enter-to, .expand-leave-from {
  opacity: 1;
  max-height: 1000px;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  display: block;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.5rem;
}

.dark .empty-state h3 {
  color: #e5e7eb;
}

.empty-state p {
  color: #9ca3af;
}

.help-card {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
}

.help-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

.help-card p {
  margin: 0 0 1.5rem;
  opacity: 0.9;
}

.help-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-help {
  padding: 0.75rem 1.5rem;
  background: white;
  color: #3b82f6;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-help:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>
