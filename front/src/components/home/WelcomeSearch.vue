<template>
<div class="pa-4">
    <v-text-field v-model="userInput" label="Search" variant="outlined" />
    <v-btn @click="submitQuery" :loading="loading">Send</v-btn>
</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCoreStore } from '@/stores/core'

const coreStore = useCoreStore()
const userInput = ref('')

const loading = computed(() => {
  return coreStore.loading
})

const submitQuery = async () => {
    if (userInput.value) {
        coreStore.setQuery(userInput.value)
        await coreStore.submitQuery()
    }
}
</script>