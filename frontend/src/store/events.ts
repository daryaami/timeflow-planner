import { defineStore } from "pinia";
import { getMonthStartDates } from "@/components/js/time-utils";
import { formatDate } from "@/components/js/time-utils";
import { BASE_API_URL } from "@/config";
import { useAuthStore } from "./auth";
import { ref } from "vue"; // Импортируем ref
import type { EventInput } from "@fullcalendar/core";

export const useEventsStore = defineStore('events', () => {
  const events = ref([] as Array<EventInput>); // Используем ref для реакции на изменения
  let fetchedKeys = [] as Array<string>;
  const authStore = useAuthStore();

  const fetchEvents = async (startDate: Date, endDate: Date) => {
    const monthsToFetch = getMonthStartDates(startDate, endDate)
      .filter(monthStart => !fetchedKeys.includes(monthStart));

    if (monthsToFetch.length === 0) {
      return { json: async () => [] };
    }

    const result = await fetch(`${BASE_API_URL}/events/?start=${formatDate(startDate)}&end=${formatDate(endDate)}`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${authStore.getAccessToken()}`
      }
    });

    fetchedKeys = [...fetchedKeys, ...monthsToFetch];

    return result;
  }

  const adaptEventToFullCalendar = (event: any) => {
    return {
      id: event.id,
      title: event.summary,
      start: event.start.dateTime,
      end: event.end?.dateTime,
      url: event.htmlLink,
      backgroundColor: '#49b5c4',
      borderColor: '#49b5c4',
    };
  }

  const getEvents = async (startDate: Date, endDate: Date) => {
    const result = await fetchEvents(startDate, endDate);
    const data: EventInput[] = await result.json();

    for (const event of data) {
      const alreadyExists = events.value.some(e => e.id === event.id); // Используем events.value для доступа
      if (!alreadyExists) {
        events.value.push(adaptEventToFullCalendar(event)); // Здесь тоже используем events.value
      }
    }

    return events.value;
  }

  return { events, getEvents }
});
