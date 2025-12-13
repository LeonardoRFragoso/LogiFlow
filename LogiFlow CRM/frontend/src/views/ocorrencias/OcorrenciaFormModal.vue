<template>
  <BaseModal v-model="show" :title="isEdit ? '✏️ Editar Ocorrência' : '⚠️ Nova Ocorrência'" size="lg">
    <form @submit.prevent="handleSubmit" class="modal-form">
      <fieldset class="modal-fieldset">
        <legend>Identificação</legend>
        <div class="form-grid-2">
          <BaseSelect v-model="form.pedido" label="Pedido" :options="pedidosOptions" required class="col-span-2" />
          <BaseSelect v-model="form.tipo" label="Tipo" :options="tipos" required />
          <BaseSelect v-model="form.prioridade" label="Prioridade" :options="prioridades" required />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Descrição</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.titulo" label="Título" required class="col-span-2" />
          <div class="col-span-2">
            <label class="field-label">Descrição detalhada *</label>
            <textarea v-model="form.descricao" placeholder="Descreva a ocorrência..." class="modal-textarea" rows="3" required></textarea>
          </div>
          <BaseInput v-model="form.local" label="Local da Ocorrência" class="col-span-2" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Informações Adicionais</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.valor_prejuizo" label="Valor do Prejuízo (R$)" type="number" step="0.01" />
          <BaseInput v-model="form.numero_bo" label="Número B.O." />
        </div>
      </fieldset>
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

const props = defineProps({ modelValue: Boolean, ocorrencia: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({ get: () => props.modelValue, set: (v) => emit('update:modelValue', v) })
const isEdit = computed(() => !!props.ocorrencia?.id)
const { create, update, loading } = useCrud('/ocorrencias/')

const form = ref({})
const pedidos = ref([])
const pedidosOptions = computed(() => pedidos.value.map(p => ({ value: p.id, label: `${p.numero} - ${p.cliente_nome}` })))

const defaultForm = {
  pedido: '', tipo: 'atraso', prioridade: 'media',
  titulo: '', descricao: '', local: '',
  valor_prejuizo: '', numero_bo: ''
}

const tipos = [
  { value: 'atraso', label: 'Atraso' },
  { value: 'avaria', label: 'Avaria' },
  { value: 'extravio', label: 'Extravio' },
  { value: 'roubo', label: 'Roubo/Furto' },
  { value: 'acidente', label: 'Acidente' },
  { value: 'devolucao', label: 'Devolução' },
  { value: 'recusa', label: 'Recusa' },
  { value: 'outro', label: 'Outro' },
]

const prioridades = [
  { value: 'baixa', label: 'Baixa' },
  { value: 'media', label: 'Média' },
  { value: 'alta', label: 'Alta' },
  { value: 'critica', label: 'Crítica' },
]

watch(() => props.modelValue, (v) => {
  if (v) {
    form.value = props.ocorrencia ? { ...props.ocorrencia } : { ...defaultForm }
  }
})

onMounted(async () => {
  const res = await api.get('/pedidos/')
  pedidos.value = res.data.results || res.data
})

async function handleSubmit() {
  try {
    const data = { ...form.value }
    if (isEdit.value) await update(props.ocorrencia.id, data)
    else await create(data)
    emit('saved')
    show.value = false
  } catch (e) {
    console.error('Erro ao salvar ocorrência:', e)
    alert('Erro ao salvar: ' + (e.response?.data?.detail || JSON.stringify(e.response?.data) || e.message))
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
.field-label { display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.5rem; }
.dark .field-label { color: #d1d5db; }
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
