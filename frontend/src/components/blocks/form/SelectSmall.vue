<script setup lang="ts">
import {ref, watch, computed} from "vue";
import Dropdown from "@/components/ui-kit/Dropdown.vue";
import NavLink from "@/components/ui-kit/NavLink.vue";
import {selectSmallOption} from "@/types/selectSmallOption";
import {useDropdown} from "@/components/composables/useDropdown";

const props = withDefaults(defineProps<{
  icon: string,
  options: selectSmallOption[],
  modelValue?: selectSmallOption | null
}>(), {
  modelValue: null
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: selectSmallOption | null): void
}>()

const activeOption = ref<selectSmallOption | null>(props.modelValue);

const buttonColor = computed(() => {
  if (!activeOption.value) return null
  return activeOption.value.color ?? 'active'
})

const toggleActiveOption = (option: selectSmallOption) => {
  isOpen.value = false;

  if (activeOption.value?.value === option.value) {
    activeOption.value = null;
    return;
  }

  activeOption.value = option;
}

watch(() => props.modelValue, (newVal) => {
  activeOption.value = newVal;
});

watch(activeOption, (newVal) => {
  emit('update:modelValue', newVal);
});


const rootEl = ref<HTMLElement | null>(null);
const { isOpen, toggle } = useDropdown(rootEl);
</script>

<template>
  <div class="select-small" ref="rootEl">
    <button class="select-small__button"
            :class="buttonColor ? buttonColor : ''"
            @click.prevent="toggle">
      <svg class="select-small__icon"
           width="16"
           height="16"
           xmlns="http://www.w3.org/2000/svg">
        <use :href="`#${ icon }`"></use>
      </svg>
    </button>

    <Dropdown class="select-small__dropdown"
              v-if="isOpen">
      <NavLink v-for="(option, i) in options"
               :key="i"
               :text="option.label"
               :leftIcon="option.icon? option.icon : undefined"
               :rightIcon="option.value === activeOption?.value ? 'check-active' : undefined"
               :class="option.color ? option.color : ''"
               @click="toggleActiveOption(option)"
      />
    </Dropdown>
  </div>
</template>


<style lang="scss">
@use '@/assets/scss/mixins/mixins' as *;

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

    &.active {
      & svg {
        color: var(--text-accent);
      }
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
