import { defineStore } from 'pinia'
import {getMonthStartDates, formatDate, addMinutes} from '@/components/js/time-utils'
import { BASE_API_URL } from '@/config'
import { useAuthStore } from './auth'
import { ref } from 'vue'
import type { EventInput } from '@fullcalendar/core'
import {DropArg} from "@fullcalendar/interaction";
import {useTasksStore} from "@/store/tasks";

export const useEventsStore = defineStore('events', () => {
  const events = ref([] as Array<EventInput>)
  let fetchedKeys = [] as Array<string>

  const authStore = useAuthStore()
  const taskStore = useTasksStore()

  const adaptEventToFullCalendar = (event: any): EventInput => {
    return {
      id: event.id,
      title: event.summary,
      start: event.start.dateTime,
      end: event.end?.dateTime,
      url: event.htmlLink,
      backgroundColor: event.color,
      borderColor: event.color,
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

  const createEvent = async (eventData: DropArg) => {
    const task = taskStore.getTaskById(Number(eventData.draggedEl.dataset.taskId))

    if (!task) return

    const data = {
      task_id: task.id,
      start: eventData.date.toISOString(),
      end: addMinutes(eventData.date, task.duration || 30).toISOString(),
      calendar_id: task.calendar
    }

    const response = await fetch(`${BASE_API_URL}/events/from-task/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `JWT ${authStore.getAccessToken()}`
      },
      body: JSON.stringify(data)
    })

    if (response.ok) {
      const event = await response.json()
      events.value.push(adaptEventToFullCalendar(event))
    }
  }

  const debounceMap = new Map<number, any>()

  const updateEventStart = (id: number, newStart: string) => {
    if (debounceMap.has(id)) {
      clearTimeout(debounceMap.get(id))
    }

    const timeout = setTimeout(async () => {
      debounceMap.delete(id) // Удаляем по завершении

      await fetch(`${BASE_API_URL}/events/`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          event_id: id,
          start: newStart
        })
      })
    }, 400)

    debounceMap.set(id, timeout)
  }

  return {
    events,
    getEvents,
    createEvent,
    updateEventStart
  }
})
