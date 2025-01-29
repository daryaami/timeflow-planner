import { createRouter, createWebHistory } from 'vue-router'
import Callback from '../components/Callback.vue'
import LoginView from '../views/LoginView.vue'
import SignInView from '@/views/SignInView.vue'
import AccessToken from '@/views/AccessToken.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
    { path: '/signin', component: SignInView },
    { path: '/access', component: AccessToken },
  ],
})

export default router
