<script setup>
import { nextTick, ref } from 'vue';

import NewTaskForm from './NewTaskForm.vue';

const isPopupOpened = ref(false);
const popup = ref(null)
const isLoading = ref(false)

const handleClickOutside = (event) => {
  if (!event.target.closest('.new-task__popup') && !event.target.closest('.new-task__button')) {
    closePopup();
  }
}

const openPopup = async () => {
  isPopupOpened.value = true;
  await nextTick();
  popup.value.show();
  document.addEventListener('click', handleClickOutside);
}

const closePopup = () => {
  if (isLoading.value) return
  isPopupOpened.value = false;
  document.removeEventListener('click', handleClickOutside);
}

const openButtonHandler = () => {
  isPopupOpened.value? closePopup(): openPopup();
}

const loadingUpdateHandler = (newValue) => {
  isLoading.value = newValue;
}
</script>

<template>
  <div class="new-task">
    <button class="new-task__button" @click="openButtonHandler">+ New Task</button>
    <Transition name="dropdown">
      <dialog class="new-task__popup" v-if="isPopupOpened" ref="popup">
        <button class="new-task__close-button icon-button" @click="closePopup"></button>
          <new-task-form
              @loading-update="loadingUpdateHandler"
            />
      </dialog>
    </Transition>
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/mixins.scss' as *;

.new-task {
    position: relative;

    &__button {
      @include reset-button;
      @include light-24;

      @include hover {
        color: $light-grey;
      }
    }

    &__popup {
      position: absolute;
      top: 0;
      right: 0;
      left: auto;
      padding: 70px 52px 40px 42px;
      box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.3);
      background-color: #ffffff;;
      border-radius: 15px;
      z-index: 1000;
      border: none;
    }

    &__close-button {
      @include reset-button;
      // @include close-icon;
      background-size: 20px 20px;
      background-position: center;
      position: absolute;
      right: 32px;
      top: 25px;
      height: 32px;
      width: 32px;
    }
  }
</style>
