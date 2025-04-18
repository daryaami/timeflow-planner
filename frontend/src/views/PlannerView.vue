<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import FullCalendar from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'

import PlannerHeaderVue from '../components/blocks/planner/PlannerHeader.vue';
import LoaderVue from '../components/blocks/loaders/Loader.vue';
import EventInfoSidebar from '@/components/blocks/planner/EventInfoSidebar.vue';

import RightSidebarVue from '@/components/blocks/planner/RightSidebar.vue';
const isSidebarOpened = ref(true);

const calendarInstance = ref(null);
const calendarApi = ref(null);

const calendarOptions = {
  plugins: [timeGridPlugin],
  headerToolbar: false,
  initialView: 'timeGridWeek',
  firstDay: 1,
  dayHeaderFormat: {
    weekday: 'short',
    day: 'numeric'
  },
  allDaySlot: false,
  nowIndicator: true,
  stickyHeaderDates: 'true',
  height: '100%',
  dayHeaderContent: (data) => {
    return {html: `<div class="planner__weekday">${data.text.split(' ')[1]}</div><div class="planner__day">${data.text.split(' ')[0]}</div>` }
  },
  slotLabelContent: (data) => {
    return `${data.date.getHours()}:00`
  },
  nowIndicatorDidMount: (data) => {

  }
}

onMounted(() => {
  calendarApi.value = calendarInstance.value.getApi();
});
</script>

<template>
  <div class="planner-wrapper">
    <div class="planner">
      <PlannerHeaderVue
        v-model="isSidebarOpened"
        :isLoading="isLoading"
        @next-week="calendarApi.next()"
        @prev-week="calendarApi.prev()"
        @today="calendarApi.today()"
      />
      <div class="planner__loader-wrapper" v-if="isLoading">
        <LoaderVue />
      </div>

      <div class="planner__calendar-wrapper">
        <FullCalendar :options="calendarOptions" ref="calendarInstance"/>
      </div>

    </div>
    <div class="planner__right-sidebar"
         v-if="false"
      :class="{
        'hidden': !isSidebarOpened,
      }"
    >
      <RightSidebarVue
        v-if="!selectedEvent"
      />

      <EventInfoSidebar
        v-if="selectedEvent"
        :event="selectedEvent"
        @close="selectedEvent = null"
      />
    </div>

  </div>


</template>

<style lang="scss">
.planner-wrapper {
  display: flex;
  overflow: hidden;
  flex-grow: 1;
}

.planner {
  height: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
  overflow: hidden;
  flex-grow: 1;

  &__weekday {
    font: var(--bold-10);
  }

  &__day {
    font: var(--light-24);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 39px;
    height: 37px;
    border-radius: 50px;
  }

  &__right-sidebar {
    width: 380px;
    height: 100%;
    transition: .15s;
    overflow: hidden;

    &.hidden {
      width: 0;
    }
  }

  &__calendar-wrapper {
    padding-left: 9px;
  }
}

.fc-theme-standard th {
  position: relative;

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: -2px;
    height: 46px;
    width: calc(100% + 4px);
    background-color: var(--bg-highlight);
    z-index: 1;
  }

  &:first-child {
    &::before {
      content: '';
      position: absolute;
      top: -1px;
      left: 0;
      height: calc(100% + 2px);
      width: 25px;
      background-color: var(--bg-highlight);
      z-index: 1;
    }
  }
}

.fc-scrollgrid-sync-inner {
  position: relative;
  z-index: 2;
}

.fc-theme-standard .fc-scrollgrid {
  border: none
}

.fc-day-today {
  & .planner__weekday {
    color: var(--bg-accent);
    position: relative;
    z-index: 2;
  }

  & .planner__day {
    background-color: var(--bg-accent);
    color: var(--text-secondary);
    margin-bottom: 14px;
    position: relative;
    z-index: 2;
  }
}

.fc .fc-timegrid-slot-label-cushion {
  color: var(--text-primary-disabled);
  font: var(--bold-12);
}

.fc-direction-ltr .fc-timegrid-slot-label-frame {
  transform: translate(-4px, -100%);
  position: relative;
  z-index: 2;

}

.fc-scroller:has(.planner__day) {
  overflow: hidden !important;
}

.fc .fc-col-header-cell-cushion {
  padding: 0;
}

.fc .fc-timegrid-slot-label {
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 0;
    height: calc(100% + 2px);
    width: 37px;
    background-color: var(--bg-highlight);
    z-index: 1;
  }
}

.fc .fc-timegrid-now-indicator-arrow {
  display: none;
}

.fc-timegrid-col.fc-day-today {
  background: none !important;
}
</style>
