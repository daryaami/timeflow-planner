import { defineStore } from "pinia";
import {ref} from "vue";

import {useAccessTokenStore} from "@/store/access-token.js";
import {BASE_API_URL} from "@/config.js";

export const useProfileStore = defineStore("userData", () => {
  const profileData = ref(null)

  const fetchProfileData = async () => {
    const accessTokenStore = useAccessTokenStore();
    const response = await fetch(`${BASE_API_URL}/api/users/profile/`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Authorization': `JWT ${accessTokenStore.getAccessTocken()}`
      }
    });
    if (response.ok) {
      const data = await response.json();
      profileData.value = data;
    }
  }

  return { profileData, fetchProfileData }
})
