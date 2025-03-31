<script setup>
import googleIcon from '@/assets/img/google-icon.png'

const props = defineProps({
  href: String,
  text: String,
});
</script>

<template>
  <a class="google-button" :href="href">
    <img class="google-button__icon" width="50" height="50"
      :src="googleIcon"
      alt="Google logo">
    <span>{{ text }}</span>
  </a>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/mixins.scss' as *;
@use '@/assets/scss/mixins/resets.scss' as *;

.google-button {
  font: var(--bold-20);
  @include reset-button;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50px;
  height: 76px;
  width: 391px;
  background-color: var(--bg-auth-google);
  color: var(--text-primary);
  gap: 8px;

  &__icon {
    display: block;
    width: 50px;
    height: 50px;
  }
}
</style>
