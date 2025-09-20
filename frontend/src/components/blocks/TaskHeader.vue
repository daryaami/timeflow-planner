<script setup lang="ts">
import BtnContainer from "@/components/ui-kit/BtnContainer.vue";
import {Button} from "@/types/button";
import ProfileDropdown from "@/components/blocks/profile-dropdown.vue";
import RoundIconButton from "@/components/ui-kit/RoundIconButton.vue";

defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: Object || null,
    default: null
  }
})

const sortingButtons: Button[] = [
  {
    icon: 'filter',
    text: 'Filter'
  },
  {
    icon: 'sort',
    text: 'Sort'
  }
]
</script>

<template>
  <div class="task-header">
    <div class="task-header__title-wrapper">
      <component :is="icon" v-if="icon" width="26" height="26"/>
      <h1 class="task-header__title">{{ title }}</h1>
    </div>

    <div class="task-header__btns">
      <BtnContainer size="l"
                    :buttons="sortingButtons" />

      <RoundIconButton icon="search"/>
      <RoundIconButton icon="dots"/>
    </div>


    <ProfileDropdown />
  </div>
</template>

<style scoped lang="scss">
.task-header {
  padding: 15px 38px;

  margin-bottom: 24px;

  display: flex;
  align-items: center;
  gap: 44px;

  &__title-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  &__title {
    font: var(--bold-24);

    margin: 0;
  }

  & .profile-dropdown {
    margin-left: auto;
  }

  &__btns {
    display: flex;
    align-items: center;
    gap: 15px;
  }
}
</style>
