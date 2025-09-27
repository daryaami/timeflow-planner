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
      await router.push('/login/')
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
      const data = await response.json();

      if (data.code === 'refresh_jwt_error') {
        await router.push('/login/')
        throw new Error('Redirected to login due to refresh JWT error')
      } else {
        await router.push('/login/?consent=true')
        throw new Error(`Redirected to login due to ${data.code}`)
      }
    }

    return response
  }

  const checkTokens = async () => {
    const token = getAccessToken()

    if (token) {
      const fetchFn = () => fetch(`${BASE_API_URL}/users/ping/`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${token}`
        }
      })

      const response = await ensureAuthorizedRequest(fetchFn)
      return response.status === 200
    } else {
      await refreshAccessToken()
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
