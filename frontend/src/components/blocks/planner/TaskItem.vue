<script setup>
const props = defineProps(['task'])
</script>

<template>
  <div class="task">
    <span class="task__color"
    :style='{
      backgroundColor: task.color,
    }'
    ></span>
    <label
      class="task__checkbox-label"
      :for="title"
    >
      <input class="visually-hidden" :id="title" type="checkbox">
    </label>
    <span>{{ task.name }}</span>
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@use '@/assets/scss/colors.scss' as *;

.task {
  @include light-20;
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
  height: 68px;
  padding: 19px 17px 19px 25px;
  border-radius: 15px;
  background-color: white;

  &__color {
    display: block;
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 10px;
    background-color: #F0F0F0;
  }


  &__checkbox-label {
    display: block;
    width: 28px;
    height: 28px;
  // @include empty-checkbox;
    background-size: 100%;
    cursor: pointer;
    transition: .1s;
    flex-shrink: 0;

    &:has(:checked) {
      // @include checked-checkbox;
    }
  }
}
</style>
