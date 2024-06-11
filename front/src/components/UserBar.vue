<template>
    <div v-if="!authStore.loading" class="pa-4">
      <router-link v-if="!isChatRoute" :to="'/'">chatbot</router-link>
        <router-link v-if="!isRagRoute" :to="'/rag'">rag</router-link>
        <router-link v-if="!isSettingsRouter" :to="'/settings'">settings</router-link>
        <router-link v-if="authStore.isAuthenticated" to="#" @click="logout">logout</router-link>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const isRagRoute = computed(() => router.currentRoute.value.path === '/rag')
const isChatRoute = computed(() => router.currentRoute.value.path === '/')
const isSettingsRouter = computed(() => router.currentRoute.value.path === '/settings')

const logout = async () => {
  try {
    await authStore.logout()
    router.push({ path: '/login' })
  } catch (error) {
    console.error(error)
  }
}

</script>