<script setup lang="ts">
import {ref} from "vue";
import {useCalendarsStore} from "@/store/calendars";
import {useTasksStore} from "@/store/tasks";

const popup = ref(null)

const calendarsStore = useCalendarsStore()
const calendars = ref(null)

const openPopup = async () => {
  popup?.value.showModal()

  if (!calendars.value) {
    calendars.value = await calendarsStore.getCalendars()

    const primaryCalendar = calendars.value?.find(c => c.primary)
    if (primaryCalendar) {
      calendar.value = primaryCalendar.id
    }
  }
}


const title = ref<string>('')
const priority = ref<string>('NONE')
const dueDate = ref(null)
const calendar = ref<string>('')

const tasksStore = useTasksStore()

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

  <dialog ref="popup">
    <form @submit.prevent="submitForm">
      <input type="text" placeholder="add title" v-model="title">

      <p>
        <select v-model="priority">
          <option value="NONE">None</option>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
          <option value="CRITICAL">Critical</option>
        </select>


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

      <p>
        <select v-if="calendars" v-model="calendar">
          <option v-for="calendar in calendars" :value="calendar.id">{{ calendar.summary }}</option>
        </select>
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
    position: fixed;
    right: 50px;
    bottom: 50px;
    z-index: 1000000000;
  }
</style>
