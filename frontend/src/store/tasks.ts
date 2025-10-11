import {defineStore} from "pinia";
import {BASE_API_URL} from "@/config";
import {useAuthStore} from "@/store/auth"
import {ref} from "vue";
import {Task, TaskCreate} from "@/types/task";

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  let isInitialized = false;

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
    if (!isInitialized) {
      await fetchTasks()
      isInitialized = true
    }

    return tasks.value as Task[]
  }

  const createTask = async (payload: TaskCreate) => {
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

  const debounceMap = new Map<number, any>()

  const toggleCompleteTask = (id: number, isCompleted: boolean) => {
    // Если был предыдущий таймер — очищаем его
    if (debounceMap.has(id)) {
      clearTimeout(debounceMap.get(id))
    }

    // Создаём новый с задержкой (например, 400 мс)
    const timeout = setTimeout(async () => {
      debounceMap.delete(id) // Удаляем по завершении

      await fetch(`${BASE_API_URL}/tasks/${id}/`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ completed: isCompleted })
      })
    }, 400)

    debounceMap.set(id, timeout)
  }

  const getTaskById = (id: number) => {
    return tasks.value.find(task => task.id === id)
  }

  return {
    tasks,
    fetchTasks,
    getTasks,
    createTask,
    deleteTask,
    getTaskById,
    toggleCompleteTask
  }
})
