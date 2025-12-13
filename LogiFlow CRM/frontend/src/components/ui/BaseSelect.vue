<template>
  <div class="mb-4">
    <label v-if="label" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }} <span v-if="required" class="text-red-500">*</span>
    </label>
    <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" :required="required" class="input-field">
      <option value="" disabled>{{ placeholder || 'Selecione...' }}</option>
      <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  options: { type: Array, default: () => [] },
  placeholder: String,
  required: Boolean
})
defineEmits(['update:modelValue'])
</script>
