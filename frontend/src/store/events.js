import { defineStore } from "pinia";
import { ref } from 'vue';
import { getCurrentWeekMonday, isSameDay } from '@/components/js/time-utils';
import { BASE_API_URL } from '@/config';

import { useAccessTockenStore } from '@/store/access-tocken';

export const useEventsStore = defineStore("events", () => {
  const events = ref([]);
  const loadedMondays = [];

  const getEvents = async (date = new Date()) => {
    const monday = getCurrentWeekMonday(date)
    const accessTockenStore = useAccessTockenStore();

    if (loadedMondays.filter(item => isSameDay(monday, item)).length) {
      return events.value
    }

    let response = await fetch(`${BASE_API_URL}/api/events/all/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${accessTockenStore.getAccessTocken()}`,
      }
    }
    );

    if (response.ok) {
      const data = await response.json();
      events.value = [...events.value, ...data].reduce((acc, current) => {
        const x = acc.find(item => item.id === current.id);
        if (!x) {
          acc.push(current);
        }
        return acc;
      }, [])

      loadedMondays.push(monday);
      return data.events;
    } else if (response.status === 401) {
      accessTockenStore.refreshAccessTocken()
    } else {
      throw new Error('Failed to fetch events');
    }
  }

  const update = (newEvents) => {
    events.value = [...events.value, ...newEvents];
  }

  return {
    events,
    loadedMondays,
    getEvents,
    update,
  }
})

