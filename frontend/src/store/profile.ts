import {defineStore} from "pinia";
import {ref} from "vue";

import {useAuthStore} from "./auth";
import {BASE_API_URL} from "@/config";

interface ProfileData {
  id: number;
  email: string;
  google_id: string;
  name: string;
  picture: string;
  joined_on: string;
  is_active: boolean;
}

export const useProfileStore = defineStore("userData", () => {
  const profileData = ref<ProfileData | null>(null)

  const fetchProfileData = async (): Promise<void> => {
    const authStore = useAuthStore();

    const fetchFn = () =>
      fetch(`${BASE_API_URL}/users/profile/`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Authorization': `JWT ${authStore.getAccessToken()}`
        }
      })

    const response = await authStore.ensureAuthorizedRequest(fetchFn)
    profileData.value = await response.json() as ProfileData
  }

  const getProfileData = async (): Promise<ProfileData | null> => {
    if (!profileData.value) {
      await fetchProfileData();
    }

    return profileData.value
  }

  return { profileData, fetchProfileData, getProfileData }
})
