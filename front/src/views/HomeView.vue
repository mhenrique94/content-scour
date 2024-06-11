<script setup>
import ChatStream from '@/components/chat-stream/ChatStream.vue'
import WelcomeSearch from '@/components/home/WelcomeSearch.vue'
import { computed } from 'vue'
import { useCoreStore, useAuthStore } from '@/stores'

const coreStore = useCoreStore()
const authStore = useAuthStore()

const openChat = computed(() => {
  return coreStore.stream.length > 0
})
</script>

<template>
  <main v-if="authStore.isAuthenticated">
    <div class="pa-4">
      <ChatStream v-if="openChat" />
      <WelcomeSearch v-else />
    </div>
  </main>
</template>
