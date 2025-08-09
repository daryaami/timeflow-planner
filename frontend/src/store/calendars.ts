import {ref} from "vue";
import {useAuthStore} from "@/store/auth";
import {BASE_API_URL} from "@/config";

export const useCalendarsStore = () => {
  const calendars = ref()

  const fetchCalendars = async () => {
    const authStore = useAuthStore();

    const fetchFn = () =>
      fetch(`${BASE_API_URL}/events/calendars/`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`
        }
      })

    const response = await authStore.ensureAuthorizedRequest(fetchFn)
    calendars.value = await response.json()
  }

  const getCalendars = async () => {
    if (!calendars.value) {
      await fetchCalendars();
    }

    return calendars.value
  }


  return { getCalendars }
}
