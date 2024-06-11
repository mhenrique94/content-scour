import { ref } from 'vue'
import { defineStore } from 'pinia'
import authApi from '@/api/auth.api.js'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref()
  const user = ref({})
  const loading = ref(true)

  async function getCSRF() {
    try {
      const csrfResponse = await authApi.getCSRF();
      const csrfToken = csrfResponse.data;
      document.cookie = `csrftoken=${csrfToken}; SameSite=Lax; Secure`;
    } catch (error) {
      throw new Error("Algo deu errado no getCSRF: ", error);
    } finally {
      loading.value = false;
    }
  }

  async function getSession() {
    try {
      const response = await authApi.getSession()
      if (response.isAuthenticated) {
        isAuthenticated.value = true
      } else {
        isAuthenticated.value = false
      }
    } catch (error) {
      throw new Error("Algo deu errado no getSession: ", error)
    } finally {
      loading.value = false
    }
  }

  async function whoAmI() {
    try {
      user.value = await authApi.whoAmI()
    } catch (error) {
      throw new Error("Algo deu errado no whoAmI: ", error)
    } finally {
      loading.value = false
    }
  }

  async function login(params) {
    try {
      const response = await authApi.login(params)
      isAuthenticated.value = response.is_authenticated
      user.value = response.user
    } catch (error) {
      throw new Error("Algo deu errado no login: ", error)
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      const response = await authApi.logout()
      if (response.status >= 200 && response.status <= 299) {
        isAuthenticated.value = response.is_authenticated
        user.value = {}
      } else {
        throw Error(response.message);
      }
    } catch (error) {
      throw new Error("Algo deu errado no logout: ", error)
    } finally {
      loading.value = false
    }
  }

  async function initSession() {
    await getSession()
  }

  return { initSession, getSession, whoAmI, login, logout, loading, isAuthenticated, user }
})
