import { ref, nextTick } from 'vue'
import { defineStore } from 'pinia'
import coreApi from '@/api/core.api.js'

export const useCoreStore = defineStore('core', () => {
  const query = ref(null)
  const stream = ref([])
  const loading = ref(false)
  async function submitQuery() {
    loading.value = true
    try {
      const resp = await coreApi.addNewPrompt(query.value)
      stream.value.push({ query: query.value, answer: resp })
    } catch (error) {
      throw new Error("Algo deu errado")
    } finally {
      loading.value = false
    }
  }

  function setQuery(userInput) {
    query.value = userInput
  }

  return { submitQuery, setQuery, query, stream, loading }
})
