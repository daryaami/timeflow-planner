<script setup>
import { computed, ref } from 'vue';
import { getDecimalHours, getStringTime } from '@/components/js/time-utils';

const props = defineProps(['card', 'gridHeight']);

const duration = computed(() => {
  return (new Date(props.card.end) - new Date(props.card.start)) / (1000 * 60 * 60)
})
const startTime = ref(getStringTime(props.card.event.start.dateTime));



const position = computed((() => getDecimalHours(props.card.start) * 100 / 24));

const height = computed(() => {
  const durationCalc = Math.max(duration.value, .25)
  return durationCalc * 100 / 24
})

const time = computed(() => `${startTime.value} - ${getStringTime(props.card.event.end.dateTime)}`);
const isPast = computed(() => {
  if (new Date(props.card.event.end.dateTime) < new Date()) {
    return true
  } else {
    return false
  }
})




// Grid
const grid = computed(() => {
  if (props.gridHeight) {
    return [10, props.gridHeight / 96]
  } else {
    return [0, 0]
  }
})

const widthParametr = computed(() => {
  return props.card.overlapLevel? props.card.overlapLevel + 1: 1
})
</script>

<template>
  <vue-draggable-resizable
    v-if="gridHeight"

    class="event-card"
    :axis="'y'"
    :grid="grid"
    :handles="['tm', 'bm']"
    :active="true"
    :style='{
      top: `${position}%`,
      height: `calc(${height}% - 2px)`,
      backgroundColor: `${card.event.background_color}`,
      color: `${card.event.foreground_color}`,
      width: `calc(100% - ${widthParametr * .75}rem)`
    }'


    :class="{
      'no-padding': duration <= .25,
      'no-right-padding': duration <= .5,
      'past': isPast,
      'overlap': card.overlapLevel,
    }"
  >
    <div v-if="duration < 0.75"
      class="event-card__short-wrapper"
    >
      <span class="event-card__name">{{ card.event.summary }},&nbsp;</span>
      <span class="event-card__time">{{ startTime }}</span>
    </div>
    <div class="event-card__name-wrapper">
      <span class="event-card__name"
        v-if="duration >= 0.75"
        :class="{
          'one-string': duration <= 1,
        }"
      >{{ card.event.summary }}</span>
    </div>

    <span class="event-card__time"
      v-if="duration >= 0.75"
    >{{ time }}</span>
  </vue-draggable-resizable>
</template>

<style lang="scss">
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@import "vue-draggable-resizable/style.css";

.event-card {
  padding: 8px;
  background-color: #E68D8D;
  color: $white;
  border-radius: 10px;
  height: 90px;
  position: absolute;
  right: .75rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: start;
  border: none;
  cursor: pointer;
  transition: box-shadow .15s;

  &.overlap {
    outline: 1px solid $white;
  }

  &.no-padding {
    padding-top: 0;
    padding-bottom: 0;
  }

  &.no-right-padding {
    padding-right: 0;
  }

  &.past {
    opacity: .5;
  }

  &.selected {
    box-shadow: 0 0 12px 0 rgba(0, 0, 0, 0.5);
  }

  &__short-wrapper {
    display: flex;

    & .event-card__name {
      flex-shrink: 0;
    }
  }

  &__name-wrapper {
    overflow: hidden
  }

  &__name {
    @include small-bold;
    margin-bottom: 4px;
    display: block;
    color: inherit;
  }

  &__time {
    @include small-light;
    color: inherit;
    display: block;
  }
}

.one-string {
  white-space: nowrap;
  width: 100%;
  overflow: hidden;
}
</style>
