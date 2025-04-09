import { ref } from 'vue'
import { defineStore } from 'pinia'
import { BASE_API_URL } from '@/config.js';
import { useRouter } from 'vue-router';

const router = useRouter()

export const useAuthStore = defineStore('access-token', () => {
  const accessToken = ref<string | null>(null)

  const setAccessToken = (newAccessToken: string) => {
    accessToken.value = newAccessToken
    localStorage.setItem('accessToken', newAccessToken)
  }

  const getAccessToken = () => {
    if (!accessToken.value) {
      const token: string = localStorage.getItem('accessToken')

      if (!token) {
        alert('Токен не найден')
      }

      accessToken.value = token
    }
    return accessToken.value
  }

  const refreshAccessToken = async () => {
    const response = await fetch(`${BASE_API_URL}/api/users/refresh/`, {
      method: 'POST',
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      console.log(data)
      setAccessToken(data.access_jwt)
    } else {
      throw new Error('Failed to refresh access token')
    }
  }

  const checkTokens = async () => {
    if (accessToken.value) {

    } else {
      try {
        await refreshAccessToken()
      } catch (error) {
        await router.push('/login')
      }
    }
  }

  return { setAccessToken, getAccessToken, refreshAccessToken, checkTokens }
})
