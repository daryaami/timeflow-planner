<script setup lang="ts">
defineProps({
  icon: String,
  size: {
    type: String,
    default: 'm'
  },
})
</script>

<template>
<button class="icon-button" :class="`icon-button--${size}`">
  <svg width="24" height="24">
    <use :href="icon"></use>
  </svg>
</button>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/mixins' as *;

.icon-button {
  @include reset-button;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--icon-primary);
  transition: .15s;

  @include hover {
    color: var(--bg-accent-secondary);
  }


  & svg {
    display: block;
    width: 100%;
    height: 100%;
  }

  &--l {
    width: 32px;
    height: 32px;
  }

  &--m {
    width: 24px;
    height: 24px;
  }

  &--s {
    width: 18px;
    height: 18px;
  }

  &--xs {
    width: 16px;
    height: 16px;
  }
}
</style>
