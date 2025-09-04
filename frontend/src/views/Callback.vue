<script setup>
import loaderVue from '../components/blocks/loaders/Loader.vue';

import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth.ts';
import { useRouter } from 'vue-router';

import {BASE_API_URL} from "../config.ts";


const accessTokenStore = useAuthStore();
const router = useRouter();

const loading = ref(true);

onMounted(async () => {
  const queryParams = new URLSearchParams(window.location.search);
  const code = queryParams.get('code');
  const state = queryParams.get('state');

  if (code && state) {
    try {
      const res = await fetch(`${BASE_API_URL}/auth/google/callback?code=${code}&state=${state}`);

      if (!res.ok) {
        const data = await res.json();

        if (data.code === 'google_auth_error') {
          await router.push('/login/?consent=true')
        }
      }

      const data = await res.json(); // преобразуем ответ в JSON
      accessTokenStore.setAccessToken(data.access_jwt);

      await router.push('/planner/')
    } catch (err) {
      console.log(err.message)
    } finally {
      loading.value = false;
    }
  } else {
    loading.value = false;
  }
});
</script>


<template>
  <div>
    <loaderVue />
  </div>
</template>
