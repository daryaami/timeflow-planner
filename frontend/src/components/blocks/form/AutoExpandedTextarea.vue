<script setup lang="ts">
import {ref} from "vue";

defineProps<{
  modelValue: string
}>()

const textarea = ref<HTMLTextAreaElement | null>(null)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const autoExpand = () => {
  const element = textarea.value
  if (!element) return

  emit('update:modelValue', element.value)

  element.style.height = 'auto'
  element.style.height = element.scrollHeight + 'px'
}
</script>

<template>
  <textarea ref="textarea" @input="autoExpand" rows="1"></textarea>
</template>

<style scoped lang="scss">
textarea {
  overflow: hidden;
  resize: none;
}
</style>
