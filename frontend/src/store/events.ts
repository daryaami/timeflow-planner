import { defineStore } from 'pinia'
import { getMonthStartDates, formatDate } from '@/components/js/time-utils'
import { BASE_API_URL } from '@/config'
import { useAuthStore } from './auth'
import { ref } from 'vue'
import type { EventInput } from '@fullcalendar/core'

export const useEventsStore = defineStore('events', () => {
  const events = ref([] as Array<EventInput>)
  let fetchedKeys = [] as Array<string>
  const authStore = useAuthStore()

  const adaptEventToFullCalendar = (event: any): EventInput => {
    return {
      id: event.id,
      title: event.summary,
      start: event.start.dateTime,
      end: event.end?.dateTime,
      url: event.htmlLink,
      backgroundColor: '#49b5c4',
      borderColor: '#49b5c4',
    }
  }

  const fetchEvents = async (startDate: Date, endDate: Date) => {
    const monthsToFetch = getMonthStartDates(startDate, endDate)
      .filter(monthStart => !fetchedKeys.includes(monthStart))

    if (monthsToFetch.length === 0) {
      return { json: async () => [] }
    }

    const fetchFn = () =>
      fetch(`${BASE_API_URL}/events/?start=${formatDate(startDate)}&end=${formatDate(endDate)}`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`
        }
    })

    const response = await authStore.ensureAuthorizedRequest(fetchFn)

    fetchedKeys = [...fetchedKeys, ...monthsToFetch]

    return response
  }

  const getEvents = async (startDate: Date, endDate: Date) => {
    const result = await fetchEvents(startDate, endDate)
    const data: EventInput[] = await result.json()

    for (const event of data) {
      const alreadyExists = events.value.some(e => e.id === event.id)
      if (!alreadyExists) {
        events.value.push(adaptEventToFullCalendar(event))
      }
    }

    return events.value
  }

  return { events, getEvents }
})
