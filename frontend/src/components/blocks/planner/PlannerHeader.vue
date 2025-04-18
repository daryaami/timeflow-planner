<script setup>
import RoundTextBtn from "@/components/blocks/buttons/round-text-btn.vue";
import {useCurrentDateStore} from "@/store/currentDate.js";
import {computed} from "vue";
import IconBtn from "@/components/blocks/buttons/icon-btn.vue";
import ProfileDropdown from "@/components/blocks/profile-dropdown.vue";

const currentDate = useCurrentDateStore();

const emit = defineEmits(['nextWeek', 'prevWeek', 'today'])

const currentMonth = computed(() => {
  if (currentDate.date) {
    const now = currentDate.date;
    return `${now.toLocaleString('default', { month: 'long' })} ${now.getFullYear()}`;
  } else {
    return ''
  }
})
</script>


<template>
  <div class="planner-header">
    <div class="planner-header__left-col">
      <RoundTextBtn text="Today"
                    @click="emit('today')"
      />
      <div class="planner-header__chevrons">
        <IconBtn
          icon="#chevron-left"
          size="s"
          @click="emit('prevWeek')"
        />
        <IconBtn
          icon="#chevron-right"
          size="s"
          @click="emit('nextWeek')"
        />
      </div>
      <span class="planner-header__date">{{ currentMonth }}</span>
    </div>

    <div class="planner-header__right-col">
      <RoundTextBtn
        text="Week"
        icon="#chevron-down"
      />
      <IconBtn class="planner-header__settings"
        icon="#settings"
        size="s"
      />

      <ProfileDropdown />
    </div>


  </div>
</template>


<style lang="scss">

.planner-header {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 15px 35px;

  &__left-col {
    display: flex;
    align-items: center;
    gap: 18px;
  }

  &__date {
    font: var(--bold-24);
  }

  &__chevrons {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  &__right-col {
    display: flex;
    align-items: center;
    margin-left: auto;
  }

  &__settings {
    margin-left: 36px;
    margin-right: 27px;
  }
}
</style>
