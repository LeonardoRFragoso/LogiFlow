<template>
  <div class="form-group">
    <label v-if="label" :for="inputId" class="form-label">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <input
        :id="inputId"
        :type="type"
        :value="displayValue"
        @input="handleInput"
        @blur="handleBlur"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :class="[
          'form-input',
          { 'border-red-500': hasError },
          { 'border-green-500': isValid && showValidation }
        ]"
      />
      <div v-if="showValidation && hasError" class="absolute right-3 top-1/2 -translate-y-1/2">
        <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
      </div>
      <div v-if="showValidation && isValid" class="absolute right-3 top-1/2 -translate-y-1/2">
        <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
      </div>
    </div>
    <p v-if="hasError && errorMessage" class="mt-1 text-sm text-red-500">
      {{ errorMessage }}
    </p>
    <p v-if="hint && !hasError" class="mt-1 text-sm text-gray-500">
      {{ hint }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useValidation } from '@/composables/useValidation'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  type: { type: String, default: 'text' },
  mask: { 
    type: String, 
    default: null,
    validator: (v) => ['cpf', 'cnpj', 'cep', 'phone', 'placa', 'money', null].includes(v)
  },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  hint: { type: String, default: '' },
  showValidation: { type: Boolean, default: true }
})

const emit = defineEmits(['update:modelValue', 'valid', 'invalid'])

const { 
  maskCPF, maskCNPJ, maskCEP, maskPhone, maskPlaca, maskMoney,
  validateCPF, validateCNPJ, validateCEP, validatePlaca, unmask
} = useValidation()

const inputId = `input-${Math.random().toString(36).substr(2, 9)}`
const touched = ref(false)
const errorMessage = ref('')

// Aplica máscara ao valor
const displayValue = computed(() => {
  const value = props.modelValue?.toString() || ''
  
  switch (props.mask) {
    case 'cpf': return maskCPF(value)
    case 'cnpj': return maskCNPJ(value)
    case 'cep': return maskCEP(value)
    case 'phone': return maskPhone(value)
    case 'placa': return maskPlaca(value)
    case 'money': return maskMoney(value)
    default: return value
  }
})

// Valida o valor
const isValid = computed(() => {
  const value = props.modelValue?.toString() || ''
  if (!value && !props.required) return true
  if (!value && props.required) return false
  
  switch (props.mask) {
    case 'cpf': return validateCPF(value)
    case 'cnpj': return validateCNPJ(value)
    case 'cep': return validateCEP(value)
    case 'placa': return validatePlaca(value)
    default: return true
  }
})

const hasError = computed(() => {
  return touched.value && !isValid.value
})

// Mensagens de erro por tipo de máscara
const getErrorMessage = () => {
  if (!props.modelValue && props.required) {
    return 'Campo obrigatório'
  }
  
  switch (props.mask) {
    case 'cpf': return 'CPF inválido'
    case 'cnpj': return 'CNPJ inválido'
    case 'cep': return 'CEP inválido'
    case 'placa': return 'Placa inválida'
    default: return 'Valor inválido'
  }
}

const handleInput = (event) => {
  let value = event.target.value
  
  // Para máscaras, emite o valor sem máscara
  if (props.mask && props.mask !== 'money') {
    value = unmask(value)
  }
  
  emit('update:modelValue', value)
}

const handleBlur = () => {
  touched.value = true
  errorMessage.value = getErrorMessage()
  
  if (isValid.value) {
    emit('valid', props.modelValue)
  } else {
    emit('invalid', props.modelValue)
  }
}

// Observa mudanças no valor para validação em tempo real
watch(() => props.modelValue, () => {
  if (touched.value) {
    errorMessage.value = getErrorMessage()
  }
})
</script>

<style scoped>
.form-group {
  @apply mb-4;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm 
         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
         disabled:bg-gray-100 disabled:cursor-not-allowed
         transition-colors duration-200;
}

.form-input.border-red-500 {
  @apply border-red-500 focus:ring-red-500 focus:border-red-500;
}

.form-input.border-green-500 {
  @apply border-green-500 focus:ring-green-500 focus:border-green-500;
}
</style>
