<template>
  <BaseModal v-model="show" :title="isEdit ? '✏️ Editar Cliente' : '👥 Novo Cliente'" size="lg">
    <form @submit.prevent="handleSubmit" class="modal-form">
      <fieldset class="modal-fieldset">
        <legend>Dados da Empresa</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.razao_social" label="Razão Social" required class="col-span-2" />
          <BaseInput v-model="form.nome_fantasia" label="Nome Fantasia" />
          <BaseInput v-model="form.cnpj" label="CNPJ" required placeholder="00.000.000/0000-00" />
          <BaseInput v-model="form.inscricao_estadual" label="Inscrição Estadual" />
          <BaseInput v-model="form.contato_nome" label="Contato Principal" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Contato</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.email" label="E-mail" type="email" placeholder="email@empresa.com" />
          <BaseInput v-model="form.telefone" label="Telefone" placeholder="(00) 0000-0000" />
          <BaseInput v-model="form.celular" label="Celular" placeholder="(00) 00000-0000" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Endereço</legend>
        <div class="form-grid-2">
          <BaseInput v-model="form.cep" label="CEP" placeholder="00000-000" />
          <BaseInput v-model="form.logradouro" label="Logradouro" class="col-span-2" />
          <BaseInput v-model="form.numero" label="Número" />
          <BaseInput v-model="form.complemento" label="Complemento" />
          <BaseInput v-model="form.bairro" label="Bairro" />
          <BaseInput v-model="form.cidade" label="Cidade" />
          <BaseSelect v-model="form.uf" label="UF" :options="ufs" />
        </div>
      </fieldset>

      <fieldset class="modal-fieldset">
        <legend>Comercial</legend>
        <div class="form-grid-2">
          <BaseSelect v-model="form.condicao_pagamento" label="Condição de Pagamento" :options="condicoes" />
          <BaseInput v-model="form.limite_credito" label="Limite de Crédito (R$)" type="number" placeholder="0,00" />
          <div class="col-span-2">
            <label class="field-label">Observações</label>
            <textarea v-model="form.observacoes" placeholder="Informações adicionais sobre o cliente..." class="modal-textarea" rows="3"></textarea>
          </div>
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
import { ref, watch, computed } from 'vue'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { useCrud } from '@/composables/useCrud'

const props = defineProps({ modelValue: Boolean, cliente: Object })
const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({ get: () => props.modelValue, set: (v) => emit('update:modelValue', v) })
const isEdit = computed(() => !!props.cliente?.id)
const { create, update, loading } = useCrud('/clientes/')

const form = ref({})
const defaultForm = { razao_social: '', nome_fantasia: '', cnpj: '', inscricao_estadual: '', contato_nome: '', email: '', telefone: '', celular: '', cep: '', logradouro: '', numero: '', complemento: '', bairro: '', cidade: '', uf: '', condicao_pagamento: '30_dias', limite_credito: '', observacoes: '' }

watch(() => props.modelValue, (v) => { if (v) form.value = props.cliente ? { ...props.cliente } : { ...defaultForm } })

const ufs = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'].map(u => ({ value: u, label: u }))
const condicoes = [{ value: 'a_vista', label: 'À Vista' }, { value: '7_dias', label: '7 dias' }, { value: '14_dias', label: '14 dias' }, { value: '21_dias', label: '21 dias' }, { value: '28_dias', label: '28 dias' }, { value: '30_dias', label: '30 dias' }, { value: '45_dias', label: '45 dias' }, { value: '60_dias', label: '60 dias' }]

async function handleSubmit() {
  try {
    if (isEdit.value) await update(props.cliente.id, form.value)
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
