<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from '@/store/auth.ts';
import {useRouter} from "vue-router";

const authStore = useAuthStore()
const router = useRouter()

const checkTokens = async () => {
  const isTokensValid = await authStore.checkTokens()

  if (isTokensValid) await router.push('/planner')
}

onMounted(() => {
  checkTokens()
})
</script>

<template>

</template>

<style scoped lang="scss">

</style>
