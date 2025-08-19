<script setup lang="ts">
import {Task} from "@/types/task";
import IconBtn from "@/components/blocks/buttons/icon-btn.vue";
import {useTasksStore} from "@/store/tasks";

defineProps<{
  task: Task
}>()

const tasksStore = useTasksStore()
</script>

<template>
  <div class="task-item">
    <label :class="`task-item__checkbox task-item__checkbox--${task.priority.toLowerCase()}`">
      <input type="checkbox" class="visually-hidden">
    </label>
    <span class="task-item__title">{{ task.title }}</span>
    <span class="task-item__due">Due Wed 18:30</span>
    <IconBtn
      @click.prevent="tasksStore.deleteTask(task.id)"
      class="task-item__delete"
      icon="#delete"
      size="xs"
    />
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/scss/mixins/mixins.scss' as *;

.task-item {
  padding: 7px 7px 7px 36px;
  border-radius: 8px;
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.07);
  background: var(--bg-highlight);
  white-space: nowrap;
  position: relative;

  cursor: pointer;
  @include hover {
    background: var(--bg-secondary);
  }

  &__checkbox {
    position: absolute;
    top: 7px;
    left: 7px;
    display: block;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    border: 1px solid var(--stroke-secondary);
    cursor: pointer;

    @include hover {
      border-color: var(--bg-accent);
      background: transparent;
    }

    &--medium {
      background: rgba(255, 212, 171, 0.3);
      border-color: #FFE15D;
    }

    &--high {
      background: rgba(255, 171, 173, 0.3);
      border-color: #FF5457;
    }

    &--critical {
      background: rgba(255, 171, 230, 0.3);
      border-color: #FF4EC7
    }
  }

  &__title {
    font: var(--light-14);
    display: block;
  }

  &__due {
    font: var(--light-11);
    color: var(--text-accent);
    display: block;
    margin-top: 6px;
  }

  &__delete {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    right: 7px;
  }
}
</style>
