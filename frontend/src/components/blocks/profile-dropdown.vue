<script setup>
import ProfilePlaceholderIcon from "@/assets/img/profile-placeholder.svg?url";
import { useProfileStore } from "@/store/profile.js";
import { onMounted } from "vue";

const profileStore = useProfileStore();

const fetchData = async () => {
  try {
    await profileStore.fetchProfileData();
  } catch (error) {
    console.error('ошибка', error);
  }
}

onMounted(() => {
  fetchData();
})
</script>

<template>
<div class="profile-dropdown">
  <img class="profile-dropdown__img" :src="ProfilePlaceholderIcon" width="40" height="40">
</div>
</template>

<style scoped lang="scss">

</style>
