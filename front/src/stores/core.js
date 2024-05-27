import { ref } from 'vue'
import { defineStore } from 'pinia'
import coreApi from '@/api/core.api.js'

export const useCoreStore = defineStore('core', () => {
  const query = ref('')
  const stream = ([])
  async function submitQuery() {
    const resp = await coreApi.addNewPrompt(query.value)
    stream.value.push({ query: query.value, answer: resp })
  }

  function setQuery(userInput) {
    query.value = userInput
  }

  return { submitQuery, setQuery, stream }
})
