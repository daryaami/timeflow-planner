<!-- // Это тестовая функция для проверки работы токенов JWT -->
<script setup>
import { ref, onMounted } from 'vue'

const accessToken = ref(null)

onMounted(async () => {
  const refresh_jwt = document.cookie.match(/refresh_jwt=([^;]+)/)[1];
  const access_jwt = document.cookie.match(/access_jwt=([^;]+)/)[1];
  const response = await fetch('http://127.0.0.1:8000/api/auth/google/access/', {
    headers: {
      Authorization: `JWT ${access_jwt}`,
    },
  }).then((res) => res.json());
  console.log(response);
  accessToken.value = response.access_token;
  // обработка ошибки когда access_jwt устарел или не верный
})

</script>

<template>
  <div>
    <h1>Your access token:</h1>
    {{ accessToken }}
  </div>
</template>
