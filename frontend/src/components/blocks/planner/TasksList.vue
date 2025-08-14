<script setup lang="ts">
import {ref} from "vue";
import {useTasksStore} from "@/store/tasks";
import {onMounted} from "vue";

const tasksStore = useTasksStore()

const tasks = ref(null)

onMounted(async () => {
  tasks.value = await tasksStore.getTasks()
})
</script>

<template>
  <div class="tasks-wrapper" v-if="tasks">
    <h2 class="tasks-wrapper__title">Tasks</h2>
    <ul class="tasks__list">
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }}
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;

.tasks-wrapper {
  min-width: 330px;
  padding: 22px 20px;

  &__title {
    font: var(--light-20);
    margin-bottom: 20px;
  }
}

.tasks__list {
  @include reset-list;
}
</style>
