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
        const response = await axios.get(`http://127.0.0.1:8000/api/auth/google/callback?code=${code}&state=${state}`);
        const refreshJwtToken = response.data.refresh_jwt;
        const accessJwtToken = response.data.access_jwt;
        const created = response.data.created;
        document.cookie = `refresh_jwt=${refreshJwtToken}; Path=/`;
        document.cookie = `access_jwt=${accessJwtToken}; Path=/`;
      } catch (err) {
        this.error = err.response?.data || err.message;
      } finally {
        this.loading = false;
      }
    } else {
      this.error = 'Invalid callback parameters or state mismatch';
      this.loading = false;
    }
  },
};
</script>
