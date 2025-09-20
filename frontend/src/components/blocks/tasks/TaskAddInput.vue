<script setup lang="ts">
import IconBtn from "@/components/ui-kit/IconBtn.vue";
import {ref} from "vue";

const title = ref<string>('')
</script>

<template>
<div class="task-add-input" :class="{filled: title.length > 0}">
  <div class="task-add-input__input-wrapper">
    <div class="task-add-input__placeholder">
      <svg width="16" height="16">
        <use href="#plus"></use>
      </svg>

      <span>Add task</span>
    </div>
    <input type="text" class="task-add-input__input"
                          placeholder="What would you like to do?"
                          v-model="title" />
  </div>

  <div class="task-add-input__buttons">
    <IconBtn class="task-add-input__submit"
             icon="arrow-up"
             variant="accent"
             size="s"
             :disabled="title.length === 0" />
  </div>
</div>
</template>

<style scoped lang="scss">
.task-add-input {
  border: 1px solid var(--stroke-primary-invisible);
  border-radius: 8px;

  min-height: 33px;

  transition: .3s;

  &:has(:focus) {
    border-color: var(--bg-accent);

    & .task-add-input__placeholder {
      display: none;
    }

    & .task-add-input__input {
      &::placeholder {
        opacity: 1;
      }
    }

    & .task-add-input__buttons {
      display: flex;
    }
  }

  &.filled {
    & .task-add-input__buttons {
      display: flex;
    }

    & .task-add-input__placeholder {
      display: none;
    }
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
    display: none;
    padding: 4px 7px 7px 7px;

    align-items: center;
  }

  &__submit {
    margin-left: auto;
  }
}
</style>
