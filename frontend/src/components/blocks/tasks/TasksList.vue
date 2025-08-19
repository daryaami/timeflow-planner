<script setup lang="ts">
import {ComponentPublicInstance, ref, watch} from "vue";
import {useTasksStore} from "@/store/tasks";
import {onMounted} from "vue";
import { Draggable } from '@fullcalendar/interaction';
import TaskItem from "@/components/blocks/tasks/TaskItem.vue";
import {Task, UiTask} from "@/types/task";

const tasksStore = useTasksStore()

const tasks = ref<UiTask[]>([])

const toUiTasks = (items: Task[]): UiTask[] =>
  items.map((t) => ({ ...t, el: null }));

const updateTasks = async () => {
  const data = await tasksStore.getTasks()
  tasks.value = toUiTasks(data)
}

onMounted(async () => {
  await updateTasks()
})

watch(
  () => tasksStore.tasks,
  async () => {
    await updateTasks()
  },
  { deep: true }
)

// Draggable
const DEFAULT_DURATION = '00:30'

const setTaskEl = (el: Element | ComponentPublicInstance | null, task: UiTask) => {
  if (!(el instanceof HTMLElement)) return;
  task.el = el

  if (!el) return

  new Draggable(el, {
    eventData: {
      title: task.title,
      duration: DEFAULT_DURATION
    }
  })
}
</script>

<template>
  <div class="tasks-wrapper" v-if="tasks && tasks.length">
    <h2 class="tasks-wrapper__title">Tasks</h2>
    <ul class="tasks__list">
      <li
          v-for="task in tasks"
          :key="task.id"
          :ref="el => setTaskEl(el, task)"
      >
        <TaskItem :task="task" />
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/scss/mixins/resets' as *;

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
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
}
</style>
