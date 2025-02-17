<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const accessToken = ref(null)

onMounted(async () => {
  const refresh_jwt = document.cookie.match(/refresh_jwt=([^;]+)/)[1];
  const access_jwt = document.cookie.match(/access_jwt=([^;]+)/)[1];
  const response = await axios.get('http://127.0.0.1:8000/api/auth/google/access/', {
    headers: {
      Authorization: `JWT ${access_jwt}`,
    },
  });
  accessToken.value = response.data.access_token;
  // обработка ошибки когда access_jwt устарел или не верный
})

</script>

<template>
  <div>
    {{ accessToken }}
  </div>
</template>
