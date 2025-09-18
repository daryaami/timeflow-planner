<script setup lang="ts">
import VueDatePicker from "@vuepic/vue-datepicker";

const props = defineProps({
  placeholder: {
    type: String || null,
    default: null
  },
});

const ui = {
  input: 'select-button-small',
}
</script>

<template>
  <VueDatePicker
    :ui="ui"
    :placeholder="placeholder"
  >
    <template #input-icon>
      <svg class="select-button-small__icon" width="16" height="16" xmlns="http://www.w3.org/2000/svg">
        <use href="#date-range"></use>
      </svg>
    </template>
  </VueDatePicker>
</template>

<style lang="scss" scoped>
@use '@/assets/scss/mixins/mixins.scss' as *;

div:has(.select-button-small) {
  width: fit-content!important;
}
.dp__input_wrap {
  .select-button-small {
    font: var(--light-11);
    color: var(--text-primary-disabled);
    padding: 4px 2px 4px 20px;
    border: none;
    border-radius: 4px;

    &:placeholder-shown {
      width: 43px;
    }

    @include hover {
      background: var(--bg-primary-hover);
    }

    &__icon {
      position: absolute;
      left: 2px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
    }
  }
}

.dp--arrow-btn-nav {
  order: 1;
}

</style>
