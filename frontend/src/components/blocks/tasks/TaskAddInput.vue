<script setup lang="ts">
import IconBtn from "@/components/ui-kit/IconBtn.vue";
import SelectSmall from "@/components/blocks/form/SelectSmall.vue";
import { selectSmallOption } from "@/types/selectSmallOption";
import { ref, computed, onMounted, onBeforeUnmount } from "vue";

const title = ref<string>("");
const priority = ref<selectSmallOption | null>(null);

const isFocused = ref(false);
const containerRef = ref<HTMLElement | null>(null);

const PRIORITIES: selectSmallOption[] = [
  {
    value: null,
    label: "No priority",
    icon: "flag",
    color: "inactive",
  },
  {
    value: "medium",
    label: "Medium",
    icon: "flag",
    color: "medium",
  },
  {
    value: "high",
    label: "High",
    icon: "flag",
    color: "high",
  },
];

function onClickOutside(e: MouseEvent) {
  if (containerRef.value && !containerRef.value.contains(e.target as Node)) {
    isFocused.value = false;
  }
}

function activateFocus() {
  isFocused.value = true;
}

const isExpanded = computed(() => isFocused.value || !!priority.value?.value);

onMounted(() => {
  document.addEventListener("click", onClickOutside);

  priority.value = PRIORITIES[0];
});
onBeforeUnmount(() => {
  document.removeEventListener("click", onClickOutside);
});
</script>

<template>
  <div
    ref="containerRef"
    class="task-add-input"
    :class="{ filled: title.length > 0, focus: isFocused }"
  >
    <div class="task-add-input__input-wrapper">
      <div class="task-add-input__placeholder">
        <svg width="16" height="16">
          <use href="#plus"></use>
        </svg>
        <span>Add task</span>
      </div>

      <input
        type="text"
        class="task-add-input__input"
        placeholder="What would you like to do?"
        v-model="title"
        @focus="activateFocus"
      />
    </div>

    <div class="task-add-input__buttons" v-if="isExpanded">
      <SelectSmall v-model="priority" :options="PRIORITIES" icon="flag" />

      <IconBtn
        type="submit"
        class="task-add-input__submit"
        icon="arrow-up"
        variant="accent"
        size="s"
        :disabled="title.length === 0"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.task-add-input {
  border: 1px solid var(--stroke-primary-invisible);
  border-radius: 8px;
  min-height: 33px;
  transition: 0.3s;

  &.focus {
    border-color: var(--bg-accent);
  }

  &.focus .task-add-input__placeholder,
  &.filled .task-add-input__placeholder {
    display: none;
  }

  &.filled .task-add-input__buttons {
    display: flex;
  }

  &__input-wrapper {
    position: relative;
  }

  &__input {
    border: none;
    outline: none;
    border-radius: 0;
    background: transparent;
    display: block;
    width: 100%;
    caret-color: var(--bg-accent);
    font: var(--light-14);
    padding: 7px 8px;

    &::placeholder {
      opacity: 0;
    }
  }

  &__placeholder {
    position: absolute;
    top: 50%;
    left: 18px;
    transform: translateY(-50%);
    color: var(--text-primary-disabled);
    font: var(--light-14);
    pointer-events: none;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  &__buttons {
    display: flex;
    padding: 4px 7px 7px 7px;
    align-items: center;
  }

  &__submit {
    margin-left: auto;
  }
}
</style>
