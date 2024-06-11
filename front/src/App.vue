<script setup>
import { onMounted } from 'vue';
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores';
import TheWelcome from '@/components/TheWelcome.vue'

const authStore = useAuthStore()

onMounted(async () => {
 await authStore.initSession()
})
</script>

<template>
  <TheWelcome />
  <RouterView />
</template>
