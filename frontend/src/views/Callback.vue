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
      const res = await fetch(`http://127.0.0.1:8000/api/auth/google/callback?code=${code}&state=${state}`);
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      const data = await res.json(); // преобразуем ответ в JSON
      const refreshJwtToken = data.refresh_jwt;
      const accessJwtToken = data.access_jwt;
      const created = data.created;

      console.log('Logged in successfully:', data);

      document.cookie = `refresh_jwt=${refreshJwtToken}; Path=/`;
      document.cookie = `access_jwt=${accessJwtToken}; Path=/`;
    } catch (err) {
      error.value = err.response?.data || err.message;
    } finally {
      loading.value = false;
    }
  } else {
    error.value = 'Invalid callback parameters or state mismatch';
    loading.value = false;
  }
});
</script>


<template>
  <div>
    <h1>You are logged in!</h1>
    <p v-if="loading">Logging in...</p>
    <p v-else-if="error">Error: {{ error }}</p>
  </div>
</template>
