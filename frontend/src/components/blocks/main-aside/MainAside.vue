<script setup>
import MainMenuVue from "./MainMenu.vue";
import AsideCalendar from "./AsideCalendar.vue";
</script>

<template>
  <div class="main-aside">
    <AsideCalendar />
    <MainMenuVue />
  </div>
</template>


<style lang="scss">
@use '@/assets/scss/colors.scss' as *;

.main-aside {
  width: 404px;
  height: 100%;
  background-color: $dark-white;
  display: block;
  padding: 20px 0;
}
</style>
