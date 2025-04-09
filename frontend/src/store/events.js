import { defineStore } from 'pinia'
import { ref } from 'vue'

import {BASE_API_URL} from "@/config.js";
import {useAuthStore} from "@/store/auth.ts";

export const useEventsStore = defineStore('events', () => {
  const events = ref([]);

  const fetchEvents = async () => {
    const accessTokenStore = useAuthStore();
    const response = await fetch(`${BASE_API_URL}/api/events/all/?start=2025-01-01&end=2025-12-31`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${accessTokenStore.getAccessToken()}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      events.value = data.events;
    }
  }

  return { events, fetchEvents }
})
