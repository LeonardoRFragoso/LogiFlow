<template>
  <div class="conversas-whatsapp-container">
    <div class="header">
      <h1>💬 Conversas WhatsApp</h1>
      <div class="header-actions">
        <button @click="carregarConversas" class="btn btn-secondary">
          <i class="icon-refresh"></i> Atualizar
        </button>
        <button @click="$router.push('/whatsapp/config')" class="btn btn-primary">
          <i class="icon-settings"></i> Configurações
        </button>
      </div>
    </div>

    <div class="layout">
      <div class="sidebar">
        <div class="filters">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchTerm" 
              @input="filtrarConversas"
              placeholder="Buscar conversa..."
              class="search-input"
            />
          </div>

          <div class="filter-tabs">
            <button 
              :class="['tab', { active: filtro === 'all' }]" 
              @click="filtro = 'all'; carregarConversas()"
            >
              Todas ({{ totalConversas }})
            </button>
            <button 
              :class="['tab', { active: filtro === 'unread' }]" 
              @click="filtro = 'unread'; carregarConversas()"
            >
              Não lidas ({{ naoLidas }})
            </button>
            <button 
              :class="['tab', { active: filtro === 'archived' }]" 
              @click="filtro = 'archived'; carregarConversas()"
            >
              Arquivadas
            </button>
          </div>
        </div>

        <div v-if="loadingConversas" class="loading-sidebar">
          <div class="spinner-small"></div>
          <p>Carregando...</p>
        </div>

        <div v-else-if="conversas.length === 0" class="empty-conversas">
          <p>Nenhuma conversa encontrada</p>
        </div>

        <div v-else class="conversas-list">
          <div 
            v-for="conversa in conversasFiltradas" 
            :key="conversa.id"
            :class="['conversa-item', { active: conversaSelecionada?.id === conversa.id, unread: conversa.unread_count > 0 }]"
            @click="selecionarConversa(conversa)"
          >
            <div class="conversa-avatar">
              {{ conversa.contact_name?.charAt(0) || '?' }}
            </div>
            <div class="conversa-info">
              <div class="conversa-header">
                <span class="conversa-nome">{{ conversa.contact_name || conversa.phone_number }}</span>
                <span class="conversa-hora">{{ formatarHora(conversa.last_message_at) }}</span>
              </div>
              <div class="conversa-preview">
                <span :class="['preview-text', { bot: conversa.last_message_direction === 'outbound' }]">
                  {{ conversa.last_message_direction === 'outbound' ? '✓ ' : '' }}
                  {{ conversa.last_message_content }}
                </span>
                <span v-if="conversa.unread_count > 0" class="unread-badge">
                  {{ conversa.unread_count }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-area">
        <div v-if="!conversaSelecionada" class="no-chat-selected">
          <div class="no-chat-icon">💬</div>
          <h3>Selecione uma conversa</h3>
          <p>Escolha uma conversa na lista à esquerda para visualizar as mensagens</p>
        </div>

        <div v-else class="chat-container">
          <div class="chat-header">
            <div class="chat-contact-info">
              <div class="contact-avatar">
                {{ conversaSelecionada.contact_name?.charAt(0) || '?' }}
              </div>
              <div class="contact-details">
                <h3>{{ conversaSelecionada.contact_name || conversaSelecionada.phone_number }}</h3>
                <p class="contact-phone">{{ conversaSelecionada.phone_number }}</p>
              </div>
            </div>
            <div class="chat-actions">
              <button @click="marcarComoLida" class="btn btn-sm btn-secondary" title="Marcar como lida">
                <i class="icon-check"></i>
              </button>
              <button @click="arquivarConversa" class="btn btn-sm btn-secondary" title="Arquivar">
                <i class="icon-archive"></i>
              </button>
              <button @click="verDetalhesCliente" class="btn btn-sm btn-primary" title="Ver cliente">
                <i class="icon-user"></i>
              </button>
            </div>
          </div>

          <div class="chat-messages" ref="messagesContainer">
            <div v-if="loadingMensagens" class="loading-messages">
              <div class="spinner-small"></div>
            </div>

            <div v-else class="messages-list">
              <div 
                v-for="msg in mensagens" 
                :key="msg.id"
                :class="['message', msg.direction]"
              >
                <div class="message-content">
                  <p>{{ msg.content }}</p>
                  <div v-if="msg.is_bot_message" class="bot-badge">
                    🤖 Bot
                  </div>
                  <div v-if="msg.bot_intent" class="intent-badge" :title="`Confiança: ${msg.bot_confidence}%`">
                    {{ formatarIntent(msg.bot_intent) }}
                  </div>
                </div>
                <div class="message-time">
                  {{ formatarDataHora(msg.timestamp) }}
                </div>
              </div>
            </div>
          </div>

          <div class="chat-input-area">
            <textarea 
              v-model="novaMensagem" 
              @keydown.enter.exact.prevent="enviarMensagem"
              placeholder="Digite sua mensagem..."
              rows="2"
              class="message-input"
            ></textarea>
            <button @click="enviarMensagem" :disabled="!novaMensagem.trim() || enviando" class="btn btn-primary send-btn">
              <i v-if="!enviando" class="icon-send"></i>
              <span v-else>...</span>
            </button>
          </div>
        </div>
      </div>

      <div class="details-panel" v-if="conversaSelecionada">
        <h3>📋 Detalhes</h3>
        
        <div class="detail-section">
          <label>Contato</label>
          <p>{{ conversaSelecionada.contact_name || 'Sem nome' }}</p>
        </div>

        <div class="detail-section">
          <label>Telefone</label>
          <p>{{ conversaSelecionada.phone_number }}</p>
        </div>

        <div class="detail-section">
          <label>Total de mensagens</label>
          <p>{{ conversaSelecionada.total_messages }}</p>
        </div>

        <div class="detail-section">
          <label>Categoria</label>
          <select v-model="conversaSelecionada.category" @change="atualizarCategoria" class="form-control">
            <option value="">Sem categoria</option>
            <option value="vendas">Vendas</option>
            <option value="suporte">Suporte</option>
            <option value="financeiro">Financeiro</option>
            <option value="operacional">Operacional</option>
          </select>
        </div>

        <div class="detail-section">
          <label>Tags</label>
          <div class="tags-list">
            <span v-for="tag in conversaSelecionada.tags" :key="tag" class="tag">
              {{ tag }}
            </span>
          </div>
          <button @click="adicionarTag" class="btn btn-sm btn-secondary">+ Tag</button>
        </div>

        <div class="detail-actions">
          <button @click="criarLead" class="btn btn-primary btn-block">
            <i class="icon-user-plus"></i> Criar Lead
          </button>
          <button @click="criarCaso" class="btn btn-secondary btn-block">
            <i class="icon-help"></i> Criar Caso
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const loadingConversas = ref(true)
const loadingMensagens = ref(false)
const enviando = ref(false)
const conversas = ref([])
const conversaSelecionada = ref(null)
const mensagens = ref([])
const novaMensagem = ref('')
const searchTerm = ref('')
const filtro = ref('all')
const totalConversas = ref(0)
const naoLidas = ref(0)
const messagesContainer = ref(null)

const conversasFiltradas = computed(() => {
  if (!searchTerm.value) return conversas.value
  
  const term = searchTerm.value.toLowerCase()
  return conversas.value.filter(c => 
    c.contact_name?.toLowerCase().includes(term) ||
    c.phone_number.includes(term) ||
    c.last_message_content?.toLowerCase().includes(term)
  )
})

async function carregarConversas() {
  loadingConversas.value = true
  try {
    const params = {
      unread_only: filtro.value === 'unread',
      archived: filtro.value === 'archived' ? true : null
    }

    const response = await api.get('/whatsapp/conversas', { params })
    conversas.value = response.data.data
    totalConversas.value = response.data.total
    
    naoLidas.value = conversas.value.filter(c => c.unread_count > 0).length
  } catch (error) {
    console.error('Erro ao carregar conversas:', error)
  } finally {
    loadingConversas.value = false
  }
}

async function selecionarConversa(conversa) {
  conversaSelecionada.value = conversa
  await carregarMensagens(conversa.id)
  
  if (conversa.unread_count > 0) {
    marcarComoLida()
  }
}

async function carregarMensagens(conversaId) {
  loadingMensagens.value = true
  try {
    const response = await api.get(`/whatsapp/conversas/${conversaId}/mensagens`)
    mensagens.value = response.data.data
    
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Erro ao carregar mensagens:', error)
  } finally {
    loadingMensagens.value = false
  }
}

async function enviarMensagem() {
  if (!novaMensagem.value.trim()) return
  
  enviando.value = true
  try {
    await api.post('/whatsapp/enviar/texto', {
      telefone: conversaSelecionada.value.phone_number,
      mensagem: novaMensagem.value
    })
    
    novaMensagem.value = ''
    await carregarMensagens(conversaSelecionada.value.id)
  } catch (error) {
    console.error('Erro ao enviar mensagem:', error)
    alert('Erro ao enviar mensagem')
  } finally {
    enviando.value = false
  }
}

async function marcarComoLida() {
  if (!conversaSelecionada.value) return
  
  try {
    await api.post(`/whatsapp/conversas/${conversaSelecionada.value.id}/marcar-lida`)
    conversaSelecionada.value.unread_count = 0
    await carregarConversas()
  } catch (error) {
    console.error('Erro ao marcar como lida:', error)
  }
}

async function arquivarConversa() {
  if (!conversaSelecionada.value) return
  
  try {
    await api.patch(`/whatsapp/conversas/${conversaSelecionada.value.id}/arquivar`, null, {
      params: { arquivar: true }
    })
    conversaSelecionada.value = null
    await carregarConversas()
  } catch (error) {
    console.error('Erro ao arquivar conversa:', error)
  }
}

function verDetalhesCliente() {
  if (conversaSelecionada.value?.cliente_id) {
    router.push(`/clientes/${conversaSelecionada.value.cliente_id}`)
  } else {
    alert('Esta conversa não está vinculada a um cliente')
  }
}

function criarLead() {
  alert('Funcionalidade de criar lead será implementada')
}

function criarCaso() {
  alert('Funcionalidade de criar caso será implementada')
}

function atualizarCategoria() {
  // Implementar atualização de categoria
}

function adicionarTag() {
  const tag = prompt('Digite a tag:')
  if (tag) {
    if (!conversaSelecionada.value.tags) {
      conversaSelecionada.value.tags = []
    }
    conversaSelecionada.value.tags.push(tag)
  }
}

function filtrarConversas() {
  // O filtro é feito pelo computed
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatarHora(data) {
  if (!data) return ''
  const d = new Date(data)
  const hoje = new Date()
  
  if (d.toDateString() === hoje.toDateString()) {
    return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  }
  
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
}

function formatarDataHora(data) {
  if (!data) return ''
  const d = new Date(data)
  return d.toLocaleString('pt-BR', { 
    day: '2-digit', 
    month: '2-digit', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

function formatarIntent(intent) {
  const intents = {
    rastreamento: '📦 Rastreamento',
    status_pedido: '📋 Status',
    prazo: '📅 Prazo',
    cancelamento: '❌ Cancelamento',
    duvida: '❓ Dúvida',
    saudacao: '👋 Saudação',
    agradecimento: '🙏 Obrigado',
    preco: '💰 Preço'
  }
  return intents[intent] || intent
}

onMounted(() => {
  carregarConversas()
})
</script>

<style scoped>
.conversas-whatsapp-container {
  height: calc(100vh - 80px);
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: white;
  border-bottom: 1px solid #e9ecef;
}

.header h1 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.layout {
  display: grid;
  grid-template-columns: 350px 1fr 300px;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background: white;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
}

.filters {
  padding: 15px;
  border-bottom: 1px solid #e9ecef;
}

.search-box {
  margin-bottom: 15px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
}

.filter-tabs {
  display: flex;
  gap: 5px;
}

.tab {
  flex: 1;
  padding: 8px;
  border: none;
  background: #f8f9fa;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.tab.active {
  background: #25D366;
  color: white;
}

.conversas-list {
  flex: 1;
  overflow-y: auto;
}

.conversa-item {
  display: flex;
  gap: 12px;
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s;
}

.conversa-item:hover {
  background: #f8f9fa;
}

.conversa-item.active {
  background: #e7f3ff;
}

.conversa-item.unread {
  background: #f0f8ff;
}

.conversa-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #25D366;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
  flex-shrink: 0;
}

.conversa-info {
  flex: 1;
  min-width: 0;
}

.conversa-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.conversa-nome {
  font-weight: 600;
  color: #333;
  font-size: 15px;
}

.conversa-hora {
  font-size: 12px;
  color: #999;
}

.conversa-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-text {
  flex: 1;
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-text.bot {
  color: #25D366;
}

.unread-badge {
  background: #25D366;
  color: white;
  border-radius: 10px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  margin-left: 8px;
}

.chat-area {
  display: flex;
  flex-direction: column;
  background: #e5ddd5;
}

.no-chat-selected {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-chat-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #f0f2f5;
  border-bottom: 1px solid #ddd;
}

.chat-contact-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.contact-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: #25D366;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
}

.contact-details h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.contact-phone {
  margin: 0;
  font-size: 13px;
  color: #666;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0icGF0dGVybiIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiPjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIiBmaWxsPSIjZTVkZGQ1Ii8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI3BhdHRlcm4pIi8+PC9zdmc+');
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 65%;
}

.message.inbound {
  align-self: flex-start;
}

.message.outbound {
  align-self: flex-end;
}

.message-content {
  padding: 8px 12px;
  border-radius: 8px;
  position: relative;
}

.message.inbound .message-content {
  background: white;
  border-radius: 8px 8px 8px 2px;
}

.message.outbound .message-content {
  background: #d9fdd3;
  border-radius: 8px 8px 2px 8px;
}

.message-content p {
  margin: 0;
  font-size: 14px;
  color: #333;
  word-wrap: break-word;
}

.bot-badge {
  display: inline-block;
  background: #25D366;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-top: 4px;
}

.intent-badge {
  display: inline-block;
  background: #007bff;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-top: 4px;
  margin-left: 4px;
}

.message-time {
  font-size: 11px;
  color: #667781;
  margin-top: 2px;
  padding: 0 8px;
}

.chat-input-area {
  display: flex;
  gap: 10px;
  padding: 15px;
  background: #f0f2f5;
  border-top: 1px solid #ddd;
}

.message-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
}

.send-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #25D366;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.details-panel {
  background: white;
  border-left: 1px solid #e9ecef;
  padding: 20px;
  overflow-y: auto;
}

.details-panel h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #666;
  margin-bottom: 5px;
}

.detail-section p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 10px;
}

.tag {
  background: #e9ecef;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 30px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
}

.btn-block {
  width: 100%;
}

.btn-primary {
  background: #25D366;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #25D366;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-sidebar,
.loading-messages,
.empty-conversas {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #999;
}
</style>
