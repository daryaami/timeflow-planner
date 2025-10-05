<script setup lang="ts">
import TaskHeader from "@/components/blocks/TaskHeader.vue";
import checklistIcon from "@/assets/img/checklist.svg"
import TasksList from "@/components/blocks/tasks/TasksList.vue";
import TaskAddInput from "@/components/blocks/tasks/TaskAddInput.vue";
</script>

<template>
  <TaskHeader
    title="All my tasks"
    :icon="checklistIcon"
  />
  <div class="tasks-page">
    <TaskAddInput class="tasks-page__form"/>
    <TasksList/>
  </div>
</template>

<style scoped lang="scss">
.tasks-page {
  max-width: 577px;
  padding-left: 30px;

  &__form {
    margin-bottom: 30px;
  }
}
</style>
