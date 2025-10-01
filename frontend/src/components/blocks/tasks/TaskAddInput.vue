<script setup lang="ts">
import IconBtn from "@/components/ui-kit/IconBtn.vue";
import SelectSmall from "@/components/blocks/form/SelectSmall.vue";
import { selectSmallOption } from "@/types/selectSmallOption";
import { ref, computed, onMounted } from "vue";
import { useCategoriesStore } from "@/store/categories";
import { Category } from "@/types/category";
import { useClickOutside } from "@/components/composables/useClickOutside";
import CustomDatePicker from "@/components/blocks/form/CustomDatePicker.vue";

const categoriesStore = useCategoriesStore();

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

const categories = ref<Category[]>([]);

const categoriesOptions = computed(() =>
  categories.value.map(
    (category) => {
      return {
        label: category.name,
        value: category.id.toString(),
        icon: category.name.toLowerCase(),
      } as selectSmallOption
    }
  )
);

const title = ref<string>("");
const priority = ref<selectSmallOption | null>(null);
const category = ref<selectSmallOption | null>(null);
const dueDate = ref<Date | null>(null);

const isFocused = ref(false);
const containerRef = ref<HTMLElement | null>(null);

useClickOutside(containerRef, () => {
  isFocused.value = false;
});

const activateFocus = () => {
  isFocused.value = true;
};

const isExpanded = computed(
  () => isFocused.value || !!priority.value?.value || title.value.length > 0 || !!dueDate.value || !!category.value?.value
);

onMounted(async () => {
  priority.value = PRIORITIES[0];
  categories.value = await categoriesStore.getCategories();
});
</script>

<template>
  <div
    ref="containerRef"
    class="task-add-input"
    :class="{ filled: title.length > 0, focus: isFocused }"
  >
    <div class="task-add-input__input-wrapper">
      <div class="task-add-input__placeholder" :class="{ hidden: isFocused || title.length > 0 }">
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
        autocomplete="off"
        spellcheck="false"
      />
    </div>

    <div class="task-add-input__buttons" v-if="isExpanded">
      <CustomDatePicker v-model="dueDate" />

      <SelectSmall v-model="priority" :options="PRIORITIES" icon="flag" />

      <SelectSmall
        v-if="categoriesOptions.length > 0"
        v-model="category"
        :options="categoriesOptions"
        icon="tag"
      />

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
  transition: border-color 0.3s ease;

  &.focus {
    border-color: var(--bg-accent);
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
    opacity: 1;
    transition: opacity 0.2s ease;

    &.hidden {
      opacity: 0;
    }
  }

  &__buttons {
    padding: 4px 7px 7px 7px;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  &__submit {
    margin-left: auto;
  }
}
</style>
