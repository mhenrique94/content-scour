<template>
    <div v-if="!stream.length > 0">
        <h3>Search, baby</h3>
        <v-text-field v-model="userInput" label="Search" variant="outlined" />
        <v-btn @click="submitQuery">Send</v-btn>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCoreStore } from '@/stores/core'

const coreStore = useCoreStore()
const userInput = ref('')

const stream = coreStore.stream

const submitQuery = async () => {
    if (userInput.value) {
        coreStore.setQuery(userInput.value)
        await coreStore.submitQuery()
    }
}
</script>