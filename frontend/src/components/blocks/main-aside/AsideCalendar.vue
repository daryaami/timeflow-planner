<script setup>
// import { ref, computed, watch } from 'vue';
// // import { getCurrentWeekMonday, getTomorrow } from '@/components/js/time-utils';
// import { useCurrentDateStore } from '@/store/currentDate';
// import IconBtn from "@/components/blocks/buttons/icon-btn.vue";
//
// const weekDays = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
//
// const currentDate = useCurrentDateStore()
//
// const currentCalendarDate = ref(new Date(currentDate.date));
//
// const days = computed(() => {
//   const daysArr = []
//
//   let firstDayofMonth;
//   let firstDay;
//
//   firstDayofMonth = new Date(currentCalendarDate.value);
//   firstDayofMonth = new Date(firstDayofMonth.setDate(1));
//
//   // firstDay = getCurrentWeekMonday(firstDayofMonth);
//
//   daysArr.push(firstDay)
//
//   for(let i = 0; i < 34; i++) {
//     // const newDay = getTomorrow(daysArr[i]);
//     daysArr.push(newDay);
//   }
//
//   return daysArr
// })
//
// const currentMonth = computed(() => {
//   return `${currentCalendarDate.value.toLocaleString('default', { month: 'long' })} ${currentCalendarDate.value.getFullYear()}`;
// })
//
// const nextMonthHandler = () => {
//   currentCalendarDate.value = new Date(currentCalendarDate.value.setMonth(currentCalendarDate.value.getMonth() + 1))
// }
//
// const prevMonthHandler = () => {
//   currentCalendarDate.value = new Date(currentCalendarDate.value.setMonth(currentCalendarDate.value.getMonth() - 1))
// }
//
// watch(currentDate, (newValue) => {
//   currentCalendarDate.value = newValue.date;
// })

</script>

<template>
<!--  <div class="aside-calendar">-->
<!--    <div class="aside-calendar__wrapper">-->
<!--      <div class="aside-calendar__month-wrapper">-->
<!--        <span class="aside-calendar__month">{{ currentMonth }}</span>-->
<!--        <div class="aside-calendar__buttons-wrapper">-->
<!--          <IconBtn-->
<!--            @click="prevMonthHandler"-->
<!--            icon="#chevron-left"-->
<!--            size="xs"-->
<!--          ></IconBtn>-->

<!--          <IconBtn-->
<!--            @click="nextMonthHandler"-->
<!--            icon="#chevron-right"-->
<!--            size="xs"-->
<!--          ></IconBtn>-->
<!--        </div>-->
<!--      </div>-->

<!--      <div class="aside-calendar__header aside-calendar__grid">-->
<!--        <span class="aside-calendar__weekday"-->
<!--          v-for="(weekDay, i) in weekDays"-->
<!--          :key="i"-->
<!--        >-->
<!--          {{ weekDay }}-->
<!--        </span>-->
<!--      </div>-->

<!--      <div class="aside-calendar__calendar aside-calendar__grid">-->
<!--        <button class="aside-calendar__day aside-calendar__date"-->
<!--          v-for="day, i in days"-->
<!--          :key="i"-->
<!--          :class="{'aside-calendar__date&#45;&#45;uncurrent': day.getMonth() !== currentCalendarDate.getMonth() }"-->
<!--          @click="currentDate.setDate(day)"-->
<!--        >-->
<!--            {{ day.getDate() }}-->
<!--      </button>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
</template>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/mixins' as *;

.aside-calendar {
  margin: 0 30px 45px 30px;

  &__wrapper {
    width: fit-content;
  }

  &__month-wrapper {
    margin-bottom: 42px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__month {
    font: var(--bold-16);
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    column-gap: 11px;
    row-gap: 10px;
  }

  &__header {
    width: fit-content;
    margin-bottom: 15px;
  }

  &__weekday {
    font: var(--bold-12);
    color: var(--text-primary-disabled);
    width: 22px;
    display: block;
    text-align: center;
  }

  &__calendar {
    width: fit-content;
  }

  &__day {
    font: var(--bold-12);
    color: var(--text-primary-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;

    @include hover {
      background: var(--bg-primary-hover);
    }
  }

  &__date {
    @include reset-button;
    //background-color: $white;
    border-radius: 50%;

    &--uncurrent {
      background: transparent;
      //color: $dark-grey;
    }
  }

  &__buttons-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}
</style>
