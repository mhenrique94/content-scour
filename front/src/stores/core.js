import { ref, nextTick } from 'vue'
import { defineStore } from 'pinia'
import coreApi from '@/api/core.api.js'

export const useCoreStore = defineStore('core', () => {
  const query = ref(null)
  const stream = ref([])
  const loading = ref(false)
  const documents = ref([])
  
  async function submitQuery() {
    loading.value = true
    try {
      const resp = await coreApi.addNewPrompt(query.value)
      stream.value.push({ query: query.value, answer: resp })
    } catch (error) {
      throw new Error("Something is wrong:", error.message)
    } finally {
      loading.value = false
    }
  }

  function setQuery(userInput) {
    query.value = userInput
  }

  const listDocuments = async () => {
    try {
      const resp = await coreApi.listDocuments()
      documents.value = resp.documents
      return documents.value
    } catch (error) {
      throw new Error("Something is wrong:", error.message)
    } finally {
      loading.value = false
    }
  }

  const submitDocuments = async (formData) => {
    try {
      const resp = await coreApi.submitDocuments(formData)
      documents.value = resp.documents
      return documents.value
    } catch (error) {
      throw new Error("Something is wrong:", error.message)
    } finally {
      loading.value = false
    }
  }

  const deleteDocument = async (id) => {
    try {
      documents.value = await coreApi.deleteDocument(id)
      documents.value = resp.documents
      return documents.value
    } catch (error) {
      throw new Error("Something is wrong:", error.message)
    } finally {
      loading.value = false
    }
  }

  const processDocument = async (id) => {
    try {
      documents.value = await coreApi.processDocument(id)
      documents.value = resp.documents
      return documents.value
    } catch (error) {
      throw new Error("Something is wrong:", error.message)
    } finally {
      loading.value = false
    }
  }

  return {
    submitQuery,
    listDocuments,
    submitDocuments,
    deleteDocument,
    processDocument,
    setQuery,
    query,
    stream,
    loading
  }
})
