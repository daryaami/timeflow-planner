<script setup>

</script>

<template>
  <div class="login-layout">
    <RouterView  />
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/colors.scss' as *;

.login-layout {
  display: flex;
  width: 100%;
  height: 100%;
  background-color: $violet;
  align-items: center;
  justify-content: center;
}
</style>
