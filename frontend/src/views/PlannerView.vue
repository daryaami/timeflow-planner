<script setup lang="ts">
import { ref, onMounted } from 'vue';
import FullCalendar from '@fullcalendar/vue3'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction';
import type { Calendar, CalendarOptions } from '@fullcalendar/core';

// components
import PlannerHeader from "../components/blocks/planner/PlannerHeader.vue";
import LoaderVue from '../components/blocks/loaders/Loader.vue';

// store
import {useEventsStore} from "@/store/events";
import {getEndOfMonth, getStartOfMonth} from "@/components/js/time-utils";

const isLoading = ref<boolean>(true);

const calendarInstance = ref<InstanceType<typeof FullCalendar> | null>(null);
const calendarApi = ref<Calendar | null>(null);

const eventsStore = useEventsStore()

const currentDate = ref<Date | null>(null)

const calendarOptions: CalendarOptions = {
  plugins: [timeGridPlugin, interactionPlugin],
  headerToolbar: false,
  initialView: 'timeGridWeek',
  firstDay: 1,
  dayHeaderFormat: {
    weekday: 'short',
    day: 'numeric'
  },
  allDaySlot: false,
  nowIndicator: true,
  stickyHeaderDates: true,
  // slotDuration: '00:15:00',
  height: '100%',
  dayHeaderContent: (data) => {
    return {html: `<div class="planner__weekday">${data.text.split(' ')[1]}</div><div class="planner__day">${data.text.split(' ')[0]}</div>` }
  },
  slotLabelContent: (data) => {
    return `${data.date.getHours()}:00`
  },
  editable: true,
  eventDurationEditable: true,
  eventResizableFromStart: true,
  datesSet: async (dateInfo) => {
    currentDate.value = dateInfo.start
    isLoading.value = true;
    const events = await eventsStore.getEvents(getStartOfMonth(currentDate.value), getEndOfMonth(currentDate.value));
    calendarApi.value?.removeAllEventSources();
    calendarApi.value?.addEventSource(events);
    isLoading.value = false;
  }
}

onMounted(async () => {
  if (calendarInstance.value) {
    calendarApi.value = calendarInstance.value.getApi();
    currentDate.value = calendarApi.value.getDate();

    const nextMonth = new Date(currentDate.value);
    nextMonth.setMonth(nextMonth.getMonth() + 1);

    const prevMonth = new Date(currentDate.value);
    prevMonth.setMonth(prevMonth.getMonth() - 1);

    const events = await eventsStore.getEvents(getStartOfMonth(prevMonth), getEndOfMonth(nextMonth));
    calendarApi.value.removeAllEventSources();
    calendarApi.value.addEventSource(events);
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="planner-wrapper">
    <div class="planner">
      <PlannerHeader
        @next-week="calendarApi?.next()"
        @prev-week="calendarApi?.prev()"
        @today="calendarApi?.today()"
        :current-date="currentDate"
      />
      <div class="planner__loader-wrapper" v-if="isLoading">
        <LoaderVue />
      </div>

      <div class="planner__calendar-wrapper">
        <FullCalendar :options="calendarOptions" ref="calendarInstance"/>
      </div>
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

  &__calendar-wrapper {
    padding-left: 9px;
  }

  &__loader-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
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

.fc .fc-timegrid-slot-minor {
  border: none;
}
</style>
