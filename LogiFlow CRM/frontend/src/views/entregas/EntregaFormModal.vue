<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <h2>{{ entrega?.id ? '✏️ Editar Entrega' : '🚚 Nova Entrega' }}</h2>
          <button @click="close" class="btn-close">✕</button>
        </div>

        <form @submit.prevent="save" class="modal-body">
          <div class="form-grid">
            <!-- Cliente -->
            <div class="form-group full">
              <label>Cliente *</label>
              <select v-model="form.cliente_id" required class="form-input">
                <option value="">Selecione o cliente</option>
                <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nome }}</option>
              </select>
            </div>

            <!-- Pedido Vinculado -->
            <div class="form-group">
              <label>Pedido Vinculado</label>
              <select v-model="form.pedido_id" class="form-input">
                <option value="">Nenhum</option>
                <option v-for="p in pedidos" :key="p.id" :value="p.id">{{ p.numero }}</option>
              </select>
            </div>

            <!-- Motorista -->
            <div class="form-group">
              <label>Motorista</label>
              <select v-model="form.motorista_id" class="form-input">
                <option value="">Não atribuído</option>
                <option v-for="m in motoristas" :key="m.id" :value="m.id">{{ m.nome }}</option>
              </select>
            </div>

            <!-- Endereço -->
            <div class="form-group full">
              <label>Endereço de Entrega *</label>
              <input v-model="form.endereco_rua" type="text" required class="form-input" placeholder="Rua, número, complemento" />
            </div>

            <div class="form-group">
              <label>CEP</label>
              <input v-model="form.endereco_cep" type="text" class="form-input" placeholder="00000-000" @blur="buscarCep" />
            </div>

            <div class="form-group">
              <label>Bairro</label>
              <input v-model="form.endereco_bairro" type="text" class="form-input" />
            </div>

            <div class="form-group">
              <label>Cidade *</label>
              <input v-model="form.endereco_cidade" type="text" required class="form-input" />
            </div>

            <div class="form-group">
              <label>UF *</label>
              <select v-model="form.endereco_uf" required class="form-input">
                <option value="">UF</option>
                <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>

            <!-- Datas -->
            <div class="form-group">
              <label>Data Prevista *</label>
              <input v-model="form.previsao_entrega" type="datetime-local" required class="form-input" />
            </div>

            <div class="form-group">
              <label>Status</label>
              <select v-model="form.status" class="form-input">
                <option value="aguardando_coleta">Aguardando Coleta</option>
                <option value="coletado">Coletado</option>
                <option value="em_transito">Em Trânsito</option>
                <option value="saiu_para_entrega">Saiu para Entrega</option>
                <option value="entregue">Entregue</option>
                <option value="devolvido">Devolvido</option>
                <option value="cancelado">Cancelado</option>
              </select>
            </div>

            <!-- Volumes -->
            <div class="form-group">
              <label>Volumes</label>
              <input v-model.number="form.volumes" type="number" min="1" class="form-input" />
            </div>

            <div class="form-group">
              <label>Peso (kg)</label>
              <input v-model.number="form.peso" type="number" step="0.01" min="0" class="form-input" />
            </div>

            <!-- Valor -->
            <div class="form-group">
              <label>Valor da Mercadoria (R$)</label>
              <input v-model.number="form.valor_mercadoria" type="number" step="0.01" min="0" class="form-input" />
            </div>

            <div class="form-group">
              <label>Valor do Frete (R$)</label>
              <input v-model.number="form.valor_frete" type="number" step="0.01" min="0" class="form-input" />
            </div>

            <!-- Observações -->
            <div class="form-group full">
              <label>Observações</label>
              <textarea v-model="form.observacoes" class="form-input" rows="3" placeholder="Instruções especiais, referências..."></textarea>
            </div>

            <!-- Contato -->
            <div class="form-group">
              <label>Telefone do Destinatário</label>
              <input v-model="form.telefone_destinatario" type="tel" class="form-input" placeholder="(00) 00000-0000" />
            </div>

            <div class="form-group">
              <label>Nome do Destinatário</label>
              <input v-model="form.nome_destinatario" type="text" class="form-input" />
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" @click="close" class="btn-cancel">Cancelar</button>
            <button type="submit" class="btn-save" :disabled="saving">
              {{ saving ? 'Salvando...' : 'Salvar Entrega' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '@/services/api'

const props = defineProps({
  modelValue: Boolean,
  entrega: Object,
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = ref(getEmptyForm())
const saving = ref(false)
const clientes = ref([])
const pedidos = ref([])
const motoristas = ref([])

const ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

function getEmptyForm() {
  return {
    cliente_id: '',
    pedido_id: '',
    motorista_id: '',
    endereco_rua: '',
    endereco_cep: '',
    endereco_bairro: '',
    endereco_cidade: '',
    endereco_uf: '',
    previsao_entrega: '',
    status: 'aguardando_coleta',
    volumes: 1,
    peso: 0,
    valor_mercadoria: 0,
    valor_frete: 0,
    observacoes: '',
    telefone_destinatario: '',
    nome_destinatario: '',
  }
}

watch(() => props.modelValue, (val) => {
  if (val) {
    if (props.entrega) {
      form.value = { ...props.entrega }
      if (props.entrega.previsao_entrega) {
        form.value.previsao_entrega = new Date(props.entrega.previsao_entrega).toISOString().slice(0, 16)
      }
    } else {
      form.value = getEmptyForm()
    }
  }
})

async function fetchData() {
  try {
    const [cRes, pRes, mRes] = await Promise.all([
      api.get('/clientes/').catch(() => ({ data: [] })),
      api.get('/pedidos/').catch(() => ({ data: [] })),
      api.get('/motoristas/').catch(() => ({ data: [] })),
    ])
    clientes.value = cRes.data.results || cRes.data || []
    pedidos.value = pRes.data.results || pRes.data || []
    motoristas.value = mRes.data.results || mRes.data || []
  } catch (e) {
    console.error('Erro ao carregar dados:', e)
  }
}

async function buscarCep() {
  const cep = form.value.endereco_cep?.replace(/\D/g, '')
  if (cep?.length === 8) {
    try {
      const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
      const data = await res.json()
      if (!data.erro) {
        form.value.endereco_rua = data.logradouro || form.value.endereco_rua
        form.value.endereco_bairro = data.bairro || ''
        form.value.endereco_cidade = data.localidade || ''
        form.value.endereco_uf = data.uf || ''
      }
    } catch (e) {
      console.error('Erro ao buscar CEP:', e)
    }
  }
}

async function save() {
  saving.value = true
  try {
    if (props.entrega?.id) {
      await api.put(`/entregas/${props.entrega.id}/`, form.value)
    } else {
      await api.post('/entregas/', form.value)
    }
    emit('saved')
    close()
  } catch (e) {
    console.error('Erro ao salvar:', e)
    alert('Erro ao salvar entrega')
  } finally {
    saving.value = false
  }
}

function close() {
  emit('update:modelValue', false)
}

onMounted(fetchData)
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; backdrop-filter: blur(4px); }
.modal-container { background: white; border-radius: 1rem; width: 100%; max-width: 700px; max-height: 90vh; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.dark .modal-container { background: #1f2937; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 1.5rem; border-bottom: 1px solid #e5e7eb; }
.dark .modal-header { border-color: #374151; }
.modal-header h2 { font-size: 1.25rem; font-weight: 600; margin: 0; color: #1f2937; }
.dark .modal-header h2 { color: white; }
.btn-close { width: 32px; height: 32px; border-radius: 0.5rem; border: none; background: #f3f4f6; color: #6b7280; cursor: pointer; font-size: 1rem; transition: all 0.2s; }
.dark .btn-close { background: #374151; color: #9ca3af; }
.btn-close:hover { background: #e5e7eb; color: #1f2937; }
.dark .btn-close:hover { background: #4b5563; color: white; }
.modal-body { flex: 1; overflow-y: auto; padding: 1.5rem; }
.form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.form-group { display: flex; flex-direction: column; gap: 0.375rem; }
.form-group.full { grid-column: 1 / -1; }
.form-group label { font-size: 0.75rem; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em; }
.dark .form-group label { color: #9ca3af; }
.form-input { padding: 0.75rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 0.875rem; color: #1f2937; transition: all 0.2s; }
.dark .form-input { background: #374151; border-color: #4b5563; color: white; }
.form-input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
textarea.form-input { resize: vertical; min-height: 80px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 0.75rem; padding: 1.25rem 1.5rem; border-top: 1px solid #e5e7eb; background: #f9fafb; }
.dark .modal-footer { background: #111827; border-color: #374151; }
.btn-cancel { padding: 0.75rem 1.5rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; background: white; color: #374151; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.dark .btn-cancel { background: #374151; border-color: #4b5563; color: white; }
.btn-cancel:hover { background: #f3f4f6; }
.dark .btn-cancel:hover { background: #4b5563; }
.btn-save { padding: 0.75rem 1.5rem; border-radius: 0.5rem; border: none; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-save:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
