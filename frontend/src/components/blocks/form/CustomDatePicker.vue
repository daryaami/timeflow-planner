<script setup lang="ts">
import VueDatePicker from "@vuepic/vue-datepicker";
import { computed } from "vue";

const props = defineProps<{
  modelValue: Date | null
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: Date | null): void
}>();

// синхронизация локального состояния с v-model
const value = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

function formatDate(date: Date): string {
  return new Intl.DateTimeFormat("en-US", {
    weekday: "short",
    day: "numeric",
    month: "short",
  }).format(date);
}

const displayValue = computed(() => {
  if (!value.value) return "Due";
  return formatDate(value.value);
});
</script>

<template>
  <VueDatePicker v-model="value">
    <template #trigger>
      <button type="button"
              class="select-button-small"
              :class="{ 'select-button-small--active': value }"
      >
        <svg class="select-button-small__icon" width="16" height="16">
          <use href="#date-range"></use>
        </svg>

        <span>{{ displayValue }}</span>
      </button>
    </template>
  </VueDatePicker>
</template>

<style scoped lang="scss">
@use '@/assets/scss/mixins/mixins' as *;

.select-button-small {
  position: relative;

  font: var(--light-14);
  color: var(--text-primary-disabled);

  padding: 4px 4px 4px 20px;
  border-radius: 4px;

  border: none;
  outline: none;
  background: transparent;

  cursor: pointer;

  @include hover {
    background-color: var(--bg-primary-hover);
  }

  &--active {
    color: var(--text-primary-hover);
  }

  &__icon {
    position: absolute;
    top: 50%;
    left: 2px;
    transform: translateY(-50%);

    pointer-events: none;
  }
}

.dp__main {
  width: fit-content!important;
}
</style>
