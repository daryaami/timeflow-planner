<script setup lang="ts">
import { Task } from "@/types/task";
import { ref, watch } from "vue";
import { useTasksStore } from "@/store/tasks";
import CustomDatePicker from "@/components/blocks/form/CustomDatePicker.vue";
import {PRIORITIES} from "@/constants/tasks";
import SelectSmall from "@/components/blocks/form/SelectSmall.vue";
import TaskCheckbox from "@/components/blocks/form/TaskCheckbox.vue";

const taskStore = useTasksStore();

const props = defineProps<{
  task: Task;
}>();

// локальный тип с датой в виде объекта
type EditableTask = Omit<Task, "due_date"> & {
  due_date: Date | null;
};

// создаём копию задачи с нормализацией даты
const taskCopy = ref<EditableTask>({
  ...props.task,
  due_date: props.task.due_date ? new Date(props.task.due_date) : null,
});


// обновление задачи (отправка на сервер)

let updateTimeout: ReturnType<typeof setTimeout>;

const updateTask = (task: EditableTask) => {
  clearTimeout(updateTimeout)

  updateTimeout = setTimeout(() => {
    const preparedTask: Task = {
      ...task,
      due_date: task.due_date ? task.due_date.toISOString() : null,
    };

    if (JSON.stringify(preparedTask) === JSON.stringify(props.task)) return;

    taskStore.updateTask(preparedTask);
  }, 500)
};

// следим за изменениями пропса (например, если обновился извне)
watch(
  () => props.task,
  (newValue) => {
    if (JSON.stringify(newValue) !== JSON.stringify(taskCopy.value)) {
      taskCopy.value = {
        ...newValue,
        due_date: newValue.due_date ? new Date(newValue.due_date) : null,
      };
    }
  },
  { deep: true }
);

watch(() => taskCopy.value.priority, () => updateTask(taskCopy.value))
watch(() => taskCopy.value.completed, () => updateTask(taskCopy.value))
</script>

<template>
  <form class="task-card">
    <div class="task-card__header">
      <CustomDatePicker v-model="taskCopy.due_date" @update:modelValue="updateTask(taskCopy)" />
      <div class="task-card__header-divider"></div>
      <SelectSmall v-model="taskCopy.priority"
                   :options="PRIORITIES"
                   icon="flag"
                   :with-label="true"
      />
    </div>

    <div class="task-card__title-wrapper">
      <TaskCheckbox v-model="taskCopy.completed"
                    :priority="taskCopy.priority.toLowerCase()"/>
      <input
        class="task-card__title"
        type="text"
        v-model="taskCopy.title"
        @blur="updateTask(taskCopy)"
      >
    </div>

  </form>
</template>

<style scoped lang="scss">
.task-card {
  padding: 30px;
  border-radius: 15px;
  height: 100%;
  width: 100%;
  box-shadow: 0 0 6px 0 rgba(0, 0, 0, 0.07);
  background: var(--bg-highlight);

  &__header {
    display: flex;
    align-items: center;
    gap: 8px;

    margin-bottom: 24px;
  }

  &__header-divider {
    width: 1px;
    height: 14px;
    background: var(--text-primary-disabled);
  }

  &__title-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  &__title {
    padding: 0;
    background: transparent;
    border: none;
    outline: none;
    font: var(--bold-18);
    color: var(--text-primary);
  }
}
</style>
