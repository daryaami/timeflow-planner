import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { BASE_API_URL } from '@/config'

export const useAuthStore = defineStore('access-token', () => {
  const accessToken = ref<string | null>(null)
  const router = useRouter()

  const setAccessToken = (newAccessToken: string) => {
    accessToken.value = newAccessToken
    localStorage.setItem('accessToken', newAccessToken)
  }

  const getAccessToken = () => {
    if (!accessToken.value) {
      accessToken.value = localStorage.getItem('accessToken')
    }
    return accessToken.value
  }

  const refreshAccessToken = async () => {
    const response = await fetch(`${BASE_API_URL}/users/refresh/`, {
      method: 'POST',
      credentials: 'include',
    })

    if (response.ok) {
      const data = await response.json()
      setAccessToken(data.access_jwt)
    } else {
      throw new Error('Failed to refresh access token')
    }
  }

  const ensureAuthorizedRequest = async (fetchFn: () => Promise<Response>) => {
    let response = await fetchFn()

    if (response.status === 401) {
      try {
        await refreshAccessToken()
        response = await fetchFn()
      } catch (e) {
        await router.push('/login/')
        throw new Error('Redirected to login after failed token refresh')
      }
    }

    if (response.status === 403) {
      await router.push('/login/?consent=true')
      throw new Error('Redirected to login due to 403')
    }

    return response
  }

  const checkTokens = async () => {
    const token = getAccessToken()
    const router = useRouter()

    if (token) {
      const response = await fetch(`${BASE_API_URL}/users/ping/`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${token}`
        }
      })

      if (response.status === 200) {
        return true
      } else if (response.status === 401) {
        await refreshAccessToken()
      } else if (response.status === 403) {
        await router.push('/login/')
        return false
      }
    } else {
      try {
        await refreshAccessToken()
      } catch (error) {
        // await router.push('/login/?consent=true')
      }
    }

    return true
  }

  return {
    setAccessToken,
    getAccessToken,
    refreshAccessToken,
    ensureAuthorizedRequest,
    checkTokens
  }
})
