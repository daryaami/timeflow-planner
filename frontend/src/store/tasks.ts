import {defineStore} from "pinia";
import {BASE_API_URL} from "@/config";
import {useAuthStore} from "@/store/auth";

export const useTasksStore = defineStore('tasks', () => {
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
  }

  return { createTask }
})
