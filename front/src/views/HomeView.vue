<script setup>
import ChatStream from '@/components/chat-stream/ChatStream.vue'
import TheWelcome from '@/components/TheWelcome.vue'
import WelcomeSearch from '@/components/WelcomeSearch.vue'
import { computed } from 'vue'
import { useCoreStore } from '@/stores/core'

const coreStore = useCoreStore()

const openChat = computed(() => {
  return coreStore.stream.length > 0
})
</script>

<template>
  <main>
    <TheWelcome />
    <ChatStream v-if="openChat" />
    <WelcomeSearch v-else />
  </main>
</template>
