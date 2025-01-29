<template>
  <div>
    <p v-if="loading">Logging in...</p>
    <p v-else-if="error">Error: {{ error }}</p>
    <!-- <p v-else>Welcome, {{ user.user_info.name }}</p> -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: true,
      error: null,
      user: null,
    };
  },
  async created() {
    const queryParams = new URLSearchParams(window.location.search);
    const code = queryParams.get('code');
    const state = queryParams.get('state');
    // const storedState = localStorage.getItem('google_auth_state');  // Получаем сохраненный state

    if (code && state) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/auth/google/callback?code=${code}&state=${state}`);
        const jwtToken = response.data.jwt;
        const created = response.data.created;
        document.cookie = `jwt=${jwtToken}; Path=/`;
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
