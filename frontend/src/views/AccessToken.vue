<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const accessToken = ref(null)

onMounted(async () => {
  const jwt = document.cookie.match(/jwt=([^;]+)/)[1];
  const response = await axios.get('http://127.0.0.1:8000/api/auth/google/access/', {
    headers: {
      Authorization: `JWT ${jwt}`,
    },
  });
  accessToken.value = response.data.access_token;
})

</script>

<template>
  <div>
    {{ accessToken }}
  </div>
</template>
