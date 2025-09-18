<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: Object || null,
    default: null
  }
})
</script>

<template>
  <div class="task-header">
    <div class="task-header__title-wrapper">
      <component :is="icon" v-if="icon" width="26" height="26"/>
      <h1 class="task-header__title">{{ title }}</h1>
    </div>
  </div>
</template>

<style scoped lang="scss">
.task-header {
  padding: 15px 38px;

  &__title-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  &__title {
    font: var(--bold-24);

    margin: 0;
  }
}
</style>
