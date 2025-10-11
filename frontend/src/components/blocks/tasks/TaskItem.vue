<script setup lang="ts">
import {Task} from "@/types/task";
import IconBtn from "@/components/ui-kit/IconBtn.vue";
import {useTasksStore} from "@/store/tasks";
import {computed} from "vue";
import {formatDueDate} from "@/components/js/time-utils";

const props = defineProps<{ task: Task }>()

const dueDate = computed(() => {
  if (!props.task.due_date) return
  const date = new Date(props.task.due_date)

  const dateString = formatDueDate(date)

  return `Due ${dateString}`
})

const tasksStore = useTasksStore()

const toggleCompleteTask = (e) => {
  tasksStore.toggleCompleteTask(props.task.id, e.target.checked)
}
</script>

<template>
  <div class="task-item">
    <label :class="`task-item__checkbox task-item__checkbox--${task.priority.toLowerCase()}`">
      <input @change="toggleCompleteTask"
             :checked="task.completed"
             type="checkbox"
             class="visually-hidden"
      >
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="15" height="15" rx="7.5" fill="currentColor" />
        <rect x="0.5" y="0.5" width="14" height="14" rx="7" stroke="currentColor" />
        <path d="M6.42133 11.7071L4.10128 9.38706C3.88744 9.17322 3.94594 8.81272 4.21643 8.67748C4.34893 8.61123 4.50577 8.61558 4.63439 8.68908L6.24521 9.60955C6.71753 9.87945 7.31896 9.72228 7.59885 9.2558L10.4395 4.52145C10.4939 4.43079 10.5789 4.36258 10.6792 4.32915C11.0496 4.20567 11.387 4.58718 11.2191 4.93974L8.12855 11.4299C7.96272 11.7782 7.61139 12 7.22568 12H7.12844C6.86322 12 6.60887 11.8947 6.42133 11.7071Z" fill="#FCFCFC" />
      </svg>
    </label>
    <span class="task-item__category" v-if="task.category">{{ task.category.name }}</span>
    <span class="task-item__title">{{ task.title }}</span>
    <span class="task-item__due" v-if="dueDate">{{ dueDate }}</span>
    <IconBtn
      @click.prevent="tasksStore.deleteTask(task.id)"
      class="task-item__delete"
      icon="delete"
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

    & .task-item__delete {
      opacity: 1;
    }
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

    &:has(:checked) {
      border: 0;
      background: transparent;

      color: var(--icon-disabled);

      @include hover {
        color: var(--bg-accent);
      }

      & svg {
        display: block;
        width: 100%;
        height: 100%;

        position: absolute;
        left: 0;
        top: 0;
      }
    }

    & svg {
      display: none;
    }
  }

  &__category {
    display: block;

    font: var(--light-11);
    color: var(--text-primary-disabled);

    margin-bottom: 6px;
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

    opacity: 0;
    transition: opacity 0.2s;
  }
}
</style>
