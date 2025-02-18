<script setup>
import { useRoute } from 'vue-router';
import LoginLayout from './layouts/LoginLayout.vue';
// import DefaultLayout from './layouts/DefaultLayout.vue';

const route = useRoute();
</script>

<template>
  <div class="container">
    <LoginLayout />
    <!-- <LoginLayout v-if="route.meta.layout == 'login'" /> -->
    <!-- <DefaultLayout v-if="route.meta.layout == 'default'"/> -->
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@use '@/assets/scss/mixins/functions.scss' as *;

* {
  box-sizing: border-box;
}

html {
  height: 100%;
  font-size: size-desktop($font-size-main);
}

#app {
  height: 100%;
  width: 100%;
}

body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  font-weight: 300;
  font-family: $main-font;
  background-color: $white;
}

a {
  color: inherit;
  text-decoration: none;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  border: 0;
  padding: 0;
  white-space: nowrap;
  clip-path: inset(100%);
  clip: rect(0 0 0 0);
  overflow: hidden;
}

.container {
  width: 100%;
  height: 100%;
}
</style>
