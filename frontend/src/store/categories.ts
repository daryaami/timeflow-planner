import {defineStore} from "pinia";
import {ref} from "vue";
import {Category} from "@/types/category";
import {useAuthStore} from "@/store/auth";
import {BASE_API_URL} from "@/config";

export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])
  const authStore = useAuthStore()

  let isInitialized = false

  const fetchCategories = async () => {
    const fetchFn = () => fetch(`${BASE_API_URL}/tasks/categories/`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`
        }
      })

    const response = await authStore.ensureAuthorizedRequest(fetchFn)
    categories.value = await response.json() as Category[]
  }

  const getCategories = async () => {
    if (!isInitialized) {
      await fetchCategories()
      isInitialized = true
    }

    return categories.value
  }

  return  { getCategories }
})
