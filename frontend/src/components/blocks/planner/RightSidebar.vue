<script setup>
// import { onMounted, ref, watch, computed } from 'vue';
// import { useProfileStore } from '@/store/profile.js';
//
// import TaskItemVue from './TaskItem.vue';
//
// const userDataStore = useProfileStore()
//
// const underlineRight = ref();
// const underlineLeft = ref();
// const habitsButton = ref(null);
// const tasksButton = ref(null);
// const activeTab = ref(null);
//
// const tasks = computed(() => userDataStore.userData.tasks);
//
// onMounted(() => {
//   activeTab.value = tasksButton.value;
// })
//
// watch(activeTab, () => {
//   underlineRight.value.style.transform = `translateX(${activeTab.value.offsetLeft}px)`;
//   underlineLeft.value.style.transform = `translateX(${activeTab.value.offsetLeft}px)`;
// })
</script>

<template>
  <div class="right-sidebar">
<!--    <div class="right-sidebar__tabs">-->
<!--      &lt;!&ndash; <button-->
<!--        ref="habitsButton"-->
<!--        class="right-sidebar__tab"-->
<!--        @click="activeTab = habitsButton"-->
<!--      >-->
<!--        <span>Habits</span>-->
<!--      </button> &ndash;&gt;-->
<!--      <button-->
<!--        ref="tasksButton"-->
<!--        class="right-sidebar__tab"-->
<!--        @click="activeTab = tasksButton"-->
<!--      >-->
<!--        <span>Tasks</span>-->
<!--      </button>-->
<!--      <div-->
<!--        class="underline"-->
<!--      >-->
<!--        <div ref="underlineRight" class="underline__closer underline__closer&#45;&#45;right"></div>-->
<!--        <div ref="underlineLeft" class="underline__closer underline__closer&#45;&#45;left"></div>-->
<!--      </div>-->
<!--    </div>-->
<!--    <div class="tasks"-->
<!--      v-if="activeTab === tasksButton"-->
<!--    >-->
<!--      <TaskItemVue-->
<!--        v-for="task in tasks"-->
<!--        :key="task.id"-->
<!--        :task='task'-->
<!--      />-->
<!--    </div>-->
  </div>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@use '@/assets/scss/colors.scss' as *;

.right-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;

  &__tabs {
    display: flex;
    position: relative;
  }

  &__tab {
    @include reset-button;
    @include light-24;
    flex-basis: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 65px;
  }
}

.underline {
  position: absolute;
  bottom: 0;
  left: 0;
  display: block;
  height: 3px;
  width: 100%;
  background: linear-gradient(to right,#0AA0DA 0%, #67DEC9 50%, #0AA0DA 100%);
  transition: .3s;
  overflow: hidden;

  &__closer {
    width: 50%;
    height: 100%;
    position: absolute;
    top: 0;
    background: white;
    transform: translateX(0);
    transition: .15s;

    &--right {
      right: 100%;
    }

    &--left {
      right: 0%;
    }
  }
}

.tasks {
  background-color: $dark-white;
  width: 100%;
  flex-basis: 100%;
  flex-shrink: 1;
  padding: 34px 16px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
</style>
