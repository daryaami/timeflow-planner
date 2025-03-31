import { defineStore } from "pinia";
import { reactive } from "vue";
import {BASE_API_URL} from "@/config.js";

export const useUserDataStore = defineStore("userData", () => {
const userData = reactive({
  hours: [],
  tasks: [],
});

  const fetchUserData = async () => {
    try {
      const response = await fetch(`${BASE_API_URL}/user_api/api/users/`);
      if (response.ok) {
        const data = await response.json();
        Object.assign(userData, data);
      } else {
        throw new Error("Failed to fetch user data");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  }

  fetchUserData()

  return {
    userData,
    fetchUserData,
  }
})
