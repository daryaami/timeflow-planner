<script setup lang="ts">
import { useAuthStore } from '@/store/auth.js';

const authStore = useAuthStore()

const checkTokens = async () => {
  const isTokensValid = await authStore.checkTokens()
}

onMounted(() => {
  checkTokens()
})
</script>

<template>

</template>

<style scoped lang="scss">

</style>
