import { useAuthStore } from '@/stores';
import { useRouter } from 'vue-router';

export default function (to, from, next) {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const authStore = useAuthStore();
    const router = useRouter()
    if (requiresAuth && !authStore.isAuthenticated) {
      next({ name: 'login' })
    } else {
      next();
    }
  }