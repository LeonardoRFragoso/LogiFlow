<template>
  <BaseModal v-model="show" :title="isEdit ? '✏️ Editar Motorista' : '🧑‍✈️ Novo Motorista'" size="lg">
    <form @submit.prevent="handleSubmit" class="modal-form">
      <fieldset class="modal-fieldset">
        <legend>Dados Pessoais</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.nome" label="Nome Completo" required class="col-span-2" />
          <BaseInput v-model="form.cpf" label="CPF" required />
          <BaseInput v-model="form.rg" label="RG" />
          <BaseInput v-model="form.data_nascimento" label="Data Nascimento" type="date" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>CNH</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.cnh_numero" label="Número CNH" required />
          <BaseSelect v-model="form.cnh_categoria" label="Categoria" :options="categorias" required />
          <BaseInput v-model="form.cnh_validade" label="Validade" type="date" required />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Contato</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.telefone" label="Telefone" />
          <BaseInput v-model="form.celular" label="Celular" />
          <BaseInput v-model="form.email" label="E-mail" type="email" class="col-span-2" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Endereço</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.cep" label="CEP" />
          <BaseInput v-model="form.endereco" label="Endereço" class="col-span-2" />
          <BaseInput v-model="form.cidade" label="Cidade" />
          <BaseSelect v-model="form.uf" label="UF" :options="ufs" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Situação</legend>
        <div class="form-grid-2">
          <BaseSelect v-model="form.status" label="Status" :options="statusOptions" />
          <BaseInput v-model="form.data_admissao" label="Data Admissão" type="date" />
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

const props = defineProps({ modelValue: Boolean, motorista: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({ get: () => props.modelValue, set: (v) => emit('update:modelValue', v) })
const isEdit = computed(() => !!props.motorista?.id)
const { create, update, loading } = useCrud('/motoristas/')

const form = ref({})
const defaultForm = { nome: '', cpf: '', rg: '', data_nascimento: '', cnh_numero: '', cnh_categoria: 'E', cnh_validade: '', telefone: '', celular: '', email: '', cep: '', endereco: '', cidade: '', uf: '', status: 'ativo', data_admissao: '', observacoes: '' }

watch(() => props.modelValue, (v) => { if (v) form.value = props.motorista ? { ...props.motorista } : { ...defaultForm } })

const ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'].map(u => ({ value: u, label: u }))
const categorias = ['A', 'B', 'C', 'D', 'E', 'AB', 'AC', 'AD', 'AE'].map(c => ({ value: c, label: c }))
const statusOptions = [{ value: 'ativo', label: 'Ativo' }, { value: 'inativo', label: 'Inativo' }, { value: 'ferias', label: 'Férias' }, { value: 'afastado', label: 'Afastado' }]

async function handleSubmit() {
  try {
    if (isEdit.value) await update(props.motorista.id, form.value)
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
