<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import Dropdown from "@/components/ui-kit/Dropdown.vue";
import NavLink from "@/components/ui-kit/NavLink.vue";
import { SelectSmallOption } from "@/types/selectSmallOption";
import { useDropdown } from "@/components/composables/useDropdown";

const props = withDefaults(
  defineProps<{
    icon: string;
    options: SelectSmallOption[];
    modelValue?: SelectSmallOption | null;
  }>(),
  {
    modelValue: null,
  }
);

const emit = defineEmits<{
  (e: "update:modelValue", value: SelectSmallOption | null): void;
}>();

// теперь через computed get/set вместо watch
const activeOption = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

const buttonColor = computed(() => {
  if (!activeOption.value) return "inactive";
  return activeOption.value.color ?? "active";
});

const rootEl = ref<HTMLElement | null>(null);
const { isOpen, toggle, close } = useDropdown(rootEl);

const toggleActiveOption = (option: SelectSmallOption) => {
  activeOption.value =
    activeOption.value?.value === option.value ? null : option;
  close();
};

// закрытие по ESC
const onKeydown = (e: KeyboardEvent) => {
  if (e.key === "Escape") close();
};

onMounted(() => document.addEventListener("keydown", onKeydown));
onBeforeUnmount(() => document.removeEventListener("keydown", onKeydown));
</script>

<template>
  <div class="select-small" ref="rootEl">
    <button type="button"
      class="select-small__button"
      :class="buttonColor"
      @click.prevent="toggle"
    >
      <svg class="select-small__icon" width="16" height="16">
        <use :href="`#${icon}`"></use>
      </svg>
    </button>

    <Dropdown class="select-small__dropdown" v-if="isOpen">
      <NavLink
        v-for="(option, i) in options"
        :key="i"
        :text="option.label"
        :leftIcon="option.icon || undefined"
        :rightIcon="option.value === activeOption?.value ? 'check-active' : undefined"
        :class="{ [option.color || '']: !!option.color }"
        @click="toggleActiveOption(option)"
      />
    </Dropdown>
  </div>
</template>

<style lang="scss">
@use "@/assets/scss/mixins/mixins" as *;

.select-small {
  position: relative;

  &__button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: transparent;
    border: none;
    outline: none;
    padding: 2px;
    border-radius: 4px;
    color: var(--icon-inactive);
    cursor: pointer;

    @include hover {
      background: var(--bg-primary-hover);
    }

    &.active svg {
      color: var(--text-accent);
    }
  }

  &__dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-width: 212px;
  }

  .inactive svg {
    color: var(--icon-inactive);
  }

  .medium svg {
    color: var(--medium);
  }

  .high svg {
    color: var(--text-error);
  }
}
</style>
