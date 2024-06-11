<template>
<div class="stream-container">
  <div class="sc-stream">
    <template v-for="(chat, index) of stream" :key="index">
      <StreamOutbound :query="chat.query" />
      <StreamInbound :answer="chat.answer" />
    </template>
  </div>
  <div class="sc-input">
    <v-text-field v-model="userQuery" label="Search" variant="outlined" />
    <v-btn @click="submitQuery" :loading="loading">Send</v-btn>
  </div>
</div>
</template>

<script setup>
import StreamInbound from './StreamInbound.vue'
import StreamOutbound from './StreamOutbound.vue'
import { computed, ref } from 'vue'
import { useCoreStore } from '@/stores/core'

const coreStore = useCoreStore()
const userQuery = ref(null)

const stream = computed(() => {
  return coreStore.stream
})

const loading = computed(() => {
  return coreStore.loading
})

const submitQuery = async () => {
  if (userQuery.value) {
    coreStore.setQuery(userQuery.value)
    await coreStore.submitQuery()
  }
}
</script>

<style scoped>
.stream-container {
  padding: 16px;
  margin: 16px;
  border: solid 1px grey;
  position: absolute;
  bottom: 0;
  height: 85%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.sc-stream {
  overflow: auto;
  height: 600px;
}

.sc-stream::-webkit-scrollbar {
  width: .5em;
}

.sc-stream::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
}

.sc-stream::-webkit-scrollbar-thumb {
  background-color: rgb(57, 59, 61);
  outline: 1px solid #333333;
}

.sc-input {
  margin-top: 16px;
}
</style>