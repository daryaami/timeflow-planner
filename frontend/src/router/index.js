import { createRouter, createWebHistory } from 'vue-router'

const Callback = import("../views/Callback.vue");
const LoginView = import("../views/LoginView.vue");
const PlannerView = import("../views/PlannerView.vue");
const AuthCheck = import("../views/AuthCheck.vue");
const TasksView = import("../views/TasksView.vue");

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
    },
    {
      path: '/tasks',
      component: TasksView,
      meta: {
        layout: 'default',
        metaTitle: 'Tasks'
      },
    }
  ],
})

export default router
