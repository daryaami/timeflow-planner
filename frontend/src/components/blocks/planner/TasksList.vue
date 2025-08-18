<script setup lang="ts">
import {ref, watch} from "vue";
import {useTasksStore} from "@/store/tasks";
import {onMounted} from "vue";
import { Draggable } from '@fullcalendar/interaction';

const tasksStore = useTasksStore()

const tasks = ref(null)

const updateTasks = async () => {
  const data = await tasksStore.getTasks()
  tasks.value = data.map(task => ({ ...task, el: null }))
}

onMounted(async () => {
  await updateTasks()
})

watch(
  () => tasksStore.tasks,
  async () => {
    await updateTasks()
  }
)

// Draggable
const DEFAULT_DURATION = '00:30'

const setTaskEl = (el: HTMLElement | null, task: any) => {
  task.el = el
  new Draggable(el, {
    eventData: {
      title: task.title,
      duration: DEFAULT_DURATION
    }
  })
}
</script>

<template>
  <div class="tasks-wrapper" v-if="tasks">
    <h2 class="tasks-wrapper__title">Tasks</h2>
    <ul class="tasks__list">
      <li class="tasks__item"
          v-for="task in tasks"
          :key="task.id"
          :ref="el => setTaskEl(el, task)"
      >
        <span>{{ task.title }}</span>
        <span class="tasks__priority">{{ task.priority }}</span>
        <span class="tasks__calendar">calendar id: {{ task.calendar }}</span>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/mixins.scss' as *;

.tasks-wrapper {
  min-width: 330px;
  padding: 22px 20px;

  &__title {
    font: var(--light-20);
    margin-bottom: 20px;
  }
}

.tasks {
  &__list {
    @include reset-list;
  }

  &__item {
    padding: 8px 16px;
    border-radius: 8px;
    display: grid;
    grid-template-columns: min-content 1fr;
    column-gap: 8px;
    row-gap: 4px;
    align-items: baseline;
    white-space: nowrap;

    cursor: pointer;
    @include hover {
      background-color: var(--bg-primary-hover);
    }
  }

  &__priority {
    font: var(--light-16);
    color: var(--text-primary-disabled);
    text-transform: lowercase;
  }

  &__calendar {
    font: var(--light-10);
    grid-column: 1 / -1;
    color: var(--text-primary-disabled);
  }
}
</style>
