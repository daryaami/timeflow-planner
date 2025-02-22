<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps(['day']);
</script>

<template>
  <div class="planner-date"
    :class="{'current': day.isToday}"
  >
    <span class="planner-date__weekday">{{ day.weekday }}</span>
    <div class="planner-date__day">
        <span>{{ day.date }}</span>
    </div>
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;

  .planner-date {
    width: 100%;
    background-color: $white;
    padding-bottom: 12px;
    position: relative;

    &::before {
      content: '';
      display: block;
      width: 1px;
      height: 45px;
      position: absolute;
      left: 0;
      bottom: 0;
      border-left: 1px solid $dark-lines;
    }

    &.current {
      & .planner-date__weekday {
        color: $blue-attention;
      }

      & .planner-date__day {
        color: $white;
        position: relative;

        & span {
          position: relative;
          z-index: 2;
        }

        &::before {
          content: '';
          display: block;
          width: 40px;
          height: 40px;
          background-color: $blue-attention;
          border-radius: 50%;
          position: absolute;
          left: 50%;
          top: calc(50% + 2px);
          transform: translate(-50%, -50%)
        }
      }
    }

    &__weekday {
      @include small-bold;
      display: block;
      margin-bottom: 3px;
      text-align: center;
    }

    &__day {
      @include header;
      display: block;
      text-align: center;
    }
  }
</style>
