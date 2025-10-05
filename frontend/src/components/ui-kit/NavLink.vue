<script setup lang="ts">
withDefaults(defineProps<{
  tag?: 'button' | 'a',
  text: string,
  leftIcon?: string,
  rightIcon?: string,
}>(), {
  tag: 'button'
})
</script>

<template>
  <component :is="tag" class="nav-link">
    <svg v-if="leftIcon" width="18" height="18">
      <use :href="`#${leftIcon}`"></use>
    </svg>

    <span class="nav-link__label">{{ text }}</span>

    <svg v-if="rightIcon" width="18" height="18">
      <use :href="`#${rightIcon}`"></use>
    </svg>
  </component>
</template>

<style scoped lang="scss">
@use '@/assets/scss/mixins/mixins' as *;

.nav-link {
  padding: 5px 6px;

  background: transparent;
  border: none;
  outline: none;

  font: var(--light-14);

  display: flex;
  align-items: center;
  gap: 4px;

  cursor: pointer;

  @include hover {
    background: var(--bg-secondary);
  }

  &__label {
    display: block;
    white-space: nowrap;
  }
}
</style>
