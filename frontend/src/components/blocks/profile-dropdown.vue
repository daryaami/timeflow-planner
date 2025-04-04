<script setup lang="ts">
import ProfilePlaceholderIcon from "@/assets/img/profile-placeholder.svg?url";
import { useProfileStore } from "@/store/profile.ts";
import {ref, onMounted} from "vue";

const profileStore = useProfileStore();
const name = ref<string>('');
const profilePic = ref<string>(ProfilePlaceholderIcon);

onMounted(async () => {
  const profileData = await profileStore.getProfileData()

  if (!profileData) return

  name.value = profileData.name;
  profilePic.value = profileData.picture;
})
</script>

<template>
<div class="profile-dropdown">
  <img class="profile-dropdown__img" :src="profilePic" :alt="name" width="40" height="40">
</div>
</template>

<style scoped lang="scss">
.profile-dropdown {
  &__img {
    border-radius: 50%;
  }
}
</style>
