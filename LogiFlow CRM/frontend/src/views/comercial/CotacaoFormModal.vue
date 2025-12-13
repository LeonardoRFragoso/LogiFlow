<template>
  <BaseModal v-model="show" :title="isEdit ? '✏️ Editar Cotação' : '💰 Nova Cotação'" size="lg">
    <form @submit.prevent="handleSubmit" class="modal-form">
      <BaseSelect v-model="form.cliente" label="Cliente" :options="clientesOptions" required />
      
      <fieldset class="modal-fieldset">
        <legend>Origem</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.origem_cidade" label="Cidade" required />
          <BaseSelect v-model="form.origem_uf" label="UF" :options="ufs" required />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Destino</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.destino_cidade" label="Cidade" required />
          <BaseSelect v-model="form.destino_uf" label="UF" :options="ufs" required />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Carga</legend>
        <div class="form-grid-2">
          <BaseSelect v-model="form.tipo_carga" label="Tipo de Carga" :options="tiposCarga" required />
          <BaseSelect v-model="form.modal" label="Modal" :options="modais" />
          <BaseInput v-model="form.peso_kg" label="Peso (kg)" type="number" step="0.01" required />
          <BaseInput v-model="form.cubagem_m3" label="Cubagem (m³)" type="number" step="0.001" />
          <BaseInput v-model="form.quantidade_volumes" label="Qtd. Volumes" type="number" />
          <BaseInput v-model="form.valor_mercadoria" label="Valor Mercadoria (R$)" type="number" step="0.01" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Valores e Prazo</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.prazo_estimado" label="Prazo (dias)" type="number" required />
          <BaseInput v-model="form.valor_frete" label="Valor Frete (R$)" type="number" step="0.01" required />
          <BaseInput v-model="form.valor_seguro" label="Seguro (R$)" type="number" step="0.01" />
          <BaseInput v-model="form.valor_adicional" label="Adicional (R$)" type="number" step="0.01" />
          <BaseInput v-model="form.validade" label="Validade" type="date" required class="col-span-2" />
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

const props = defineProps({ modelValue: Boolean, cotacao: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({ get: () => props.modelValue, set: (v) => emit('update:modelValue', v) })
const isEdit = computed(() => !!props.cotacao?.id)
const { create, update, loading } = useCrud('/cotacoes/')

const form = ref({})
const clientes = ref([])
const clientesOptions = computed(() => clientes.value.map(c => ({ value: c.id, label: c.nome_fantasia || c.razao_social })))

const defaultForm = {
  cliente: '',
  origem_cidade: '', origem_uf: '',
  destino_cidade: '', destino_uf: '',
  tipo_carga: 'geral', modal: 'rodoviario',
  peso_kg: '', cubagem_m3: '', quantidade_volumes: 1,
  valor_mercadoria: '', prazo_estimado: 5,
  valor_frete: '', valor_seguro: 0, valor_adicional: 0,
  validade: new Date(Date.now() + 15*24*60*60*1000).toISOString().split('T')[0],
  observacoes: ''
}

watch(() => props.modelValue, (v) => {
  if (v) {
    if (props.cotacao) {
      form.value = { ...props.cotacao }
      if (form.value.validade) form.value.validade = form.value.validade.split('T')[0]
    } else {
      form.value = { ...defaultForm }
    }
  }
})

onMounted(async () => {
  const res = await api.get('/clientes/')
  clientes.value = res.data.results || res.data
})

const ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'].map(u => ({ value: u, label: u }))
const tiposCarga = [
  { value: 'geral', label: 'Carga Geral' },
  { value: 'fracionada', label: 'Fracionada' },
  { value: 'lotacao', label: 'Lotação' },
  { value: 'refrigerada', label: 'Refrigerada' },
  { value: 'perigosa', label: 'Perigosa' },
]
const modais = [
  { value: 'rodoviario', label: 'Rodoviário' },
  { value: 'aereo', label: 'Aéreo' },
  { value: 'maritimo', label: 'Marítimo' },
]

async function handleSubmit() {
  try {
    const data = { ...form.value }
    if (isEdit.value) await update(props.cotacao.id, data)
    else await create(data)
    emit('saved')
    show.value = false
  } catch (e) {
    console.error('Erro ao salvar cotação:', e)
    alert('Erro ao salvar: ' + (e.response?.data?.detail || e.message))
  }
}
</script>

<style scoped>
.modal-form { display: flex; flex-direction: column; gap: 1rem; }
.modal-fieldset { border: 1px solid #4b5563; border-radius: 0.5rem; padding: 1rem 1.25rem; }
.modal-fieldset legend { padding: 0 0.5rem; font-weight: 600; font-size: 0.875rem; color: #374151; }
.dark .modal-fieldset legend { color: #e5e7eb; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.col-span-2 { grid-column: span 2; }
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
