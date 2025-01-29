<template>
  <div>
    <button @click="loginWithGoogle">Login with Google</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async loginWithGoogle() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/auth/google/', { withCredentials: true });
        // localStorage.setItem('google_auth_state', response.data.google_auth_state);  // Сохраняем state на фронте
        // console.log(response.data.google_auth_state);
        window.location.href = response.data.auth_url;
      } catch (error) {
        console.error('Error initiating Google login:', error);
      }
    },
  },
};
</script>
