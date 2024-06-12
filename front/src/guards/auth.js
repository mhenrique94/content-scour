import { useAuthStore } from '@/stores'

export default function (to, from, next) {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const authStore = useAuthStore();
  if (requiresAuth && !authStore.isAuthenticated) {
    next({ path: '/login' })
  } else {
    next();
  }
}