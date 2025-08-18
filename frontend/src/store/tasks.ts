import {defineStore} from "pinia";
import {BASE_API_URL} from "@/config";
import {useAuthStore} from "@/store/auth"
import {ref} from "vue";

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref(null)

  const authStore = useAuthStore()


  const createTask = async (data: object) => {
    await fetch(`${BASE_API_URL}/tasks/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${authStore.getAccessToken()}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    await fetchTasks()
  }

  const fetchTasks = async () => {
    const fetchFn = () => fetch(`${BASE_API_URL}/tasks`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`
        }
      })

    const response = await authStore.ensureAuthorizedRequest(fetchFn)
    tasks.value = await response.json()
  }

  const getTasks = async () => {
    if (!tasks.value) {
      await fetchTasks()
    }

    return tasks.value
  }

  return { tasks, fetchTasks, getTasks, createTask }
})
