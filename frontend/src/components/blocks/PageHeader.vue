<script setup>
import NewTaskBlockVue from './new-task/NewTaskBlock.vue';
import SearchBlock from './SearchBlock.vue'

import logoIcon from '@/assets/img/logo.svg';

const props = defineProps({
  title: String,
});

</script>


<template>
  <div class="page-header">
    <div class="page-header__title-wrapper">
      <img :src="logoIcon" alt="TimeFlow" width="40" height="40">

      <h1 class="page-header__title">TimeFlow</h1>
    </div>
    <new-task-block-vue/>
    <search-block />
  </div>
</template>


<style lang="scss">
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;

.page-header {
  display: flex;
  align-items: center;
  gap: 41px;
  width: 100%;
  padding: 20px 17px 20px 46px;
  border-bottom: 1px solid $light-lines;

  &__title-wrapper {
    margin-right: auto;
    display: flex;
    align-items: center;
    gap: 15px;

    & img {
      display: block;
      width: 40px;
      height: 40px;
    }
  }

  &__title {
    font-weight: 400;
    font-size: 34px;
    line-height: 100%;
    letter-spacing: -0.04em;
    color: $basic-dark;
    margin: 0;
  }
}
</style>
