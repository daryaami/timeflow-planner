import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAccessTockenStore = defineStore('access-tocken', () => {
  const accessTocken = ref(null)

  const setAccessTocken = (newAccessTocken) => {
    accessTocken.value = newAccessTocken
  }

  const getAccessTocken = () => {
    return accessTocken.value
  }

  return { setAccessTocken, getAccessTocken }
})
