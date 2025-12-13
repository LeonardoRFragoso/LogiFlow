<template>
  <BaseModal v-model="show" :title="isEdit ? '✏️ Editar Veículo' : '🚚 Novo Veículo'" size="lg">
    <form @submit.prevent="handleSubmit" class="modal-form">
      <fieldset class="modal-fieldset">
        <legend>Identificação</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.placa" label="Placa" required />
          <BaseSelect v-model="form.tipo" label="Tipo" :options="tipos" required />
          <BaseInput v-model="form.renavam" label="RENAVAM" />
          <BaseInput v-model="form.chassi" label="Chassi" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Características</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.marca" label="Marca" />
          <BaseInput v-model="form.modelo" label="Modelo" />
          <BaseInput v-model="form.ano_fabricacao" label="Ano Fabricação" type="number" />
          <BaseInput v-model="form.ano_modelo" label="Ano Modelo" type="number" />
          <BaseInput v-model="form.cor" label="Cor" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Capacidade</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.capacidade_kg" label="Capacidade (kg)" type="number" />
          <BaseInput v-model="form.capacidade_m3" label="Capacidade (m³)" type="number" />
          <BaseInput v-model="form.km_atual" label="KM Atual" type="number" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Propriedade e Documentação</legend>
        <div class="form-grid-2">
          <BaseSelect v-model="form.propriedade" label="Propriedade" :options="propriedades" />
          <BaseInput v-model="form.proprietario_nome" label="Proprietário" />
          <BaseInput v-model="form.licenciamento_validade" label="Licenciamento" type="date" />
          <BaseInput v-model="form.seguro_validade" label="Seguro Validade" type="date" />
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
import { ref, watch, computed } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { useCrud } from '@/composables/useCrud'

const props = defineProps({ modelValue: Boolean, veiculo: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({ get: () => props.modelValue, set: (v) => emit('update:modelValue', v) })
const isEdit = computed(() => !!props.veiculo?.id)
const { create, update, loading } = useCrud('/veiculos/')

const form = ref({})
const defaultForm = { placa: '', tipo: 'truck', renavam: '', chassi: '', marca: '', modelo: '', ano_fabricacao: '', ano_modelo: '', cor: '', capacidade_kg: '', capacidade_m3: '', km_atual: 0, propriedade: 'proprio', proprietario_nome: '', licenciamento_validade: '', seguro_validade: '', observacoes: '' }

watch(() => props.modelValue, (v) => { if (v) form.value = props.veiculo ? { ...props.veiculo } : { ...defaultForm } })

const tipos = [{ value: 'moto', label: 'Moto' }, { value: 'fiorino', label: 'Fiorino' }, { value: 'van', label: 'Van' }, { value: 'vuc', label: 'VUC' }, { value: 'toco', label: 'Toco' }, { value: 'truck', label: 'Truck' }, { value: 'carreta', label: 'Carreta' }, { value: 'bitrem', label: 'Bitrem' }]
const propriedades = [{ value: 'proprio', label: 'Próprio' }, { value: 'terceiro', label: 'Terceiro' }, { value: 'agregado', label: 'Agregado' }, { value: 'alugado', label: 'Alugado' }]

async function handleSubmit() {
  try {
    if (isEdit.value) await update(props.veiculo.id, form.value)
    else await create(form.value)
    emit('saved')
    show.value = false
  } catch (e) { console.error(e) }
}
</script>

<style scoped>
.modal-form { display: flex; flex-direction: column; gap: 1rem; }
.modal-fieldset { border: 1px solid #4b5563; border-radius: 0.5rem; padding: 1rem 1.25rem; }
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
