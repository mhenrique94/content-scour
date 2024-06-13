<template>
  <main v-if="authStore.isAuthenticated">
    <div class="pa-4">
        <div class="stream-container">
            <div class="sc-stream">
                <v-card v-if="documentsCount === 0" class="pa-2">
                    <p>This is a Retrieval-augmented generation assistent: the Ai will answer based on the documents provided through the 'settings' page.</p>
                </v-card>
                <template v-for="(chat, index) of ragStream" :key="index">
                    <StreamOutbound :query="chat.query" />
                    <v-card class="pa-2 my-2 yellow lighten-1">
                        {{ chat.answer }}
                    </v-card>
                </template>
            </div>
            <div class="d-flex flex-column justify-center">
                <div class="sc-input">
                    <v-text-field v-model="userInput" :disabled="documentsCount === 0" label="Search" variant="outlined" />
                </div>
                <div class="d-flex justify-space-between">
                    <v-btn :disabled="documentsCount === 0" @click="submitQuery" :loading="loading">Send</v-btn>
                    <p class="mr-4">Embedded documents: {{ documentsCount }}</p>
                </div>
            </div>
        </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useCoreStore, useAuthStore } from '@/stores'
import StreamOutbound from '@/components/chat-stream/StreamOutbound.vue'

const coreStore = useCoreStore()
const authStore = useAuthStore()

onMounted(async () => {
    await coreStore.listDocuments()
})

const userInput = ref('')
const loading = computed(() => {
  return coreStore.loading
})
const ragStream = computed(() => {
  return coreStore.ragStream
})

const documentsCount = computed(() => {
  return coreStore.documents.length
})

const submitQuery = async () => {
    if (userInput.value) {
        await coreStore.ragFromQuery(userInput.value)
        userInput.value = null
    }
}
</script>

<style scoped>
.stream-container {
  padding: 16px;
  border: solid 1px grey;
  position: absolute;
  bottom: 0;
  height: 85%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 100%;
}
.sc-stream {
  overflow: auto;
  height: 100%;
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