<script setup lang="ts">
interface Button {
  label: string,
  icon: string
}

interface Props {
  label?: string,
  buttons: Button[],
  name?: string
}

const props = withDefaults(defineProps<Props>(), {
  name: 'toggle-buttons'
})
</script>

<template>
  <div class="toggle-buttons">
    <span class="toggle-buttons__label"
          v-if="label">{{ label }}</span>

    <div class="toggle-buttons__buttons">
      <label class="toggle-buttons__button" v-for="button in buttons">
        <input type="radio" :name="name" class="visually-hidden">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <use :href="`#${button.icon}`"></use>
        </svg>
        <span>{{ button.label }}</span>
      </label>
    </div>
  </div>
</template>

<style scoped lang="scss">
.toggle-buttons {
  &__label {
    font: var(--light-14);
    color: var(--text-primary-disabled);

    display: block;

    margin-bottom: 10px;
  }

  &__buttons {
    display: flex;

    padding: 2px;
    border-radius: 20px;

    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.07);
    background: var(--bg-primary-hover);
  }

  &__button {
    display: flex;
    gap: 6px;
    padding: 4px 6px;

    cursor: pointer;
    font: var(--bold-12);
    align-items: center;
  }
}
</style>
