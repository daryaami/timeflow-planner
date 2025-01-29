<template>
  <div>
    <h1>HELLOHELLO</h1>
    <p v-if="loading">Logging in...</p>
    <p v-else-if="error">Error: {{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  console.log('Mounted');
  const queryParams = new URLSearchParams(window.location.search);
  const code = queryParams.get('code');
  const state = queryParams.get('state');

  if (code && state) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/auth/google/callback?code=${code}&state=${state}`);
      const data = await response.json();
      const jwtToken = data.jwt;
      const created = data.created;
      document.cookie = `jwt=${jwtToken}; Path=/`;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  } else {
    error.value = 'Invalid callback parameters or state mismatch';
    loading.value = false;
  }
});
</script>
