<script setup>
import loaderVue from '../components/blocks/loaders/Loader.vue';

import { ref, onMounted } from 'vue';
import { useAccessTockenStore } from '@/store/access-tocken';

const accessTockenStore = useAccessTockenStore();

const loading = ref(true);
const error = ref(null);

onMounted(async () => {
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
      accessTockenStore.setAccessTocken(data.access_jwt);

      window.location.href = '/planner/';
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
    <loaderVue />
  </div>
</template>
