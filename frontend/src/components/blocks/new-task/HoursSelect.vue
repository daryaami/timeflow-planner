<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useDropdown } from "@/components/composables/dropdown";
import { useUserDataStore } from "@/store/profile.js";

const { isDropdownOpen, dropdownClickHandler, closeDropdown } = useDropdown();
const userDataStore = useUserDataStore()

const currentValue = defineModel();

const hours = computed(() => userDataStore.userData.hours)
const currentOption = ref(userDataStore.userData.hours[0])

watch(hours, (newValue) => {
  currentOption.value = newValue[0];
})

const optionClickHandler = (option) => {
  currentOption.value = option;
  closeDropdown();
}

watch(currentOption, (newValue) => {
  currentValue.value = newValue.id;
})


onMounted(async () => {
  currentOption.value = hours.value[0];
})
</script>

<template>
  <div class="hours-select input dropdown-wrapper">
    <div @click="dropdownClickHandler" class="input__input">
      <span v-if="currentOption">{{ currentOption.name }}</span>
      <div class="hours-select__arrow"
        :class="{'rotated': isDropdownOpen}"
      ></div>
    </div>
    <span class="input__label">Hours</span>
    <Transition name="dropdown">
      <ul v-if="isDropdownOpen && hours"  class="hours-select__dropdown">
        <li class="hours-select__dropdown-item"
          v-for="(option, i) in hours"
          :key="i"
        >
          <div class="hours-select__dropdown-button"
            @click.stop="optionClickHandler(option)"
            tabindex="0"
          >
            <span>{{ option.name }}</span>
          </div>
        </li>
      </ul>
    </Transition>
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/mixins.scss' as *;

.hours-select {
  cursor: pointer;
  margin-bottom: 30px;

  &__arrow {
    // @include chevron-down;
    background-size: 100% 100%;
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    transition: .2s;

    &.rotated {
      transform: translateY(-50%) rotate(-180deg);
    }
  }

  &__dropdown {
    @include reset-list;
    position: absolute;
    top: 100%;
    left: 0;
    padding-top: 17px;
    padding-bottom: 16px;
    border-radius: 15px;
    width: 100%;
    background: #ebf6ff;
    z-index: 100;
  }

  &__dropdown-item {
    @include light-16;

    & svg {
      display: block;
      width: 17px;
      height: 17px;
    }
  }

  &__dropdown-button {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 9px 21px 9px 21px;
    width: 100%;
    cursor: pointer;

    & span {
      white-space: nowrap;
    }

    @include hover {
      background: #dee8f0;
    }
  }
}
</style>
