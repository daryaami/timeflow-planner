<script setup lang="ts">
import {useTasksStore} from "@/store/tasks";
import {onMounted, ref, watch} from "vue";
import {Task} from "@/types/task";
import TaskItem from "@/components/blocks/tasks/TaskItem.vue";

const tasksStore = useTasksStore()

const tasks = ref<Task[]>([])

onMounted(async () => {
  tasks.value = await tasksStore.getTasks()
})

watch(() => tasksStore.tasks, async () => {
  tasks.value = await tasksStore.getTasks()
})
</script>

<template>
<div class="tasks-list">
  <TaskItem v-for="task in tasks" :key="task.id" :task="task" />
</div>
</template>

<style scoped lang="scss">
.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
