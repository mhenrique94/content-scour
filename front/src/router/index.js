import { createRouter, createWebHistory } from 'vue-router'
import authGuard from '@/guards/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RagView from '@/views/RagView.vue'
import SettingsView from '@/views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chatbot',
      meta: { requiresAuth: true },
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/rag',
      name: 'rag',
      meta: { requiresAuth: true },
      component: RagView
    },
    {
      path: '/settings',
      name: 'settings',
      meta: { requiresAuth: true },
      component: SettingsView
    }
  ]
})

router.beforeEach(authGuard)

export default router
