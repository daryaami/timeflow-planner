import { createRouter, createWebHistory } from 'vue-router'
import Callback from '../components/Callback.vue'
import LoginView from '../views/LoginView.vue'
import SignInView from '@/views/SignInView.vue'
import HomeView from '../views/HomeView.vue'
import AccessToken from '@/views/AccessToken.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    { path: '/auth/google/callback', component: Callback },
    { path: '/login', component: LoginView },
    { path: '/signin', component: SignInView },
    { path: '/access', component: AccessToken },
  ],
})

export default router
