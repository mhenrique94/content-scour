<template>
<div v-if="stream.length > 0" class="stream-container">
  <div class="sc-stream">
    <template v-for="(chat, index) of stream" :key="index">
      <StreamOutbound :query="chat.query" />
      <StreamInbound :answer="chat.answer" />
    </template>
  </div>
  <div class="sc-input">
    <v-text-field v-model="userQuery" label="Search" variant="outlined" />
    <v-btn @click="submitQuery">Send</v-btn>
  </div>
</div>
</template>

<script setup>
import StreamInbound from './StreamInbound.vue'
import StreamOutbound from './StreamOutbound.vue'
import { ref } from 'vue'
import { useCoreStore } from '@/stores/core'

const coreStore = useCoreStore()
const userQuery = ref(null)
const stream = coreStore.stream

const submitQuery = async () => {
  if (userQuery.value) {
    coreStore.setQuery(userQuery.value)
    await coreStore.submitQuery()
  }
}
</script>