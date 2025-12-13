<template>
  <BaseModal v-model="show" :title="isEdit ? '✏️ Editar Pedido' : '📦 Novo Pedido'" size="lg">
    <form @submit.prevent="handleSubmit" class="modal-form">
      <BaseSelect v-model="form.cliente" label="Cliente" :options="clientesOptions" required />
      
      <fieldset class="modal-fieldset">
        <legend>Origem</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.origem_endereco" label="Endereço" required />
          <BaseInput v-model="form.origem_cidade" label="Cidade" required />
          <BaseSelect v-model="form.origem_uf" label="UF" :options="ufs" required />
          <BaseInput v-model="form.remetente_nome" label="Remetente" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Destino</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.destino_endereco" label="Endereço" required />
          <BaseInput v-model="form.destino_cidade" label="Cidade" required />
          <BaseSelect v-model="form.destino_uf" label="UF" :options="ufs" required />
          <BaseInput v-model="form.destinatario_nome" label="Destinatário" required />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Carga e Valores</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.tipo_carga" label="Tipo de Carga" required />
          <BaseInput v-model="form.peso_kg" label="Peso (kg)" type="number" step="0.01" required />
          <BaseInput v-model="form.quantidade_volumes" label="Qtd. Volumes" type="number" />
          <BaseInput v-model="form.valor_frete" label="Valor Frete (R$)" type="number" step="0.01" required />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Operacional</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.previsao_entrega" label="Previsão Entrega" type="date" required />
          <BaseSelect v-model="form.motorista" label="Motorista" :options="motoristasOptions" />
          <BaseSelect v-model="form.veiculo" label="Veículo" :options="veiculosOptions" />
        </div>
      </fieldset>

      <textarea v-model="form.observacoes" placeholder="Observações" class="modal-textarea" rows="2"></textarea>
    </form>
    <template #footer>
      <div class="modal-footer-actions">
        <button type="button" @click="show = false" class="modal-btn-cancel">Cancelar</button>
        <button @click="handleSubmit" :disabled="loading" class="modal-btn-save">
          <span v-if="loading" class="modal-spinner"></span>
          {{ loading ? 'Salvando...' : 'Salvar' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { useCrud } from '@/composables/useCrud'
import api from '@/services/api'

const props = defineProps({ modelValue: Boolean, pedido: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({ get: () => props.modelValue, set: (v) => emit('update:modelValue', v) })
const isEdit = computed(() => !!props.pedido?.id)
const { create, update, loading } = useCrud('/pedidos/')

const form = ref({})
const clientes = ref([])
const motoristas = ref([])
const veiculos = ref([])

const clientesOptions = computed(() => clientes.value.map(c => ({ value: c.id, label: c.nome_fantasia || c.razao_social })))
const motoristasOptions = computed(() => [{ value: '', label: 'Selecione...' }, ...motoristas.value.map(m => ({ value: m.id, label: m.nome }))])
const veiculosOptions = computed(() => [{ value: '', label: 'Selecione...' }, ...veiculos.value.map(v => ({ value: v.id, label: v.placa }))])

const defaultForm = {
  cliente: '',
  origem_endereco: '', origem_cidade: '', origem_uf: '', remetente_nome: '',
  destino_endereco: '', destino_cidade: '', destino_uf: '', destinatario_nome: '',
  tipo_carga: 'geral', peso_kg: '', quantidade_volumes: 1,
  valor_frete: '', previsao_entrega: '',
  motorista: '', veiculo: '', observacoes: ''
}

watch(() => props.modelValue, (v) => {
  if (v) {
    if (props.pedido) {
      form.value = { ...props.pedido }
      if (form.value.previsao_entrega) form.value.previsao_entrega = form.value.previsao_entrega.split('T')[0]
    } else {
      form.value = { ...defaultForm }
    }
  }
})

onMounted(async () => {
  const [c, m, v] = await Promise.all([
    api.get('/clientes/'),
    api.get('/motoristas/'),
    api.get('/veiculos/')
  ])
  clientes.value = c.data.results || c.data
  motoristas.value = m.data.results || m.data
  veiculos.value = v.data.results || v.data
})

const ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'].map(u => ({ value: u, label: u }))

async function handleSubmit() {
  try {
    const data = { ...form.value }
    if (!data.motorista) delete data.motorista
    if (!data.veiculo) delete data.veiculo
    if (isEdit.value) await update(props.pedido.id, data)
    else await create(data)
    emit('saved')
    show.value = false
  } catch (e) {
    console.error('Erro ao salvar pedido:', e)
    alert('Erro ao salvar: ' + (e.response?.data?.detail || JSON.stringify(e.response?.data) || e.message))
  }
}
</script>

<style scoped>
.modal-form { display: flex; flex-direction: column; gap: 1rem; }
.modal-fieldset { border: 1px solid #4b5563; border-radius: 0.5rem; padding: 1rem 1.25rem; }
.dark .modal-fieldset { border-color: #4b5563; }
.modal-fieldset legend { padding: 0 0.5rem; font-weight: 600; font-size: 0.875rem; color: #374151; }
.dark .modal-fieldset legend { color: #e5e7eb; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.modal-textarea { width: 100%; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 0.9rem; resize: vertical; background: white; color: #1f2937; }
.dark .modal-textarea { background: #1f2937; border-color: #374151; color: #e5e7eb; }
.modal-textarea:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); }
.modal-footer-actions { display: flex; justify-content: flex-end; gap: 0.75rem; }
.modal-btn-cancel { padding: 0.75rem 1.5rem; background: #f3f4f6; color: #374151; border: none; border-radius: 0.5rem; font-weight: 500; cursor: pointer; }
.dark .modal-btn-cancel { background: #374151; color: #e5e7eb; }
.modal-btn-save { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer; }
.modal-btn-save:disabled { opacity: 0.7; cursor: not-allowed; }
.modal-spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
