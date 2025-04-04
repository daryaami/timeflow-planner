import { defineStore } from 'pinia'
import { ref } from 'vue'

import {BASE_API_URL} from "@/config.js";
import {useAccessTokenStore} from "@/store/access-token.js";

export const useEventsStore = defineStore('events', () => {
  const events = ref([]);

  const fetchEvents = async () => {
    const accessTokenStore = useAccessTokenStore();
    const response = await fetch(`${BASE_API_URL}/api/events/all/`, {
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
