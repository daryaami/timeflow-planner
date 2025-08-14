<script setup lang="ts">
import {ref} from "vue";
import {useCalendarsStore} from "@/store/calendars";
import {useTasksStore} from "@/store/tasks";

import MultiSelect from 'vue-multiselect'

const popup = ref(null)

const calendarsStore = useCalendarsStore()
const calendars = ref(null)


const openPopup = async () => {
  popup?.value.showModal()

  if (!calendars.value) {
    calendars.value = await calendarsStore.getCalendars()

    calendar.value = calendars.value?.find(c => c.primary);
  }
}


const title = ref<string>('')
const priority = ref<string>('NONE')
const dueDate = ref(null)
const calendar = ref<string>('')

const tasksStore = useTasksStore()

const PRIORITY_OPTIONS = [
  {
    value: 'NONE',
    label: 'None'
  },
  {
    value: 'LOW',
    label: 'Low'
  },
  {
    value: 'MEDIUM',
    label: 'Medium'
  },
  {
    value: 'HIGH',
    label: 'High'
  },
  {
    value: 'CRITICAL',
    label: 'Critical'
  }
]

const submitForm = async () => {
  const data = {
    title: title.value,
    priority: priority.value,
    due_date: dueDate.value,
    calendar: calendar.value,
  }

  await tasksStore.createTask(data)
}
</script>

<template>
  <button class="button" @click="openPopup">
    + Add
  </button>

  <dialog ref="popup"
  >
    <form @submit.prevent="submitForm">
      <input type="text" placeholder="add title" v-model="title">

      <p>
        <MultiSelect v-model="priority"
                     :options="PRIORITY_OPTIONS"
                     track-by="value"
                     label="label"
                     :allow-empty="false"
                     :clearOnSelect="false"
                     placeholder="Select priority"
                     :showLabels="false"
        ></MultiSelect>
      </p>

      <p>
        <label>Schedule</label>
        <input type="datetime-local">
      </p>

      <p>
        <label>Add due date</label>
        <input type="datetime-local" v-model="dueDate">
      </p>

      <p>
        <label>Duration</label>
        <input type="text">
      </p>

      <p v-if="calendars">
        <MultiSelect v-model="calendar"
                     :options="calendars"
                     track-by="id"
                     label="summary"
                     :allow-empty="false"
                     :clearOnSelect="false"
                     placeholder="Select calendar"
                     :showLabels="false"
        ></MultiSelect>
      </p>

      <p>
        <textarea placeholder="add notes..."></textarea>
      </p>

      <button type="submit">Save</button>
    </form>
  </dialog>
</template>

<style scoped lang="scss">
  .button {
    position: absolute;
    right: 50px;
    bottom: 50px;
    z-index: 1000000000;
  }
</style>
