import {defineStore} from "pinia";
import {ref} from "vue";

import {useAuthStore} from "@/store/auth.ts";
import {BASE_API_URL} from "@/config.js";

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
    const response = await fetch(`${BASE_API_URL}/api/users/profile/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${authStore.getAccessToken()}`
      }
    });
    if (response.ok) {
      profileData.value = await response.json() as ProfileData
    }
  }

  const getProfileData = async (): Promise<ProfileData | null> => {
    if (!profileData.value) {
      await fetchProfileData();
    }

    return profileData.value
  }

  return { profileData, fetchProfileData, getProfileData }
})
