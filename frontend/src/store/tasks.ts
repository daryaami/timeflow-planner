import {defineStore} from "pinia";
import {BASE_API_URL} from "@/config";
import {useAuthStore} from "@/store/auth"
import {ref} from "vue";
import {Task} from "@/types/task";

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])

  const authStore = useAuthStore()

  const fetchTasks = async () => {
    const fetchFn = () => fetch(`${BASE_API_URL}/tasks`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`
        }
      })

    const response = await authStore.ensureAuthorizedRequest(fetchFn)
    tasks.value = await response.json() as Task[]
  }

  const getTasks = async (): Promise<Task[]> => {
    if (!tasks.value || !tasks.value.length) {
      await fetchTasks()
    }

    return tasks.value as Task[]
  }

  const createTask = async (payload: object) => {
    // @TO-DO Типизировать payload
    await fetch(`${BASE_API_URL}/tasks/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${authStore.getAccessToken()}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    await fetchTasks()
  }

  const deleteTask = async (id: number) => {
    await fetch(`${BASE_API_URL}/tasks/${id}/`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${authStore.getAccessToken()}`,
        'Content-Type': 'application/json'
      }
    })

    await fetchTasks()
  }

  return { tasks, fetchTasks, getTasks, createTask, deleteTask }
})
