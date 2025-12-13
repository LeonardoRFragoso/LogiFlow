<template>
  <div class="mb-4">
    <label v-if="label" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }} <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      class="input-field"
      :class="{ 'border-red-500 dark:border-red-400': error }"
    />
    <p v-if="error" class="text-red-500 dark:text-red-400 text-sm mt-1">{{ error }}</p>
    <p v-if="hint" class="text-gray-500 dark:text-gray-400 text-sm mt-1">{{ hint }}</p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  required: Boolean,
  disabled: Boolean,
  error: String,
  hint: String
})
defineEmits(['update:modelValue'])
</script>
