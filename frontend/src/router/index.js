import { createRouter, createWebHistory } from 'vue-router'
import Callback from '../views/Callback.vue'
import LoginView from '../views/LoginView.vue'
import PlannerView from '../views/PlannerView.vue'
import AuthCheck from "@/views/AuthCheck.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AuthCheck,
      meta: {
        layout: 'login',
      }
    },
    {
      path: '/auth/google/callback',
      component: Callback,
      meta: {
        layout: 'login',
        metaTitle: 'Log in to TimeFlow'
      },
    },
    {
      path: '/login',
      component: LoginView,
      meta: {
        layout: 'login',
        metaTitle: 'Log in to TimeFlow'
      },
    },
    {
      path: '/planner',
      component: PlannerView,
      meta: {
        layout: 'default',
        metaTitle: 'Planner'
      },
    }
  ],
})

export default router
