import { ref } from 'vue'
import { defineStore } from 'pinia'
import { BASE_API_URL } from '@/config';

export const useAccessTokenStore = defineStore('access-tocken', () => {
  const accessTocken = ref(null)

  const setAccessTocken = (newAccessTocken) => {
    accessTocken.value = newAccessTocken
  }

  const getAccessTocken = () => {
    return accessTocken.value
  }

  const refreshAccessTocken = async () => {
    const response = await fetch(`${BASE_API_URL}/api/users/refresh/`, {
      method: 'POST',
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      console.log(data)
      setAccessTocken(data.access_jwt)
    } else {
      throw new Error('Failed to refresh access tocken')
    }
  }

  return { setAccessTocken, getAccessTocken, refreshAccessTocken }
})
